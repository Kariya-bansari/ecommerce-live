import os
import re

DIR = 'templates/'

# We want to replace the whole <nav class="header-nav"> ... </nav> block
pattern = re.compile(r'document\.getElementById\(\'menu-btn\'\)\.addEventListener.*?\}\);|const menuBtn = document\.getElementById\(\'menu-btn\'\).*?\}', re.DOTALL)

for filename in ['home.html', 'about1.html']:
    filepath = os.path.join(DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = pattern.sub('', content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Cleaned JS in', filename)
