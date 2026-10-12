#!/usr/bin/env python3
"""Build Forces Notes using the Kinematics notes design and Chapter 3 questions.

Requires Pillow, BeautifulSoup, Matplotlib, Poppler, and the chapter-tutorial-html skill.
Run: python tools/build_forces_notes.py
"""
from pathlib import Path
import base64
import html
import io
import re
import subprocess
import sys
import tempfile

from bs4 import BeautifulSoup
from PIL import Image
from forces_spring_graphs import build_spring_graphs

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
if not GENERATOR.exists():
    GENERATOR = Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
OUTPUT = ROOT / 'forces-notes.html'
SOURCE = BeautifulSoup((ROOT / 'bc-forces-questions.html').read_text(), 'html.parser')
TOPICS = [
    ('76', [1]), ('77–78', [2]), ('78–80, 83–84', [3, 6]),
    ('81–82', [4, 5]), ('85–86', [7]), ('86–88, 92', [8, 9, 13]),
    ('89–91', [10, 11, 12]), ('93–94, 97', [14, 15, 18]),
    ('95–96', [16, 17]), ('98–100', [19, 20]),
]

EXTRA_CSS = '''
@media(min-width:801px){.sidebar{max-height:calc(100vh - 115px);overflow-y:auto;scrollbar-width:thin;padding-right:6px}}
.practice-set{margin-top:32px;padding-top:14px;border-top:1px solid var(--line)}
.practice-set>h3{margin-top:12px}.practice-question{padding:20px 0;border-bottom:1px solid var(--line)}
.practice-question:last-child{border-bottom:0}.practice-question-meta{display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between;font-size:12px;color:var(--muted);margin-bottom:12px}
.question-image img,.shared img,.context img{display:block;max-width:100%;height:auto;margin:12px 0}
.context{border:1px solid var(--line);padding:14px;border-radius:8px;margin:16px 0}
.context>summary{cursor:pointer;color:var(--accent);font-size:14px}.shared{margin:18px 0}
.shared figcaption{font-size:12px;color:var(--muted)}.answer-body h3{font-size:16px}.answer-body svg{max-width:100%;height:auto}
.table-wrap{overflow-x:auto}.reference-table{width:100%;border-collapse:collapse;font-size:14px;margin:16px 0}
.reference-table th,.reference-table td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line)}
.reference-table th{background:var(--soft)}.notes-links{display:flex;gap:20px;flex-wrap:wrap}
.layout>main,.sidebar{min-width:0}
.investigation-pair{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:24px;align-items:start;margin:18px 0 24px}
.investigation-pair .diagram{margin:0;padding:12px}.investigation-explanation>p:first-child{margin-top:0}
.investigation-explanation pre{font-size:15px;padding:14px 16px}
@media(max-width:1050px){.investigation-pair{grid-template-columns:minmax(0,1fr);gap:18px}}
@media(max-width:800px){.layout{grid-template-columns:minmax(0,1fr)}}
@media print{.investigation-pair{display:block}.investigation-pair .diagram{margin-bottom:16px}}
@media print{.practice-question-meta a{display:none}.context{display:block}.context>summary{display:none}.practice-question{break-inside:auto}.practice-question-meta{break-after:avoid}.question-image img{break-inside:avoid}.table-wrap{overflow:visible}}
'''

template = (ROOT / 'tools/vectors-page.html').read_text()
template = template.replace('https://hamber.mrlamphysics.com/wp-content/uploads/Vectors-Notes.pdf', 'bc_science_physics_11.pdf#page=81')
template = template.replace('The complete Vectors Notes, transcribed into readable Physics 11 notes with equations, diagrams, practice questions.',
    'Forces tutorial based on BC Science Physics 11 Chapter 3, with 79 original questions and hidden worked answers.')
