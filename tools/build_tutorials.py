#!/usr/bin/env python3
"""Rebuild the offline tutorials from the editable Markdown content."""
from pathlib import Path
import argparse
import html
import importlib.util
import json
import re
import subprocess
import sys

from course_content import UNITS
from build_textbook_problems import section as textbook_problem_section

ROOT = Path(__file__).resolve().parents[1]
PDF = 'Physics%20text%20%28TOC%29.pdf'
VSB = 'https://www.vsb.bc.ca/vln/physics-11'
BC = 'https://curriculum.gov.bc.ca/curriculum/science/11/physics'
SKILL = Path('/Users/chenguagnghui/.agents/skills/chapter-tutorial-html/scripts/generate_chapter_html.py')
CSS = (ROOT/'tools/page.css').read_text()
JS = (ROOT/'tools/page.js').read_text()
E = html.escape

def render_vectors(body):
    """Draw vector accents without relying on combining-glyph font support.

    Keep the original combining mark in textContent for equation copying.
    Only process code text, leaving attributes and scripts untouched.
    """
    def accent(match):
        letter, mark = match.groups()
        return (f'<span class="vector-symbol">{letter}'
                f'<span class="vector-mark">{mark}</span>'
                '<svg viewBox="0 0 14 8" aria-hidden="true" focusable="false">'
                '<path d="M1 6H13L9 2" fill="none" stroke="currentColor" '
                'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
                '</svg></span>')
    return re.sub(r'(<code>)(.*?)(</code>)',
                  lambda m: m[1] + re.sub(r'([A-Za-z])([\u20d1\u20d7])', accent, m[2]) + m[3],
                  body, flags=re.S)

def slug(u):
    return f"unit-{u['number']:02d}-" + re.sub('[^a-z0-9]+','-',u['title'].lower()).strip('-')

def page(title, body, *, nested=False, side='', cls=''):
    body = render_vectors(body)
    home = '../index.html' if nested else 'index.html'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Detailed algebra-based Physics 11 tutorials with worked examples, practice solutions, and textbook references.">
<title>{E(title)} | Physics 11</title><style>{CSS}</style></head>
<body class="{cls}"><a class="skip" href="#main">Skip to lesson content</a>
<header class="top"><a class="brand" href="{home}">PHYSICS / 11</a><small>Think in models. Check with evidence.</small><a href="{'../' if nested else ''}course-outline.md">Course outline</a></header>
<div class="{'layout' if side else 'home'}">{side}<main id="main">{body}</main></div>
<script>{JS}</script></body></html>'''

def toolbar():
    return '''<div class="toolbar"><label for="mode">Reading mode</label><select id="mode"><option value="study">Study</option><option value="simple">Simple</option><option value="slides">Slides</option></select><button id="show-answers">Show answers</button><button id="hide-answers">Hide answers</button><button id="print">Print / Save PDF</button></div>
