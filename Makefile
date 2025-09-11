.PHONY: help setup install dev-install lint format type test cov demo clean build publish

help: ## Show this help message
	@echo "Digital Me Community Edition - Development Commands"
	@echo "=================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Set up development environment
	@echo "Setting up development environment..."
	python -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && pip install -e .[dev]
	@echo "✅ Development environment ready!"
	@echo "Activate with: source .venv/bin/activate"

install: ## Install package in production mode
	pip install .

dev-install: ## Install package in development mode
	pip install -e .[dev]

lint: ## Run linting checks
	@echo "Running linting checks..."
	. .venv/bin/activate && ruff check .
	. .venv/bin/activate && black --check .
	. .venv/bin/activate && isort --check-only .

format: ## Format code with black and isort
	@echo "Formatting code..."
	. .venv/bin/activate && black .
	. .venv/bin/activate && isort .
	. .venv/bin/activate && ruff check --fix .

type: ## Run type checking with mypy
	@echo "Running type checks..."
	. .venv/bin/activate && mypy src

test: ## Run tests
	@echo "Running tests..."
	. .venv/bin/activate && pytest -q --maxfail=1 --disable-warnings

test-verbose: ## Run tests with verbose output
	@echo "Running tests (verbose)..."
	. .venv/bin/activate && pytest -v

cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	. .venv/bin/activate && pytest --cov=src/digital_me_community --cov-report=term-missing --cov-report=html

demo: ## Run hello plugin demo
	@echo "Running hello plugin demo..."
	. .venv/bin/activate && python examples/hello_plugin/hello_plugin.py

security: ## Run security checks
	@echo "Running security checks..."
	. .venv/bin/activate && bandit -r src/
	. .venv/bin/activate && safety check

clean: ## Clean up build artifacts
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	@echo "Building package..."
	. .venv/bin/activate && python -m build

publish: ## Publish to PyPI (requires credentials)
	@echo "Publishing to PyPI..."
	. .venv/bin/activate && python -m twine upload dist/*

check-all: lint type test security ## Run all checks (lint, type, test, security)

ci: check-all ## Run CI pipeline locally

ci-local: format lint type test ## Run local CI (format, lint, type, test)

sec: ## Run security scans
	@echo "Running security scans..."
	. .venv/bin/activate && bandit -r src -ll
	. .venv/bin/activate && safety check || true

scan: ## Run Trivy security scan
	@echo "Running Trivy security scan..."
	trivy fs --severity CRITICAL,HIGH .

smoke: ## Run smoke tests
	@echo "Running smoke tests..."
	. .venv/bin/activate && pytest -q --maxfail=1 --disable-warnings
	@echo "✅ Smoke tests passed"

# Development helpers
venv: ## Create virtual environment
	python -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

update-deps: ## Update dependencies
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install --upgrade -e .[dev]

# Documentation
docs: ## Build documentation
	@echo "Building documentation..."
	. .venv/bin/activate && sphinx-build -b html docs/ docs/_build/html

docs-serve: ## Serve documentation locally
	@echo "Serving documentation at http://localhost:8000"
	cd docs/_build/html && python -m http.server 8000

# Plugin development
create-plugin: ## Create a new plugin (usage: make create-plugin PLUGIN_NAME=my-plugin)
	@if [ -z "$(PLUGIN_NAME)" ]; then echo "Usage: make create-plugin PLUGIN_NAME=my-plugin"; exit 1; fi
	@echo "Creating plugin: $(PLUGIN_NAME)"
	@mkdir -p examples/$(PLUGIN_NAME)
	@cp examples/hello_plugin/plugin.yaml examples/$(PLUGIN_NAME)/
	@cp examples/hello_plugin/hello_plugin.py examples/$(PLUGIN_NAME)/$(PLUGIN_NAME)_plugin.py
	@echo "✅ Plugin $(PLUGIN_NAME) created in examples/$(PLUGIN_NAME)/"

validate-plugin: ## Validate plugin structure (usage: make validate-plugin PLUGIN_PATH=examples/my-plugin)
	@if [ -z "$(PLUGIN_PATH)" ]; then echo "Usage: make validate-plugin PLUGIN_PATH=examples/my-plugin"; exit 1; fi
	@echo "Validating plugin at $(PLUGIN_PATH)..."
	@test -f $(PLUGIN_PATH)/plugin.yaml || (echo "❌ Missing plugin.yaml" && exit 1)
	@test -f $(PLUGIN_PATH)/*_plugin.py || (echo "❌ Missing plugin Python file" && exit 1)
	@echo "✅ Plugin structure is valid"

# Docker helpers
docker-build: ## Build Docker image
	docker build -t digital-me-community:latest .

docker-run: ## Run Docker container
	docker run -p 8080:8080 --rm --name digital-me-community digital-me-community:latest

docker-demo: ## Run demo in Docker
	docker run --rm digital-me-community:latest python examples/hello_plugin/hello_plugin.py

docker-up: ## Start Docker Compose services
	docker compose -f examples/hello_plugin/docker-compose.yaml up --build -d

docker-down: ## Stop Docker Compose services
	docker compose -f examples/hello_plugin/docker-compose.yaml down -v

docker-logs: ## Show Docker Compose logs
	docker compose -f examples/hello_plugin/docker-compose.yaml logs -f

docker-health: ## Check Docker service health
	curl -f http://localhost:8080/health || echo "Service not responding"

# Git helpers
pre-commit: ## Install pre-commit hooks
	. .venv/bin/activate && pre-commit install

pre-commit-run: ## Run pre-commit on all files
	. .venv/bin/activate && pre-commit run --all-files

# Release helpers
version: ## Show current version
	@python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

bump-version: ## Bump version (usage: make bump-version PART=patch|minor|major)
	@if [ -z "$(PART)" ]; then echo "Usage: make bump-version PART=patch|minor|major"; exit 1; fi
	. .venv/bin/activate && bump2version $(PART)

# Status and info
status: ## Show project status
	@echo "Digital Me Community Edition - Project Status"
	@echo "============================================="
	@echo "Version: $$(make version)"
	@echo "Python: $$(python --version)"
	@echo "Virtual env: $$(if [ -d .venv ]; then echo "✅ Active"; else echo "❌ Not found"; fi)"
	@echo "Dependencies: $$(if [ -f .venv/pyvenv.cfg ]; then echo "✅ Installed"; else echo "❌ Not installed"; fi)"
	@echo ""
	@echo "Quick commands:"
	@echo "  make setup     - Set up development environment"
	@echo "  make test      - Run tests"
	@echo "  make demo      - Run hello plugin demo"
	@echo "  make check-all - Run all checks"