template = template.replace('Math tools · Class notes', 'BC Science · Chapter 3')
template = template.replace('<span>10 source pages</span><span>7 topics</span>',
    '<span>10 study topics</span><span>79 textbook questions</span><span>Pages 76–100</span>')
template = template.replace('Try “velocity”', 'Try “spring”, “weight”, or “friction”')
template = re.sub(r'<aside class="conversion-note">.*?</aside>', '', template, flags=re.S)
hero = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true"><path d="M20 155H242" stroke="#dce4e7" stroke-width="3"/><rect x="90" y="94" width="82" height="60" rx="7" fill="#edf6f4" stroke="#086b72" stroke-width="2"/><path d="M131 92V30m-7 8 7-8 7 8" fill="none" stroke="#087cff" stroke-width="3"/><path d="M131 156v42m-7-8 7 8 7-8" fill="none" stroke="#f14231" stroke-width="3"/><path d="M174 124h62m-8-7 8 7-8 7" fill="none" stroke="#086b72" stroke-width="3"/><path d="M88 124H26m8-7-8 7 8 7" fill="none" stroke="#f14231" stroke-width="3"/><text x="147" y="43" fill="#087cff" font-size="14">normal</text><text x="146" y="192" fill="#f14231" font-size="14">weight</text><text x="189" y="108" fill="#086b72" font-size="14">push</text><text x="18" y="108" fill="#f14231" font-size="14">friction</text></svg>'''
template = re.sub(r'<svg class="hero-art".*?</svg>', lambda _: hero, template, flags=re.S)
template = template.replace('</style>', EXTRA_CSS + '\n</style>')
with tempfile.TemporaryDirectory(prefix='forces-notes-') as temp:
    custom = Path(temp) / 'template.html'
    custom.write_text(template)
    subprocess.run([sys.executable, str(GENERATOR), '--input', str(ROOT / 'content/forces-notes.md'),
        '--output', str(OUTPUT), '--template', str(custom)], check=True)
page = OUTPUT.read_text()
sections = re.findall(r'    <section>\n(.*?)    </section>', page, re.S)
assert len(sections) == len(TOPICS) == 10

def disclosure(solution, ident):
    return (f'<details class="answer-disclosure" id="{ident}"><summary>'
        '<span class="show-answer-label">Show answer</span>'
        '<span class="hide-answer-label">Hide answer</span></summary>'
        '<div class="answer-body"><h4>Worked answer</h4>' + solution + '</div></details>')

def source_diagram(pdf_page, box, alt, caption):
    folder = ROOT / 'tmp/bc-ch3-render'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'page-{pdf_page:03}.png'
    if not path.exists():
        subprocess.run(['pdftoppm', '-f', str(pdf_page), '-l', str(pdf_page), '-scale-to', '2000',
            '-png', str(ROOT / 'bc_science_physics_11.pdf'), str(folder / 'page')], check=True)
    with Image.open(path) as image:
        # Chapter 3's source pages measure 603 × 783 PDF points.
        coords = tuple(round(v * (image.width / 603 if i % 2 == 0 else image.height / 783)) for i, v in enumerate(box))
        stream = io.BytesIO()
        image.crop(coords).convert('RGB').save(stream, format='WEBP', lossless=True)
    data = 'data:image/webp;base64,' + base64.b64encode(stream.getvalue()).decode()
    return f'<figure class="diagram"><img src="{data}" alt="{html.escape(alt, quote=True)}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

