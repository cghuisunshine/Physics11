"""Build the short student review: python3 tools/build_newtons_laws_review.py."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
generator = Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
if not generator.exists():
    generator = Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
output = ROOT / 'newtons-laws-review.html'
subprocess.run([
    sys.executable, str(generator), '--input', str(ROOT / 'content/newtons-laws-review.md'),
    '--output', str(output), '--template', str(ROOT / 'tools/newtons-laws-review-template.html'),
], check=True)
page = output.read_text()
page_number = 0


def identify_section(_):
    global page_number
    page_number += 1
    answer_class = ' class="answer-page"' if page_number >= 8 else ''
    return f'<section id="page-{page_number}"{answer_class}>'


page = re.sub(r'<section>', identify_section, page)
page = re.sub(r'<p><strong>Q(\d+)\.</strong>',
              r'<p class="question" id="q-\1"><strong>Q\1.</strong>', page)
# Format equation subscripts in text nodes without changing markup or URLs.
def notation(text):
    return re.sub(r'\b(F|p|v|a|m|μ|ΣF)_(net,avg|net|g|N|fr|push|static|pull|new|total,before|total,after|total|Ai|Bi|Af|Bf|i|f|A|B|k|s)\b',
                  r'\1<sub>\2</sub>', text)


page = ''.join(part if part.startswith('<') else notation(part)
               for part in re.split(r'(<[^>]+>)', page))
assert page_number == 9
assert page.count('class="question"') == 21
assert '{{' not in page
output.write_text(page)
print('Built newtons-laws-review.html: 9 pages, 21 questions, 2 answer pages.')
