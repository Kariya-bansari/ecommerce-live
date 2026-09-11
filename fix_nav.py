import os
import re

DIR = 'templates/'
pattern1 = re.compile(r'({%\s*if\s+(?:request\.)?user\.is_authenticated\s*%}\s*<a[^>]*>.*?</a>\s*)({%\s*else\s*%})', re.IGNORECASE | re.DOTALL)

for filename in os.listdir(DIR):
    if not filename.endswith('.html'): continue
    filepath = os.path.join(DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{% if ' in content and 'user.is_authenticated %}' in content:
        if '/logout/' not in content:
            new_content = pattern1.sub(r'\1<a href="/logout/" class="login-btn">Logout</a>\n        \2', content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print('Updated', filename)
