import os
import re
import urllib.parse

def encode_urls(content):
    # Regex to find src="/uploads/..." or href="/uploads/..."
    pattern = r'(src|href)="(/uploads/[^"]+)"'
    
    def replacer(match):
        attr = match.group(1)
        path = match.group(2)
        # Split path to keep /uploads/ part clean and only encode the rest
        # But actually, we can just encode the whole path except the leading /
        encoded_path = urllib.parse.quote(path)
        # Restore the leading / if it was removed by quote
        if not encoded_path.startswith('/'):
            encoded_path = '/' + encoded_path
        # But wait, urllib.parse.quote will encode / as %2F. We want / to stay.
        # So we use quote with safe='/'
        encoded_path = urllib.parse.quote(path, safe='/')
        return f'{attr}="{encoded_path}"'

    return re.sub(pattern, replacer, content)

content_dir = 'src/content'
for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = encode_urls(content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
