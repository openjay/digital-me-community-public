# SETUP GUIDE — Digital Me Community

> Goal: run SDK + example plugin locally and in Docker with reproducible steps.

## 1) Prerequisites
- Python 3.11+
- Git, Make
- Docker + Docker Compose (optional for container run)

## 2) Clone & bootstrap
```bash
git clone https://github.com/YOURORG/digital-me-community.git
cd digital-me-community
make setup
```

Expected:

* Virtualenv created at `.venv/`
* Dev deps installed (`pytest`, `ruff`, `mypy`, `black`)
* Project installs in editable mode

## 3) Run tests & quality gates

```bash
make lint
make type
make cov
```

Expected:

* Ruff + Black pass
* Mypy strict passes
* Pytest coverage summary

## 4) Run the Hello Plugin (local)

```bash
make demo
```

Expected:

* Health printout `{"ok": true, "running": true, "plugin": "hello-plugin"}`
* Deterministic stub LLM output

## 5) Run with Docker

```bash
docker build -t dmce-hello:0.1.0 -f examples/hello_plugin/Dockerfile .
docker compose -f examples/hello_plugin/docker-compose.yaml up --build
curl -s http://localhost:8080/health
```

Expected:

* `{"ok":true,"service":"hello","version":"0.1.0"}`

## 6) Troubleshooting

* **Port in use**: change `ports` mapping in `docker-compose.yaml`
* **SSL/mTLS demo**: see `ENTERPRISE_INTEGRATION.md` for local cert generation
* **CI failures**: check `.github/workflows/*` logs; run `make ci-local`