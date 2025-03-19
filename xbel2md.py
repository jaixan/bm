#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

def convert_xbel_to_md(xbel_file, md_file):
    # Parse the XBEL file
    tree = ET.parse(xbel_file)
    root = tree.getroot()
    
    # Open the markdown file for writing
    with open(md_file, 'w', encoding='utf-8') as f:
        # Write the main title
        f.write("# Bookmarks à Etienne\n\n")
        
        # Process top-level bookmarks
        for bookmark in root.findall('./bookmark'):
            title = bookmark.find('title').text
            href = bookmark.get('href')
            f.write(f"- [{title}]({href})\n")
        
        # Process folders
        for folder in root.findall('./folder'):
            folder_title = folder.find('title').text
            f.write(f"\n## {folder_title}\n\n")
            
            # Process bookmarks in this folder
            for bookmark in folder.findall('./bookmark'):
                title = bookmark.find('title').text
                href = bookmark.get('href')
                f.write(f"- [{title}]({href})\n")
    
    print(f"Conversion complete. Markdown file saved to {md_file}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xbel_file = os.path.join(script_dir, "template", "bookmarks.xbel")
    md_file = os.path.join(script_dir, "docs", "bookmarks.md")
    
    convert_xbel_to_md(xbel_file, md_file)