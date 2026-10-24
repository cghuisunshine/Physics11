#!/usr/bin/env python3
"""Extract Chapter 4 question crops into a single offline HTML file.

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
from bc_newtons_laws_answers import ANSWERS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'bc_science_physics_11.pdf'
WORK = ROOT / 'tmp/bc-ch4-render'
WORK.mkdir(parents=True, exist_ok=True)
BBOX = ROOT / 'tmp/bc-ch4-bbox.html'
subprocess.run(['pdftotext', '-f', '107', '-l', '135', '-bbox-layout', str(SOURCE), str(BBOX)], check=True)
raw = BBOX.read_text()
raw = ''.join(chr(0xe000 + ord(c)) if ord(c) < 32 and c not in '\t\n\r' else c for c in raw)
NS = {'x': 'http://www.w3.org/1999/xhtml'}
pages = ET.fromstring(raw).findall('.//x:page', NS)
LINES = {}
DIMS = {}
for number, page in enumerate(pages, 107):
    DIMS[number] = (float(page.attrib['width']), float(page.attrib['height']))
    lines = []
    for line in page.findall('.//x:line', NS):
        text = ' '.join(w.text or '' for w in line.findall('x:word', NS))
        text = ''.join(chr(ord(c)-0xe000) if 0xe000 <= ord(c) < 0xe020 else c for c in text)
        text = ''.join(chr(ord(c)+31) if ord(c) < 96 and c not in '\n\r\t\f ' else c for c in text)
        lines.append({**{k: float(v) for k, v in line.attrib.items()}, 'text': text})
    LINES[number] = lines

if not all((WORK / f'page-{p:03}.png').exists() for p in range(107, 136)):
    subprocess.run(['pdftoppm', '-f', '107', '-l', '135', '-scale-to', '2000', '-png', str(SOURCE), str(WORK / 'page')], check=True)

GROUPS = []
def group(topic, kind, title, shared=None, context=None):
    g = dict(id=f'set-{len(GROUPS)+1}', topic=topic, kind=kind, title=title, questions=[], shared=shared or [], context=context or [])
    GROUPS.append(g)
    return g

def add(g, label, boxes):
    texts = []
    for page, x0, y0, x1, y1 in boxes:
        texts += [l['text'] for l in LINES[page] if x0 <= l['xMin'] < x1 and y0 <= l['yMin'] < y1]
    g['questions'].append(dict(label=str(label), boxes=boxes, text=' '.join(texts)))

def full(page, y0, y1):
    return (page, 54, y0, 575, y1)

# Text crops follow complete Poppler line bounds, preventing clipped descenders.
def text_box(page,y0,y1,x0=54,x1=575):
    lines=[l for l in LINES[page] if x0 <= l['xMin'] < x1 and y0 <= l['yMin'] < y1]
    assert lines, (page,y0,y1)
    return (page,x0,min(l['yMin'] for l in lines)-.4,x1,max(l['yMax'] for l in lines)+.4)

def entries(g,page,ranges,x0=54,x1=575):
    for label,a,b in ranges: add(g,label,[text_box(page,a,b,x0,x1)])

def reviews(topic,title,page_numbers,expected,kind='Section review'):
    g=group(topic,kind,title)
    for page in page_numbers:
        left=63 if (page-5)%2 else 48
        for x0,x1,anchor in [(left-4,left+243,left),(left+254,576,left+258)]:
            starts=[]
            for line in LINES[page]:
                m=re.match(r'^(\d+)[.]?\s+',line['text'])
                if m and abs(line['xMin']-anchor)<2 and 40<line['yMin']<718:
                    starts.append((int(m[1]),line['yMin']))
            starts.sort(key=lambda v:v[1])
            for i,(label,y) in enumerate(starts):
                end=starts[i+1][1]-.01 if i+1<len(starts) else 725
                add(g,label,[(page,x0,y-.4,x1,end-.4)])
    g['questions'].sort(key=lambda q:int(q['label']))
    assert [int(q['label']) for q in g['questions']]==list(range(1,expected+1)),title
    return g

g=group('4.1','Warm-up',"Inertia and Newton's first law: warm-up");add(g,'Warm-up',[text_box(107,123,166)])
g=group('4.1','Quick check','Inertial mass: quick check');entries(g,108,[(1,453,467),(2,515,557)])
g=group('4.1','Quick check',"Newton's first law: quick check");entries(g,109,[(1,379,407),(2,473,515),(3,581,610)])
g=group('4.1','Investigation','Investigation 4-1, Problem 1: seatbelts',context=[full(110,60,409)])
entries(g,110,[(1,424,438),(2,438,451),(3,451,465)])
g=group('4.1','Investigation','Investigation 4-1, Problem 2: air and inertia',context=[(110,54,474,347,607),(110,349,474,576,713)])
entries(g,110,[(1,622,650)],x1=347)
g=group('4.1','Investigation','Investigation 4-1, Problem 3: an air track',context=[full(111,60,181),full(111,244,334)])
entries(g,111,[(1,197,210),(2,210,224),(3,224,238)])
g=group('4.1','Investigation','Investigation 4-1, Problem 4: the train track',context=[full(111,349,509),full(111,548,702)])
entries(g,111,[(1,525,538)])
g=group('4.1','Investigation','Investigation 4-1, Problem 5: breaking string',context=[(112,54,60,375,222),(112,375,60,576,257)])
entries(g,112,[(1,237,251),(2,251,279)],x1=375)
g=group('4.1','Investigation','Investigation 4-1, Problem 6: the pop-up coaster',context=[full(112,287,572)])
entries(g,112,[(1,587,601),(2,601,614),(3,614,643)])
g=group('4.1','Investigation','Investigation 4-1: concluding question');add(g,'Concluding question',[text_box(112,666.5,714)])
reviews('4.1',"4.1 Review: inertia and Newton's first law",[113],9)
spool_setup=text_box(114,124,166)
g=group('4.2','Warm-up',"Newton's second law: warm-up",shared=[spool_setup]);entries(g,114,[(1,179,208),(2,267,295)])
g=group('4.2','Quick check','Net force, mass, and acceleration: quick check');entries(g,115,[(1,88,118),(2,223,239),(3,345,374)])
g=group('4.2','Sample prompt','Sample 4.2.1: multiple forces acting on a body');add(g,'4.2.1',[full(116,80,318)])
g=group('4.2','Practice','Practice 4.2.1: multiple forces acting on a body');entries(g,117,[(1,81,112),(2,204,232),(3,321,353),(4,446,597)])
g=group('4.2','Investigation',"Investigation 4-2: Newton's second law",context=[full(118,60,724),full(119,60,526)])
entries(g,119,[(1,541,555),(2,555,582),(3,582,609),(4,609,622),(5,622,652)])
reviews('4.2',"4.2 Review: Newton's second law",[120],6)
third_law_warmup=full(121,130,454)
g=group('4.3','Warm-up',"Newton's third law: warm-up");add(g,1,[third_law_warmup])
g=group('4.3','Quick check','Action and reaction: quick check',shared=[third_law_warmup]);entries(g,122,[(1,532,545),(2,545,574),(3,624,653)])
g=group('4.3','Investigation','Investigation 4-3, Part 1: exploding carts',context=[full(123,60,358)])
entries(g,123,[(1,359,438),(2,438,502),(3,502,547)])
g=group('4.3','Investigation','Investigation 4-3, Part 2: motion from rest',context=[full(124,60,234)])
entries(g,124,[(1,235,305),(2,305,319)])
g=group('4.3','Investigation','Investigation 4-3, Part 3: tug of war',context=[full(124,333,530)])
entries(g,124,[(1,531,564),(2,564,597),(3,597,627)])
g=group('4.3','Investigation','Investigation 4-3: concluding questions');entries(g,124,[(1,649,678),(2,682,711)])
reviews('4.3',"4.3 Review: Newton's third law",[125],7)
momentum_setup=text_box(126,127,190)
g=group('4.4','Warm-up','Momentum: warm-up',shared=[momentum_setup]);entries(g,126,[(1,201,296),(2,308,412)])
g=group('4.4','Quick check','Momentum: quick check');entries(g,127,[(1,89,104),(2,156,171),(3,237,253)])
g=group('4.4','Quick check','Impulse: quick check');add(g,1,[text_box(128,88,340)])
g=group('4.4','Sample prompt','Sample 4.4.1: conservation of momentum');add(g,'4.4.1',[text_box(129,258,295)])
g=group('4.4','Practice','Practice 4.4.1: conservation of momentum');entries(g,130,[(1,82,125),(2,217,246),(3,339,368)])
reviews('4.4','4.4 Review: momentum and impulse',[131],7)
reviews('Chapter review','Chapter 4 Review Questions',[132,133,134],15,kind='Chapter review')
reviews('Extra practice','Chapter 4 Extra Practice',[135],18,kind='Extra practice')
assert sum(len(g['questions']) for g in GROUPS)==121

# Catch cut text in question images, setup references, and procedures.
for g in GROUPS:
    for box in g['shared'] + g['context'] + [b for q in g['questions'] for b in q['boxes']]:
        page,x0,y0,x1,y1=box
        for line in LINES[page]:
            if line['xMax'] > x0 and line['xMin'] < x1:
                assert not (line['yMin'] < y0 < line['yMax'] or line['yMin'] < y1 < line['yMax']), (g['title'], box, line['text'])

CACHE={}
def crop(box, compact=True):
    page,x0,y0,x1,y1=box
    if page not in CACHE: CACHE[page]=Image.open(WORK/f'page-{page:03}.png').convert('RGB')
    im=CACHE[page]; pw,ph=DIMS[page]; sx=im.width/pw; sy=im.height/ph
    im=im.crop((round(x0*sx),round(y0*sy),round(x1*sx),round(y1*sy)))
    # Collapse only wholly blank horizontal bands, preserving charts and tables.
    mask=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda v:255 if v>32 else 0)
    if compact:
        occupied=[mask.crop((0,y,im.width,y+1)).getbbox() is not None for y in range(im.height)]
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
TOPICS=[('4.1',"4.1 Inertia and Newton's first law"),('4.2',"4.2 Newton's second law"),('4.3',"4.3 Newton's third law"),('4.4','4.4 Momentum'),('Chapter review','Chapter review'),('Extra practice','Extra practice')]
KINDS=['Warm-up','Sample prompt','Practice','Quick check','Investigation','Section review','Chapter review','Extra practice']
options=lambda items:''.join(f'<option value="{html.escape(value,quote=True)}">{html.escape(label)}</option>' for value,label in items)
nav=''.join(f'<a href="#{g["id"]}">{g["title"]}</a>' for g in GROUPS)
template='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 4 Newton’s Laws of Motion - All Questions | BC Science Physics 11</title>
<meta name="description" content="121 question entries from Chapter 4 Newton’s Laws of Motion, with original graphs, tables, and individually revealed worked answers. A single offline HTML file.">
<style>
:root{--ink:#203440;--muted:#596b73;--accent:#096a70;--line:#d8e1df;--paper:#f5f6f2}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}a{color:var(--accent)}button,input,select{font:inherit}button,select,input[type=search]{border:1px solid var(--line);border-radius:8px;background:white;color:var(--ink);padding:9px 12px}button{cursor:pointer}button:hover{border-color:var(--accent)}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #66bcb8;outline-offset:3px}header{max-width:1260px;margin:auto;padding:46px 30px 28px}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:12px;color:var(--accent);font-weight:750}h1{font-size:clamp(36px,5vw,58px);line-height:1.1;margin:12px 0 18px;letter-spacing:-.04em}header p{max-width:820px;margin:8px 0;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:9px;margin-top:24px}.chips span{border:1px solid var(--line);padding:5px 12px;border-radius:30px;font-size:13px}.controls-wrap{position:sticky;top:0;z-index:3;background:#f5f6f2f5;border-block:1px solid var(--line);backdrop-filter:blur(8px)}.controls{max-width:1260px;margin:auto;padding:13px 30px;display:flex;flex-wrap:wrap;gap:12px;align-items:end}.control{display:grid;gap:4px}.control label{font-size:12px;color:var(--muted)}.control.search{flex:1;min-width:190px}.controls button{margin-bottom:0}.status{max-width:1260px;margin:18px auto 0;padding:0 30px;font-size:14px;color:var(--muted)}.layout{max-width:1260px;margin:25px auto 60px;padding:0 30px;display:grid;grid-template-columns:225px minmax(0,1fr);gap:32px}aside{align-self:start;position:sticky;top:128px;max-height:calc(100vh - 150px);overflow:auto}aside h2{font-size:13px;letter-spacing:.08em;text-transform:uppercase}nav{display:grid;gap:5px}nav a{font-size:12px;text-decoration:none;padding:6px 9px;border-left:2px solid var(--line)}nav a:hover{background:#e6eeeb;border-color:var(--accent)}.question-set{background:white;border:1px solid var(--line);border-radius:14px;margin-bottom:24px;padding:28px 30px;scroll-margin-top:130px}.set-heading>span{font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:750;color:var(--accent)}h2{font-size:23px;line-height:1.3;margin:9px 0}.set-heading p{font-size:13px;color:var(--muted);margin:0 0 24px}.question{border-top:1px solid var(--line);padding:22px 0;scroll-margin-top:145px}.question:last-child{padding-bottom:0}.question-top{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:14px;font-size:12px;color:var(--muted)}.question-top a{font-weight:750;font-size:14px;text-decoration:none}.question-top label{margin-left:auto;cursor:pointer;display:flex;align-items:center;gap:6px}.question-top input{accent-color:var(--accent);width:17px;height:17px}.question-image img,.context img,.shared img{display:block;margin:12px 0}.question[data-done=true] .question-top a::after{content:' ✓';color:var(--accent)}figure{margin:0 0 24px}figcaption{font-size:12px;color:var(--muted)}.context{border:1px solid var(--line);border-radius:8px;padding:12px 16px;margin-bottom:22px}.context summary{cursor:pointer;font-size:14px;color:var(--accent)}.empty{padding:35px;background:white;border:1px solid var(--line);border-radius:12px}footer{max-width:1260px;margin:auto;padding:20px 30px 40px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}[hidden]{display:none!important}.skip{position:absolute;top:-100px}.skip:focus{top:10px;background:white;padding:10px;z-index:5}
.answer-toggle{margin-top:12px;border-color:var(--accent);color:var(--accent);font-weight:650}.answer-toggle[aria-expanded=true]{background:var(--accent);color:white}.answer{margin-top:14px;padding:18px 20px;background:#f0f7f3;border:1px solid #c9dfd4;border-radius:10px;overflow-wrap:anywhere}.answer h3{font-size:16px;margin:0 0 12px;color:var(--accent)}.answer p{margin:10px 0}.answer p:last-child{margin-bottom:0}.answer-parts{padding-left:24px;margin:0}.answer-parts li{padding-left:4px;margin:10px 0}.answer-table{overflow-x:auto;margin:16px 0}.answer table{border-collapse:collapse;font-size:14px;background:white;min-width:260px}.answer th,.answer td{text-align:left;padding:7px 14px;border:1px solid var(--line);white-space:nowrap}.answer th{background:#e3eee8}.answer-graph{margin:18px 0 8px}.answer-graph svg{display:block;width:100%;max-width:450px;height:auto;background:white;border:1px solid var(--line);border-radius:8px;font:12px system-ui,sans-serif;fill:var(--ink)}.answer-graph figcaption{margin-top:7px}.answer sub{font-size:.75em}
@media(max-width:850px){.layout{grid-template-columns:1fr;padding:0 16px}aside{position:static;max-height:none}aside nav{grid-template-columns:1fr 1fr}header{padding:30px 18px}.controls{padding:12px 16px}.control{flex:1;min-width:150px}.controls button{flex:0 0 auto}.question-set{padding:23px 18px}.status{padding:0 16px}.question-top label{margin-left:0}}
@media(max-width:600px){.question-image,.shared,.context{overflow-x:auto}.question-image img,.shared img,.context img{max-width:none!important}}
@media print{.answer-toggle{display:none!important}.answer{background:white;border-color:#bbb}.answer-graph{break-inside:avoid}}
@media print{body{background:white;color:black;font-size:11pt}header{padding:0 0 16px}h1{font-size:30pt}.controls-wrap,aside,.status,.chips,.question-top label,.skip,footer,.empty{display:none!important}.layout{display:block;margin:0;padding:0}.question-set{border:0;border-radius:0;padding:16px 0;margin:0}.question{break-inside:avoid}.question-image img{max-width:100%!important}.question-top{margin-bottom:6px}h2,.set-heading{break-after:avoid}.shared{break-inside:avoid}.context{display:none}.question-set[hidden],.question[hidden]{display:none!important}}
@@HOMEWORK_STYLES@@
@@FILTER_STYLES@@
</style></head><body><a class="skip" href="#questions">Skip to questions</a>
<header><div class="eyebrow">BC Science Physics 11 / Chapter 4</div><h1>Newton’s Laws of Motion<br>Questions &amp; answers</h1><p>Every warm-up, quick check, practice problem, section and chapter review, and extra-practice problem, plus both sample-problem prompts and the investigation questions.</p><p>Try each question, then select <strong>Show answer</strong> to reveal its worked answer. Investigation answers explain how to use your measurements. Procedures open below their headings. On narrow screens, swipe wide extracts sideways.</p><p>Answers use g = 9.81 m/s² unless a question specifies another value. Choose a positive direction before adding forces or momenta. Assumptions and ambiguous wording are explained in the affected answers. Printing includes the answers you have revealed.</p><div class="chips"><span>121 question entries, including subparts</span><span>Worked answers · Hidden until opened</span><span>Printed pages 102-130</span><span>Single file · Works offline</span></div></header>
<div class="controls-wrap"><div class="controls"><div class="control search"><label for="search">Search questions</label><input id="search" type="search" placeholder="Try inertia, momentum, or 4.2"></div><div class="control"><label for="topic">Section</label><select id="topic"><option value="">All sections</option>@@TOPICS@@</select></div><div class="control"><label for="kind">Question type</label><select id="kind"><option value="">All types</option>@@KINDS@@</select></div><button id="reset" type="button">Clear filters</button><button id="print" type="button">Print / Save PDF</button><button id="create-homework" type="button" aria-expanded="false" aria-controls="homework-panel">Create homework</button><button id="all-questions" type="button" hidden>Show all questions</button></div></div>
<section id="homework-panel" class="homework-panel" aria-label="Create homework" hidden>
<h2>Create homework</h2><p>Select <strong>Homework</strong> beside individual questions, or filter the collection and select all shown questions. Your selection is saved on this device.</p>
<div class="homework-fields"><label>Homework title<input id="homework-name" maxlength="160" placeholder="Newton’s Laws of Motion homework"></label><label>Instructions (optional)<textarea id="homework-instructions" maxlength="2000" rows="2" placeholder="Show your working and include units."></textarea></label></div>
<label class="homework-answers"><input id="homework-answers" type="checkbox"> Include worked answers</label>
<fieldset class="homework-sampling"><legend>Choose questions by section</legend>
<p id="sampling-help">Use a percentage of the eligible questions in each section. Section, type, and search filters apply across the full collection. Odd/even uses the textbook question number within each set; unnumbered warm-ups and sample labels such as 2.1.1 are included only with All numbers.</p>
<div class="sampling-controls"><label>Question numbers<select id="homework-parity"><option value="all">All numbers</option><option value="odd">Odd numbers</option><option value="even">Even numbers</option></select></label><label>Selection method<select id="homework-sampling-order"><option value="random">Random sample</option><option value="first">First in order</option><option value="ai">AI selection</option></select></label><label>Set all sections to (%)<input id="homework-all-percent" type="number" min="0" max="100" step="1" value="50"></label><button id="set-section-percentages" type="button">Set all percentages</button></div>
<div class="homework-ai-criteria"><label for="homework-ai-prompt">AI selection criteria (optional)</label><textarea id="homework-ai-prompt" rows="3" maxlength="4000" aria-describedby="homework-ai-help" placeholder="Example: Choose beginner questions applying Newton's second law. Avoid momentum and collision questions."></textarea></div>
<p id="homework-ai-help">Describe the topics, skills, difficulty, or question styles you want, then click <strong>AI: choose questions</strong>. Leave the criteria blank to choose the most difficult questions. AI respects your section percentages, filters, and odd/even choice. With criteria, each percentage is a maximum: AI may choose fewer questions or none if there are not enough matches. Use 100% to find all matching questions in a section; 0% skips it. AI selection needs internet access and sends your criteria and eligible questions to the practice studio's AI service. Reasons are shown after selection, and you can adjust the result.</p>
<div class="sampling-table-wrap"><table class="sampling-table"><thead><tr><th scope="col">Section</th><th scope="col">Select (%)</th><th scope="col">Questions to select</th></tr></thead><tbody id="homework-sections"></tbody></table></div>
<p>Counts round up. 0% skips a section. With AI criteria, the count is a maximum and 100% searches all eligible questions for matches. For random sampling, first in order, or AI with blank criteria, 100% selects every eligible question. Applying percentages replaces the selection within the current filters and keeps selections outside them.</p>
<div class="homework-actions"><button id="apply-section-percentages" type="button" data-single-selection-action>Choose random questions</button><button id="select-matching-numbers" type="button">Add matching numbers</button><button id="cancel-homework-ai" type="button" hidden>Cancel AI selection</button></div>
<p id="homework-ai-status" role="status"></p><details id="homework-ai-results" hidden><summary>Why AI selected these questions</summary><ul id="homework-ai-list"></ul></details>
</fieldset>
<div class="homework-actions"><button id="select-shown" type="button">Select shown questions</button><button id="clear-selection" type="button">Clear selection</button><button type="button" data-edit-selection>Adjust questions</button><button id="preview-homework" type="button">Preview homework</button><button id="copy-homework" type="button">Copy homework link</button><button id="download-homework" type="button">Download homework HTML</button><button id="print-homework" type="button">Print homework / Save PDF</button></div>
<div class="homework-ai-criteria"><label for="homework-refine-prompt">AI criteria to filter the current selection</label><textarea id="homework-refine-prompt" rows="2" maxlength="4000" aria-describedby="homework-refine-help" placeholder="Example: Remove momentum and collision questions. Or: Keep the five easiest net-force questions."></textarea><div class="homework-actions"><button id="refine-homework-ai" type="button">AI: filter selected questions</button><button id="cancel-homework-refine" type="button" hidden>Cancel AI filtering</button></div><p id="homework-refine-help">Select homework questions and enter what to keep or remove. AI reviews the current selection together, then shows the remaining questions. Internet access is required. A failed or canceled request keeps your selection unchanged.</p><p id="homework-refine-status" role="status"></p><details id="homework-refine-results" hidden><summary>Why AI kept these questions</summary><ul id="homework-refine-list"></ul></details></div>
<p id="homework-count" aria-live="polite"></p><p id="homework-message" role="status"></p>
<div id="homework-link-row" hidden><label for="homework-link">Homework link</label><input id="homework-link" type="url" readonly></div>
</section>
<section id="homework-banner" class="homework-banner" hidden><h1 id="homework-title"></h1><p id="homework-details"></p><p id="homework-directions"></p><button type="button" data-edit-selection>Adjust questions</button></section>
<p class="status" id="status" aria-live="polite"></p><div class="layout"><aside aria-label="Question sets"><h2>Browse the chapter</h2><nav>@@NAV@@</nav></aside><main id="questions">@@SECTIONS@@<p class="empty" id="empty" hidden>No questions match. Try a different word or clear the filters.</p></main></div>
<footer>Source: BC Science Physics 11, Chapter 4 Newton’s Laws of Motion, Edvantage Interactive (2012). Original numbering restarts in each set. Worked answers are independently calculated for this collection. All question images, answers, styles, and controls are embedded. Viewing questions, manual homework selection, and exports work offline; AI selection and filtering require internet access. Completion marks are saved in this browser when local storage is available.</footer>
<script>
@@FILTER_SCRIPT@@
</script><script>
@@HOMEWORK_AI_SCRIPT@@
</script><script>
@@HOMEWORK_SCRIPT@@
</script></body></html>'''
template=template.replace('@@TOPICS@@',options(TOPICS)).replace('@@KINDS@@',options([(k,k) for k in KINDS])).replace('@@NAV@@',nav).replace('@@SECTIONS@@',''.join(sections))
template=template.replace('@@HOMEWORK_STYLES@@',(ROOT/'tools/bc-kinematics-homework.css').read_text()).replace('@@HOMEWORK_SCRIPT@@',(ROOT/'tools/bc-kinematics-homework.js').read_text().replace('bc-physics11-ch2','bc-physics11-ch4').replace('Kinematics','Newton’s Laws of Motion').replace('Chapter 2','Chapter 4').replace('bc-kinematics-questions.html','bc-newtons-laws-questions.html').replace('kinematics-homework','newtons-laws-homework'))
template=template.replace("`${set.querySelectorAll('.question').length} entries`", "`${set.querySelectorAll('.question').length} ${set.querySelectorAll('.question').length===1?'entry':'entries'}`")
template=template.replace('@@HOMEWORK_AI_SCRIPT@@',(ROOT/'tools/bc-kinematics-homework-ai.js').read_text().replace('kinematics-difficulty','newtons-laws-difficulty'))
template=template.replace('@@FILTER_STYLES@@',(ROOT/'tools/bc-question-filter-picker.css').read_text()).replace('@@FILTER_SCRIPT@@',(ROOT/'tools/bc-question-filter-picker.js').read_text())
output=ROOT/'bc-newtons-laws-questions.html'; output.write_text(template)
manifest=ROOT/'content/bc-newtons-laws-questions.json'
manifest.write_text(json.dumps(dict(source=SOURCE.name,chapter=4,title="Newton's Laws of Motion",question_count=sequence,groups=GROUPS),indent=2,ensure_ascii=False))
print(f'Created {output}: {sequence} entries, {len(GROUPS)} sets, {output.stat().st_size:,} bytes')
