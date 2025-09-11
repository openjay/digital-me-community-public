#!/bin/bash

# Security Scan Script
# Performs comprehensive security scanning

set -e

echo "🔒 Starting Security Scan..."

# Install security tools if not present
echo "📦 Installing security tools..."
pip install bandit safety

# Run Bandit security scan
echo "🔍 Running Bandit security scan..."
bandit -r src/ -f json -o bandit-report.json || true
bandit -r src/ -f txt

# Check for high severity issues
if [ -f "bandit-report.json" ]; then
    HIGH_SEVERITY=$(jq '.results[] | select(.issue_severity == "HIGH")' bandit-report.json | wc -l)
    if [ "$HIGH_SEVERITY" -gt 0 ]; then
        echo "❌ ERROR: Found $HIGH_SEVERITY high severity security issues"
        jq '.results[] | select(.issue_severity == "HIGH")' bandit-report.json
        exit 1
    fi
fi

# Run Safety scan for known vulnerabilities
echo "🛡️  Running Safety scan..."
safety check --json --output safety-report.json || true
safety check

# Check for critical vulnerabilities
if [ -f "safety-report.json" ]; then
    CRITICAL_VULNS=$(jq '.vulnerabilities[] | select(.severity == "critical")' safety-report.json | wc -l)
    if [ "$CRITICAL_VULNS" -gt 0 ]; then
        echo "❌ ERROR: Found $CRITICAL_VULNS critical vulnerabilities"
        jq '.vulnerabilities[] | select(.severity == "critical")' safety-report.json
        exit 1
    fi
fi

# Check for hardcoded secrets
echo "🔐 Checking for hardcoded secrets..."
if grep -r -i "password\|secret\|key\|token" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "test_" | grep -v "example" | grep -v "stub" | grep -q .; then
    echo "❌ ERROR: Found potential hardcoded secrets!"
    grep -r -i "password\|secret\|key\|token" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "test_" | grep -v "example" | grep -v "stub"
    exit 1
fi

# Check for insecure file permissions
echo "📁 Checking file permissions..."
if find . -type f -perm /o+w | grep -q .; then
    echo "⚠️  WARNING: Found files with world-writable permissions"
    find . -type f -perm /o+w
fi

# Check for insecure network configurations
echo "🌐 Checking network configurations..."
if grep -r -i "http://" --include="*.py" --include="*.yaml" --include="*.yml" . | grep -v "localhost" | grep -v "127.0.0.1" | grep -q .; then
    echo "⚠️  WARNING: Found insecure HTTP URLs"
    grep -r -i "http://" --include="*.py" --include="*.yaml" --include="*.yml" . | grep -v "localhost" | grep -v "127.0.0.1"
fi

# Check for proper error handling
echo "⚠️  Checking error handling..."
if grep -r "except:" --include="*.py" . | grep -q .; then
    echo "⚠️  WARNING: Found bare except clauses"
    grep -r "except:" --include="*.py" .
fi

# Check for proper input validation
echo "✅ Checking input validation..."
if grep -r -i "eval\|exec\|subprocess" --include="*.py" . | grep -v "test_" | grep -q .; then
    echo "⚠️  WARNING: Found potentially dangerous functions"
    grep -r -i "eval\|exec\|subprocess" --include="*.py" . | grep -v "test_"
fi

# Clean up temporary files
rm -f bandit-report.json safety-report.json

echo "✅ Security Scan completed successfully!"
echo "🎯 No critical security issues found."
