#!/usr/bin/env python3
"""Build the offline Halliday Chapter 2 question collection.

Requires Pillow and Poppler. Crops preserve the original math character maps.
Source coordinates are PDF points; solution pages belong to the companion PDF.
"""
from pathlib import Path
import base64
import html
import io
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Physics text (TOC).pdf'
SOLUTIONS = ROOT / 'Physics answer (TOC).pdf'
WORK = ROOT / 'tmp/halliday-ch2-render'
NS = {'x': 'http://www.w3.org/1999/xhtml'}
LINES, WORDS, DIMS, CACHE = {}, {}, {}, {}


def load_pdf(source, first, last, prefix, bbox):
    prefix.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['pdftotext', '-f', str(first), '-l', str(last),
                    '-bbox-layout', str(source), str(bbox)], check=True)
    pages = ET.parse(bbox).findall('.//x:page', NS)
    for number, page in enumerate(pages, first):
        key = (source.name, number)
        DIMS[key] = (float(page.get('width')), float(page.get('height')))
        LINES[key] = [{**{k: float(v) for k, v in line.attrib.items()},
                       'text': ' '.join(w.text or '' for w in line.findall('x:word', NS))}
                      for line in page.findall('.//x:line', NS)]
        WORDS[key] = [{**{k:float(v) for k,v in w.attrib.items()},'text':w.text or ''}
                      for w in page.findall('.//x:word',NS)]
    if not all(Path(f'{prefix}-{p:04}.png').exists() for p in range(first, last+1)):
        subprocess.run(['pdftoppm', '-f', str(first), '-l', str(last), '-scale-to',
                        '2000', '-png', str(source), str(prefix)], check=True)


load_pdf(SOURCE, 49, 75, WORK / 'page', ROOT / 'tmp/halliday-ch2-bbox.html')
load_pdf(SOLUTIONS, 31, 89, ROOT / 'tmp/halliday-ch2-answer-page',
         ROOT / 'tmp/halliday-ch2-answer-bbox.html')

# Complete figure rectangles. Floating figures are removed from prompt crops
# and appended once, in full, to the questions that refer to them.
FIGURES = {
    15: (66, 67, 417, 328, 533),
    24: (68, 453, 583, 602, 679),
    25: (69, 66, 360, 325, 432),
    26: (69, 489, 630, 602, 749),
    27: (70, 341, 65, 602, 127),
    28: (70, 491, 133, 602, 227),
    29: (70, 499, 311, 602, 435),
    30: (70, 464, 493, 602, 607),
    31: (71, 208, 103, 325, 201),
    32: (71, 66, 475, 325, 617),
    33: (71, 385, 329, 602, 438),
    34: (71, 492, 440, 602, 548),
    35: (72, 173, 123, 331, 256),
    36: (72, 218, 606, 331, 745),
    37: (72, 374, 187, 602, 319),
    38: (72, 430, 321, 602, 444),
    39: (72, 464, 515, 602, 622),
    40: (72, 474, 625, 602, 747),
    41: (73, 66, 463, 325, 533),
    42: (73, 66, 652, 325, 747),
    43: (73, 464, 374, 602, 493),
    44: (73, 464, 615, 602, 746),
    45: (74, 67, 225, 326, 303),
    46: (74, 216, 634, 326, 755),
    47: (74, 385, 376, 602, 497),
}
FIGURE_PROBLEMS = {
    15:[65],24:[8],25:[12],26:[23],27:[34,35],28:[35],29:[37],
    30:[39],31:[41],32:[43],33:[50],34:[51],35:[56],36:[64],
    37:[66],38:[67],39:[68],40:[69],41:[74],42:[76],43:[79],
    44:[82],45:[83],46:[90],47:[95],
}


