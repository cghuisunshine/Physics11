#!/usr/bin/env python3
"""Build the standalone kinematics transcription from 1600 px page PNGs.

Usage: python3 tools/build_kinematics_notes.py /private/tmp/kinematics-render
Uses Pillow, Matplotlib, and the installed chapter-tutorial-html generator.
"""
from pathlib import Path
import base64
import html
import io
import re
import subprocess
import sys
import tempfile

from PIL import Image
from notes_answer_support import decorate_answers

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = Path('/Users/chenguagnghui/.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py')
render_dir = Path(sys.argv[1])
output = ROOT / 'kinematics-notes.html'
source = 'https://hamber.mrlamphysics.com/wp-content/uploads/Kinematics-Notes.pdf'
template = (ROOT / 'tools/vectors-page.html').read_text()
template = template.replace('https://hamber.mrlamphysics.com/wp-content/uploads/Vectors-Notes.pdf', source)
template = template.replace('10 source pages', '22 source pages').replace('7 topics', '11 topics')
template = template.replace('Math tools · Class notes', 'Motion · Class notes')
template = template.replace('the complete Vectors Notes', 'the complete Kinematics Notes').replace('The complete Vectors Notes', 'The complete Kinematics Notes')
hero = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true"><path d="M20 180H245M25 185V20" stroke="#dce4e7" stroke-width="1.5"/><path d="M30 170Q120 -65 235 170" stroke="#086b72" stroke-width="4" fill="none"/><circle cx="80" cy="91" r="8" fill="#f14231"/><path d="M80 91H122M115 85 122 91 115 97" stroke="#087cff" stroke-width="3" fill="none"/><path d="M80 91V137M74 130 80 137 86 130" stroke="#f14231" stroke-width="3" fill="none"/><text x="122" y="85" fill="#087cff" font-size="15">vₓ</text><text x="91" y="138" fill="#f14231" font-size="15">g</text><text x="83" y="200" fill="#526875" font-size="13">projectile motion</text></svg>'''
template = re.sub(r'<svg class="hero-art".*?</svg>', lambda _: hero, template, flags=re.S)
template = re.sub(r'<aside class="conversion-note">.*?</aside>', '', template, flags=re.S)
template = template.replace('</style>', '@media(min-width:801px){.sidebar{max-height:calc(100vh - 115px);overflow-y:auto;scrollbar-width:thin;padding-right:6px}}\n</style>')
with tempfile.TemporaryDirectory(prefix='kinematics-html-') as temp:
    template_path = Path(temp) / 'template.html'
    template_path.write_text(template)
    subprocess.run([sys.executable, str(GENERATOR), '--input', str(ROOT / 'content/kinematics-notes.md'), '--output', str(output), '--template', str(template_path)], check=True)
page = output.read_text()

