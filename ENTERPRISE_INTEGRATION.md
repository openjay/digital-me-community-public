# Enterprise Integration Patterns

This document describes production-minded patterns (inspired by Ericsson-grade practices).

## 1) Health & Metrics Endpoints
- `/health` → liveness/readiness JSON
- `/metrics` → Prometheus plaintext (optional add-on)
- Standardize across plugins to enable platform discovery & monitoring.

## 2) mTLS (X.509) — local demo
Generate local CA + client/server certs (dev only):
```bash
mkdir -p infra/certs && cd infra/certs
openssl req -x509 -newkey rsa:4096 -days 365 -nodes -keyout ca.key -out ca.crt -subj "/CN=dmce-local-ca"
# server
openssl req -newkey rsa:4096 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
# client
openssl req -newkey rsa:4096 -nodes -keyout client.key -out client.csr -subj "/CN=dmce-client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -out client.crt -days 365
```

Example service start with mTLS (Python uvicorn):

```bash
UVICORN_CMD="uvicorn examples.hello_plugin.service:app --host 0.0.0.0 --port 8443 \
 --ssl-keyfile=infra/certs/server.key --ssl-certfile=infra/certs/server.crt"
$UVICORN_CMD
```

Client curl with mutual auth:

```bash
curl --cacert infra/certs/ca.crt --cert infra/certs/client.crt --key infra/certs/client.key https://localhost:8443/health
```

## 3) RBAC Model (minimal)

* **Roles**: `viewer`, `operator`, `admin`
* JWT with `role` claim (dev stub) → middleware enforces:

  * viewer: GET `/health`, `/metrics`
  * operator: + POST `/action/*`
  * admin: all endpoints

## 4) Logging & Tracing

* Structured JSON logs: `{"ts": "...", "level": "INFO", "service": "hello", "msg": "..."}`
* Optional: OTLP exporter for traces/metrics/logs.

## 5) Production notes

* Rotate keys & certs
* Enforce TLS 1.2+
* Pin dependencies (`requirements*.txt`)
* Scan containers (Trivy) in CI