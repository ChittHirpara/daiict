
import os

env_path = ".env"

try:
    with open(env_path, 'rb') as f:
        content_bytes = f.read()

    # Check for UTF-16 LE BOM
    if content_bytes.startswith(b'\xff\xfe'):
        print("Detected UTF-16 LE encoding. Converting to UTF-8...")
        content_str = content_bytes.decode('utf-16-le')
    else:
        print("Encoding seems normal (not UTF-16 LE). Checking content...")
        try:
             content_str = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
             print("Could not decode as UTF-8. Trying system default...")
             content_str = content_bytes.decode(errors='ignore')

    # Clean up content (remove extra nulls if any, strip whitespace)
    content_str = content_str.strip()
    
    # Write back as UTF-8
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content_str)
        
    print(f"Successfully wrote .env as UTF-8. Content length: {len(content_str)}")
    print("Content preview: " + content_str[:20] + "...")

except Exception as e:
    print(f"Error fixing .env: {e}")
