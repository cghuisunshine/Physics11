#!/usr/bin/env python3
"""Extract Chapter 5 question crops into a single offline HTML file.

Run with Python containing Pillow (e.g. the local miniconda Python).
Poppler pdftotext and pdftoppm must be on PATH. Original math and diagrams
are preserved as images because the source PDF has faulty character maps.
"""
from pathlib import Path
import base64
import html
import io
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops
from bc_energy_answers import ANSWERS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'bc_science_physics_11.pdf'
WORK = ROOT / 'tmp/bc-ch5-render'
WORK.mkdir(parents=True, exist_ok=True)
BBOX = ROOT / 'tmp/bc-ch5-bbox.html'
subprocess.run(['pdftotext', '-f', '137', '-l', '177', '-bbox-layout', str(SOURCE), str(BBOX)], check=True)
raw = BBOX.read_text()
raw = ''.join(chr(0xe000 + ord(c)) if ord(c) < 32 and c not in '\t\n\r' else c for c in raw)
NS = {'x': 'http://www.w3.org/1999/xhtml'}
pages = ET.fromstring(raw).findall('.//x:page', NS)
LINES = {}
DIMS = {}
for number, page in enumerate(pages, 137):
    DIMS[number] = (float(page.attrib['width']), float(page.attrib['height']))
    lines = []
    for line in page.findall('.//x:line', NS):
        text = ' '.join(w.text or '' for w in line.findall('x:word', NS))
        text = ''.join(chr(ord(c)-0xe000) if 0xe000 <= ord(c) < 0xe020 else c for c in text)
        text = ''.join(chr(ord(c)+31) if ord(c) < 96 and c not in '\n\r\t\f ' else c for c in text)
        lines.append({**{k: float(v) for k, v in line.attrib.items()}, 'text': text})
    LINES[number] = lines

if not all((WORK / f'page-{p:03}.png').exists() for p in range(137, 178)):
    subprocess.run(['pdftoppm', '-f', '137', '-l', '177', '-scale-to', '2000', '-png', str(SOURCE), str(WORK / 'page')], check=True)

from bc_energy_inventory import build_groups
GROUPS = build_groups(LINES)

# Catch cut text in question images, setup references, and procedures.
for g in GROUPS:
    for box in g['shared'] + g['context'] + [b for q in g['questions'] for b in q['boxes']]:
        page,x0,y0,x1,y1=box
        for line in LINES[page]:
            if line['xMax'] > x0 and line['xMin'] < x1:
                assert not (line['yMin'] < y0 < line['yMax'] or line['yMin'] < y1 < line['yMax']), (g['title'], box, line['text'])
                if y0 <= line['yMin'] < y1 and x0 <= line['xMin'] < x1:
                    assert line['xMax'] <= x1 + .5, ('Horizontal text cut',g['title'],box,line['text'])

CACHE={}
def crop(box, compact=True):
    page,x0,y0,x1,y1=box
    if page not in CACHE: CACHE[page]=Image.open(WORK/f'page-{page:03}.png').convert('RGB')
    im=CACHE[page]; pw,ph=DIMS[page]; sx=im.width/pw; sy=im.height/ph
    im=im.crop((round(x0*sx),round(y0*sy),round(x1*sx),round(y1*sy)))
    # Collapse only wholly blank horizontal bands, preserving charts and tables.
    mask=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda v:255 if v>32 else 0)
    if compact:
        occupied=mask.getprojection()[1]
        ranges=[]; start=0; y=0
        while y<len(occupied):
            if occupied[y]: y+=1; continue
            stop=y
            while stop<len(occupied) and not occupied[stop]: stop+=1
            if stop-y>50:
                ranges.append((start,min(y+12,stop))); start=max(y+12,stop-12)
            y=stop
        ranges.append((start,im.height))
        height=sum(b-a for a,b in ranges)
        out=Image.new('RGB',(im.width,height),'white'); cursor=0
        for a,b in ranges: out.paste(im.crop((0,a,im.width,b)),(0,cursor)); cursor+=b-a
        im=out
    bounds=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda v:255 if v>32 else 0).getbbox()
    if bounds:
        a,b,c,d=bounds; im=im.crop((max(0,a-8),max(0,b-8),min(im.width,c+8),min(im.height,d+8)))
    stream=io.BytesIO(); im.save(stream,'WEBP',lossless=True)
    return 'data:image/webp;base64,'+base64.b64encode(stream.getvalue()).decode(),im.width,im.height

def pictures(boxes, alt, compact=True):
    rendered=[]
    for box in boxes:
        src,w,h=crop(box,compact)
        # Keep equivalent physical font sizes for narrow and full-width crops.
        width=round(w/(2000/794)*1.45)
        rendered.append(f'<img src="{src}" alt="{html.escape(alt,quote=True)}" width="{w}" height="{h}" style="width:{width}px;max-width:100%;height:auto" loading="lazy">')
    return ''.join(rendered)

