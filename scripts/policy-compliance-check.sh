#!/bin/bash

# Policy Compliance Check Script
# Verifies compliance with UNIVERSAL_PROJECT_FILE_MANAGEMENT_POLICY.md

set -e

echo "📋 Starting Policy Compliance Check..."

# Check for required governance files
echo "📄 Checking for required governance files..."
REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "SECURITY.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "SUPPORT.md"
    "pyproject.toml"
    "requirements.txt"
    "requirements-dev.txt"
    "Makefile"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ERROR: Missing required file: $file"
        exit 1
    fi
done

# Check for prohibited root directory files
echo "🚫 Checking for prohibited root directory files..."
PROHIBITED_PATTERNS=(
    "*.log"
    "*.tmp"
    "*.temp"
    "*.bak"
    "*.backup"
    "*.old"
    "PHASE_*.md"
    "*REPORT*.md"
    "*COMPLETION*.md"
    "temp_*"
    "backup_*"
    "old_*"
)

for pattern in "${PROHIBITED_PATTERNS[@]}"; do
    if find . -maxdepth 1 -name "$pattern" | grep -q .; then
        echo "❌ ERROR: Found prohibited root directory file: $pattern"
        find . -maxdepth 1 -name "$pattern"
        exit 1
    fi
done

# Check for proper directory structure
echo "📁 Checking directory structure..."
REQUIRED_DIRS=(
    "src/"
    "tests/"
    "docs/"
    "examples/"
    ".github/workflows/"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ ERROR: Missing required directory: $dir"
        exit 1
    fi
done

# Check for proper file extensions in directories
echo "🔍 Checking file extensions in directories..."
if find src/ -name "*.py" | wc -l | grep -q "^0$"; then
    echo "❌ ERROR: No Python files found in src/ directory"
    exit 1
fi

if find tests/ -name "test_*.py" | wc -l | grep -q "^0$"; then
    echo "❌ ERROR: No test files found in tests/ directory"
    exit 1
fi

# Check for proper naming conventions
echo "📝 Checking naming conventions..."
if find . -name "PHASE_*" -o -name "temp_*" -o -name "backup_*" -o -name "old_*" | grep -q .; then
    echo "❌ ERROR: Found files with prohibited naming patterns"
    find . -name "PHASE_*" -o -name "temp_*" -o -name "backup_*" -o -name "old_*"
    exit 1
fi

# Check for duplicate content
echo "🔄 Checking for duplicate content..."
if [ -f "DEVELOPMENT_PLAN.md" ] && [ -f "ENHANCED_DEVELOPMENT_PLAN.md" ]; then
    echo "⚠️  WARNING: Found duplicate development plan files"
    echo "Consider consolidating DEVELOPMENT_PLAN.md and ENHANCED_DEVELOPMENT_PLAN.md"
fi

# Check for proper documentation structure
echo "📚 Checking documentation structure..."
if [ -d "docs/" ]; then
    if find docs/ -name "*.md" | wc -l | grep -q "^0$"; then
        echo "⚠️  WARNING: No documentation files found in docs/ directory"
    fi
fi

# Check for proper CI/CD configuration
echo "🔧 Checking CI/CD configuration..."
if [ ! -f ".github/workflows/ci.yml" ]; then
    echo "❌ ERROR: Missing CI workflow file"
    exit 1
fi

if [ ! -f ".github/workflows/security.yml" ]; then
    echo "❌ ERROR: Missing security workflow file"
    exit 1
fi

# Check for proper .gitignore
echo "🚫 Checking .gitignore configuration..."
if [ ! -f ".gitignore" ]; then
    echo "❌ ERROR: Missing .gitignore file"
    exit 1
fi

# Check for coverage artifacts
echo "📊 Checking for coverage artifacts..."
if [ -d "htmlcov/" ] || [ -f "coverage.xml" ]; then
    echo "❌ ERROR: Coverage artifacts found in repository"
    echo "These should be in .gitignore and not committed"
    exit 1
fi

# Check for Python cache files
echo "🐍 Checking for Python cache files..."
if find . -name "__pycache__" -o -name "*.pyc" | grep -q .; then
    echo "❌ ERROR: Python cache files found in repository"
    echo "These should be in .gitignore and not committed"
    exit 1
fi

echo "✅ Policy Compliance Check completed successfully!"
echo "🎯 All policy requirements met."
