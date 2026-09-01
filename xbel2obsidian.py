#!/usr/bin/env python3
"""
xbel_to_md.py

Convert an XBEL bookmarks file into individual Markdown files.
Each bookmark becomes one .md file:
  - filename = bookmark title (sanitized for the filesystem)
  - frontmatter contains:
      created: <ISO date/time from the "added" attribute, if present>
      url: <the bookmark's href>

Usage:
    python xbel_to_md.py input.xbel -o output_folder

If -o is omitted, files are written to ./bookmarks_md
"""

import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def sanitize_filename(name: str, max_length: int = 150) -> str:
    """Make a string safe to use as a filename on Windows/Mac/Linux."""
    name = name.strip() or "Untitled"
    # Replace characters that are invalid/problematic in filenames
    name = re.sub(r'[\\/:*?"<>|]', "-", name)
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    # Remove trailing dots/spaces (problematic on Windows)
    name = name.rstrip(" .")
    if not name:
        name = "Untitled"
    return name[:max_length]


def unique_path(folder: Path, base_name: str, suffix: str = ".md") -> Path:
    """Return a path that doesn't collide with an existing file."""
    candidate = folder / f"{base_name}{suffix}"
    if not candidate.exists():
        return candidate
    counter = 2
    while True:
        candidate = folder / f"{base_name} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def yaml_escape(value: str) -> str:
    """Quote a string for safe inclusion in YAML frontmatter."""
    value = value.replace('"', '\\"')
    return f'"{value}"'


def iter_bookmarks(element):
    """Recursively yield all <bookmark> elements in the XBEL tree."""
    for child in element:
        tag = child.tag.split("}")[-1]  # strip any namespace
        if tag == "bookmark":
            yield child
        # Recurse into folders (and anything else that might nest bookmarks)
        yield from iter_bookmarks(child)


def get_title(bookmark_el) -> str:
    for child in bookmark_el:
        if child.tag.split("}")[-1] == "title":
            return (child.text or "").strip()
    return bookmark_el.get("href", "Untitled")


def convert(xbel_path: Path, output_dir: Path) -> int:
    tree = ET.parse(xbel_path)
    root = tree.getroot()

    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for bookmark in iter_bookmarks(root):
        url = bookmark.get("href", "")
        created = bookmark.get("added", "")
        title = get_title(bookmark)

        filename = sanitize_filename(title)
        filepath = unique_path(output_dir, filename)

        lines = ["---"]
        lines.append(f"created: {yaml_escape(created)}" if created else "created:")
        lines.append(f"url: {yaml_escape(url)}" if url else "url:")
        lines.append("---")
        lines.append("")

        filepath.write_text("\n".join(lines), encoding="utf-8")
        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Convert an XBEL file to Markdown files with frontmatter.")
    parser.add_argument("xbel_file", type=Path, help="Path to the .xbel file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("bookmarks_md"),
        help="Output folder for the generated Markdown files (default: ./bookmarks_md)",
    )
    args = parser.parse_args()

    if not args.xbel_file.exists():
        print(f"Error: file not found: {args.xbel_file}", file=sys.stderr)
        sys.exit(1)

    try:
        count = convert(args.xbel_file, args.output)
    except ET.ParseError as e:
        print(f"Error parsing XBEL file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Done. Created {count} Markdown file(s) in '{args.output}'.")


if __name__ == "__main__":
    main()