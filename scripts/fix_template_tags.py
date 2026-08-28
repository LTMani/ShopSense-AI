from pathlib import Path
import re

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / 'app' / 'templates'

for html_file in TEMPLATE_DIR.rglob('*.html'):
    content = html_file.read_text(encoding='utf-8')
    blocks = re.findall(r'{%\s*block\s+([a-zA-Z0-9_]+)\s*%}', content)
    endblocks = re.findall(r'{%\s*endblock\s*(?:[a-zA-Z0-9_]+)?\s*%}', content)
    
    if len(blocks) != len(endblocks):
        print(f"Mismatch in {html_file.relative_to(TEMPLATE_DIR)}: {len(blocks)} blocks vs {len(endblocks)} endblocks")
        # If missing exactly 1 endblock at the end
        if len(blocks) > len(endblocks):
            content = content.rstrip() + "\n{% endblock %}\n"
            html_file.write_text(content, encoding='utf-8')
            print(f"  Fixed {html_file.relative_to(TEMPLATE_DIR)}")
