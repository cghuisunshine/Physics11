#!/usr/bin/env python3
"""Index complete problem sets from course-related chapters; preserve original pages."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Physics text (TOC).pdf'
MANIFEST = ROOT / 'content/textbook-problems.json'
ASSETS = ROOT / 'assets/textbook-problems'
PDF_URL = 'Physics%20text%20%28TOC%29.pdf'
NS = {'x': 'http://www.w3.org/1999/xhtml'}
# Inclusive PDF viewer pages, from the Problems heading to the chapter's end.
CHAPTERS = {
    1: ('Measurement', 44, 48),
    2: ('Motion Along a Straight Line', 68, 75),
    3: ('Vectors', 93, 97),
    4: ('Motion in Two and Three Dimensions', 120, 129),
    5: ('Force and Motion—I', 152, 159),
    6: ('Force and Motion—II', 176, 184),
    7: ('Kinetic Energy and Work', 206, 212),
    8: ('Potential Energy and Conservation of Energy', 238, 249),
    12: ('Equilibrium and Elasticity', 381, 389),
    15: ('Oscillations', 472, 479),
    16: ('Waves—I', 508, 514),
    17: ('Waves—II', 542, 549),
    18: ('Temperature, Heat, and the First Law of Thermodynamics', 577, 584),
    24: ('Electric Potential', 746, 752),
    26: ('Current and Resistance', 801, 806),
    27: ('Circuits', 831, 838),
}
EXPECTED_COUNTS = {1: 60, 2: 119, 3: 79, 4: 138, 5: 97, 6: 105, 7: 85, 8: 136,
                   12: 88, 15: 116, 16: 96, 17: 111, 18: 108, 24: 103, 26: 85, 27: 105}
E = html.escape


def extract():
    from pypdf import PdfReader
    reader = PdfReader(SOURCE)
    titles = {}

    def bookmarks(items):
        for item in items:
            if isinstance(item, list):
                bookmarks(item)
            else:
                match = re.match(r'^(\d+-\d+)\s+(.+)', item.title)
                if match:
                    title = match[2].capitalize().replace('newton', 'Newton').replace('ohm', 'Ohm').replace('rc circuits', 'RC circuits').replace('celsius', 'Celsius').replace('fahrenheit', 'Fahrenheit')
                    titles[match[1]] = title
    bookmarks(reader.outline)
    chapters = []
    with tempfile.TemporaryDirectory() as temp:
        for chapter, (title, start, end) in CHAPTERS.items():
            bbox = Path(temp) / f'ch{chapter}.html'
            subprocess.run(['pdftotext', '-f', str(start), '-l', str(end),
                            '-bbox-layout', str(SOURCE), str(bbox)], check=True)
            modules = []
            problems = []
            current = None
            module = None
            for page_number, page in enumerate(ET.parse(bbox).findall('.//x:page', NS), start):
                lines = page.findall('.//x:line', NS)
                def words(line):
                    return ' '.join(word.text or '' for word in line.findall('x:word', NS))
                top = 0
                if page_number == start:
                    heading = next(line for line in lines if words(line) == 'Problems')
                    top = float(heading.attrib['yMin'])
                # Poppler sometimes separates a bold problem number from its first
                # sentence. Join aligned lines before reading the two columns.
                rows = []
                for column in (False, True):
                    column_lines = sorted((line for line in lines if (float(line.attrib['xMin']) > 330) == column),
                                          key=lambda line: float(line.attrib['yMin']))
                    for line in column_lines:
                        y = float(line.attrib['yMin'])
                        if rows and rows[-1]['column'] == column and abs(rows[-1]['y'] - y) < 2.5:
                            rows[-1]['lines'].append(line)
                        else:
                            rows.append({'column': column, 'y': y, 'lines': [line]})
                for row in rows:
                    aligned = sorted(row['lines'], key=lambda line: float(line.attrib['xMin']))
                    x, y = float(aligned[0].attrib['xMin']), row['y']
                    if y < top or y < 60 or y > 757:
                        continue
                    text = ' '.join(words(line) for line in aligned)
                    match = re.match(r'^Module (\d+-\d+)\b', text)
                    if match or text == 'Additional Problems':
                        code = match[1] if match else f'{chapter}-mixed'
                        module = {'id': code, 'title': titles[code] if match else 'Additional problems · mixed review',
                                  'page': page_number, 'problems': []}
                        modules.append(module)
                        current = None
                        continue
                    match = re.match(r'^(?:•+\s*)?(\d+)(?=\s|$)', text)
                    if (match and int(match[1]) == len(problems) + 1
                            and (60 < x < 78 or 335 < x < 355)
                            and module and (module['id'].endswith('-mixed') or text.startswith('•'))):
                        if module is None:
                            raise ValueError(f'Problem without module: chapter {chapter}, page {page_number}')
                        current = {'number': int(match[1]), 'module': module['id'], 'page': page_number,
                                   'x': round(x, 2), 'y': round(y, 2), 'search_text': ''}
                        problems.append(current)
                        module['problems'].append(current['number'])
                    if current:
                        # Text is used only for searching. Original page images are authoritative
                        # because the PDF's math font has an unreliable character map.
                        current['search_text'] += text + ' '
            if len(problems) != EXPECTED_COUNTS[chapter] or not modules[-1]['problems']:
                raise ValueError(f'Incomplete problem extraction: chapter {chapter}')
            for i, problem in enumerate(problems):
                next_page = problems[i + 1]['page'] if i + 1 < len(problems) else end
                problem['pages'] = list(range(problem['page'], next_page + 1))
                problem['search_text'] = re.sub(r'\s+', ' ', problem['search_text']).strip()
            chapters.append({'number': chapter, 'title': title, 'start_page': start, 'end_page': end,
                             'count': len(problems), 'modules': modules, 'problems': problems})
            print(f'Chapter {chapter}: {len(problems)} consecutive problems', flush=True)
    data = {'source': SOURCE.name, 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'textbook': 'Halliday & Resnick Fundamentals of Physics, 10th edition, Extended, Jearl Walker',
            'scope': 'Complete end-of-chapter Problems sections from chapters used by the course. Includes additional mixed problems and extension topics.',
            'chapters': chapters, 'problem_count': sum(ch['count'] for ch in chapters)}
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return data


def render(data):
    from PIL import Image
    ASSETS.mkdir(parents=True, exist_ok=True)
    def chapter_images(chapter):
        start, end = chapter['start_page'], chapter['end_page']
        if all((ASSETS / f'page-{number:04d}.webp').exists() for number in range(start, end + 1)):
            return
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp) / 'page'
            subprocess.run(['pdftoppm', '-f', str(start), '-l', str(end), '-png',
                            '-scale-to-x', '1800', '-scale-to-y', '-1',
                            str(SOURCE), str(prefix)], check=True, stderr=subprocess.DEVNULL)
            images = list(Path(temp).glob('page-*.png'))
            if len(images) != end - start + 1:
                raise ValueError(f'Missing rendered pages in chapter {chapter["number"]}')
            for image in images:
                page_number = int(image.stem.split('-')[-1])
                with Image.open(image) as pixels:
                    pixels.save(ASSETS / f'page-{page_number:04d}.webp', lossless=True, method=4)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(chapter_images, data['chapters']))


def section(data=None):
    data = data or json.loads(MANIFEST.read_text())
    outline = json.loads((ROOT / 'course-outline.json').read_text())
    units = outline['units']
    module_units = {}
    for unit in units:
        for lesson in unit['lessons']:
            for reference in lesson['textbook_references']:
                module_units.setdefault(reference['section'], set()).add(unit['number'])
    def numbers(values):
        return ','.join(str(value) for value in sorted(values))
    page_count = sum(ch['end_page'] - ch['start_page'] + 1 for ch in data['chapters'])
    output = f'''<section id="textbook-problems" class="textbook-bank" aria-labelledby="textbook-title">
<div class="eyebrow">Practice from your textbook</div><h2 id="textbook-title">Textbook problem bank</h2>
<p>All {data['problem_count']:,} numbered problems from the 16 chapters used in this course, including their additional mixed problem sets. Choose a number to read the original question with its equations, tables, and diagrams.</p>
<p class="status">Topics that match the lesson references are marked <strong>Lesson focus</strong>. Other topics are marked <strong>Extension</strong>; mixed sets can include both. Some source problems require calculus or additional physics. Problem numbers restart in every chapter.</p>
<div class="bank-controls"><label for="problem-unit">Course unit<select id="problem-unit"><option value="all">All units</option>'''
    output += ''.join(f'<option value="{unit["number"]}">{unit["number"]}. {E(unit["title"])}</option>' for unit in units)
    output += '''</select></label><label for="problem-search">Find a problem<input id="problem-search" type="search" placeholder="e.g. friction, pendulum, or 4.23"></label><button id="problem-reset" type="button">Reset filters</button></div>
<p id="problem-status" class="status" aria-live="polite"></p><noscript><p>Expand a chapter and use its PDF links to read the original problems. Enable JavaScript for search and the inline page viewer.</p></noscript>'''
    for chapter in data['chapters']:
        n = chapter['number']
        by_number = {problem['number']: problem for problem in chapter['problems']}
        related = set().union(*(module_units.get(module['id'], set()) for module in chapter['modules']))
        output += f'''<details class="problem-chapter" id="problems-ch-{n}" data-units="{numbers(related)}"><summary><span><strong>Chapter {n} · {E(chapter['title'])}</strong><span class="chapter-meta">{chapter['count']} problems · printed pp. {chapter['start_page']-36}–{chapter['end_page']-36}</span></span></summary>
<div class="chapter-body"><p class="status">Related course units: {', '.join(str(value) for value in sorted(related))}. <a href="{PDF_URL}#page={chapter['start_page']}" target="_blank" rel="noopener">Open this problem set in the PDF ↗</a></p>'''
        for module in chapter['modules']:
            matched = module_units.get(module['id'], set())
            mixed = module['id'].endswith('-mixed')
            label = 'Mixed review' if mixed else 'Lesson focus' if matched else 'Extension'
            output += f'''<div class="problem-module" data-units="{numbers(matched)}"><h3>{'' if mixed else '§'+module['id']+' · '}{E(module['title'])} <span class="topic-tag {'focus' if matched else ''}">{label}</span></h3><div class="problem-numbers">'''
            for number in module['problems']:
                problem = by_number[number]
                keywords = (f'{n}.{number} {n}-{number} chapter {n} problem {number} '
                            f'{chapter["title"]} {module["title"]} {problem["search_text"]}').lower()
                output += f'''<a class="problem-number" href="{PDF_URL}#page={problem['page']}" data-target="problem-page-{problem['page']}" data-pages="{numbers(problem['pages'])}" data-y="{problem['y']}" data-x="{problem['x']}" data-number="{n}.{number}" data-search="{E(keywords, quote=True)}" aria-label="Chapter {n}, problem {number}">{number}</a>'''
            output += '</div></div>'
        output += '<div class="source-pages"><h3>Original problem pages</h3><p class="status">Open a page below, or choose a problem number above. Use “Enlarge page” for small print. PDF pages use the viewer numbering; printed pages are 36 lower.</p>'
        for page_number in range(chapter['start_page'], chapter['end_page'] + 1):
            starts = [problem['number'] for problem in chapter['problems'] if problem['page'] == page_number]
            range_text = str(starts[0]) if len(starts) == 1 else f'{starts[0]}–{starts[-1]}' if starts else 'continuations'
            description = f'Chapter {n} problems, printed page {page_number-36}, PDF page {page_number}. Problems starting here: {range_text}. May include continuations from the preceding page.'
            asset = f'assets/textbook-problems/page-{page_number:04d}.webp'
            output += f'''<details class="problem-page" id="problem-page-{page_number}"><summary>PDF p. {page_number} · printed p. {page_number-36} · problems {range_text}</summary><div class="page-tools"><span class="page-selection" aria-live="polite"></span><a href="{asset}" target="_blank" rel="noopener">Enlarge page ↗</a><a href="{PDF_URL}#page={page_number}" target="_blank" rel="noopener">Open PDF ↗</a><button class="close-problem-page" type="button">Close page</button></div><div class="problem-image"><img data-src="{asset}" width="1800" height="2150" alt="{E(description)}"><span class="problem-marker" hidden aria-hidden="true"></span></div></details>'''
        output += '</div></div></details>'
    return output + f'''<p id="problem-empty" hidden>No problems match these filters. Try another word or choose All units.</p><p class="status bank-credit">Source: {E(data['textbook'])}, supplied <a href="{PDF_URL}">{E(data['source'])}</a>. {page_count} original problem pages are included locally. Search uses the PDF text layer; consult the displayed original for mathematical notation. Continuation pages are opened with the selected problem when needed.</p></section>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true', help='Re-extract the numbered problem index (requires pypdf and pdftotext).')
    parser.add_argument('--render', action='store_true', help='Create missing lossless local page images (requires pdftoppm and Pillow).')
    args = parser.parse_args()
    data = extract() if args.extract else json.loads(MANIFEST.read_text())
    if args.render:
        render(data)
    print(f'Built bank: {data["problem_count"]:,} problems in {len(data["chapters"])} chapters.')
