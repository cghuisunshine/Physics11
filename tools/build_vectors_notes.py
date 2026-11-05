#!/usr/bin/env python3
"""Build the standalone transcription using the chapter-tutorial-html generator.

Requires Pillow and Matplotlib. Pass the directory of the ten page PNGs
rendered at 1600 px maximum dimension.
Example: python3 tools/build_vectors_notes.py /private/tmp/vectors-render
"""
from pathlib import Path
import base64
import html
import io
import re
import subprocess
import sys

from PIL import Image
from notes_answer_support import decorate_answers

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = Path('/Users/chenguagnghui/.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py')
render_dir = Path(sys.argv[1])
output = ROOT / 'vectors-notes.html'
subprocess.run([sys.executable, str(GENERATOR), '--input', str(ROOT / 'content/vectors-notes.md'), '--output', str(output), '--template', str(ROOT / 'tools/vectors-page.html')], check=True)
page = output.read_text()

def data_image(number, crop=None):
    with Image.open(render_dir / f'page-{number:02d}.png') as im:
        if crop:
            im = im.crop(crop)
        stream = io.BytesIO()
        im.convert('RGB').save(stream, format='PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(stream.getvalue()).decode()

source_pages = [[1], [2], [3, 4], [5], [6, 7], [8], [9, 10]]
labels = ['Page 1', 'Pages 2–3', 'Pages 3–4', 'Page 5', 'Pages 6–7', 'Page 8', 'Pages 9–10']
diagrams = {
    2: [(2, (270, 145, 990, 470), 'Directions from Vancouver: Whistler north, Seattle south, and Kamloops 30 degrees north of east.'),
        (2, (180, 945, 650, 1175), 'The Vancouver to Kamloops vector forms a right triangle with horizontal component d x and vertical component d y.')],
    3: [(4, (255, 190, 1090, 435), 'Green vector a followed by blue vector b. The red resultant c connects the initial tail to the final head.')],
    5: [(6, (250, 1050, 1100, 1410), 'To subtract b from a, reverse b and add negative b head to tail. The red vector c is the resultant.')],
    6: [(8, (225, 398, 1030, 675), 'Plane velocity relative to air points right. Wind points down. Plane velocity relative to ground points diagonally down and right.')],
    7: [(9, (620, 170, 1025, 530), 'Boat velocity relative to water points across the river. Current carries the boat downstream. The red resultant is velocity relative to shore.')],
}
sections = re.findall(r'    <section>\n(.*?)    </section>', page, re.S)
assert len(sections) == 7
contents = []
for number, body in enumerate(sections, 1):
    title = re.search(r'<h2>(.*?)</h2>', body).group(1)
    contents.append(f'<a href="#topic-{number}">{title}</a>')
    search_text = ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', body)).lower().split())
    figures = ''
    for p, box, alt in diagrams.get(number, []):
        figures += f'<figure class="diagram"><img src="{data_image(p, box)}" alt="{html.escape(alt, quote=True)}" loading="lazy"><figcaption>Diagram from source page {p}.</figcaption></figure>'
    # Insert source diagrams after the title, before the transcribed notes.
    body = re.sub(r'(</h2>)', lambda m: m.group(1) + figures, body, count=1)
    body = decorate_answers(body, 'vectors', number)
    replacement = f'<section class="section-card" id="topic-{number}" aria-labelledby="heading-{number}" data-search="{html.escape(search_text, quote=True)}"><div class="page-ref">{labels[number-1]} / Original notes</div>' + body.replace('<h2>', f'<h2 id="heading-{number}">', 1) + '</section>'
    page = page.replace('    <section>\n' + sections[number-1] + '    </section>', replacement, 1)
page = page.replace('%%CONTENTS%%', ''.join(contents))

def vector_notation(match):
    delta, symbol, subscript = match.groups()
    return (delta or '') + f'<span class="vector">{symbol}</span>' + (f'<sub>{subscript}</sub>' if subscript else '')

# Use an ordinary arrow above the symbol for reliable system font support.
page = ''.join(part if part.startswith('<') else re.sub(r'(Δ)?([abcvx])⃗([A-Za-z]{1,2})?', vector_notation, part) for part in re.split(r'(<[^>]+>)', page))
page = page.replace('Vector subscripts are written on the same line for reliable offline display.', 'Vector arrows and subscripts are formatted for reliable offline display.')
assert '{{' not in page and '%%CONTENTS%%' not in page
assert 'class="originals"' not in page
output.write_text(page)
print(f'Created {output} ({output.stat().st_size:,} bytes; 7 topics).')
