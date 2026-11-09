"""Render a BC textbook question collection using source-page coordinates."""
from pathlib import Path
import base64
import html
import io
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'bc_science_physics_11.pdf'


def read_pages(first, last, work, scale=2000):
    work.mkdir(parents=True, exist_ok=True)
    raw = subprocess.run(
        ['pdftotext', '-f', str(first), '-l', str(last), '-bbox-layout', str(SOURCE), '-'],
        check=True, capture_output=True, text=True,
    ).stdout
    raw = ''.join(chr(0xe000 + ord(c)) if ord(c) < 32 and c not in '\t\n\r' else c for c in raw)
    namespace = {'x': 'http://www.w3.org/1999/xhtml'}
    pages = ET.fromstring(raw).findall('.//x:page', namespace)
    lines_by_page = {}
    dimensions = {}
    for number, page in enumerate(pages, first):
        dimensions[number] = (float(page.attrib['width']), float(page.attrib['height']))
        lines = []
        for line in page.findall('.//x:line', namespace):
            text = ' '.join(w.text or '' for w in line.findall('x:word', namespace))
            text = ''.join(chr(ord(c)-0xe000) if 0xe000 <= ord(c) < 0xe020 else c for c in text)
            text = ''.join(chr(ord(c)+31) if ord(c) < 96 and c not in '\n\r\t\f ' else c for c in text)
            lines.append({**{k: float(v) for k, v in line.attrib.items()}, 'text': text})
        lines_by_page[number] = lines

    if not all((work / f'page-{p:03}.png').exists() for p in range(first, last + 1)):
        subprocess.run(
            ['pdftoppm', '-f', str(first), '-l', str(last), '-scale-to', str(scale),
             '-png', str(SOURCE), str(work / 'page')], check=True,
        )
    return lines_by_page, dimensions


