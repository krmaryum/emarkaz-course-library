#!/bin/bash

# ============================================================
# eMarkaz Course Library Upload Script
# ============================================================
# Description:
# This script automates the upload workflow for the eMarkaz
# Course Library project.
#
# What it does:
# 1. Goes to the eMarkaz course library repository.
# 2. Runs generate_file_pages.py to automatically create/update
#    semester index.html pages for supported files.
# 3. Shows Git status.
# 4. Stages all changes using git add -A.
# 5. Asks the user for a custom commit message.
# 6. If the user presses Enter without typing anything, it uses
#    the default commit message.
# 7. Commits and pushes changes to GitHub main branch.
#
# Supported file types depend on generate_file_pages.py:
# .pdf, .docx, .md, .xlsx
# ============================================================

set -e

REPO_DIR="/c/Linux/emarkaz-course-library"
DEFAULT_COMMIT_MESSAGE="Add semester files and update pages"

echo "=========================================="
echo " eMarkaz Course Library Upload Script"
echo "=========================================="
echo
echo "Description:"
echo "This script generates course pages, stages changes,"
echo "commits them, and pushes them to GitHub."
echo

cd "$REPO_DIR" || {
  echo "ERROR: Repository folder not found: $REPO_DIR"
  exit 1
}

echo "Current folder:"
pwd
echo

echo "Step 1: Generating course pages..."
python generate_file_pages.py
echo

echo "Step 2: Checking Git status..."
git status
echo

echo "Step 3: Staging all changes..."
git add -A
echo

if git diff --cached --quiet; then
  echo "No changes to commit."
  echo "Nothing was pushed."
  exit 0
fi

echo "Step 4: Commit message"
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

echo "Step 5: Committing changes..."
git commit -m "$COMMIT_MESSAGE"
echo

echo "Step 6: Pushing to GitHub..."
git push origin main
echo

echo "Done. Your GitHub Pages website will update shortly."