figures = {
    3: ('Cavendish\'s measurement', source_diagram(84, (180, 392, 431, 611),
        'Cavendish torsion balance: a rod suspended by a wire, with small masses attracted toward larger nearby spheres.',
        'Figure 3.1.2, textbook p. 79. Small gravitational forces twist the suspended rod.')),
    6: ('The normal force is perpendicular to the surface', source_diagram(91, (168, 310, 480, 468),
        'A block on a level surface and a block on a slope. Normal force is perpendicular to each surface; gravity points downward.',
        'Figure 3.2.2, textbook p. 86. Weight and normal force are different forces; their magnitudes are equal only under the stated conditions.')),
    8: ('Reading a force-versus-extension graph', '<figure class="diagram">' +
        str(SOURCE.select_one('#set-15 .shared img')) +
        '<figcaption>Figure 3.3.1, textbook p. 93. The force-versus-extension slope is the spring constant; the horizontal axis is in centimetres.</figcaption></figure>'),
}
spring_figures = build_spring_graphs()
investigation_figures = {7: [
    ('Investigation 3-2, Part 1: friction and weight', source_diagram(94, (88, 494, 394, 678),
        'Figure 3.2.3: a vertical spring balance weighs a block, then a horizontal spring balance pulls stacks of one, two, three, and four blocks.',
        'Figure 3.2.3, textbook p. 89. First weigh the blocks vertically. Then pull one to four stacked blocks horizontally: total weight increases while the bottom contact area stays the same.')),
    ('Investigation 3-2, Part 2: contact area', source_diagram(95, (72, 488, 394, 650),
        'Figure 3.2.4: the same four blocks are arranged with one, two, three, and four bottom faces contacting the bench, labelled a, b, c, and d.',
        'Figure 3.2.4, textbook p. 90. Arrangements (a), (b), (c), and (d) have contact areas A, 2A, 3A, and 4A. All use the same four blocks, so total weight is unchanged.')),
], 9: [
    ('Investigation 3-3: another way to weigh', source_diagram(100, (88, 249, 389, 466),
        'Figure 3.3.2: C-clamps hold a horizontal metre stick at the bench; a paper clip suspends a mass at the free end, with a pointer and vertical ruler to measure its downward depression.',
        'Figure 3.3.2, textbook p. 95. The clamped stick bends under the load. Read the pointer against the vertical ruler, then use the calibrated force-versus-depression relationship to find the load\'s weight.')),
]}
COEFFICIENTS = [('Wood on wood', '0.25'), ('Steel on steel', '0.50'), ('Lubricated steel on steel', '0.10'),
    ('Rubber on dry asphalt', '0.40'), ('Rubber on wet asphalt', '0.20'), ('Rubber on ice', '0.005'), ('Steel on ice', '0.01')]
table = '<div class="table-wrap"><table class="reference-table"><caption>Table 3.2.1, textbook p. 87: approximate kinetic coefficients</caption><thead><tr><th scope="col">Surfaces in contact</th><th scope="col">μ_k</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{name}</td><td>{value}</td></tr>' for name, value in COEFFICIENTS) + '</tbody></table></div>'

used = []
def practice(group_number):
    group = SOURCE.select_one(f'#set-{group_number}')
    title = group.select_one('h2').get_text()
    body = f'<div class="practice-set" id="forces-set-{group_number}"><h3>{html.escape(title)}</h3>'
    for reference in group.select(':scope > .shared, :scope > .context'):
        body += str(reference)
    for question in group.select('.question'):
        ident = question['id']
        assert ident not in used
        used.append(ident)
        label = question.select_one('.question-top a').get_text()
        ref = question.select_one('.question-top span').get_text()
        answer = BeautifulSoup(str(question.select_one('.answer')), 'html.parser').select_one('.answer')
        answer.select_one('h3').decompose()
        solution = ''.join(str(child) for child in answer.contents)
        body += (f'<article class="practice-question" id="forces-{ident}" data-source-id="{ident}">'
            f'<div class="practice-question-meta"><strong>{html.escape(label)}</strong><span>{html.escape(ref)}</span>'
            f'<a href="bc-forces-questions.html#{ident}">Open in question collection</a></div>'
            + str(question.select_one('.question-image')) + disclosure(solution, f'forces-answer-{ident}') + '</article>')
    return body + '</div>'

