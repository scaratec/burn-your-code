// Package geofence provides a point-in-polygon test for geographic coordinates.
package geofence

// Point represents a geographic coordinate as longitude/latitude pair.
type Point struct {
	Lon float64 `json:"lon"`
	Lat float64 `json:"lat"`
}

// IsPointInside reports whether p lies inside the closed polygon using the
// ray-casting algorithm. The polygon must be closed (first == last vertex).
// Works correctly for both convex and concave (non-self-intersecting) polygons.
func IsPointInside(p Point, polygon []Point) bool {
	n := len(polygon)
	if n < 3 {
		return false
	}
	inside := false
	j := n - 1
	for i := 0; i < n; i++ {
		xi, yi := polygon[i].Lon, polygon[i].Lat
		xj, yj := polygon[j].Lon, polygon[j].Lat
		if ((yi > p.Lat) != (yj > p.Lat)) &&
			(p.Lon < (xj-xi)*(p.Lat-yi)/(yj-yi)+xi) {
			inside = !inside
		}
		j = i
	}
	return inside
}
