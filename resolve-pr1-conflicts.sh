#!/bin/bash
# Script to resolve PR #1 merge conflicts
# This script should be run by someone with repository access

set -e

echo "=== Resolving PR #1 Merge Conflicts ==="
echo ""

# Configuration
REPO_URL="https://github.com/scotlaclair/SOMAS.git"
PR_BRANCH="copilot/initialize-somas-lite-pipeline"
MAIN_BRANCH="main"

echo "Step 1: Fetch latest changes from both branches"
git fetch origin $MAIN_BRANCH
git fetch origin $PR_BRANCH

echo ""
echo "Step 2: Checkout PR branch"
git checkout $PR_BRANCH

echo ""
echo "Step 3: Merge main into PR branch"
echo "This will create conflicts that need manual resolution"
git merge origin/$MAIN_BRANCH || {
    echo ""
    echo "=== CONFLICTS DETECTED ==="
    echo ""
    echo "Conflicting files:"
    git status --short | grep "^UU\|^AA\|^DD"
    
    echo ""
    echo "=== Resolution Strategy ==="
    echo ""
    echo "For README.md:"
    echo "  - Merge both versions"
    echo "  - Document both SOMAS Lite (5-stage) and SOMAS Extended (7-stage) approaches"
    echo ""
    echo "For .github/workflows/somas-pipeline.yml:"
    echo "  - Keep main's version (has security fixes and improvements)"
    echo "  - OR: Rename PR #1's version to somas-lite-pipeline.yml and keep both"
    echo ""
    echo "For .somas/config.yml:"
    echo "  - Merge configurations, keeping both sets of agents"
    echo ""
    echo "For agent files:"
    echo "  - Keep all agents from both branches (they have different names)"
    echo ""
    
    echo "After resolving conflicts:"
    echo "  git add <resolved-files>"
    echo "  git commit -m 'Resolve merge conflicts between SOMAS Lite and main'"
    echo "  git push origin $PR_BRANCH"
    
    exit 1
}

echo ""
echo "Step 4: Push merged changes"
git push origin $PR_BRANCH

echo ""
echo "=== SUCCESS ==="
echo "PR #1 branch has been updated with main's changes"
echo "The PR should now be mergeable"