def crop(box, solution=False, remove_figures=False):
    p, x0, y0, x1, y1 = box
    source = SOLUTIONS if solution else SOURCE
    key = (source.name, p)
    if key not in CACHE:
        path = ROOT / f'tmp/halliday-ch2-answer-page-{p:04}.png' if solution else WORK / f'page-{p:04}.png'
        CACHE[key] = Image.open(path).convert('RGB')
    im = CACHE[key]
    pw, ph = DIMS[key]
    sx, sy = im.width/pw, im.height/ph
    if tuple(box)==(55,270,73,493,242):
        # Keep Figure 2-6a and its axis labels without the neighboring callout.
        im=im.copy()
        background=im.getpixel((round(270*sx),round(220*sy)))
        ImageDraw.Draw(im).rectangle((round(414*sx),round(219*sy),
                                     round(602*sx),round(258*sy)),fill=background)
    if tuple(box)==(64,343,308,602,551):
        # This figure floats beside the sample heading; exclude its title tail.
        im=im.copy()
        background=im.getpixel((round(440*sx),round(315*sy)))
        ImageDraw.Draw(im).rectangle((round(343*sx),round(308*sy),
                                     round(420*sx),round(325*sy)),fill=background)
    if remove_figures:
        im = im.copy()
        draw = ImageDraw.Draw(im)
        for fp, a, b, c, d in FIGURES.values():
            if fp == p:
                draw.rectangle((round(a*sx), round(b*sy), round(c*sx), round(d*sy)), fill='white')
    im = im.crop((round(x0*sx), round(y0*sy), round(x1*sx), round(y1*sy)))
    mask = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).convert('L').point(lambda v: 255 if v>32 else 0)
    bounds = mask.getbbox()
    if bounds:
        a, b, c, d = bounds
        im = im.crop((max(0,a-8), max(0,b-8), min(im.width,c+8), min(im.height,d+8)))
    stream = io.BytesIO()
    im.save(stream, 'WEBP', lossless=True)
    return 'data:image/webp;base64,'+base64.b64encode(stream.getvalue()).decode(), im.width, im.height, sx


def pictures(boxes, alt, solution=False, remove_figures=False):
    rendered = []
    for box in boxes:
        src, w, h, scale = crop(box, solution, remove_figures)
        width = round(w/scale*1.7)
        rendered.append(f'<img src="{src}" alt="{html.escape(alt,quote=True)}" width="{w}" height="{h}" style="width:{width}px;max-width:100%;height:auto" loading="lazy">')
    return ''.join(rendered)


GROUPS = []
def group(topic, kind, title):
    g = dict(id=f'set-{len(GROUPS)+1}', topic=topic, kind=kind, title=title,
             questions=[], shared=[], context=[])
    GROUPS.append(g)
    return g


def add(g, label, boxes, answer='', solution_boxes=None, text=None, figures=None, sample=False):
    if text is None:
        text = ' '.join(l['text'] for p,x0,y0,x1,y1 in boxes
                        for l in LINES[(SOURCE.name,p)]
                        if x0 <= l['xMin'] < x1 and y0 <= l['yMin'] < y1)
    g['questions'].append(dict(label=str(label), boxes=boxes, text=text,
                              answer_html=answer, solution_boxes=solution_boxes or [],
                              solution_source=SOURCE.name if sample else SOLUTIONS.name,
                              figures=figures or [], sample=sample))


def text_box(p,y0,y1,x0=66,x1=602):
    lines=[l for l in LINES[(SOURCE.name,p)] if x0<=l['xMin']<x1 and y0<=l['yMin']<y1]
    assert lines, (p,y0,y1)
    return (p,x0,min(l['yMin'] for l in lines)-.5,x1,max(l['yMax'] for l in lines)+.5)


CHECKPOINTS = [
    ('2-1',51,313,355,66,405,'<p>Δx = x<sub>f</sub> − x<sub>i</sub>: (a) +8 m, (b) −4 m, (c) −10 m. The negative displacements are <strong>(b) and (c)</strong>.</p>'),
    ('2-2',54,539,602,261,602,'<p>Differentiate each position: (1) v = 3 m/s; (2) v = −8t; (3) v = −4/t³; (4) v = 0. <strong>(a) Constant in (1) and (4). (b) Negative in (2) and (3)</strong> for t &gt; 0.</p>'),
    ('2-3',58,190,252,260,602,'<p>The speed increases when velocity and acceleration have the same sign. Thus (a) positive, (b) negative, (c) negative, (d) positive.</p>'),
    ('2-4',61,71,123,66,405,'<p>The constant-acceleration equations apply to <strong>(1) and (4)</strong>. Their second derivatives are 0 and 10 m/s². The second derivatives of (2) and (3) depend on time.</p>'),
    ('2-5',64,222,274,260,602,'<p>Taking upward as positive: (a) ascent displacement is positive; (b) descent displacement is negative; (c) acceleration at the highest point is <strong>−9.8 m/s²</strong>, downward. Zero instantaneous velocity does not imply zero acceleration.</p>'),
]
SAMPLES = [
    ('2-1','2.01','Average velocity: pickup truck',[(53,97,176,66,327),(53,335,360,66,327),(53,597,634,66,327),(53,242,291,340,602)],[(53,66,73,602,710)]),
    ('2-2','2.02','Velocity and slope: elevator cab',[(54,654,691,66,327)],[(54,66,628,602,749),(55,66,60,602,741)]),
    ('2-3','2.03','Acceleration and dv/dt',[(58,306,397,66,328),(58,580,592,66,328),(58,693,711,66,328)],[(58,66,281,602,713)]),
    ('2-4','2.04','Drag race: car and motorcycle',[(61,179,316,66,327)],[(61,66,156,602,735),(62,66,60,602,349)]),
    ('2-5','2.05','Baseball toss',[(64,331,374,66,328),(64,535,548,66,328),(64,627,652,66,328)],[(64,66,308,602,711)]),
    ('2-6','2.06','Graphical integration: whiplash injury',[(66,100,305,66,329)],[(66,66,77,602,544)]),
]

