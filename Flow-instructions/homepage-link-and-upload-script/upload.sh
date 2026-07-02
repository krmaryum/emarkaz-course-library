#!/bin/bash

# ============================================================
# eMarkaz Course Library Auto Upload Script
# ============================================================
# Workflow:
# 1. You create folders/files yourself.
# 2. This script asks if you want to add any folder link to homepage.
# 3. It generates/updates library pages.
# 4. It commits and pushes to GitHub.
# ============================================================

set -e

REPO_DIR="/c/Linux/emarkaz-course-library"
DEFAULT_COMMIT_MESSAGE="Add books and update library pages"

echo "=========================================="
echo " eMarkaz Course Library Auto Upload"
echo "=========================================="
echo
echo "This script will:"
echo "1. Ask if any folder should be linked on homepage"
echo "2. Generate/update website pages"
echo "3. Stage all changes"
echo "4. Ask for a commit message"
echo "5. Commit and push to GitHub"
echo

cd "$REPO_DIR" || {
  echo "ERROR: Repository folder not found:"
  echo "$REPO_DIR"
  exit 1
}

echo "Current folder:"
pwd
echo

echo "Step 1: Checking required files..."
if [ ! -f "generate_file_pages.py" ]; then
  echo "ERROR: generate_file_pages.py not found in repo root."
  exit 1
fi

if [ ! -f "index.html" ]; then
  echo "ERROR: index.html not found in repo root."
  exit 1
fi

echo "Required files found."
echo

echo "Step 2: Checking for oversized files above 95 MB..."
LARGE_FILES=$(find . -path ./.git -prune -o -type f -size +95M -print 2>/dev/null || true)

if [ -n "$LARGE_FILES" ]; then
  echo "WARNING: These files are larger than 95 MB:"
  echo "$LARGE_FILES"
  echo
  echo "GitHub blocks files above 100 MB."
  echo "Please remove or compress these files before pushing."
  echo
  read -p "Do you still want to continue? Type yes to continue: " CONTINUE_LARGE
  if [ "$CONTINUE_LARGE" != "yes" ]; then
    echo "Stopped. No changes were committed or pushed."
    exit 1
  fi
fi

echo "Step 3: Adding .gitkeep to empty folders..."
find . -path ./.git -prune -o -type d -empty -exec touch {}/.gitkeep \; 2>/dev/null || true
echo

echo "Step 4: Homepage link helper..."
if [ -f "homepage_link_helper.py" ]; then
  python homepage_link_helper.py
elif [ -f "update_homepage_links.py" ]; then
  echo "homepage_link_helper.py not found, using old update_homepage_links.py."
  python update_homepage_links.py
else
  echo "No homepage helper found. Skipping homepage link helper."
fi
echo

echo "Step 5: Generating library pages..."
python generate_file_pages.py
echo

echo "Step 6: Checking Git status..."
git status
echo

echo "Step 7: Staging all changes..."
git add -A
echo

if git diff --cached --quiet; then
  echo "No changes to commit."
  echo "Nothing was pushed."
  exit 0
fi

echo "Step 8: Commit message"
echo "Default commit message:"
echo "$DEFAULT_COMMIT_MESSAGE"
echo
read -p "Enter custom commit message, or press Enter to use default: " USER_COMMIT_MESSAGE

if [ -z "$USER_COMMIT_MESSAGE" ]; then
  COMMIT_MESSAGE="$DEFAULT_COMMIT_MESSAGE"
else
  COMMIT_MESSAGE="$USER_COMMIT_MESSAGE"
fi

echo
echo "Using commit message:"
echo "$COMMIT_MESSAGE"
echo

echo "Step 9: Committing changes..."
git commit -m "$COMMIT_MESSAGE"
echo

echo "Step 10: Pushing to GitHub..."
git push origin main
echo

echo "=========================================="
echo "Done."
echo "GitHub Pages will update shortly."
echo "Check:"
echo "https://emarkazlibrary.com"
echo "=========================================="
