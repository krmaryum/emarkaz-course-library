#!/bin/bash

# ============================================================
# eMarkaz Course Library Auto Upload Script
# ============================================================
# Description:
# This script automates the upload workflow for the eMarkaz
# Course Library website.
#
# What it does:
# 1. Goes to the eMarkaz course library repository.
# 2. Checks that generate_file_pages.py exists.
# 3. Runs generate_file_pages.py to automatically create/update:
#      - course semester pages
#      - nested semester folder pages
#      - emarkaz-books pages
#      - quran-juzz pages
# 4. Shows Git status.
# 5. Stages all changes using git add -A.
# 6. Stops safely if there are no changes.
# 7. Asks for a custom commit message.
# 8. If you press Enter, it uses the default commit message.
# 9. Commits and pushes changes to GitHub main branch.
#
# Supported file types depend on generate_file_pages.py:
# .pdf, .docx, .md, .xlsx, .xls
#
# Use this after adding folders or files inside:
# books/
# emarkaz-books/
# quran-juzz/
# ============================================================

set -e

REPO_DIR="/c/Linux/emarkaz-course-library"
DEFAULT_COMMIT_MESSAGE="Add books and update library pages"

echo "=========================================="
echo " eMarkaz Course Library Auto Upload"
echo "=========================================="
echo
echo "This script will:"
echo "1. Generate/update website pages"
echo "2. Stage all changes"
echo "3. Ask for a commit message"
echo "4. Commit and push to GitHub"
echo

cd "$REPO_DIR" || {
  echo "ERROR: Repository folder not found:"
  echo "$REPO_DIR"
  exit 1
}

echo "Current folder:"
pwd
echo

echo "Step 1: Checking generator file..."
if [ ! -f "generate_file_pages.py" ]; then
  echo "ERROR: generate_file_pages.py not found in repo root."
  echo "Please make sure this file exists:"
  echo "$REPO_DIR/generate_file_pages.py"
  exit 1
fi

echo "Generator found."
echo

echo "Step 2: Checking for oversized files above 95 MB..."
LARGE_FILES=$(find books emarkaz-books quran-juzz -type f -size +95M 2>/dev/null || true)

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
find books emarkaz-books quran-juzz -type d -empty -exec touch {}/.gitkeep \; 2>/dev/null || true
echo

echo "Step 4: Generating library pages..."
python generate_file_pages.py
echo

echo "Step 5: Checking Git status..."
git status
echo

echo "Step 6: Staging all changes..."
git add -A
echo

if git diff --cached --quiet; then
  echo "No changes to commit."
  echo "Nothing was pushed."
  exit 0
fi

echo "Step 7: Commit message"
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

echo "Step 8: Committing changes..."
git commit -m "$COMMIT_MESSAGE"
echo

echo "Step 9: Pushing to GitHub..."
git push origin main
echo

echo "=========================================="
echo "Done."
echo "GitHub Pages will update shortly."
echo "Check:"
echo "https://emarkazlibrary.com"
echo "=========================================="
