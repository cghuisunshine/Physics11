"""Build the short student review: python3 tools/build_energy_review.py."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
generator = next((path for path in (
    Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
    Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
) if path.exists()), None)
if generator is None:
    raise FileNotFoundError('Install the chapter-tutorial-html skill to rebuild this review.')

output = ROOT / 'energy-review.html'
subprocess.run([
    sys.executable, str(generator), '--input', str(ROOT / 'content/energy-review.md'),
    '--output', str(output), '--template', str(ROOT / 'tools/energy-review-template.html'),
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


def notation(text):
    return re.sub(
        r'(?<![A-Za-z0-9_])(W|E|P|F|d|v|h|T)_(avg,1|avg,2|student|gravity|useful|input|water|net|out|in|ext|th|mi|mf|e|l|k|p|i|f|1|2)(?![A-Za-z0-9_])',
        r'\1<sub>\2</sub>', text)


page = ''.join(part if part.startswith('<') else notation(part)
               for part in re.split(r'(<[^>]+>)', page))
assert page_number == 9
assert page.count('class="question"') == 21
assert page.count('class="answer-page"') == 2
assert '{{' not in page
output.write_text(page)
print('Built energy-review.html: 9 pages, 21 questions, 2 answer pages.')