def data_image(number, crop=None):
    with Image.open(render_dir / f'page-{number:02d}.png') as im:
        if crop:
            im = im.crop(crop)
        stream = io.BytesIO()
        im.convert('RGB').save(stream, format='PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(stream.getvalue()).decode()

source_pages = [[1, 2], [3], [4], [5, 6, 7], [8, 9, 10], [11, 12], [13], [14, 15], [16, 17], [18, 19, 20], [21, 22]]
labels = ['Pages 1–2', 'Pages 2–4', 'Page 4', 'Pages 5–7', 'Pages 8–10', 'Pages 11–12', 'Page 13', 'Pages 14–15', 'Pages 16–17', 'Pages 18–20', 'Pages 21–22']
diagrams = {
    1: [(1, (255, 835, 925, 1195), 'Positions A and B measured from an origin, with a displacement arrow from A to B.', 'Position and displacement'),
        (2, (360, 165, 940, 395), 'Distance follows the curved path from start to finish; displacement is the direct arrow joining the endpoints.', 'Distance'),
        (2, (175, 800, 385, 1005), 'A square block with 100 metre sides. The route goes up the left side and right along the top, ending at the opposite corner.', 'Practice example: a dog around a city block')],
    6: [(11, (125, 365, 1090, 775), 'A position-time graph rises steadily, stays horizontal while the object rests, and falls steadily as it moves back.', 'Reading straight segments'),
        (12, (165, 365, 805, 775), 'Position-time graph: 0 metres at 0 seconds, 20 metres at 2 seconds, 20 metres at 4 seconds, and about 5 metres at 8 seconds.', 'Practice example: piecewise motion')],
    7: [(13, (115, 205, 1120, 600), 'Four curve regions: speeding up forwards, slowing down forwards, speeding up backwards, and slowing down backwards.', 'Four parts of the source curve'),
        (13, (155, 940, 800, 1340), 'Curved position-time graph rising from zero towards 20 metres at 8 seconds with decreasing slope. Estimate a tangent at 4 seconds.', 'Practice example: instantaneous and average velocity')],
    8: [(14, (190, 205, 1080, 890), 'Velocity-time graph illustrating positive and negative accelerations, constant velocity, and speeding up or slowing down in either direction.', 'Reading the source diagram'),
        (14, (335, 1150, 1100, 1450), 'Red area above the time axis represents positive displacement; blue area below it represents negative displacement.', 'Slope and area'),
        (15, (180, 835, 735, 1200), 'Velocity is plus 10 metres per second at 0 seconds, decreases linearly to minus 10 at 8 seconds, stays at minus 10 until 12 seconds, and rises to zero at 14 seconds.', 'Practice example: a velocity graph')],
    9: [(16, (235, 785, 920, 975), 'An angled throw and a horizontal launch both have gravitational acceleration pointing down.', 'Independent components'),
        (17, (140, 925, 1120, 1450), 'A parabolic trajectory with horizontal range and vertical displacement. Launch velocity resolves into v x equals v i cosine theta and v y i equals v i sine theta.', 'Time links the components')],
    10: [(18, (225, 735, 1110, 1165), 'A soccer ball leaves a 100 metre cliff at 20 metres per second right. The source chooses right and down as positive.', 'Direction convention and givens'),
         (20, (230, 710, 740, 1020), 'Impact velocity triangle: 20 metres per second right and 44.2719 metres per second down form the final velocity, angled below the horizontal.', 'Combine the components')],
}
sections = re.findall(r'    <section>\n(.*?)    </section>', page, re.S)
assert len(sections) == len(source_pages) == 11
contents = []
for number, body in enumerate(sections, 1):
    title = re.search(r'<h2>(.*?)</h2>', body).group(1)
    contents.append(f'<a href="#topic-{number}">{title}</a>')
    search_text = ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', body)).lower().split())
    for p, box, alt, heading in diagrams.get(number, []):
        figure = f'<figure class="diagram"><img src="{data_image(p, box)}" alt="{html.escape(alt, quote=True)}" loading="lazy"><figcaption>Diagram from source page {p}.</figcaption></figure>'
        anchor = '<h3>' + html.escape(heading) + '</h3>'
        assert anchor in body, heading
        body = body.replace(anchor, anchor + figure, 1)
    body = decorate_answers(body, 'kinematics', number)
    replacement = f'<section class="section-card" id="topic-{number}" aria-labelledby="heading-{number}" data-search="{html.escape(search_text, quote=True)}"><div class="page-ref">{labels[number-1]} / Original notes</div>' + body.replace('<h2>', f'<h2 id="heading-{number}">', 1) + '</section>'
    page = page.replace('    <section>\n' + sections[number-1] + '    </section>', replacement, 1)
page = page.replace('%%CONTENTS%%', ''.join(contents))

def math_notation(text):
    text = re.sub(r'(Δ)?([abcvxd])⃗([A-Za-z]{1,2})?', lambda m: (m[1] or '') + f'<span class="vector">{m[2]}</span>' + (f'<sub>{m[3]}</sub>' if m[3] else ''), text)
    return re.sub(r'(?<![A-Za-z_])([vda])_([a-z]+)(?![A-Za-z_])', lambda m: f'{m[1]}<sub>{m[2]}</sub>', text)

page = ''.join(part if part.startswith('<') else math_notation(part) for part in re.split(r'(<[^>]+>)', page))
assert '{{' not in page and '%%CONTENTS%%' not in page
assert 'class="originals"' not in page
output.write_text(page)
print(f'Created {output} ({output.stat().st_size:,} bytes; 11 topics).')
