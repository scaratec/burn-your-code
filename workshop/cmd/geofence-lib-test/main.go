// Command geofence-lib-test is a thin CLI wrapper around the geofence library.
// It reads a JSON request from stdin and writes a JSON result to stdout so that
// the Python BDD step code can call the Go library without a running service.
//
// Input (stdin):
//
//	{"point": {"lon": 9.61, "lat": 53.23}, "polygon": [{"lon":...,"lat":...},...]}
//
// Output (stdout):
//
//	{"is_inside": true}
package main

import (
	"encoding/json"
	"fmt"
	"os"

	"equiguard/internal/geofence"
)

type request struct {
	Point   geofence.Point   `json:"point"`
	Polygon []geofence.Point `json:"polygon"`
}

type response struct {
	IsInside bool `json:"is_inside"`
}

func main() {
	var req request
	if err := json.NewDecoder(os.Stdin).Decode(&req); err != nil {
		fmt.Fprintf(os.Stderr, "failed to decode input: %v\n", err)
		os.Exit(1)
	}
	result := geofence.IsPointInside(req.Point, req.Polygon)
	if err := json.NewEncoder(os.Stdout).Encode(response{IsInside: result}); err != nil {
		fmt.Fprintf(os.Stderr, "failed to encode output: %v\n", err)
		os.Exit(1)
	}
}