contents = []
for number, (raw, (refs, groups)) in enumerate(zip(sections, TOPICS), 1):
    body = raw
    title = re.search(r'<h2>(.*?)</h2>', body).group(1)
    contents.append(f'<a href="#topic-{number}">{title}</a>')
    answer_count = [0]
    def wrap(match):
        answer_count[0] += 1
        first = '<p>' + match[1].strip() + '</p>' if match[1].strip() else ''
        return disclosure(first + match[2], f'forces-example-{number}-{answer_count[0]}')
    body = re.sub(r'<p><strong>Worked answer</strong>(.*?)</p>\s*(.*?)(?=\s*<h3>|\Z)', wrap, body, flags=re.S)
    if number in figures:
        heading, figure = figures[number]
        anchor = '<h3>' + html.escape(heading) + '</h3>'
        assert anchor in body, heading
        body = body.replace(anchor, anchor + figure, 1)
    if number == 6:
        body = body.replace('<h3>Approximate surface coefficients</h3>', '<h3>Approximate surface coefficients</h3>' + table, 1)
    if number == 8:
        for heading, figure in spring_figures.items():
            anchor = '<h3>' + html.escape(heading) + '</h3>'
            assert anchor in body, heading
            body = body.replace(anchor, anchor + figure, 1)
    for heading, figure in investigation_figures.get(number, []):
        anchor = '<h3>' + html.escape(heading) + '</h3>'
        pattern = re.escape(anchor) + r'\s*(.*?)(?=\s*<h3>|\Z)'
        body, matches = re.subn(pattern, lambda match: anchor + '<div class="investigation-pair">' + figure +
            '<div class="investigation-explanation">' + match[1] + '</div></div>', body, count=1, flags=re.S)
        assert matches == 1, heading
    source_text = ' '.join(q['data-search'] for g in groups for q in SOURCE.select(f'#set-{g} .question'))
    search_text = ' '.join((BeautifulSoup(raw, 'html.parser').get_text(' ') + ' ' + source_text).lower().split())
    body += ''.join(practice(g) for g in groups)
    replacement = (f'<section class="section-card" id="topic-{number}" aria-labelledby="heading-{number}" data-search="{html.escape(search_text, quote=True)}">'
        f'<div class="page-ref">BC Science Chapter 3 / Textbook pp. {refs}</div>'
        + body.replace('<h2>', f'<h2 id="heading-{number}">', 1) + '</section>')
    page = page.replace('    <section>\n' + raw + '    </section>', replacement, 1)

assert len(used) == 79 and set(used) == {q['id'] for q in SOURCE.select('.question')}
page = page.replace('%%CONTENTS%%', ''.join(contents))
def notation(text):
    return re.sub(r'(?<![A-Za-z_])([Frgkμ])_([A-Za-z]+(?:,[A-Za-z]+)?)', lambda m: m[1] + '<sub>' + m[2] + '</sub>', text)
page = ''.join(part if part.startswith('<') else notation(part) for part in re.split(r'(<[^>]+>)', page))
footer = ('<footer><div class="notes-links"><a href="content.html">All Physics 11 notes</a>'
    '<a href="bc-forces-questions.html">Forces questions and homework tools</a>'
    '<a href="bc_science_physics_11.pdf#page=81">Read the textbook chapter</a></div>'
    '<p>Tutorial adapted from BC Science Physics 11, Edvantage Interactive (2012), Chapter 3 Forces, printed pp. 76–100 (PDF pp. 81–105). '
    'All 79 questions, original figures, shared references, procedures, and independently worked answers are reused from the Forces question collection. '
    'Examples and explanations clarify the models and units. All learning content is embedded and works offline; source links need their companion files or internet access.</p></footer>')
page = page.replace('</body>', footer + '</body>')
assert '{{' not in page and '%%CONTENTS%%' not in page
OUTPUT.write_text(page)
print(f'Created {OUTPUT}: 10 topics, {len(used)} questions, {OUTPUT.stat().st_size:,} bytes.')
