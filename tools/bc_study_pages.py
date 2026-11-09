#!/usr/bin/env python3
"""Build printable reviews and offline study notes from shared BC chapter templates."""
import base64
from dataclasses import dataclass
from html import escape
import io
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'bc_science_physics_11.pdf'


@dataclass(frozen=True)
class Chapter:
    slug: str
    title: str
    number: int
    first_page: int
    last_page: int
    references: list
    figures: list
    hero: str
    search_hint: str
    worked_answers: int
    review_labels: list
    sources: tuple = ()

    @property
    def pages(self):
        return f'{self.first_page - 5}–{self.last_page - 5}'

    @property
    def links(self):
        return (
            ('content.html', 'All Physics 11 notes'),
            (f'bc-{self.slug}-questions.html', f'{self.title} questions and homework'),
            (f'{self.slug}-review.html', 'Quick Review · 21 questions'),
        )

def render_outline(manuscript, template, work):
    generator = next((p for p in (
        Path.home() / '.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
        Path.home() / '.codex/skills/chapter-tutorial-html/scripts/generate_chapter_html.py',
    ) if p.exists()), None)
    if generator is None:
        raise FileNotFoundError('Install the chapter-tutorial-html skill to rebuild the chapter pages.')
    custom = work / 'template.html'
    output = work / 'outline.html'
    custom.write_text(template)
    subprocess.run([sys.executable, str(generator), '--input', str(ROOT / 'content' / manuscript),
                    '--output', str(output), '--template', str(custom)], check=True)
    return output.read_text()


def figure(page, box, alt, caption, work):
    path = work / f'page-{page:03}.png'
    if not path.exists():
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1500',
                        '-png', str(ROOT / SOURCE), str(work / 'page')], check=True)
    with Image.open(path) as source:
        coords = tuple(round(value * (source.height / 794 if i % 2 else source.width / 614))
                       for i, value in enumerate(box))
        crop = source.crop(coords).convert('RGB')
    stream = io.BytesIO()
    crop.save(stream, 'WEBP', lossless=True)
    data = base64.b64encode(stream.getvalue()).decode()
    return (f'<figure class="diagram source-diagram"><img src="data:image/webp;base64,{data}" '
            f'width="{crop.width}" height="{crop.height}" alt="{escape(alt, quote=True)}" loading="lazy">'
            f'<figcaption>{escape(caption)} '
            f'<a href="{SOURCE}#page={page}">View source page</a></figcaption></figure>')