def build_collection(groups, answers, lines_by_page, dimensions, work, *,
                     chapter, title, slug, topics, kinds, template, scale=2000):
    output_name = f'bc-{slug}-questions'
    # Catch cut text in question images, setup references, and procedures.
    for group in groups:
        question_boxes = [box for question in group['questions'] for box in question['boxes']]
        for box in group['shared'] + group['context'] + question_boxes:
            page, left, top, right, bottom = box
            for line in lines_by_page[page]:
                if line['xMax'] <= left or line['xMin'] >= right:
                    continue
                assert not (line['yMin'] < top < line['yMax'] or
                            line['yMin'] < bottom < line['yMax']), (group['title'], box, line['text'])
                if top <= line['yMin'] < bottom and left <= line['xMin'] < right:
                    assert line['xMax'] <= right + .5, ('Horizontal text cut', group['title'], box, line['text'])

    cache = {}

    def ink_mask(image):
        white = Image.new('RGB', image.size, 'white')
        return ImageChops.difference(image, white).convert('L').point(lambda value: 255 if value > 32 else 0)

    def crop(box, compact):
        page, left, top, right, bottom = box
        if page not in cache:
            with Image.open(work / f'page-{page:03}.png') as source:
                cache[page] = source.convert('RGB')
        source = cache[page]
        page_width, page_height = dimensions[page]
        sx, sy = source.width / page_width, source.height / page_height
        image = source.crop((round(left * sx), round(top * sy), round(right * sx), round(bottom * sy)))
        # Collapse only wholly blank horizontal bands, preserving charts and tables.
        if compact:
            occupied = ink_mask(image).getprojection()[1]
            ranges = []
            start = row = 0
            while row < len(occupied):
                if occupied[row]:
                    row += 1
                    continue
                stop = row
                while stop < len(occupied) and not occupied[stop]:
                    stop += 1
                if stop - row > 50:
                    ranges.append((start, min(row + 12, stop)))
                    start = max(row + 12, stop - 12)
                row = stop
            ranges.append((start, image.height))
            height = sum(end - begin for begin, end in ranges)
            trimmed = Image.new('RGB', (image.width, height), 'white')
            cursor = 0
            for begin, end in ranges:
                trimmed.paste(image.crop((0, begin, image.width, end)), (0, cursor))
                cursor += end - begin
            image = trimmed
        bounds = ink_mask(image).getbbox()
        if bounds:
            left, top, right, bottom = bounds
            image = image.crop((max(0, left - 8), max(0, top - 8),
                                min(image.width, right + 8), min(image.height, bottom + 8)))
        stream = io.BytesIO()
        image.save(stream, 'WEBP', lossless=True)
        return 'data:image/webp;base64,' + base64.b64encode(stream.getvalue()).decode(), image.width, image.height

    def pictures(boxes, alt, compact=True):
        rendered = []
        alt = html.escape(alt, quote=True)
        for box in boxes:
            src, width, height = crop(box, compact)
            # Keep equivalent physical font sizes for narrow and full-width crops.
            display_width = round(width / (scale / 794) * 1.45)
            rendered.append(f'<img src="{src}" alt="{alt}" width="{width}" height="{height}" '
                            f'style="width:{display_width}px;max-width:100%;height:auto" loading="lazy">')
        return ''.join(rendered)

    sections = []
    sequence = 0
    for group in groups:
        body = []
        group_title = group['title']
        if group['shared']:
            body.append('<figure class="shared">' + pictures(group['shared'], 'Shared reference for ' + group_title, False)
                        + '<figcaption>Use this reference for the questions in this set.</figcaption></figure>')
        if group['context']:
            body.append('<details class="context"><summary>Investigation procedure and data tables</summary>'
                        + pictures(group['context'], 'Procedure and data for ' + group_title, False) + '</details>')
        for question in group['questions']:
            sequence += 1
            key = f'q-{sequence}'
            question['id'] = key
            question['answer_html'] = answers[key]
            page_numbers = sorted({box[0] - 5 for box in question['boxes']})
            pages_label = ', '.join(map(str, page_numbers))
            label, question_text = question['label'], question['text']
            search = html.escape(f'{group_title} {label} {question_text}'.lower(), quote=True)
            alt = f'{group_title}, question {label}. {question_text}'
            body.append(
                f'<article class="question" id="{key}" data-search="{search}">'
                f'<div class="question-top"><a href="#{key}">Question {html.escape(label)}</a>'
                f'<span>Textbook p. {pages_label}</span><label><input type="checkbox" data-complete="{key}"> Done</label>'
                f'<label class="homework-select" hidden><input type="checkbox" data-homework="{key}"> Homework</label></div>'
                f'<div class="question-image">{pictures(question["boxes"], alt)}</div>'
                f'<button class="answer-toggle" id="toggle-{key}" type="button" data-answer-toggle '
                f'aria-expanded="false" aria-controls="answer-{key}">Show answer</button>'
                f'<div class="answer" id="answer-{key}" role="region" aria-labelledby="toggle-{key}" hidden>'
                f'<h3>Answer</h3>{answers[key]}</div></article>'
            )
        sections.append(
            f'<section class="question-set" id="{group["id"]}" data-topic="{group["topic"]}" data-kind="{group["kind"]}">'
            f'<div class="set-heading"><span>{group["kind"]}</span><h2>{group_title}</h2>'
            f'<p>{len(group["questions"])} entries</p></div>{"".join(body)}</section>'
        )

    assert set(answers) == {q['id'] for group in groups for q in group['questions']}

    def options(items):
        return ''.join(f'<option value="{html.escape(value, quote=True)}">{html.escape(label)}</option>'
                       for value, label in items)

    files = ROOT / 'tools'
    homework = (files / 'bc-kinematics-homework.js').read_text()
    homework = (homework.replace('bc-physics11-ch2', f'bc-physics11-ch{chapter}')
                .replace('Kinematics', title).replace('Chapter 2', f'Chapter {chapter}')
                .replace('bc-kinematics-questions.html', f'{output_name}.html')
                .replace('kinematics-homework', f'{slug}-homework')
                .replace("`${set.querySelectorAll('.question').length} entries`",
                         "`${set.querySelectorAll('.question').length} ${set.querySelectorAll('.question').length===1?'entry':'entries'}`"))
    replacements = {
        '@@TOPICS@@': options(topics),
        '@@KINDS@@': options((kind, kind) for kind in kinds),
        '@@NAV@@': ''.join(f'<a href="#{group["id"]}">{group["title"]}</a>' for group in groups),
        '@@SECTIONS@@': ''.join(sections),
        '@@HOMEWORK_STYLES@@': (files / 'bc-kinematics-homework.css').read_text(),
        '@@HOMEWORK_SCRIPT@@': homework,
        '@@HOMEWORK_AI_SCRIPT@@': (files / 'bc-kinematics-homework-ai.js').read_text().replace(
            'kinematics-difficulty', f'{slug}-difficulty'),
        '@@FILTER_STYLES@@': (files / 'bc-question-filter-picker.css').read_text(),
        '@@FILTER_SCRIPT@@': (files / 'bc-question-filter-picker.js').read_text(),
    }
    for marker, replacement in replacements.items():
        template = template.replace(marker, replacement)
    output = ROOT / f'{output_name}.html'
    output.write_text(template)
    manifest = ROOT / 'content' / f'{output_name}.json'
    manifest.write_text(json.dumps(dict(source=SOURCE.name, chapter=chapter, title=title,
                                        question_count=sequence, groups=groups), indent=2, ensure_ascii=False))
    print(f'Created {output}: {sequence} entries, {len(groups)} sets, {output.stat().st_size:,} bytes')
