import os
import re

DIR = 'templates/'

# We want to replace the whole <nav class="header-nav"> ... </nav> block
pattern = re.compile(r'<nav class="header-nav">.*?</nav>', re.DOTALL)

for filename in os.listdir(DIR):
    if not filename.endswith('.html'): continue
    if filename == 'header.html': continue
    
    filepath = os.path.join(DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<nav class="header-nav">' in content:
        new_content = pattern.sub('{% include "header.html" %}', content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Injected header into', filename)
