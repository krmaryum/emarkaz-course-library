#!/bin/bash

# Upload all courses books to their folders
cd /c/Linux/emarkaz-course-library
python generate_file_pages.py
git status
git add -A
git commit -m "Add semester files and update pages"
git push origin main