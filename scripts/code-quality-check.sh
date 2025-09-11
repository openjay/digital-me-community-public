#!/bin/bash

# Code Quality Check Script
# Performs comprehensive code quality checks

set -e

echo "🔍 Starting Code Quality Check..."

# Install quality tools if not present
echo "📦 Installing quality tools..."
pip install ruff black isort mypy

# Run Ruff linting
echo "🔧 Running Ruff linting..."
ruff check . --output-format=json --output-file=ruff-report.json || true
ruff check .

# Run Black formatting check
echo "🎨 Running Black formatting check..."
black --check . --diff

# Run isort import sorting check
echo "📦 Running isort import sorting check..."
isort --check-only . --diff

# Run MyPy type checking
echo "🔍 Running MyPy type checking..."
mypy src/ --json-report mypy-report.json || true
mypy src/

# Run pytest with coverage
echo "🧪 Running pytest with coverage..."
pytest --cov=src/digital_me_community --cov-report=xml --cov-report=term-missing --cov-fail-under=90

# Check for TODO/FIXME comments
echo "📝 Checking for TODO/FIXME comments..."
if grep -r -i "TODO\|FIXME\|XXX\|HACK" --include="*.py" . | grep -q .; then
    echo "⚠️  WARNING: Found TODO/FIXME comments"
    grep -r -i "TODO\|FIXME\|XXX\|HACK" --include="*.py" .
fi

# Check for proper docstrings
echo "📚 Checking for proper docstrings..."
if find src/ -name "*.py" -exec grep -L '"""' {} \; | grep -q .; then
    echo "⚠️  WARNING: Found Python files without docstrings"
    find src/ -name "*.py" -exec grep -L '"""' {} \;
fi

# Check for proper error handling
echo "⚠️  Checking error handling..."
if grep -r "except:" --include="*.py" . | grep -q .; then
    echo "⚠️  WARNING: Found bare except clauses"
    grep -r "except:" --include="*.py" .
fi

# Check for proper logging
echo "📝 Checking logging practices..."
if find src/ -name "*.py" -exec grep -L "import logging\|from logging" {} \; | grep -q .; then
    echo "⚠️  WARNING: Found Python files without logging imports"
    find src/ -name "*.py" -exec grep -L "import logging\|from logging" {} \;
fi

# Clean up temporary files
rm -f ruff-report.json mypy-report.json

echo "✅ Code Quality Check completed successfully!"
echo "🎯 All quality gates passed."
