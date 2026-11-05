#!/usr/bin/env python3
"""Build standalone Energy Notes with the shared Kinematics notes template.

Requires Pillow, BeautifulSoup, Matplotlib, Poppler on PATH, and the installed
chapter-tutorial-html skill. Run: python tools/build_energy_notes.py
"""
from pathlib import Path
import base64
import html
import io
import os
import re
import subprocess
import sys
import tempfile

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'energy-notes.html'
WORK = ROOT / 'tmp/bc-energy-render'
WORK.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/energy-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GENERATOR = next((p for p in (
    Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
    Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
) if p.exists()), None)
if GENERATOR is None:
    raise FileNotFoundError('Install the chapter-tutorial-html skill to rebuild these notes.')

# Printed references and corresponding PDF page for each topic.
REFERENCES = [
    ('132–133', 137), ('133–135', 138), ('136–138', 141), ('142–144', 147),
    ('143–144', 148), ('145–147', 150), ('142, 148–149', 147),
    ('150–152', 155), ('151–152', 156), ('152–154', 157), ('155–158', 160),
    ('160–161', 165), ('134, 162–163', 167), ('164–172', 169),
]


def image_figure(pdf_page, box, alt, caption):
    """Crop a diagram with coordinates relative to a 1155 × 1500 page render."""
    path = WORK / f'page-{pdf_page:03}.png'
    if not path.exists():
        subprocess.run(['pdftoppm', '-f', str(pdf_page), '-l', str(pdf_page),
                        '-scale-to', '1500', '-png', str(ROOT / 'bc_science_physics_11.pdf'),
                        str(WORK / 'page')], check=True)
    with Image.open(path) as source:
        coords = tuple(round(v * (source.width / 1155 if i % 2 == 0 else source.height / 1500))
                       for i, v in enumerate(box))
        crop = source.crop(coords).convert('RGB')
        if pdf_page == 151:
            # The source's adjacent prompt intrudes into the figure's upper-left
            # whitespace. Exclude that prose while preserving the full diagram.
            crop.paste('white', (0, 0, round(78 * source.width / 1155),
                                round(116 * source.height / 1500)))
        stream = io.BytesIO()
        crop.save(stream, format='WEBP', lossless=True)
        width, height = crop.size
    data = base64.b64encode(stream.getvalue()).decode()
    return (f'<figure class="diagram source-diagram"><img src="data:image/webp;base64,{data}" '
            f'width="{width}" height="{height}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
            f'<figcaption>{html.escape(caption)} '
            f'<a href="bc_science_physics_11.pdf#page={pdf_page}">View source page</a>'
            '</figcaption></figure>')


def heating_graph():
    """Plot topic 14's illustrative measurements without revealing the answer."""
    fig, ax = plt.subplots(figsize=(5, 3.8), layout='constrained')
    ax.plot([0, 30, 60, 90, 120], [20, 23, 26, 29, 32], 'o-',
            color='#086b72', linewidth=2.5, markersize=6)
    ax.set(xlabel='Time (s)', ylabel='Water temperature (°C)',
           title='Illustrative hot-plate data', xlim=(-5, 125), ylim=(18, 34),
           xticks=[0, 30, 60, 90, 120], yticks=[20, 23, 26, 29, 32])
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_title('Illustrative hot-plate data', fontsize=14)
    ax.set_xlabel('Time (s)', fontsize=14)
    ax.set_ylabel('Water temperature (°C)', fontsize=14)
    ax.tick_params(labelsize=12)
    ax.grid(alpha=.2)
    ax.set_axisbelow(True)
    assets = ROOT / 'assets/energy-notes'
    assets.mkdir(parents=True, exist_ok=True)
    stream = io.BytesIO()
    fig.savefig(stream, format='png', dpi=160)
    plt.close(fig)
    raw = stream.getvalue()
    (assets / 'heating-data.png').write_bytes(raw)
    data = base64.b64encode(raw).decode()
    return ('<figure class="diagram heating-graph"><img src="data:image/png;base64,' + data +
            '" width="800" height="608" alt="Illustrative heating graph: time 0, 30, 60, 90, '
            'and 120 seconds corresponds to water temperatures 20, 23, 26, 29, and 32 degrees Celsius.">'
            '<figcaption>Illustrative data for the example below, rather than measured textbook results. '
            'Find the temperature change and divide by the elapsed time.</figcaption></figure>')