for i,(topic,p,a,b,x0,x1,answer) in enumerate(CHECKPOINTS,1):
    g=group(topic,'Checkpoint',f'Checkpoint {i}')
    add(g,i,[text_box(p,a,b,x0,x1)],answer)
for topic,label,title,ranges,solutions in SAMPLES:
    g=group(topic,'Sample prompt',f'Sample {label}: {title}')
    boxes=[text_box(p,a,b,x0,x1) for p,a,b,x0,x1 in ranges]
    if label=='2.02': boxes.append((55,270,73,493,242))  # Figure 2-6a only; v(t) remains hidden.
    if label=='2.04': boxes.append((61,66,568,327,732))  # Figure 2-10.
    if label=='2.05': boxes.append((64,343,308,602,551))  # Figure 2-13.
    if label=='2.06': boxes.append(FIGURES[15])
    add(g,label,boxes,solution_boxes=solutions,sample=True)

concept=group('Conceptual questions','Conceptual question','Chapter 2 conceptual questions')
concept_boxes=[
    [(67,66,379,214,457),(67,228,372,327,486)],
    [(67,66,459.9,214,504.1),(67,66,504.1,245,516),(67,66,528,327,613)],
    [(67,66,625,218,725),(67,230,623,327,728)],
    [(67,66,730,327,754),(67,341,380,486,447),(67,489,370,602,485)],
    [(67,341,456,486,589),(67,490,494,602,583)],
    [(67,341,594,491,705)],
    [(67,341,709.5,491,755),(68,66,65,255,100),(67,495,592,602,755)],
    [(68,66,104,255,161)],
    [(68,66,166,255,276),(68,260,65,326,288)],
    [(68,66,282.5,255,293.6),(68,66,293.6,327,317),(68,342,65,602,144)],
    [(68,342,146,602,192),(68,395,214,542,321)],
]
concept_answers=[
    '<p>(a) Initially in the negative x direction. (b) Finally in the positive x direction. (c) Yes, at the zero crossing of v(t). (d) Acceleration is positive. (e) It is constant because the velocity graph has a constant positive slope.</p>',
    '<p><strong>Period E</strong>, where a = 0 throughout the interval. Zero acceleration means constant velocity and therefore constant speed.</p>',
    '<p>(a) <strong>1 = 2 = 3 = 4</strong>: each path has the same positive displacement and duration. (b) <strong>4 &gt; 1 = 2 &gt; 3</strong>: average speed depends on the total path length, including reversals.</p>',
    '<p>(a) Negative initial position. Velocity is the slope of x(t): (b) positive at 1 s; (c) zero at 2 s; (d) negative at 3 s. (e) The particle passes x = 0 <strong>twice</strong>, at 1 s and 3 s.</p>',
    '<p>(a) Positive direction at t = 0. (b) Negative direction at point 4. (c) It reverses at <strong>3 and 5</strong>, where velocity changes sign. (d) Compare absolute slopes: <strong>2 = 6 &gt; 3 = 5 &gt; 1 = 4</strong>; the slopes vanish at 1 and 4.</p>',
    '<p>(a) <strong>2 and 3</strong>, because acceleration initially opposes velocity. (b) <strong>1 and 3 certainly cross the origin</strong>. Situation 2 crosses only if v₀²/(2|a|) &gt; 20 m; equality means it reaches the origin and turns there. (c) <strong>4 never reaches the origin</strong>; situation 2 also fails to reach it if v₀²/(2|a|) &lt; 20 m. The signs alone do not settle situation 2.</p>',
    '<p>(a) <strong>D</strong> for the dropped egg: zero initial velocity and constant negative slope −g. (b) <strong>E</strong> for the thrown egg: negative initial velocity and the same slope −g.</p>',
    '<p><strong>(a) and (c)</strong>. Their derivatives give constant accelerations 0 and 3, respectively. In (b) and (d), acceleration depends on time.</p>',
    '<p>(a) Average speed: <strong>3 &gt; 2 &gt; 1</strong>. (b) Passage time: <strong>1 &gt; 2 &gt; 3</strong>. (c) Acceleration magnitude: <strong>1 = 2 = 3</strong> (= g). (d) Signed change in speed: <strong>3 &gt; 2 &gt; 1</strong>, since Δv = −gΔt. The greatest magnitude of speed lost is at window 1, then 2, then 3.</p>',
    '<p>(a) 9.8 m/s². (b) Downward. (c) Moving upward immediately after release. (d) 2 m/s, inherited from the balloon. (e) Its speed initially decreases as gravity opposes its upward motion; it later reverses and speeds up downward.</p>',
    '<p><strong>1 = 2 &gt; 3</strong>. Velocity increase is the area under a(t). Regions 1 and 2 each cover eight grid squares; region 3 covers seven.</p>',
]
for n,(boxes,answer) in enumerate(zip(concept_boxes,concept_answers),1): add(concept,n,boxes,answer)