sections=[]; sequence=0
for g in GROUPS:
    body=''
    if g['shared']:
        caption='Use this reference for the questions in this set.'
        body+='<figure class="shared">'+pictures(g['shared'],'Shared reference for '+g['title'],False)+f'<figcaption>{caption}</figcaption></figure>'
    if g['context']: body+='<details class="context"><summary>Investigation procedure and data tables</summary>'+pictures(g['context'],'Procedure and data for '+g['title'],False)+'</details>'
    for q in g['questions']:
        sequence+=1; key=f'q-{sequence}'; q['id']=key
        q['answer_html']=ANSWERS[key]
        page_nums=sorted(set(box[0]-5 for box in q['boxes']))
        pages_label=', '.join(map(str,page_nums))
        alt=f"{g['title']}, question {q['label']}. "+q['text']
        body+=f'<article class="question" id="{key}" data-search="{html.escape((g["title"]+" "+q["label"]+" "+q["text"]).lower(),quote=True)}"><div class="question-top"><a href="#{key}">Question {html.escape(q["label"])}</a><span>Textbook p. {pages_label}</span><label><input type="checkbox" data-complete="{key}"> Done</label><label class="homework-select" hidden><input type="checkbox" data-homework="{key}"> Homework</label></div><div class="question-image">{pictures(q["boxes"],alt)}</div><button class="answer-toggle" id="toggle-{key}" type="button" data-answer-toggle aria-expanded="false" aria-controls="answer-{key}">Show answer</button><div class="answer" id="answer-{key}" role="region" aria-labelledby="toggle-{key}" hidden><h3>Answer</h3>{q["answer_html"]}</div></article>'
    sections.append(f'<section class="question-set" id="{g["id"]}" data-topic="{g["topic"]}" data-kind="{g["kind"]}"><div class="set-heading"><span>{g["kind"]}</span><h2>{g["title"]}</h2><p>{len(g["questions"])} entries</p></div>{body}</section>')

assert set(ANSWERS) == {q['id'] for g in GROUPS for q in g['questions']}
TOPICS=[('5.1','5.1 Work, power, and machines'),('5.2','5.2 Mechanical energy'),('5.3','5.3 Temperature and heat transfer'),('5.4','5.4 Thermal energy and efficiency'),('Chapter review','Chapter review'),('Extra practice','Extra practice')]
KINDS=['Warm-up','Sample prompt','Practice','Quick check','Investigation','Challenge','Section review','Chapter review','Extra practice']
options=lambda items:''.join(f'<option value="{html.escape(value,quote=True)}">{html.escape(label)}</option>' for value,label in items)
nav=''.join(f'<a href="#{g["id"]}">{g["title"]}</a>' for g in GROUPS)
template=(ROOT/'tools/bc-energy-template.html').read_text()
template=template.replace('@@TOPICS@@',options(TOPICS)).replace('@@KINDS@@',options([(k,k) for k in KINDS])).replace('@@NAV@@',nav).replace('@@SECTIONS@@',''.join(sections))
template=template.replace('@@HOMEWORK_STYLES@@',(ROOT/'tools/bc-kinematics-homework.css').read_text()).replace('@@HOMEWORK_SCRIPT@@',(ROOT/'tools/bc-kinematics-homework.js').read_text().replace('bc-physics11-ch2','bc-physics11-ch5').replace('Kinematics','Energy').replace('Chapter 2','Chapter 5').replace('bc-kinematics-questions.html','bc-energy-questions.html').replace('kinematics-homework','energy-homework'))
template=template.replace("`${set.querySelectorAll('.question').length} entries`", "`${set.querySelectorAll('.question').length} ${set.querySelectorAll('.question').length===1?'entry':'entries'}`")
template=template.replace('@@HOMEWORK_AI_SCRIPT@@',(ROOT/'tools/bc-kinematics-homework-ai.js').read_text().replace('kinematics-difficulty','energy-difficulty'))
template=template.replace('@@FILTER_STYLES@@',(ROOT/'tools/bc-question-filter-picker.css').read_text()).replace('@@FILTER_SCRIPT@@',(ROOT/'tools/bc-question-filter-picker.js').read_text())
output=ROOT/'bc-energy-questions.html'; output.write_text(template)
manifest=ROOT/'content/bc-energy-questions.json'
manifest.write_text(json.dumps(dict(source=SOURCE.name,chapter=5,title="Energy",question_count=sequence,groups=GROUPS),indent=2,ensure_ascii=False))
print(f'Created {output}: {sequence} entries, {len(GROUPS)} sets, {output.stat().st_size:,} bytes')
