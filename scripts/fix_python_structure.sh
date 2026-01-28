#!/bin/bash
# Fix Python Package Structure
# Removes misplaced subdirectories from somas/agents that duplicate top-level packages

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

echo "🔍 Checking SOMAS Python package structure..."

# Define the incorrect nested directories
MISPLACED_DIRS=(
    "somas/agents/apo"
    "somas/agents/core"
    "somas/agents/analytics"
    "somas/agents/somas"
)

FOUND_ISSUES=0

for dir in "${MISPLACED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "❌ Found misplaced directory: $dir"
        echo "   Removing..."
        rm -rf "$dir"
        FOUND_ISSUES=1
    fi
done

if [ $FOUND_ISSUES -eq 0 ]; then
    echo "✅ Structure looks correct. No misplaced directories found in somas/agents/."
else
    echo "✅ Cleanup complete. Redundant directories removed."
fi

# Verify expected structure exists
echo "📂 Verifying expected structure:"
[ -d "somas/core" ] && echo "  ✅ somas/core exists" || echo "  ❌ somas/core MISSING"
[ -d "somas/apo" ] && echo "  ✅ somas/apo exists" || echo "  ❌ somas/apo MISSING"
[ -d "somas/analytics" ] && echo "  ✅ somas/analytics exists" || echo "  ❌ somas/analytics MISSING"
[ -d "somas/agents" ] && echo "  ✅ somas/agents exists" || echo "  ❌ somas/agents MISSING"
