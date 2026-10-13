#!/usr/bin/env python3
"""Build Newton's Laws Notes using the shared Kinematics design and Chapter 4 questions.

Requires Pillow, BeautifulSoup, Matplotlib, Poppler, and the chapter-tutorial-html skill.
Run: python tools/build_newtons_laws_notes.py
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
from newtons_laws_graphs import build_graphs

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
if not GENERATOR.exists():
    GENERATOR = Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py'
OUTPUT = ROOT / 'newtons-laws-notes.html'
SOURCE = BeautifulSoup((ROOT / 'bc-newtons-laws-questions.html').read_text(), 'html.parser')
TOPICS = [
    ('102–103', [1, 2]), ('104, 108', [3, 11]), ('105–107', list(range(4, 11))),
    ('109–110', [12, 13]), ('110–112, 115', [14, 15, 17]), ('113–114', [16]),
    ('116–117, 120', [18, 19, 24]), ('118–119', [20, 21, 22, 23]),
    ('121–122', [25, 26]), ('122–123', [27]), ('123–126', [28, 29, 30]),
    ('127–130', [31, 32]),
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
.answer-table{width:100%;font-size:14px;overflow-x:auto}.answer-table table{border-collapse:collapse;width:100%}.answer-table th,.answer-table td{border:1px solid var(--line);padding:8px;text-align:left}.answer-table th{background:var(--soft)}
.answer-graph{margin:18px 0 8px}.answer-graph svg{display:block;width:100%;max-width:450px;height:auto;background:white;border:1px solid var(--line);border-radius:8px;font:12px system-ui,sans-serif;fill:var(--ink)}.answer-graph figcaption{margin-top:7px}.answer-parts>li{margin-bottom:12px}
.notes-links{display:flex;gap:20px;flex-wrap:wrap}
.layout>main,.sidebar{min-width:0}
.investigation-pair{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:24px;align-items:start;margin:18px 0 24px}
.investigation-pair .diagram{margin:0;padding:12px}.investigation-explanation>p:first-child{margin-top:0}
.investigation-explanation pre{font-size:15px;padding:14px 16px}
@media(max-width:1050px){.investigation-pair{grid-template-columns:minmax(0,1fr);gap:18px}}
@media(max-width:800px){.layout{grid-template-columns:minmax(0,1fr)}}
@media(max-width:480px){.law-graph{overflow-x:auto}.law-graph img{min-width:500px}}
@media print{.investigation-pair{display:block}.investigation-pair .diagram{margin-bottom:16px}}
@media print{.practice-question-meta a{display:none}.context{display:block}.context>summary{display:none}.practice-question{break-inside:auto}.practice-question-meta{break-after:avoid}.question-image img{break-inside:avoid}.answer-table{overflow:visible}.answer-graph{break-inside:avoid}.law-graph img{min-width:0}}
'''

template = (ROOT / 'tools/vectors-page.html').read_text()
template = template.replace('https://hamber.mrlamphysics.com/wp-content/uploads/Vectors-Notes.pdf', 'bc_science_physics_11.pdf#page=107')
template = template.replace('The complete Vectors Notes, transcribed into readable Physics 11 notes with equations, diagrams, practice questions.',
    'Newton’s laws tutorial based on BC Science Physics 11 Chapter 4, with 121 original questions and hidden worked answers.')
template = template.replace('Math tools · Class notes', 'BC Science · Chapter 4')
template = template.replace('{{PAGE_SUBTITLE}}',
    'Learn inertia, the three laws, momentum, and impulse through explanations, paired investigation diagrams, and practice with hidden worked answers.')
template = template.replace('<span>10 source pages</span><span>7 topics</span>',
    '<span>12 study topics</span><span>121 textbook questions</span><span>Pages 102–130</span>')
template = template.replace('Try “velocity”', 'Try “inertia” or “impulse”')
template = re.sub(r'<aside class="conversion-note">.*?</aside>', '', template, flags=re.S)
hero = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true"><path d="M20 155H242" stroke="#dce4e7" stroke-width="3"/><rect x="90" y="94" width="82" height="60" rx="7" fill="#edf6f4" stroke="#086b72" stroke-width="2"/><path d="M131 92V30m-7 8 7-8 7 8" fill="none" stroke="#087cff" stroke-width="3"/><path d="M131 156v42m-7-8 7 8 7-8" fill="none" stroke="#f14231" stroke-width="3"/><path d="M174 124h62m-8-7 8 7-8 7" fill="none" stroke="#086b72" stroke-width="3"/><path d="M88 124H26m8-7-8 7 8 7" fill="none" stroke="#f14231" stroke-width="3"/><text x="147" y="43" fill="#087cff" font-size="14">normal</text><text x="146" y="192" fill="#f14231" font-size="14">weight</text><text x="189" y="108" fill="#086b72" font-size="14">push</text><text x="18" y="108" fill="#f14231" font-size="14">friction</text></svg>'''
template = re.sub(r'<svg class="hero-art".*?</svg>', lambda _: hero, template, flags=re.S)
template = template.replace('</style>', EXTRA_CSS + '\n</style>')
with tempfile.TemporaryDirectory(prefix='newtons-laws-notes-') as temp:
    custom = Path(temp) / 'template.html'
    custom.write_text(template)
    subprocess.run([sys.executable, str(GENERATOR), '--input', str(ROOT / 'content/newtons-laws-notes.md'),
        '--output', str(OUTPUT), '--template', str(custom)], check=True)
page = OUTPUT.read_text()
sections = re.findall(r'    <section>\n(.*?)    </section>', page, re.S)
assert len(sections) == len(TOPICS) == 12

def disclosure(solution, ident):
    return (f'<details class="answer-disclosure" id="{ident}"><summary>'
        '<span class="show-answer-label">Show answer</span>'
        '<span class="hide-answer-label">Hide answer</span></summary>'
        '<div class="answer-body"><h4>Worked answer</h4>' + solution + '</div></details>')

def source_diagram(pdf_page, box, alt, caption):
    folder = ROOT / 'tmp/bc-ch4-render'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'page-{pdf_page:03}.png'
    if not path.exists():
        subprocess.run(['pdftoppm', '-f', str(pdf_page), '-l', str(pdf_page), '-scale-to', '2000',
            '-png', str(ROOT / 'bc_science_physics_11.pdf'), str(folder / 'page')], check=True)
    with Image.open(path) as image:
        # Chapter 4's source pages measure 603 × 783 PDF points.
        coords = tuple(round(v * (image.width / 603 if i % 2 == 0 else image.height / 783)) for i, v in enumerate(box))
        stream = io.BytesIO()
        image.crop(coords).convert('RGB').save(stream, format='WEBP', lossless=True)
    data = 'data:image/webp;base64,' + base64.b64encode(stream.getvalue()).decode()
    return f'<figure class="diagram"><img src="{data}" alt="{html.escape(alt, quote=True)}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

# The source crops contain the apparatus, not the surrounding question answers.
def apparatus(page, box, alt, label, explanation):
    return source_diagram(page, box, alt, f'{label}, textbook p. {page-5}. {explanation}')

pairs = {
    1: [('Turning in a car', apparatus(107, (166, 349, 425, 551),
        'Figure 4.1.1: a car turns left while the passenger initially continues along the original straight direction.',
        'Figure 4.1.1', 'Changing direction requires a force on the passenger as well as on the car.'))],
    3: [
        ('Problem 1: how a seatbelt works', apparatus(110, (75, 157, 392, 292),
            'Figure 4.1.2: a toy passenger on a toy vehicle approaching an obstruction.', 'Figure 4.1.2',
            'Compare an unattached passenger with one taped to the vehicle.')),
        ('Problem 2: air has inertia', apparatus(110, (352, 523, 558, 691),
            'Figure 4.1.3: a student holds a large bag filled with air.', 'Figure 4.1.3',
            'Observe the air-filled bag when its motion starts and stops.')),
        ('Problem 3: a glider on an air track', apparatus(111, (86, 251, 455, 316),
            'Figure 4.1.4: an air track supports a glider with an arrow along the level track.', 'Figure 4.1.4',
            'The air cushion reduces friction so nearly constant velocity can be observed.')),
        ('Problem 4: leaving a curved train track', apparatus(111, (75, 549, 273, 682),
            'Figure 4.1.5: a toy train approaches the open end of a curved track.', 'Figure 4.1.5',
            'The initial direction after leaving the track is tangent to the curve.')),
        ('Problem 5: a slow pull and a sudden pull', apparatus(112, (382, 90, 558, 239),
            'Figure 4.1.6: identical masses suspended from upper strings, with lower strings available for pulling.', 'Figure 4.1.6',
            'Compare a slowly increasing pull with a short, sharp tug.')),
        ('Problem 6: the pop-up coaster', apparatus(112, (75, 308, 324, 428),
            'Figure 4.1.7: two views of the moving cannon cart, with the ball in the cannon and then above it.', 'Figure 4.1.7',
            'The ball retains the cart’s horizontal velocity after launch.')),
    ],
    5: [('Draw forces on one chosen object', apparatus(116, (72, 116, 394, 299),
        'Figure 4.2.1: a pushed block has normal force upward, gravity downward, applied force left, and friction right.',
        'Figure 4.2.1', 'Sum forces on the block along each axis to find its acceleration.'))],
    6: [('Read the cart and hanging-mass setup', apparatus(118, (90, 343, 419, 702),
        'Figure 4.2.2: eight cart and pulley arrangements, comparing increasing hanging weight at fixed total mass with increasing total mass at fixed hanging weight.',
        'Figure 4.2.2', 'Left: change driving force while keeping total mass fixed. Right: change total mass while keeping driving force fixed.'))],
    7: [('The horse and cart', apparatus(122, (182, 306, 456, 447),
        'Figure 4.3.1: a horse pulls a cart; opposing harness forces act on the cart and horse separately.',
        'Figure 4.3.1', 'The harness forces act on different objects. Forward ground force on the horse can move the combined system.'))],
    8: [
        ('Part 1: exploding carts', apparatus(123, (73, 170, 432, 317),
            'Figure 4.3.2: laboratory carts with spring bumpers for the exploding-cart demonstration.',
            'Figure 4.3.2', 'The same interaction produces equal forces on the two carts; different masses give different accelerations.')),
        ('Part 2: a car on a movable road', apparatus(124, (75, 109, 357, 202),
            'Figure 4.3.3: a toy car sits on a light movable board supported by an air table.',
            'Figure 4.3.3', 'The car moves forward and pushes its movable road backward.')),
        ('Part 3: tug of war with spring balances', apparatus(124, (75, 351, 278, 501),
            'Figure 4.3.4: two hands pull a string with a spring balance in series at each end.',
            'Figure 4.3.4', 'At steady tension, both balances have the same reading.')),
    ],
}
graphs = build_graphs()

used = []
def practice(group_number):
    group = SOURCE.select_one(f'#set-{group_number}')
    title = group.select_one('h2').get_text()
    body = f'<div class="practice-set" id="newtons-set-{group_number}"><h3>{html.escape(title)}</h3>'
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
        body += (f'<article class="practice-question" id="newtons-{ident}" data-source-id="{ident}">'
            f'<div class="practice-question-meta"><strong>{html.escape(label)}</strong><span>{html.escape(ref)}</span>'
            f'<a href="bc-newtons-laws-questions.html#{ident}">Open in question collection</a></div>'
            + str(question.select_one('.question-image')) + disclosure(solution, f'newtons-answer-{ident}') + '</article>')
    return body + '</div>'

contents = []
for number, (raw, (refs, groups)) in enumerate(zip(sections, TOPICS), 1):
    body = raw.replace('<h3>Notes</h3>', '', 1)
    title = re.search(r'<h2>(.*?)</h2>', body).group(1)
    contents.append(f'<a href="#topic-{number}">{title}</a>')
    answer_count = [0]
    def wrap(match):
        answer_count[0] += 1
        first = '<p>' + match[1].strip() + '</p>' if match[1].strip() else ''
        return disclosure(first + match[2], f'newtons-example-{number}-{answer_count[0]}')
    body = re.sub(r'<p><strong>Worked answer</strong>(.*?)</p>\s*(.*?)(?=\s*<h3>|\Z)', wrap, body, flags=re.S)
    if number == 6:
        heading = '<h3>Three graphs to test the model</h3>'
        assert heading in body
        # Introduce the illustrative values before displaying the graphs.
        body = re.sub(re.escape(heading) + r'(\s*<p>.*?</p>)', lambda m: heading + m[1] + graphs, body, count=1, flags=re.S)
    for heading, figure in pairs.get(number, []):
        anchor = '<h3>' + html.escape(heading) + '</h3>'
        pattern = re.escape(anchor) + r'\s*(.*?)(?=\s*<h3>|\Z)'
        body, matches = re.subn(pattern, lambda match: anchor + '<div class="investigation-pair">' + figure +
            '<div class="investigation-explanation">' + match[1] + '</div></div>', body, count=1, flags=re.S)
        assert matches == 1, heading
    source_text = ' '.join(q['data-search'] for g in groups for q in SOURCE.select(f'#set-{g} .question'))
    search_text = ' '.join((BeautifulSoup(raw, 'html.parser').get_text(' ') + ' ' + source_text).lower().split())
    body += ''.join(practice(g) for g in groups)
    replacement = (f'<section class="section-card" id="topic-{number}" aria-labelledby="heading-{number}" data-search="{html.escape(search_text, quote=True)}">'
        f'<div class="page-ref">BC Science Chapter 4 / Textbook pp. {refs}</div>'
        + body.replace('<h2>', f'<h2 id="heading-{number}">', 1) + '</section>')
    page = page.replace('    <section>\n' + raw + '    </section>', replacement, 1)

assert len(used) == 121 and set(used) == {q['id'] for q in SOURCE.select('.question')}
page = page.replace('%%CONTENTS%%', ''.join(contents))
def notation(text):
    return re.sub(r'(?<![A-Za-z_])([Fpmvagμ])_([A-Za-z]+(?:,[A-Za-z]+)?)', lambda m: m[1] + '<sub>' + m[2] + '</sub>', text)
page = ''.join(part if part.startswith('<') else notation(part) for part in re.split(r'(<[^>]+>)', page))
footer = ('<footer><div class="notes-links"><a href="content.html">All Physics 11 notes</a>'
    '<a href="bc-newtons-laws-questions.html">Newton’s laws questions and homework tools</a>'
    '<a href="bc_science_physics_11.pdf#page=107">Read the textbook chapter</a></div>'
    '<p>Tutorial adapted from BC Science Physics 11, Edvantage Interactive (2012), Chapter 4 Newton’s Laws of Motion, printed pp. 102–130 (PDF pp. 107–135). '
    'All 121 questions, original figures, shared references, procedures, and independently worked answers are reused from the Newton’s laws question collection. '
    'Examples and explanations clarify the models and units. All learning content is embedded and works offline; source links need their companion files or internet access.</p></footer>')
page = page.replace('</body>', footer + '</body>')
assert '{{' not in page and '%%CONTENTS%%' not in page
page = '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
OUTPUT.write_text(page)
print(f'Created {OUTPUT}: 12 topics, {len(used)} questions, {OUTPUT.stat().st_size:,} bytes.')
