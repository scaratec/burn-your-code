# Build stage — compile the geofence-processor binary
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Cache dependency downloads separately from source changes
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build a statically linked binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w" \
    -o bin/geofence-processor \
    ./cmd/geofence-processor/

# Runtime stage — minimal image with just the binary
FROM alpine:3.19

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app
COPY --from=builder /app/bin/geofence-processor .

EXPOSE 8081

CMD ["./geofence-processor"]