def disclosure(solution, ident):
    return (f'<details class="answer-disclosure" id="{ident}"><summary>'
            '<span class="show-answer-label">Show answer</span>'
            '<span class="hide-answer-label">Hide answer</span></summary>'
            '<div class="answer-body"><h4>Worked answer</h4>' + solution + '</div></details>')


def build():
    template = (ROOT / 'tools/vectors-page.html').read_text()
    template = template.replace(
        'https://hamber.mrlamphysics.com/wp-content/uploads/Vectors-Notes.pdf',
        'bc_science_physics_11.pdf#page=137')
    template = template.replace(
        'The complete Vectors Notes, transcribed into readable Physics 11 notes with equations, diagrams, practice questions.',
        'Energy notes adapted from BC Science Physics 11 Chapter 5: work, power, machines, mechanical energy, heat transfer, and thermal calculations.')
    template = template.replace('Math tools · Class notes', 'BC Science · Chapter 5')
    template = template.replace('<span>10 source pages</span><span>7 topics</span>',
                                '<span>14 study topics</span><span>Textbook pp. 132–172</span>')
    template = template.replace('Try “velocity”', 'Try “pulley” or “heat”')
    template = template.replace('>Original PDF ↗', '>Textbook: Energy chapter ↗')
    template = template.replace('<button class="print-button"',
                                '<a class="source-link" href="content.html">All Physics 11 notes</a>'
                                '<a class="source-link" href="bc-energy-questions.html">Energy questions and homework</a>'
                                '<a class="source-link" href="energy-review.html">Quick Review · 21 questions</a>'
                                '<button class="print-button"', 1)
    template = re.sub(r'<aside class="conversion-note">.*?</aside>', '', template, flags=re.S)
    hero = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true">
<path d="M24 176H240M34 38V176" fill="none" stroke="#dce4e7" stroke-width="2"/>
<path d="M46 62C95 62 108 158 160 158H226" fill="none" stroke="#086b72" stroke-width="4"/>
<circle cx="51" cy="61" r="11" fill="#f14231"/>
<circle cx="196" cy="147" r="11" fill="#087cff"/>
<path d="M50 88V145m-6-8 6 8 6-8M211 146h27m-7-6 7 6-7 6" fill="none" stroke="#526875" stroke-width="2"/>
<text x="70" y="38" font-size="15" fill="#086b72">potential</text>
<text x="155" y="193" font-size="15" fill="#087cff">kinetic</text>
<text x="59" y="120" font-size="15" fill="#526875">h</text>
</svg>'''
    template = re.sub(r'<svg class="hero-art".*?</svg>', lambda _: hero, template, flags=re.S)
    template = template.replace('</style>', '''