<p class="status">Study: try questions before opening answers. Simple: all answers visible. Slides: one lesson at a time; use arrow keys.</p>'''

def explorer(u):
    n=u['number']; configs={
      1: ('vector','Vector components',[('magnitude','Force magnitude (N)',5,35,20,1),('angle','Angle from +x (°)',0,360,30,5)]),
      2: ('motion','Velocity-time graph',[('initial-speed','Initial velocity (m/s)',-10,10,2,1),('acceleration','Acceleration (m/s²)',-4,4,2,.5),('duration','Duration (s)',1,8,3,.5)]),
      3: ('projectile','Trajectory explorer',[('launch-speed','Launch speed (m/s)',5,30,20,1),('launch-angle','Launch angle (°)',0,80,30,1),('height','Launch height (m)',0,20,0,1)]),
      4: ('forces','Forces on a sliding block',[('mass','Mass (kg)',1,15,5,1),('push','Horizontal pull (N)',0,100,30,1),('friction','Kinetic coefficient',0,.6,.2,.05)]),
      5: ('ramp','Sliding ramp model',[('mass','Mass (kg)',1,10,4,1),('incline','Incline angle (°)',5,60,30,1),('friction','Kinetic coefficient',0,.6,.2,.05)]),
      6: ('energy','Energy transformations',[('mass','Mass (kg)',1,10,2,1),('start-height','Initial height (m)',1,10,5,1),('current-height','Remaining height (%)',0,100,50,1)]),
      7: ('circuit','Series and parallel circuit explorer',[('voltage','Ideal source voltage (V)',1,24,12,1),('resistance1','Resistance R₁ (Ω)',1,20,6,1),('resistance2','Resistance R₂ (Ω)',1,20,3,1)]),
      8: ('wave','Wave snapshot explorer',[('frequency','Frequency (Hz)',1,8,2,.5),('wave-speed','Wave speed (m/s)',1,8,4,.5),('amplitude','Amplitude (cm)',.2,1.5,1,.1)])}
    kind,title,fields=configs[n]
    controls=''.join(f'<label for="{id}">{label}<input id="{id}" type="range" min="{lo}" max="{hi}" value="{value}" step="{step}"></label>' for id,label,lo,hi,value,step in fields)
    if n==7:controls+='<label for="connection">Connection<select id="connection"><option value="series">Series</option><option value="parallel">Parallel</option></select></label>'
    return f'''<section class="panel explorer" data-kind="{kind}" aria-labelledby="explorer-title"><div class="eyebrow">Predict → adjust → explain</div><h2 id="explorer-title">{title}</h2><p>Change one input at a time. Predict what will change before checking the calculated readout.</p><div class="controls">{controls}</div><output aria-live="polite"></output><figure><svg viewBox="0 0 660 320" role="img" aria-label="{title}"></svg><figcaption>This diagram is an ideal-model visualization. Calculated values are not experimental measurements.</figcaption></figure><noscript>Enable JavaScript for the adjustable diagram. All lesson text and practice answers remain available below.</noscript></section>'''

QUIZZES = {
1:[('Which value has three significant figures?',['0.0030','3.00','3000 (precision unspecified)'],1,'The final two zeros after the decimal are significant.'),('The slope of a position-time graph has units of',['m/s','m/s²','m²/s'],0,'Position divided by time gives velocity units.'),('A 10 N force acts at 60° from +x. Its x-component is',['8.66 N','10 N','5 N'],2,'Fₓ = F cos 60° = 5 N.')],
2:[('An object has v < 0 and a < 0. At that instant it is',['Slowing down','Speeding up','At rest'],1,'Velocity and acceleration have the same sign.'),('Signed area under a velocity-time graph gives',['Acceleration','Position at t = 0','Displacement'],2,'Area has units (m/s)s = m.'),('A full round trip to the start must have',['Zero displacement','Zero distance','Zero elapsed time'],0,'Displacement depends only on endpoints.')],
3:[('At the peak of an angled ideal projectile,',['All velocity is zero','Vertical velocity is zero','Acceleration is zero'],1,'Horizontal velocity remains nonzero for an ordinary angled launch.'),('At fixed height, doubling horizontal launch speed makes flight time',['Double','Halve','Stay the same'],2,'The vertical motion determines time.'),('The shortcut R = v₀² sin(2θ)/g requires',['Equal launch and landing heights','Zero horizontal speed','Air resistance'],0,'It assumes equal heights, constant g, and negligible drag.')],
4:[('Static friction below the slipping threshold is',['Always μₛN','Whatever balance requires, up to μₛN','Always zero'],1,'μₛN is its maximum, not its automatic value.'),('An interaction pair acts on',['The same body','Two different bodies','Neither body'],1,'Newton’s third-law forces act on the two interacting objects.'),('An upward-moving elevator is slowing. Apparent weight is',['Greater than mg','Equal to mg','Less than mg'],2,'The acceleration is downward.')],
5:[('On an otherwise unforced frictionless ramp, N equals',['mg','mg sin θ','mg cos θ'],2,'The normal balances gravity perpendicular to the ramp.'),('An ideal force advantage of 4 means input distance is',['Four times the output distance','One quarter of output distance','Equal to output distance'],0,'Ideal work in equals useful work out.'),('For a block sliding up a ramp, kinetic friction acts',['Up the ramp','Down the ramp','Vertically upward'],1,'It opposes relative sliding along the surface.')],
6:[('Doubling speed changes kinetic energy by a factor of',['2','4','½'],1,'K is proportional to v².'),('Energy converted into thermal energy by friction is',['Destroyed','Still included in total energy','Always useful mechanical output'],1,'Mechanical energy can fall while total energy is conserved.'),('Equal temperature at equilibrium implies',['Equal internal energy','Equal mass','No net heat transfer between the objects'],2,'Internal energy also depends on mass, material, and state.')],
7:[('Parallel resistors share the same',['Current','Resistance','Voltage'],2,'Both endpoints connect to the same two nodes.'),('A discharging real battery has terminal voltage',['ε - Ir','ε + Ir','Always zero'],0,'Internal resistance reduces delivered voltage under load.'),('A kilowatt-hour is a unit of',['Power','Energy','Current'],1,'It is power multiplied by time.')],
8:[('At a stationary boundary into a slower medium, wave frequency',['Increases','Stays fixed','Decreases'],1,'The same source drives both sides; wavelength decreases.'),('An ideal open-closed pipe supports',['Only odd harmonics','Only even harmonics','No fundamental'],0,'A displacement node and antinode require odd quarter-wavelength patterns.'),('Sound sources at 440 Hz and 443 Hz give beat frequency',['883 Hz','441.5 Hz','3 Hz'],2,'The beat frequency is the absolute frequency difference.')]
}

def quiz(u):
    h='<form class="panel quiz"><div class="eyebrow">Check understanding</div><h2>Unit checkpoint</h2><p>Select an answer for each question, then check your reasoning. You can retry.</p>'
    for i,(q,choices,answer,why) in enumerate(QUIZZES[u['number']]):
        h+=f'<fieldset data-answer="{answer}" data-explanation="{E(why,quote=True)}"><legend>{i+1}. {E(q)}</legend>'
        for j,c in enumerate(choices):h+=f'<label><input type="radio" name="q{i}" value="{j}"> {E(c)}</label>'
        h+='<p class="feedback" aria-live="polite"></p></fieldset>'
    return h+'<button type="submit">Check answers</button><p class="score" aria-live="polite"></p></form>'

def markdown(u):
    h=f"@chapter: Physics 11 · Unit {u['number']}\n@title: Unit {u['number']}: {u['title']}\n@subtitle: {u['summary']}\n\n"
    for i,l in enumerate(u['lessons'],1):
        h+=f"## {u['number']}.{i} {l['title']}\n\n### Learning goal\n{l['goal']}\n\n### Understand the model\n{l['explanation']}\n\n### Equations and units\n```text\n{l['equations']}\n```\n\n### Worked example\n{l['example']}\n\n"
        h+='\n'.join(f'{j}. {s}' for j,s in enumerate(l['steps'],1))+'\n\n'
        h+=f"### Common mistakes\n{l['pitfalls']}\n\n### Your turn\n"
        h+='\n'.join(f'{j}. {q}' for j,(q,a) in enumerate(l['practice'],1))+'\n\n'
        h+='### Solutions and reasoning\n'+'\n\n'.join(f'**{j}.** {a}' for j,(q,a) in enumerate(l['practice'],1))+'\n\n'
        h+='### Textbook reading\n'+'; '.join(f'Section {sec}, PDF page {p} (printed page {p-36})' for sec,p in l['refs'])+'.\n\n'
    h+=f"## {u['number']}.{len(u['lessons'])+1} Investigate and reflect\n\n### Inquiry task\n{u['inquiry']}\n\n### Evidence checklist\n- State the question and a testable prediction.\n- Identify independent, dependent, and controlled variables.\n- Record units, resolution, repeated trials, and a justified uncertainty estimate.\n- Use a labelled graph or table and explain slope or area when relevant.\n- Compare the result with the model and identify specific limitations.\n- Explain an improvement and connect the result to a practical application.\n\n"
    return h

def enrich(rendered,u):
    i=0
    def change(m):
        nonlocal i
        raw=re.sub(r'<h3>Notes</h3>\s*','',m.group(1));i+=1
        if i>len(u['lessons']):return f'<section class="panel inquiry" id="inquiry">{raw}</section>'
        l=u['lessons'][i-1];sid=f"lesson-{u['number']}-{i}"
        # Turn the generator's ordinary headings into purposeful study blocks.
        chunks=re.split(r'(<h3>.*?</h3>)',raw,flags=re.S)
        result=chunks[0]
        for j in range(1,len(chunks),2):
            heading=chunks[j];body=chunks[j+1];title=re.sub('<.*?>','',heading)
            if title=='Equations and units':result+='<div class="equations"><button class="copy" type="button">Copy equations</button>'+heading+body+'</div>'
            elif title=='Worked example':result+='<div class="worked">'+heading+body+'</div>'
            elif title=='Common mistakes':result+='<div class="pitfall">'+heading+body+'</div>'
            elif title=='Solutions and reasoning':result+='<details class="solution"><summary>Reveal practice solutions and reasoning</summary>'+body+'</details>'
            elif title=='Textbook reading':
                links=''.join(f'<a href="../{PDF}#page={p}" target="_blank" rel="noopener">§{sec} · PDF p. {p} / print p. {p-36}</a>' for sec,p in l['refs'])
                result+='<div class="sources">Read in the supplied textbook: '+links+'</div>'
            else:result+=heading+body
        complete=f'<label class="complete"><input type="checkbox" data-key="{sid}"> Mark this lesson complete</label>'
        return f'<section class="lesson" id="{sid}">{complete}{result}</section>'
    return re.sub(r'<section>(.*?)</section>',change,rendered,flags=re.S)

FORMULAS=[
('Measurement','percent uncertainty = (absolute uncertainty/|value|) × 100%','State how uncertainty was estimated; defined unit conversions are exact.'),
('Vectors','Aₓ = A cos θ; Aᵧ = A sin θ; A = √(Aₓ² + Aᵧ²)','Angle θ measured from +x; use signs and check the quadrant.'),
('Motion','v_avg = Δx/Δt; a_avg = Δv/Δt','Velocity uses displacement; average speed uses distance.'),
('Constant acceleration','v = v₀ + at; Δx = v₀t + ½at²','Valid over a constant-acceleration interval.'),
('Constant acceleration','v² = v₀² + 2aΔx; Δx = ½(v₀ + v)t','Velocity squared does not determine direction.'),
('Free fall','aᵧ = -g; g ≈ 9.81 m/s²','Up is positive; negligible drag, near Earth.'),
('Projectiles','Δx = v₀ cos θ × t; Δy = v₀ sin θ × t - ½gt²','The same elapsed time links both axes.'),
('Equal-height projectile','R = v₀² sin(2θ)/g; t_flight = 2v₀ sin θ/g','Use only when launch and landing heights match.'),
('Forces','ΣFₓ = maₓ; ΣFᵧ = maᵧ; F_g = mg','Use a free-body diagram; sum external forces on the chosen object.'),
('Spring and friction','Fₛ = -kx; fₛ ≤ μₛN; fₖ = μₖN','Spring displacement is from relaxed length; static friction adjusts up to its maximum.'),
('Apparent weight','N = m(g + aᵧ)','Upward is positive; only gravity and vertical support force.'),
('Ramp','N = mg cos θ; a_down = g(sin θ - μₖ cos θ)','No other perpendicular force; already sliding down.'),
('Ideal connected masses','a = (m₂ - m₁)g/(m₁ + m₂)','Ideal Atwood system with m₂ downward positive.'),
('Machines','MA = F_out/F_in; IMA = d_in/d_out; η = (MA/IMA) × 100%','Corresponding input/output motions; no unaccounted energy source.'),
('Work','W = Fd cos θ; W_net = ΔK','Constant force; θ is between force and displacement.'),
('Energy','K = ½mv²; U_g = mgh; U_s = ½kx²','Nonrelativistic speed; near Earth; Hooke-law spring.'),
('Conservation','K_i + U_i + W_ext = K_f + U_f + ΔE_th','Choose the system; do not count friction or gravity twice.'),
('Power','P = E/t; P = Fv cos θ; η = E_useful/E_input × 100%','Match time intervals and distinguish amount from rate.'),
('Thermal','Q = mcΔT; ΣQ = 0','No phase change; approximately constant c; isolated calorimetry system.'),
('Electric quantities','I = q/t; V = E/q; V = IR','Steady current; voltage is energy per charge; R constant for an ohmic model.'),
('Circuit equivalents','R_series = ΣR; 1/R_parallel = Σ(1/R)','Series shares current; parallel shares voltage.'),
('Kirchhoff','ΣI_in = ΣI_out; ΣΔV_loop = 0','Charge and energy conservation with consistent signs.'),
('Real battery','I = ε/(R_load + r); V_terminal = ε - Ir','Discharging battery model.'),
('Electrical power','P = VI; P_resistor = I²R = V²/R; E = Pt','1 kWh = 3.6 × 10⁶ J.'),
('Waves','f = 1/T; v = fλ; v_string = √(F_tension/μ_linear)','T is period; μ_linear is string mass per length, not a friction coefficient.'),
('Resonance','f_n = nv/(2L); open-closed pipe f_n = nv/(4L)','First formula: fixed-end string or open-open pipe, integer n. Open-closed: odd n only; neglect end corrections.'),
('Sound','f_beat = |f₁ - f₂|; I = P/(4πr²); β = 10 log₁₀(I/I₀)','Point-source spreading assumption; I₀ = 10⁻¹² W/m².'),
('Doppler','f_obs = f v/(v - v_s)','Subsonic source approaches stationary observer in still air; velocities referenced to medium.')]

REVIEW=[
('Motion to forces','A 2.00 kg cart moves at +3.00 m/s. A constant net force of +4.00 N acts for 2.00 s. Find final velocity and displacement.', 'a = F_net/m = 2.00 m/s². v = 3.00 + 2.00(2.00) = 7.00 m/s. Δx = 3.00(2.00) + ½(2.00)(2.00)² = 10.0 m. Check: F_netΔx = 40.0 J, equal to ½(2.00)(7.00² - 3.00²).'),
('Projectile components','A horizontal projectile leaves a 4.90 m platform at 6.00 m/s. Find range and impact velocity with g = 9.81 m/s².', 't = √(2 × 4.90/9.81) = 0.999 s. Range = 6.00t = 6.00 m after rounding. vₓ = 6.00 m/s and vᵧ = -9.80 m/s. Speed = 11.5 m/s, at 58.5° below horizontal.'),
('Ramp and friction','A 5.00 kg block already slides down a 30.0° ramp with μₖ = 0.200. Find normal force and acceleration.', 'N = 5.00(9.81) cos 30.0° = 42.5 N. fₖ = 8.50 N. Downslope force = 24.525 - 8.496 = 16.0 N. a = 3.21 m/s² downhill. The kinetic model assumes sliding; it does not decide release from rest.'),
('Work and energy','A 1.00 kg object starts from rest at height 2.00 m. During descent, the object-track-Earth system gains 3.00 J of thermal energy. Find bottom speed.', 'Initial U = 19.62 J. Final K = 19.62 - 3.00 = 16.62 J. v = √(2K/m) = 5.77 m/s. Total energy is conserved; mechanical energy drops by 3.00 J.'),
('Thermal equilibrium','An insulated mixture contains 0.100 kg water at 70.0 °C and 0.200 kg at 25.0 °C. Ignore container heat capacity. Find T_f.', 'Equal specific heat cancels. T_f = [0.100(70.0) + 0.200(25.0)]/0.300 = 40.0 °C. With c = 4180, Q_hot = -12 540 J and Q_cool = +12 540 J.'),
('Circuit and power','A 9.00 V ideal source connects to 3.00 Ω in series with two 6.00 Ω resistors in parallel. Find source current, branch currents, and total power.', 'The parallel equivalent is 3.00 Ω; total is 6.00 Ω. Source current = 1.50 A. The series resistor drops 4.50 V, leaving 4.50 V across both branches. Each branch carries 0.750 A. Total power = 9.00 × 1.50 = 13.5 W.'),
('Real battery energy rates','A 6.00 V EMF battery with internal resistance 0.500 Ω supplies a 2.50 Ω load. Find terminal voltage and compare energy transfer rates.', 'I = 6.00/(2.50 + 0.500) = 2.00 A. Terminal voltage = 5.00 V. Source power = 12.0 W; load power = 10.0 W; internal heating = I²r = 2.00 W. The rates add correctly.'),
('Sound resonance and beats','An ideal open-closed pipe has length 0.250 m in air at 343 m/s. Find its fundamental and next allowed harmonic. A 345 Hz tone plays with its fundamental; find beat frequency.', 'f₁ = 343/[4(0.250)] = 343 Hz. The next allowed harmonic is f₃ = 1029 Hz ≈ 1.03 × 10³ Hz. Beat frequency = |345 - 343| = 2 Hz, using the assigned source values.')]

def build(seed=False):
    if not SKILL.exists():raise SystemExit(f'Chapter generator missing: {SKILL}')
    (ROOT/'content').mkdir(exist_ok=True);(ROOT/'tutorials').mkdir(exist_ok=True)
    outline={'title':'Physics 11','sources':{'outline':[VSB,BC], 'textbook':'Physics text (TOC).pdf', 'textbook_title':'Halliday & Resnick Fundamentals of Physics, 10th edition, Extended, Jearl Walker', 'page_numbering':'PDF page is the 1-based viewer page; relevant printed pages are PDF page minus 36.'}, 'units':[]}
    for u in UNITS:
        stem=slug(u);md=ROOT/'content'/f'{stem}.md'
        if seed or not md.exists():md.write_text(markdown(u))
        hero=f'''<div class="hero"><div class="eyebrow">Physics 11 · Unit {u['number']}</div><h1>{E(u['title'])}</h1><p class="lead">{E(u['summary'])}</p><div class="stats"><span class="tag">{len(u['lessons'])} lessons</span><span class="tag">{len(u['lessons'])} worked examples</span><span class="tag">{2*len(u['lessons'])} practice questions</span><span class="tag">{E(u['chapters'])}</span></div>{toolbar()}</div>'''
        side='''<aside class="sidebar" aria-label="Lesson navigation"><label for="lesson-search">Search this unit</label><input id="lesson-search" type="search" placeholder="e.g. acceleration"><p class="small" id="search-status">Search explanations and examples.</p><hr><div class="eyebrow">Lesson outline</div><nav>'''
        side+=''.join(f'<a href="#lesson-{u["number"]}-{i}">{u["number"]}.{i} {E(l["title"])}</a>' for i,l in enumerate(u['lessons'],1))
        side+=f'''<a href="#inquiry">Investigate and reflect</a></nav><hr><progress id="progress" max="{len(u['lessons'])}" value="0" aria-label="Lesson completion"></progress><p class="small" id="progress-count"></p><p class="small">Progress is stored only in this browser when local storage is available.</p><div class="course-links"><a href="../index.html">All units</a> · <a href="review.html">Formula review</a><br><a href="../content/{stem}.md">Editable notes</a></div></aside>'''
        nav='<div class="footnav">'
        if u['number']>1:nav+=f'<a class="button" href="{slug(UNITS[u["number"]-2])}.html">← Previous unit</a>'
        else:nav+='<a class="button" href="../index.html">← Course home</a>'
        if u['number']<8:nav+=f'<a class="button" href="{slug(UNITS[u["number"]])}.html">Next unit →</a>'
        else:nav+='<a class="button" href="review.html">Formula review →</a>'
        nav+='</div>'
        footer=f'''<footer class="footer"><p>Course sequence: <a href="{VSB}">VLN Physics 11</a>. Scope check: <a href="{BC}">BC Physics 11 curriculum</a>. Physics reading: the supplied Halliday & Resnick textbook. Explanations are adapted at Grade 11 algebra level; numerical examples and practice questions are authored for these tutorials.</p><p>Textbook links open the supplied PDF at the referenced viewer page. If your viewer ignores page anchors, enter the PDF page number manually. References point to section openings; read onward within the section for the full discussion.</p></footer>'''
        body=hero+explorer(u)+'{{SECTIONS}}<p id="empty" class="empty" hidden>No lessons match. Try another term.</p>'+quiz(u)+'<div class="slide-controls"><button id="prev-slide">← Previous</button><span id="slide-count" aria-live="polite"></span><button id="next-slide">Next →</button></div>'+nav+footer
        template=ROOT/'work'/f'template-{u["number"]}.html';template.write_text(page('{{PAGE_TITLE}}',body,nested=True,side=side))
        dest=ROOT/'tutorials'/f'{stem}.html'
        subprocess.run([sys.executable,str(SKILL),'--input',str(md),'--output',str(dest),'--template',str(template)],check=True,stdout=subprocess.DEVNULL)
        dest.write_text(render_vectors(enrich(dest.read_text(),u)))
        outline['units'].append({'number':u['number'],'title':u['title'],'summary':u['summary'],'page':str(dest.relative_to(ROOT)),'notes':str(md.relative_to(ROOT)),'textbook_chapters':u['chapters'],'inquiry':u['inquiry'],'lessons':[{'id':f'lesson-{u["number"]}-{i}','title':l['title'],'goal':l['goal'],'equations':l['equations'].splitlines(),'textbook_references':[{'section':s,'pdf_page':p,'printed_page':p-36} for s,p in l['refs']]} for i,l in enumerate(u['lessons'],1)]})
    (ROOT/'course-outline.json').write_text(json.dumps(outline,ensure_ascii=False,indent=2)+'\n')
    h='# Physics 11 course outline\n\nAn algebra-based tutorial sequence following the eight units listed by VLN. The BC curriculum is used to check scope, including inquiry, evidence, and community connections.\n\n'
    h+=f'## Sources\n\n- [VLN course outline]({VSB})\n- [BC Physics 11 curriculum]({BC})\n- Supplied PDF: Halliday & Resnick Fundamentals of Physics, 10th edition, Extended, Jearl Walker.\n\nPDF references use viewer page numbers; the relevant printed textbook page is PDF page minus 36. Text is adapted to Grade 11 without requiring calculus. Qualitative curriculum bridge topics include diffraction, refraction, and simple-machine terminology.\n\n'
    for u in outline['units']:
        h+=f'## Unit {u["number"]}: {u["title"]}\n\n{u["summary"]}\n\nTextbook: {u["textbook_chapters"]}.\n\n'
        for l in u['lessons']:h+=f'- **{l["id"].replace("lesson-", "").replace("-", ".")} {l["title"]}:** {l["goal"]}\n'
        h+=f'\nInquiry: {u["inquiry"]}\n\n'
    h+='## Curriculum scope crosswalk\n\n- Scalars, vectors, graphs, and measurement: Units 1–2.\n- Uniform and accelerated motion: Unit 2.\n- Vertical, horizontal, and angled projectiles: Unit 3.\n- Contact forces, Newton’s laws, mass, gravity, and apparent weight: Unit 4.\n- Angled forces, systems, ramps, pulleys, simple machines, and mechanical advantage: Unit 5.\n- Work, conservation of energy, power, efficiency, thermal equilibrium, and specific heat: Unit 6.\n- DC circuits, Kirchhoff’s laws, Ohm’s law, EMF, terminal voltage, and electrical power: Unit 7.\n- Wave generation, propagation, boundary behaviors, interference, sound, resonance, beats, and Doppler effects: Unit 8.\n- Inquiry, uncertainty, model evaluation, communication, and respectful community research: distributed investigation tasks.\n'
    (ROOT/'course-outline.md').write_text(h)
    cards=''
    for u in UNITS:
        ids=','.join(f'lesson-{u["number"]}-{i}' for i in range(1,len(u['lessons'])+1))
        cards+=f'''<a class="unit-card" href="tutorials/{slug(u)}.html" data-lessons="{ids}"><div class="eyebrow">Unit {u['number']:02d}</div><h2>{E(u['title'])}</h2><p>{E(u['summary'])}</p><div class="meta">{len(u['lessons'])} lessons · {2*len(u['lessons'])} practice questions · <span class="completion">0/{len(u['lessons'])} complete</span></div><ul>'''+''.join(f'<li>{E(l["title"])}</li>' for l in u['lessons'])+'</ul></a>'
    intro='''<div class="hero"><div class="eyebrow">BC Physics 11 · A complete study sequence</div><h1>Make sense of motion,<br>energy, and waves.</h1><p class="lead">Detailed tutorials that connect physical ideas to equations, worked examples, and evidence. Start with the math tools, then follow the eight units in order.</p><div class="stats"><span class="tag">8 units · 49 lessons</span><span class="tag">49 worked examples</span><span class="tag">98 practice questions + 24 checkpoint items</span><span class="tag">8 adjustable diagrams</span></div><div class="toolbar"><a class="button" href="tutorials/unit-01-math-tools-measurement.html">Start Unit 1 →</a><a class="button" href="tutorials/review.html">Formula sheet & mixed review</a><a class="button" href="course-outline.json">JSON outline</a></div></div>'''
    startup='''<section class="panel"><div class="eyebrow">Start-up</div><h2>Prepare your toolkit</h2><p>You will use algebra, right-triangle trigonometry, a scientific calculator, and careful unit reasoning. Review any unfamiliar skills in Unit 1 before proceeding.</p><div class="checklist"><label><input type="checkbox"> Calculator set to degrees for degree angles</label><label><input type="checkbox"> SI prefixes and unit conversions reviewed</label><label><input type="checkbox"> Rearranging equations and square roots reviewed</label><label><input type="checkbox"> Graph axes, slopes, and areas reviewed</label></div><p class="status">Preparation checkboxes are a temporary checklist. Lesson completion is saved by the browser when available.</p></section>'''
    how='''<section class="panel"><h2>Use each lesson in four passes</h2><ol><li><strong>Understand:</strong> read the model, identify its assumptions, and connect the equations to the explanation.</li><li><strong>Predict:</strong> sketch a diagram and estimate the direction or size before checking a worked solution.</li><li><strong>Practise:</strong> solve the two questions before revealing their reasoning, then try the unit checkpoint.</li><li><strong>Investigate:</strong> use the inquiry task to evaluate the model with observations and uncertainty.</li></ol><p>Reading modes switch between Study, Simple, and Slides. Search within a unit, copy equations, mark completed lessons, or print the page with answers. These pages work offline without libraries, web fonts, or external scripts; source links open when you have internet access.</p></section>'''
    sources=f'''<footer class="footer"><h2>Sources and scope</h2><p>The sequence follows the <a href="{VSB}">VLN course outline</a> linked in resource.txt and is checked against the <a href="{BC}">BC Physics 11 curriculum</a>. Content is adapted from the relevant sections of the supplied <a href="{PDF}">Halliday & Resnick textbook</a>. University-level calculus and unrelated later chapters are outside this introductory course.</p><p>The worked examples are newly authored, rather than copied textbook exercises. Each lesson links to supporting textbook sections with both PDF and printed page numbers. Community-research tasks ask for locally appropriate, publicly shared sources and respectful attribution.</p></footer>'''
    intro = intro.replace('<a class="button" href="course-outline.json">', '<a class="button" href="#textbook-problems">Textbook problems →</a><a class="button" href="course-outline.json">')
    (ROOT/'index.html').write_text(page('Course home',intro+startup+'<h2>Choose a unit</h2><div class="grid">'+cards+'</div>'+textbook_problem_section()+how+sources))
    rows=''.join(f'<tr><th scope="row">{E(topic)}</th><td><code>{E(eq)}</code></td><td>{E(note)}</td></tr>' for topic,eq,note in FORMULAS)
    review='''<div class="hero"><div class="eyebrow">Course companion</div><h1>Formula sheet & mixed review</h1><p class="lead">Choose the model before choosing the equation. Every relationship below has conditions that determine when it works.</p><div class="toolbar"><a class="button" href="../index.html">← All units</a><button id="show-answers">Show solutions</button><button id="hide-answers">Hide solutions</button><button id="print">Print / Save PDF</button></div></div><section class="panel"><h2>Symbols and units</h2><p>Δ means final minus initial. Subscript 0 or i means initial; f can mean final as a subscript, or frequency as a variable. T denotes tension in a force problem and period in a wave problem; N denotes normal-force magnitude and also appears as the unit symbol for newton. Use the context and units. μₛ and μₖ are dimensionless friction coefficients; μ_linear is string mass per length in kg/m.</p><p>Core SI units: m, kg, s, A, K. Derived units: N = kg·m/s²; J = N·m; W = J/s; C = A·s; V = J/C; Ω = V/A; Hz = s⁻¹. Use g = 9.81 m/s² unless another value is assigned, and use 343 m/s for sound in air at approximately 20 °C when appropriate.</p></section>'''
    review+='<section class="panel"><h2>Relationships and conditions</h2><div class="table-wrap"><table class="formula-table"><thead><tr><th>Topic</th><th>Equation</th><th>Conditions / interpretation</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>'
    review+='<section class="panel"><h2>Eight mixed problems</h2><p>Write a diagram, givens, model assumptions, symbolic equation, substitutions, and a checked answer for each.</p>'
    for i,(topic,q,a) in enumerate(REVIEW,1):review+=f'<h3>{i}. {E(topic)}</h3><p>{E(q)}</p><details class="solution"><summary>Reveal solution</summary><p>{E(a)}</p></details>'
    review+='</section><section class="panel"><h2>Check your solution</h2><ul><li>Does the equation apply to the physical situation and time interval?</li><li>Do units cancel correctly, and do the signs match the chosen axes?</li><li>Is the result plausible in a limiting case?</li><li>Did you include all relevant forces or energy transfers once?</li><li>Are precision, uncertainty, and model limitations stated where relevant?</li></ul></section><footer class="footer">The unit pages provide detailed derivations, practice, and textbook section references. This is a study reference, not an authorized exam formula sheet.</footer>'
    (ROOT/'tutorials/review.html').write_text(page('Formula sheet & mixed review',review,nested=True))
    print('Built index, 8 unit pages, review, and Markdown/JSON outlines.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed-content',action='store_true',help='Regenerate Markdown from authored Python lesson data; overwrites edits to the notes.')
    build(p.parse_args().seed_content)
