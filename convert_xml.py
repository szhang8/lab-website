import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

# Namespaces in WordPress XML export
namespaces = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

def clean_title(title):
    # Remove characters that might break filenames
    return re.sub(r'[^a-zA-Z0-9_\-\s]', '', title).strip().replace(' ', '-')

def parse_wp_xml(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all items (posts, pages, etc.)
    channel = root.find('channel')
    if channel is None:
        print("Invalid XML: No <channel> found.")
        return
        
    for item in channel.findall('item'):
        post_type = item.find('wp:post_type', namespaces)
        if post_type is None or post_type.text not in ['post', 'page']:
            continue
            
        status = item.find('wp:status', namespaces)
        if status is None or status.text != 'publish':
            continue
            
        title_element = item.find('title')
        title = title_element.text if title_element is not None and title_element.text else "Untitled"
        
        post_name_element = item.find('wp:post_name', namespaces)
        post_name = post_name_element.text if post_name_element is not None and post_name_element.text else clean_title(title)
        
        pub_date_element = item.find('wp:post_date', namespaces)
        if pub_date_element is not None and pub_date_element.text and pub_date_element.text != "0000-00-00 00:00:00":
            # Extract date part
            pub_date = pub_date_element.text.split(' ')[0]
        else:
            pub_date = datetime.now().strftime('%Y-%m-%d')
            
        content_element = item.find('content:encoded', namespaces)
        content = content_element.text if content_element is not None and content_element.text else ""
        
        # Simple extraction of categories
        categories = []
        for cat in item.findall('category'):
            if 'domain' in cat.attrib and cat.attrib['domain'] == 'category':
                categories.append(cat.text)
                
        # Create markdown file
        filename = f"{pub_date}-{post_name}.md" if post_name else f"{pub_date}.md"
        filepath = os.path.join(output_dir, filename)
        
        file_content = f"""---
title: "{title.replace('"', '\\"')}"
pubDate: '{pub_date}'
description: ''
"""
        # Add tags if any
        if categories:
            file_content += "tags:\n"
            for c in categories:
                file_content += f"  - '{c.replace('`', '')}'\n"
        
        file_content += f"""---

{content}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
        print(f"Created {filepath}")

if __name__ == "__main__":
    xml_file = "../wp_export/welcometoszhanglaboratory.WordPress.2026-03-04.xml"
    output_dir = "src/content/blog"
    os.makedirs(output_dir, exist_ok=True)
    parse_wp_xml(xml_file, output_dir)
    print("Conversion complete!")