def build_notes(chapter, work):
    template = (ROOT / 'tools/vectors-page.html').read_text()
    links = ''.join(f'<a class="source-link" href="{url}">{label}</a>' for url, label in chapter.links)
    template = (template.replace('https://hamber.mrlamphysics.com/wp-content/uploads/Vectors-Notes.pdf',
                                 f'{SOURCE}#page={chapter.first_page}')
                .replace('The complete Vectors Notes, transcribed into readable Physics 11 notes with equations, diagrams, practice questions.',
                         f'Physics 11 {chapter.title} study notes, textbook diagrams, investigations, and worked examples.')
                .replace('Math tools · Class notes', f'BC Science · Chapter {chapter.number}')
                .replace('<span>10 source pages</span><span>7 topics</span>',
                         f'<span>{len(chapter.references)} study topics</span><span>Textbook pp. {chapter.pages}</span>')
                .replace('Try “velocity”', chapter.search_hint)
                .replace('>Original PDF ↗', '>Textbook chapter ↗')
                .replace('<button class="print-button"', links + '<button class="print-button"', 1))
    template = re.sub(r'<svg class="hero-art".*?</svg>', lambda _: chapter.hero, template, count=1, flags=re.S)
    template = template.replace('</style>', '''
@media(min-width:801px){.sidebar{max-height:calc(100vh - 115px);overflow-y:auto;scrollbar-width:thin;padding-right:6px}}
.page-ref a{text-decoration:none}.page-ref a:hover{text-decoration:underline}
.source-diagram img{max-width:560px}.source-diagram figcaption{line-height:1.6}
.notes-links{display:flex;gap:20px;flex-wrap:wrap}
</style>''')
    page = render_outline(f'{chapter.slug}-notes.md', template, work)
    sections = re.findall(r'    <section>\n(.*?)    </section>', page, flags=re.S)
    nav = []
    answer_count = 0
    for number, (raw, (refs, source_page)) in enumerate(zip(sections, chapter.references, strict=True), 1):
        title = re.search(r'<h2>(.*?)</h2>', raw).group(1)
        nav.append(f'<a href="#topic-{number}">{title}</a>')
        search = ' '.join(BeautifulSoup(raw, 'html.parser').get_text(' ').lower().split())
        body = raw.replace('<h2>', f'<h2 id="heading-{number}">', 1)
        body, count = re.subn(
            r'<p><strong>Worked answer</strong></p>\s*(.*?)(?=\s*<h3>|\Z)',
            r'<details class="answer-disclosure"><summary><span class="show-answer-label">Show answer</span>'
            r'<span class="hide-answer-label">Hide answer</span></summary>'
            r'<div class="answer-body"><h4>Worked answer</h4>\1</div></details>',
            body, flags=re.S,
        )
        assert count
        answer_count += count
        for topic, heading, pdf_page, box, alt, caption in reversed(chapter.figures):
            if topic == number:
                anchor = f'<h3>{escape(heading)}</h3>'
                assert anchor in body, heading
                body = body.replace(anchor, anchor + figure(pdf_page, box, alt, caption, work), 1)
        ref = (f'<div class="page-ref"><a href="{SOURCE}#page={source_page}">'
               f'Pages {refs} / BC Science Physics 11</a></div>')
        section = (f'<section class="section-card" id="topic-{number}" aria-labelledby="heading-{number}" '
                   f'data-search="{escape(search, quote=True)}">{ref}{body}</section>')
        page = page.replace(f'    <section>\n{raw}    </section>', section, 1)
    page = page.replace('%%CONTENTS%%', ''.join(nav))
    footer_links = ''.join(f'<a href="{url}">{label}</a>' for url, label in chapter.links)
    source_links = ''.join(f'<p><a href="{escape(url, quote=True)}">{escape(label)}</a></p>'
                           for url, label in chapter.sources)
    footer = (f'<footer><div class="notes-links">{footer_links}</div>'
              f'<p>Adapted from BC Science Physics 11, Edvantage Interactive (2012), Chapter {chapter.number}, '
              f'printed pp. {chapter.pages}. The lessons, diagrams, and worked answers are embedded for offline study. '
              f'Textbook and companion links use the files beside this page.</p>{source_links}</footer>')
    assert '{{' not in page and '%%' not in page and answer_count == chapter.worked_answers
    (ROOT / f'{chapter.slug}-notes.html').write_text(page.replace('</body>', footer + '</body>'))
    print(f'Built {chapter.slug}-notes.html: {len(sections)} topics and {answer_count} worked answers.')


def build_review(chapter, work):
    template = (ROOT / 'tools/energy-review-template.html').read_text()
    template = (template.replace('Energy', chapter.title).replace('ENERGY REVIEW', f'{chapter.title.upper()} REVIEW')
                .replace('energy-notes.html', f'{chapter.slug}-notes.html')
                .replace('<a href="#page-8">Answer key</a>',
                         f'<a href="bc-{chapter.slug}-questions.html">Textbook questions</a><a href="#page-8">Answer key</a>'))
    navigation = ''.join(f'<a href="#page-{i}">{str(i) + " · " if i < 8 else ""}{label}</a>'
                         for i, label in enumerate([*chapter.review_labels, "8–9 · Answers"], 1))
    template = re.sub(r'(<nav aria-label="Review pages">).*?(</nav>)',
                      lambda m: m[1] + navigation + m[2], template, count=1)
    page = render_outline(f'{chapter.slug}-review.md', template, work)
    assert page.count('<section>') == 9
    for number in range(1, 10):
        css = ' class="answer-page"' if number >= 8 else ''
        page = page.replace('<section>', f'<section id="page-{number}"{css}>', 1)
    page = re.sub(r'<p><strong>Q(\d+)\.</strong>',
                  r'<p class="question" id="q-\1"><strong>Q\1.</strong>', page)
    assert page.count('class="question"') == 21 and '{{' not in page
    (ROOT / f'{chapter.slug}-review.html').write_text(page)
    print(f'Built {chapter.slug}-review.html: 9 pages, 21 questions, 2 answer pages.')


def build_study_pages(chapter):
    with TemporaryDirectory(prefix=f'{chapter.slug}-') as directory:
        work = Path(directory)
        build_notes(chapter, work)
        build_review(chapter, work)
