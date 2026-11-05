from pathlib import Path
source=Path('tools/build_bc_forces_questions.py').read_text()
head=source[:source.index("g=group('3.1'")]
head=head.replace('Chapter 3','Chapter 4').replace('bc_forces_answers','bc_newtons_laws_answers').replace('bc-ch3','bc-ch4').replace("'-f', '81', '-l', '105'","'-f', '107', '-l', '135'").replace('enumerate(pages, 81)','enumerate(pages, 107)').replace('range(81, 106)','range(107, 136)')
groups='''# Text crops follow complete Poppler line bounds, preventing clipped descenders.
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
                m=re.match(r'^(\\d+)[.]?\\s+',line['text'])
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
g=group('4.1','Investigation','Investigation 4-1: concluding question');add(g,'Concluding question',[text_box(112,667,714)])
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
g=group('4.4','Quick check','Impulse: quick check');add(g,1,[text_box(128,88,373)])
g=group('4.4','Sample prompt','Sample 4.4.1: conservation of momentum');add(g,'4.4.1',[text_box(129,259,295)])
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

'''
tail=source[source.index('CACHE={}'):]
tail=tail.replace("caption='Reference constants from section 3.1.' if g['shared']==[gravity_constants] else 'Use this graph for the questions in this set.'", "caption='Use this reference for the questions in this set.'")
tail=tail.replace("TOPICS=[('3.1','3.1 Force of gravity'),('3.2','3.2 Friction'),('3.3',\"3.3 Hooke's law\"),('Chapter review','Chapter review'),('Extra practice','Extra practice')]", "TOPICS=[('4.1',\"4.1 Inertia and Newton's first law\"),('4.2',\"4.2 Newton's second law\"),('4.3',\"4.3 Newton's third law\"),('4.4','4.4 Momentum'),('Chapter review','Chapter review'),('Extra practice','Extra practice')]")
tail=tail.replace('Chapter 3','Chapter 4').replace('Forces',"Newton’s Laws of Motion").replace('79 question','121 question').replace('Printed pages 76-100','Printed pages 102-130').replace('Try gravity, friction, or 3.3','Try inertia, momentum, or 4.2')
tail=tail.replace('bc-forces-questions','bc-newtons-laws-questions').replace('chapter=3','chapter=4').replace("title='Newton’s Laws of Motion'",'title="Newton\'s Laws of Motion"')
tail=tail.replace(".replace('bc-physics11-ch2','bc-physics11-ch3')", ".replace('bc-physics11-ch2','bc-physics11-ch4')")
tail=tail.replace(".replace('Chapter 2','Chapter 4')", ".replace('Chapter 2','Chapter 4')")
tail=tail.replace(".replace('kinematics-homework','forces-homework')", ".replace('kinematics-homework','newtons-laws-homework')").replace(".replace('kinematics-difficulty','forces-difficulty')", ".replace('kinematics-difficulty','newtons-laws-difficulty')")
tail=tail.replace('Answers use g = 9.81 N/kg and G = 6.67 × 10⁻¹¹ N·m²/kg² unless stated otherwise. Graph readings are approximate. Missing units and source misprints are explained in the affected answers.', 'Answers use g = 9.81 m/s² unless a question specifies another value. Choose a positive direction before adding forces or momenta. Assumptions and ambiguous wording are explained in the affected answers.')
tail=tail.replace('plus the sample-problem prompt, investigation questions, and challenges.', 'plus both sample-problem prompts and the investigation questions.').replace("'Investigation','Challenge','Section review'", "'Investigation','Section review'")
Path('tools/build_bc_newtons_laws_questions.py').write_text(head+groups+tail)
Path('tools/bc_newtons_laws_answers.py').write_text('"""Worked answers for Chapter 4, keyed by the extracted question IDs."""\nANSWERS = {}\n')
