#!/usr/bin/env python3
"""
homepage_link_helper.py

Interactive homepage link helper for eMarkaz Course Library.

Purpose:
- You create folders yourself.
- This script asks if you want to add any folder link to the homepage.
- You provide the folder path from repo root.
- Script verifies the folder exists.
- Script checks if the homepage already contains that link.
- If not, it adds the link to a selected homepage section.

Run from repo root:
    python homepage_link_helper.py

Example:
    mkdir -p books/ac-alim-course/semester-11
    python homepage_link_helper.py

When asked for folder path, type:
    books/ac-alim-course/semester-11
"""

from pathlib import Path
from html import escape
import re

INDEX_FILE = Path("index.html")

HOMEPAGE_SECTIONS = {
    "1": {
        "name": "AC - Alim Course",
        "section_id": "ac",
        "default_label_source": "semester",
    },
    "2": {
        "name": "DC - Ilm-e-Deen Course",
        "section_id": "dc",
        "default_label_source": "semester",
    },
    "3": {
        "name": "TIF - Takhasus fil Ifta",
        "section_id": "tif",
        "default_label_source": "semester",
    },
    "4": {
        "name": "TFA - Takhasus fil Aqaid",
        "section_id": "tfa",
        "default_label_source": "semester",
    },
    "5": {
        "name": "General Library",
        "section_id": "general-library",
        "default_label_source": "folder",
    },
}

def normalize_folder_path(user_path: str) -> str:
    path = user_path.strip().strip('"').strip("'")
    path = path.replace("\\", "/")
    path = path.strip("/")
    return path

def folder_to_href(folder_path: str) -> str:
    return folder_path.rstrip("/") + "/"

def clean_name(text: str) -> str:
    return " ".join(text.replace("_", " ").replace("-", " ").split())

def semester_label_from_path(folder_path: str) -> str:
    name = Path(folder_path).name
    match = re.search(r"semester-(\d+)", name, re.IGNORECASE)
    if match:
        return f"Semester {int(match.group(1)):02d}"
    return clean_name(name).title()

def default_label(folder_path: str, label_source: str) -> str:
    if label_source == "semester":
        return semester_label_from_path(folder_path)
    return clean_name(Path(folder_path).name).title()

def find_section_block(html: str, section_id: str):
    # For course blocks such as <div id="ac" class="note">
    div_marker = f'<div id="{section_id}" class="note">'
    div_start = html.find(div_marker)

    if div_start != -1:
        next_br = html.find("\n      <br>", div_start)
        end_section = html.find("\n    </section>", div_start)

        if next_br != -1 and (end_section == -1 or next_br < end_section):
            div_end = next_br
        else:
            div_end = end_section

        if div_end == -1:
            return None

        return div_start, div_end, html[div_start:div_end]

    # For section such as <section id="general-library" class="container">
    section_marker = f'<section id="{section_id}"'
    section_start = html.find(section_marker)
    if section_start == -1:
        return None

    section_end = html.find("\n    </section>", section_start)
    if section_end == -1:
        return None

    section_end += len("\n    </section>")
    return section_start, section_end, html[section_start:section_end]

def add_link_to_section(html: str, section_id: str, href: str, label: str) -> str:
    found = find_section_block(html, section_id)
    if not found:
        raise RuntimeError(f"Could not find section id in index.html: {section_id}")

    start, end, block = found

    list_marker = '<div class="semester-list">'
    list_start = block.find(list_marker)

    if list_start == -1:
        raise RuntimeError(f"Could not find semester-list inside section: {section_id}")

    list_content_start = list_start + len(list_marker)
    list_end = block.find("</div>", list_content_start)

    if list_end == -1:
        raise RuntimeError(f"Could not find closing div for semester-list inside section: {section_id}")

    link_html = f'\n          <a class="semester" href="{escape(href)}">{escape(label)}</a>'
    new_block = block[:list_end] + link_html + block[list_end:]

    return html[:start] + new_block + html[end:]

def ask_yes_no(question: str) -> bool:
    answer = input(question).strip().lower()
    return answer in {"y", "yes"}

def main():
    if not INDEX_FILE.exists():
        print("ERROR: index.html not found.")
        print("Run this script from repo root: /c/Linux/emarkaz-course-library")
        return 1

    print("==========================================")
    print(" eMarkaz Homepage Link Helper")
    print("==========================================")
    print()
    print("You create folders yourself first.")
    print("This helper can add a selected folder link to homepage.")
    print()

    if not ask_yes_no("Do you want to check/add a folder link to homepage? Type yes or no: "):
        print("Skipped homepage link helper.")
        return 0

    html = INDEX_FILE.read_text(encoding="utf-8")
    changed = False

    while True:
        print()
        folder_input = input("Enter folder path from repo root, for example books/ac-alim-course/semester-11: ")
        folder_path = normalize_folder_path(folder_input)

        if not folder_path:
            print("No folder path entered. Skipping.")
        else:
            folder = Path(folder_path)

            if not folder.exists() or not folder.is_dir():
                print()
                print("ERROR: Folder does not exist:")
                print(folder_path)
                print("Create the folder first, then run this script again.")
            else:
                href = folder_to_href(folder_path)

                print()
                print("Folder found:")
                print(folder_path)
                print()
                print("Homepage href will be:")
                print(href)

                if href in html:
                    print()
                    print("This link already exists in index.html. No homepage change needed.")
                else:
                    print()
                    if ask_yes_no("Do you want to add this folder to homepage? Type yes or no: "):
                        print()
                        print("Where should this homepage button be added?")
                        for key, section in HOMEPAGE_SECTIONS.items():
                            print(f"{key}) {section['name']}")
                        print()

                        choice = input("Choose section number: ").strip()

                        if choice not in HOMEPAGE_SECTIONS:
                            print("Invalid section choice. Skipping this folder.")
                        else:
                            section = HOMEPAGE_SECTIONS[choice]
                            suggested = default_label(folder_path, section["default_label_source"])

                            print()
                            print(f"Suggested button label: {suggested}")
                            custom_label = input("Enter custom button label, or press Enter to use suggested label: ").strip()
                            label = custom_label if custom_label else suggested

                            try:
                                html = add_link_to_section(html, section["section_id"], href, label)
                                changed = True
                                print()
                                print("Homepage link added:")
                                print(f'<a class="semester" href="{href}">{label}</a>')
                            except RuntimeError as error:
                                print()
                                print(f"ERROR: {error}")

                    else:
                        print("Skipped homepage link for this folder.")

        print()
        if not ask_yes_no("Do you want to check another folder? Type yes or no: "):
            break

    if changed:
        INDEX_FILE.write_text(html, encoding="utf-8")
        print()
        print("Homepage updated successfully: index.html")
    else:
        print()
        print("No homepage changes made.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
