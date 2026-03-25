// Command geofence-processor is an HTTP service that receives GPS telemetry
// events via Pub/Sub push, checks whether the device has left its assigned
// geofence, and persists an alert document in Firestore if a violation is
// detected.
//
// Environment variables:
//
//	PORT                    TCP port to listen on (default: 8081)
//	PROJECT_ID              Google Cloud project ID
//	FIRESTORE_EMULATOR_HOST host:port of the Firestore emulator (optional)
package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/firestore"
	"equiguard/internal/geofence"
)

// pubSubEnvelope is the outer wrapper delivered by a Pub/Sub push subscription.
type pubSubEnvelope struct {
	Message struct {
		Data      string `json:"data"`
		MessageID string `json:"messageId"`
	} `json:"message"`
}

// telemetryPayload is the business payload encoded inside the Pub/Sub message.
// Pointers are used so we can distinguish a missing field from a zero value.
type telemetryPayload struct {
	Lon       *float64 `json:"lon"`
	Lat       *float64 `json:"lat"`
	Zone      string   `json:"zone"`
	Device    string   `json:"device"`
	Timestamp string   `json:"timestamp"`
}

// geofencePoint mirrors the Firestore document structure with explicit tags.
type geofencePoint struct {
	Lon float64 `firestore:"lon"`
	Lat float64 `firestore:"lat"`
}

// geofenceDoc represents a geofence document stored in Firestore.
type geofenceDoc struct {
	Polygon []geofencePoint `firestore:"polygon"`
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}
	projectID := os.Getenv("PROJECT_ID")
	if projectID == "" {
		projectID = "equiguard"
	}

	ctx := context.Background()
	db, err := firestore.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("firestore.NewClient: %v", err)
	}
	defer db.Close()

	mux := http.NewServeMux()
	mux.HandleFunc("/health", handleHealth)
	mux.HandleFunc("/telemetry-push", func(w http.ResponseWriter, r *http.Request) {
		handleTelemetry(w, r, ctx, db)
	})

	log.Printf("geofence-processor listening on :%s", port)
	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("ListenAndServe: %v", err)
	}
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, `{"status":"ok"}`)
}

func handleTelemetry(w http.ResponseWriter, r *http.Request, ctx context.Context, db *firestore.Client) {
	// Decode Pub/Sub envelope.
	var env pubSubEnvelope
	if err := json.NewDecoder(r.Body).Decode(&env); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}

	// Decode base64 payload.
	raw, err := base64.StdEncoding.DecodeString(env.Message.Data)
	if err != nil {
		http.Error(w, "invalid base64 data", http.StatusBadRequest)
		return
	}

	// Unmarshal business payload.
	var payload telemetryPayload
	if err := json.Unmarshal(raw, &payload); err != nil {
		http.Error(w, "invalid telemetry payload", http.StatusBadRequest)
		return
	}

	// Validate mandatory fields (Guideline 2.1 — no magic defaults).
	if payload.Lon == nil || payload.Lat == nil {
		http.Error(w, "missing required field: lon and lat", http.StatusBadRequest)
		return
	}
	if payload.Zone == "" {
		http.Error(w, "missing required field: zone", http.StatusBadRequest)
		return
	}

	// Read geofence polygon from Firestore.
	snap, err := db.Collection("geofences").Doc(payload.Zone).Get(ctx)
	if err != nil {
		log.Printf("geofence %q not found: %v", payload.Zone, err)
		http.Error(w, fmt.Sprintf("geofence %q not found", payload.Zone), http.StatusInternalServerError)
		return
	}
	var geoDoc geofenceDoc
	if err := snap.DataTo(&geoDoc); err != nil {
		log.Printf("failed to parse geofence document: %v", err)
		http.Error(w, "failed to parse geofence document", http.StatusInternalServerError)
		return
	}

	// Convert Firestore points to library points.
	polygon := make([]geofence.Point, len(geoDoc.Polygon))
	for i, p := range geoDoc.Polygon {
		polygon[i] = geofence.Point{Lon: p.Lon, Lat: p.Lat}
	}

	// Perform point-in-polygon check.
	point := geofence.Point{Lon: *payload.Lon, Lat: *payload.Lat}
	if !geofence.IsPointInside(point, polygon) {
		alert := map[string]interface{}{
			"device":    payload.Device,
			"type":      "GEOFENCE_VIOLATION",
			"zone":      payload.Zone,
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		}
		if _, _, err := db.Collection("alerts").Add(ctx, alert); err != nil {
			log.Printf("failed to write alert: %v", err)
			http.Error(w, "failed to write alert", http.StatusInternalServerError)
			return
		}
		log.Printf("ALERT: device=%s zone=%s lon=%.7f lat=%.7f",
			payload.Device, payload.Zone, *payload.Lon, *payload.Lat)
	}

	w.WriteHeader(http.StatusOK)
}
