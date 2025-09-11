#!/bin/bash

# IP Protection Scan Script
# Scans for potential enterprise IP leakage in public branches

set -e

echo "🔍 Starting IP Protection Scan..."

# Define patterns that indicate enterprise IP
ENTERPRISE_PATTERNS=(
    "enterprise"
    "proprietary"
    "internal"
    "confidential"
    "secret"
    "private"
    "core.*engine"
    "orchestration.*engine"
    "marketplace"
    "24/7.*recovery"
    "advanced.*security"
    "enterprise.*features"
    "proprietary.*algorithms"
    "internal.*analytics"
    "private.*api"
    "secret.*key"
    "confidential.*data"
)

# Define files that should never be in public branches
RESTRICTED_FILES=(
    "enterprise/"
    "proprietary/"
    "internal/"
    "confidential/"
    "secrets/"
    "private/"
    "core-engine/"
    "orchestration-engine/"
    "marketplace/"
    "recovery-system/"
    "advanced-security/"
)

# Check for restricted file patterns
echo "📁 Checking for restricted file patterns..."
for pattern in "${RESTRICTED_FILES[@]}"; do
    if find . -path "*/$pattern*" -type f | grep -q .; then
        echo "❌ ERROR: Found restricted file pattern: $pattern"
        find . -path "*/$pattern*" -type f
        exit 1
    fi
done

# Check for enterprise IP patterns in code
echo "🔍 Scanning for enterprise IP patterns in code..."
for pattern in "${ENTERPRISE_PATTERNS[@]}"; do
    if grep -r -i "$pattern" --include="*.py" --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "README.md" | grep -v "BRANCH_STRATEGY.md" | grep -q .; then
        echo "⚠️  WARNING: Found potential enterprise IP pattern: $pattern"
        grep -r -i "$pattern" --include="*.py" --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "README.md" | grep -v "BRANCH_STRATEGY.md"
        echo "Please review and ensure this is community-safe content."
    fi
done

# Check for hardcoded secrets or API keys
echo "🔐 Checking for hardcoded secrets..."
if grep -r -i "api_key\|secret_key\|password\|token" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "test_" | grep -v "example" | grep -q .; then
    echo "❌ ERROR: Found potential hardcoded secrets!"
    grep -r -i "api_key\|secret_key\|password\|token" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "test_" | grep -v "example"
    exit 1
fi

# Check for enterprise-specific configuration
echo "⚙️  Checking for enterprise-specific configuration..."
if grep -r -i "enterprise\|proprietary\|internal" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "README.md" | grep -v "BRANCH_STRATEGY.md" | grep -q .; then
    echo "⚠️  WARNING: Found enterprise-specific configuration"
    grep -r -i "enterprise\|proprietary\|internal" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v "README.md" | grep -v "BRANCH_STRATEGY.md"
    echo "Please review and ensure this is community-safe configuration."
fi

echo "✅ IP Protection Scan completed successfully!"
echo "🎯 No enterprise IP leakage detected."
