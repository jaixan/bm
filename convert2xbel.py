import re
import sys
import xml.etree.ElementTree as ET

def extract_links_from_markdown(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Regex to match markdown links [text](url)
    link_pattern = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', content)
    return link_pattern

def create_xbel(links, output_file):
    xbel = ET.Element("xbel")
    xbel.set("version", "1.0")
    
    for text, url in links:
        bookmark = ET.SubElement(xbel, "bookmark", href=url)
        title = ET.SubElement(bookmark, "title")
        title.text = text
    
    tree = ET.ElementTree(xbel)
    ET.indent(tree, space="  ")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert2xbel.py input.md output.xbel")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    
    links = extract_links_from_markdown(markdown_file)
    if not links:
        print("No links found in the markdown file.")
    else:
        create_xbel(links, output_file)
        print(f"XBEL file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()