@media(min-width:801px){.sidebar{max-height:calc(100vh - 115px);overflow-y:auto;scrollbar-width:thin;padding-right:6px}}
.page-ref a{text-decoration:none}.page-ref a:hover{text-decoration:underline}
.source-diagram img{max-width:560px}.source-diagram figcaption,.heating-graph figcaption{line-height:1.6}
.notes-links{display:flex;gap:20px;flex-wrap:wrap}
@media print{.page-ref a{color:inherit}}
</style>''')
    with tempfile.TemporaryDirectory(prefix='energy-notes-') as temp:
        custom = Path(temp) / 'template.html'
        custom.write_text(template)
        subprocess.run([sys.executable, str(GENERATOR), '--input', str(ROOT / 'content/energy-notes.md'),
                        '--output', str(OUTPUT), '--template', str(custom)], check=True)
    page = OUTPUT.read_text()
    sections = re.findall(r'    <section>\n(.*?)    </section>', page, re.S)
    assert len(sections) == len(REFERENCES) == 14

    figures = {
        3: [('Investigation 5-1A: getting work done with pulleys', image_figure(
            141, (490, 306, 1040, 761),
            'Two positions of a pulley system: a load rises 10 centimetres while the effort end of the rope moves farther.',
            'Figure 5.1.1, textbook p. 136. Compare the load distance and effort distance.'))],
        5: [('From stored energy to motion', image_figure(
            148, (705, 854, 1110, 1290),
            'Basketball at three levels: at the top it has gravitational potential energy; lower down it also has kinetic energy; at floor level its energy is kinetic in the ideal model.',
            'Figure 5.2.1, textbook p. 143. The floor is the zero of gravitational potential energy.'))],
        6: [('Sample problem 5.2.1: a pendulum', image_figure(
            151, (620, 160, 1030, 425),
            'A pendulum bob is raised and released. At the top it has gravitational potential energy; at the bottom it has kinetic energy.',
            'Figure 5.2.2, textbook p. 146. Height is measured vertically from the lowest position.'))],
        8: [('The kinetic molecular picture', image_figure(
            155, (315, 750, 620, 1020),
            'Three particle-motion diagrams: translation along a line, rotation around an axis, and vibration about a separation.',
            'Figure 5.3.1, textbook p. 150. Translational, rotational, and vibrational motion.'))],
        11: [('Investigation 5-3B: convection', image_figure(
            162, (712, 313, 1051, 806),
            'A ring-shaped glass tube of water with a burner under one lower corner, used to trace a convection current.',
            'Figure 5.3.6, textbook p. 157. Predict the circulation, then compare with a dye trace.'))],
        14: [('Investigation 5-4: power of a hot plate', image_figure(
            169, (570, 345, 990, 650),
            'A beaker containing 300 millilitres of water sits on a hot plate. A clamped thermometer measures water temperature while a stopwatch measures time.',
            'Figure 5.4.1, textbook p. 164. Measure the water temperature without touching the beaker bottom.')),
            ('Practice example: from slope to power', heating_graph())],
    }
    contents, total_answers = [], 0
    for number, (raw, (refs, pdf_page)) in enumerate(zip(sections, REFERENCES), 1):
        body = raw.replace('<h3>Notes</h3>', '', 1)
        title = re.search(r'<h2>(.*?)</h2>', body).group(1)
        contents.append(f'<a href="#topic-{number}">{title}</a>')
        counter = [0]

        def wrap(match):
            counter[0] += 1
            first = '<p>' + match[1].strip() + '</p>' if match[1].strip() else ''
            return disclosure(first + match[2], f'energy-answer-{number}-{counter[0]}')

        body = re.sub(r'<p><strong>Worked answer</strong>(.*?)</p>\s*(.*?)(?=\s*<h3>|\Z)',
                      wrap, body, flags=re.S)
        total_answers += counter[0]
        for heading, figure in figures.get(number, []):
            anchor = '<h3>' + html.escape(heading) + '</h3>'
            assert anchor in body, heading
            body = body.replace(anchor, anchor + figure, 1)
        search = ' '.join(BeautifulSoup(raw, 'html.parser').get_text(' ').lower().split())
        ref = (f'<div class="page-ref"><a href="bc_science_physics_11.pdf#page={pdf_page}">'
               f'Pages {refs} / BC Science Physics 11</a></div>')
        replacement = (f'<section class="section-card" id="topic-{number}" '
                       f'aria-labelledby="heading-{number}" data-search="{html.escape(search, quote=True)}">'
                       + ref + body.replace('<h2>', f'<h2 id="heading-{number}">', 1) + '</section>')
        page = page.replace('    <section>\n' + raw + '    </section>', replacement, 1)
    page = page.replace('%%CONTENTS%%', ''.join(contents))

    # Replace the manuscript's compact notation with real HTML subscripts.
    notation = {
        'Eₖᵢ': 'E<sub>k,i</sub>', 'Eₖf': 'E<sub>k,f</sub>',
        'Eₘᵢ': 'E<sub>m,i</sub>', 'Eₘf': 'E<sub>m,f</sub>',
        'Eₚᵢ': 'E<sub>p,i</sub>', 'Eₚf': 'E<sub>p,f</sub>',
        'Wₙₑₜ': 'W<sub>net</sub>', 'Wₑₓₜ': 'W<sub>ext</sub>',
        'Wᵢₙ': 'W<sub>in</sub>', 'Wₒᵤₜ': 'W<sub>out</sub>',
        'Pₒᵤₜ': 'P<sub>out</sub>', 'ΔEₜₕ': 'ΔE<sub>th</sub>',
        'Eₖ': 'E<sub>k</sub>', 'Eₚ': 'E<sub>p</sub>', 'Eₘ': 'E<sub>m</sub>',
        'Eᵢ': 'E<sub>i</sub>', 'Ef': 'E<sub>f</sub>',
        'Wf': 'W<sub>f</sub>',
        'Fₑ': 'F<sub>e</sub>', 'Fₗ': 'F<sub>l</sub>', 'dₑ': 'd<sub>e</sub>',
        'dₗ': 'd<sub>l</sub>', 'fₖ': 'f<sub>k</sub>',
        'v²f': 'v<sub>f</sub>²', 'v²i': 'v<sub>i</sub>²',
        'vᵢ': 'v<sub>i</sub>', 'vf': 'v<sub>f</sub>',
        'hᵢ': 'h<sub>i</sub>', 'hf': 'h<sub>f</sub>',
        'Tᵢ': 'T<sub>i</sub>', 'Tf': 'T<sub>f</sub>',
    }
    for letter, labels in {'E': ['useful', 'input', 'other', 'black', 'shiny', 'elastic'],
                           'P': ['useful', 'input', 'water', 'light'],
                           'Q': ['water'], 'F': ['load', 'effort', 'average']}.items():
        for label in labels:
            notation[letter + label] = f'{letter}<sub>{label}</sub>'
    pattern = re.compile(r'(?<![A-Za-z])(?:' +
                         '|'.join(re.escape(x) for x in sorted(notation, key=len, reverse=True)) +
                         r')(?![A-Za-z])')
    page = ''.join(part if part.startswith('<') else pattern.sub(lambda m: notation[m[0]], part)
                   for part in re.split(r'(<[^>]+>)', page))
    footer = (f'<footer><div class="notes-links"><a href="content.html">All Physics 11 notes</a>'
              '<a href="energy-review.html">Energy quick review</a>'
              '<a href="bc-energy-questions.html">Energy questions and homework</a>'
              '<a href="bc_science_physics_11.pdf#page=137">Read the Energy chapter</a></div>'
              '<p>Adapted from BC Science Physics 11, Edvantage Interactive (2012), Chapter 5: Energy, '
              'printed pp. 132–172 (PDF pp. 137–177). Covers sections 5.1–5.4 with selected textbook questions, '
              'investigation summaries, original source figures, and additional review examples. '
              f'{total_answers} worked-answer panels are hidden until opened. '
              'All learning content is embedded and works offline. Textbook and index links require the companion files. '
              'Printing includes the answers you have opened.</p></footer>')
    page = page.replace('</body>', footer + '</body>')
    assert '{{' not in page and '%%CONTENTS%%' not in page
    parsed = BeautifulSoup(page, 'html.parser')
    assert len(parsed.select('.section-card')) == 14
    assert len(parsed.select('details.answer-disclosure')) == total_answers
    assert not parsed.select('details.answer-disclosure[open]')
    assert len(parsed.select('.source-diagram')) == 6
    OUTPUT.write_text('\n'.join(line.rstrip() for line in page.splitlines()) + '\n')
    print(f'Created {OUTPUT}: 14 topics, {total_answers} worked-answer panels, {OUTPUT.stat().st_size:,} bytes.')


if __name__ == '__main__':
    build()