# Companion solutions: detect consecutive numbered starts, then preserve every
# continuation page and graph until the next solution begins.
starts=[]
for p in range(31,90):
    for line in sorted(LINES[(SOLUTIONS.name,p)],key=lambda l:l['yMin']):
        m=re.match(r'^(\d+)\.\s',line['text'])
        if m and abs(line['xMin']-90)<1:
            starts.append((int(m[1]),p,line['yMin']))
assert [n for n,p,y in starts]==list(range(1,120)), 'Solution numbering is incomplete'
solution_boxes={}
for i,(n,p,y) in enumerate(starts):
    ep,ey=(starts[i+1][1],starts[i+1][2]-.5) if i+1<len(starts) else (89,794)
    solution_boxes[n]=[(sp,89,y-.5 if sp==p else 67,508,ey if sp==ep else 794)
                       for sp in range(p,ep+1)]

chapter=next(c for c in json.loads((ROOT/'content/textbook-problems.json').read_text())['chapters'] if c['number']==2)
problems=chapter['problems']
assert [p['number'] for p in problems]==list(range(1,120))
module_groups={m['id']:group(m['id'],'Additional problem' if m['id']=='2-mixed' else 'Problem',
                          'Additional problems: mixed review' if m['id']=='2-mixed' else f"{m['id']} {m['title']}")
               for m in chapter['modules']}
def column_index(p): return (p['page']-68)*2+(p['x']>330)
for i,p in enumerate(problems):
    begin=column_index(p)
    end=column_index(problems[i+1]) if i+1<len(problems) else 15
    boxes=[]
    for col in range(begin,end+1):
        page=68+col//2
        x0,x1=(66,328) if col%2==0 else (341,603)
        y0=p['y']-.1 if col==begin else (439 if page==68 else 65)
        y1=problems[i+1]['y']-.5 if i+1<len(problems) and col==end else 755
        headings=[l['yMin']-.5 for l in LINES[(SOURCE.name,page)]
                  if x0<=l['xMin']<x1 and y0<l['yMin']<y1
                  and (l['text'].startswith('Module ') or l['text']=='Additional Problems')]
        if headings: y1=min(headings)
        # A continuation column can contain only a floating figure. Its full
        # figure is attached separately, so do not render an empty prompt image.
        text_remains=any(
            x0<=(w['xMin']+w['xMax'])/2<x1 and y0<=(w['yMin']+w['yMax'])/2<y1
            and not any(fp==page and a<=(w['xMin']+w['xMax'])/2<=c
                        and b<=(w['yMin']+w['yMax'])/2<=d
                        for fp,a,b,c,d in FIGURES.values())
            for w in WORDS[(SOURCE.name,page)])
        if y1>y0+1 and text_remains: boxes.append((page,x0,y0,x1,y1))
    figs=[f for f,numbers in FIGURE_PROBLEMS.items() if p['number'] in numbers]
    add(module_groups[p['module']],p['number'],boxes,solution_boxes=solution_boxes[p['number']],
        text=p['search_text'],figures=figs)

