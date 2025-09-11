#!/bin/bash

# Documentation Check Script
# Verifies documentation completeness and quality

set -e

echo "📚 Starting Documentation Check..."

# Check for required documentation files
echo "📄 Checking for required documentation files..."
REQUIRED_DOCS=(
    "README.md"
    "SECURITY.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "SUPPORT.md"
    "SETUP_GUIDE.md"
    "ENHANCED_DEVELOPMENT_PLAN.md"
    "BRANCH_STRATEGY.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ ! -f "$doc" ]; then
        echo "❌ ERROR: Missing required documentation: $doc"
        exit 1
    fi
done

# Check for proper README structure
echo "📖 Checking README structure..."
if ! grep -q "## 🚀 Quick Start" README.md; then
    echo "⚠️  WARNING: README.md missing Quick Start section"
fi

if ! grep -q "## ✨ Features" README.md; then
    echo "⚠️  WARNING: README.md missing Features section"
fi

if ! grep -q "## 📚 Documentation" README.md; then
    echo "⚠️  WARNING: README.md missing Documentation section"
fi

# Check for proper documentation structure
echo "📁 Checking documentation structure..."
if [ -d "docs/" ]; then
    if [ ! -f "docs/architecture/README.md" ]; then
        echo "⚠️  WARNING: Missing architecture documentation"
    fi
    
    if [ ! -f "docs/plugin_development/README.md" ]; then
        echo "⚠️  WARNING: Missing plugin development documentation"
    fi
    
    if [ ! -f "docs/quickstart/README.md" ]; then
        echo "⚠️  WARNING: Missing quickstart documentation"
    fi
    
    if [ ! -f "docs/sdk_reference/README.md" ]; then
        echo "⚠️  WARNING: Missing SDK reference documentation"
    fi
fi

# Check for proper code documentation
echo "🔍 Checking code documentation..."
if find src/ -name "*.py" -exec grep -L '"""' {} \; | grep -q .; then
    echo "⚠️  WARNING: Found Python files without docstrings"
    find src/ -name "*.py" -exec grep -L '"""' {} \;
fi

# Check for proper example documentation
echo "📝 Checking example documentation..."
if [ -d "examples/" ]; then
    for example in examples/*/; do
        if [ -d "$example" ] && [ ! -f "$example/README.md" ]; then
            echo "⚠️  WARNING: Example $(basename "$example") missing README.md"
        fi
    done
fi

# Check for proper API documentation
echo "🔌 Checking API documentation..."
if find src/ -name "*.py" -exec grep -L "Args:\|Returns:\|Raises:" {} \; | grep -q .; then
    echo "⚠️  WARNING: Found Python files without proper API documentation"
    find src/ -name "*.py" -exec grep -L "Args:\|Returns:\|Raises:" {} \;
fi

# Check for proper license information
echo "⚖️  Checking license information..."
if ! grep -q "Apache-2.0" LICENSE; then
    echo "⚠️  WARNING: LICENSE file may not contain Apache-2.0 license"
fi

# Check for proper security documentation
echo "🔒 Checking security documentation..."
if ! grep -q "Reporting a Vulnerability" SECURITY.md; then
    echo "⚠️  WARNING: SECURITY.md missing vulnerability reporting section"
fi

# Check for proper contribution guidelines
echo "🤝 Checking contribution guidelines..."
if ! grep -q "Getting Started" CONTRIBUTING.md; then
    echo "⚠️  WARNING: CONTRIBUTING.md missing Getting Started section"
fi

# Check for proper support documentation
echo "🆘 Checking support documentation..."
if ! grep -q "Getting Help" SUPPORT.md; then
    echo "⚠️  WARNING: SUPPORT.md missing Getting Help section"
fi

# Check for proper setup documentation
echo "⚙️  Checking setup documentation..."
if ! grep -q "Prerequisites" SETUP_GUIDE.md; then
    echo "⚠️  WARNING: SETUP_GUIDE.md missing Prerequisites section"
fi

echo "✅ Documentation Check completed successfully!"
echo "🎯 Documentation quality verified."