assert sum(len(g['questions']) for g in GROUPS)==141
sections=[]
sequence=0
for g in GROUPS:
    body=''
    for q in g['questions']:
        sequence+=1
        key=f'q-{sequence}'
        q['id']=key
        alt=f"{g['title']}, question {q['label']}. {q['text']}"
        prompt=pictures(q['boxes'],alt,remove_figures=g['kind'] in ('Problem','Additional problem'))
        for f in q['figures']:
            prompt+=pictures([FIGURES[f]],f'Figure 2-{f} for problem {q["label"]}')
        if q['solution_boxes']:
            q['answer_html']='<div class="answer-image">'+pictures(q['solution_boxes'],f'Worked solution for {g["title"]}, question {q["label"]}',solution=not q['sample'])+'</div>'
        pp=', '.join(map(str,sorted(set(b[0]-36 for b in q['boxes']))))
        body+=f'<article class="question" id="{key}" data-search="{html.escape((g["title"]+" "+q["label"]+" "+q["text"]).lower(),quote=True)}"><div class="question-top"><a href="#{key}">Question {html.escape(q["label"])}</a><span>Textbook p. {pp}</span><label><input type="checkbox" data-complete="{key}"> Done</label><label class="homework-select" hidden><input type="checkbox" data-homework="{key}"> Homework</label></div><div class="question-image">{prompt}</div><button class="answer-toggle" id="toggle-{key}" type="button" data-answer-toggle aria-expanded="false" aria-controls="answer-{key}">Show answer</button><div class="answer" id="answer-{key}" role="region" aria-labelledby="toggle-{key}" hidden><h3>Answer</h3>{q["answer_html"]}</div></article>'
    sections.append(f'<section class="question-set" id="{g["id"]}" data-topic="{g["topic"]}" data-kind="{g["kind"]}"><div class="set-heading"><span>{g["kind"]}</span><h2>{html.escape(g["title"])}</h2><p>{len(g["questions"])} entries</p></div>{body}</section>')

TOPICS=[(m['id'],f"{m['id']} {m['title']}") for m in chapter['modules']]
TOPICS.insert(6,('Conceptual questions','Conceptual questions'))
KINDS=['Checkpoint','Sample prompt','Conceptual question','Problem','Additional problem']
options=lambda items:''.join(f'<option value="{html.escape(v,quote=True)}">{html.escape(t)}</option>' for v,t in items)
template=(ROOT/'tools/halliday-motion-template.html').read_text()
replacements={
    '@@TOPICS@@':options(TOPICS),'@@KINDS@@':options([(k,k) for k in KINDS]),
    '@@NAV@@':''.join(f'<a href="#{g["id"]}">{html.escape(g["title"])}</a>' for g in GROUPS),
    '@@SECTIONS@@':''.join(sections),
    '@@HOMEWORK_STYLES@@':(ROOT/'tools/bc-kinematics-homework.css').read_text(),
    '@@HOMEWORK_SCRIPT@@':(ROOT/'tools/bc-kinematics-homework.js').read_text()
        .replace('bc-physics11-ch2','halliday-physics-ch2')
        .replace('bc-kinematics-questions.html','halliday-motion-questions.html')
        .replace('kinematics-homework','halliday-motion-homework')
        .replace('Kinematics','Motion Along a Straight Line')
        .replace('Source: BC Science Physics 11, Chapter 2 Motion Along a Straight Line, Edvantage Interactive (2012).',
                 'Source: Halliday & Resnick, Fundamentals of Physics, 10th edition, Extended, Chapter 2 Motion Along a Straight Line. Problem solutions: Physics answer (TOC).pdf, Chapter 2.'),
    '@@HOMEWORK_AI_SCRIPT@@':(ROOT/'tools/bc-kinematics-homework-ai.js').read_text().replace('kinematics-difficulty','halliday-motion-difficulty'),
}
for token,value in replacements.items(): template=template.replace(token,value)
template=template.replace("`${set.querySelectorAll('.question').length} entries`", "`${set.querySelectorAll('.question').length} ${set.querySelectorAll('.question').length===1?'entry':'entries'}`")
output=ROOT/'halliday-motion-questions.html'
output.write_text(template)
# Images are embedded in HTML. Keep the reusable manifest compact.
manifest_groups=json.loads(json.dumps(GROUPS))
for g in manifest_groups:
    for q in g['questions']:
        if q['solution_boxes']: q['answer_html']=''
(ROOT/'content/halliday-motion-questions.json').write_text(json.dumps(dict(
    source=SOURCE.name,solutions_source=SOLUTIONS.name,chapter=2,title=chapter['title'],
    question_count=sequence,figures=FIGURES,groups=manifest_groups),indent=2,ensure_ascii=False)+'\n')
print(f'Created {output}: {sequence} entries, {len(GROUPS)} sets, {output.stat().st_size:,} bytes')
