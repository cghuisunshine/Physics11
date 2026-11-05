from pathlib import Path
source=Path('tools/build_bc_kinematics_questions.py').read_text()
head=source[:source.index("g=group('2.1'")]
head=head.replace('Chapter 2','Chapter 3').replace('bc_kinematics_answers','bc_forces_answers').replace('bc-ch2','bc-ch3').replace("'-f', '42', '-l', '79'","'-f', '81', '-l', '105'").replace('enumerate(pages, 42)','enumerate(pages, 81)').replace('range(43, 80)','range(81, 106)').replace("'-f', '43', '-l', '79'","'-f', '81', '-l', '105'")
groups='''g=group('3.1','Warm-up','Force of gravity: warm-up'); add(g,'Warm-up',[full(81,124,191)])
g=group('3.1','Quick check','Weight and gravitational field strength: quick check')
for n,a,b in [(1,268,285),(2,362,380),(3,470,505)]: add(g,n,[full(82,a,b)])
g=group('3.1','Quick check','Universal gravitation: quick check')
add(g,1,[full(85,275,437)]); add(g,2,[full(85,461,672)])
g=group('3.1','Investigation','Investigation 3-1A: the force of gravity',context=[full(86,77,552)])
for n,a,b in [(1,569,596),(2,596,637),(3,637,664),(4,664,710)]: add(g,n,[full(86,a,b)])
g=group('3.1','Investigation','Investigation 3-1B: gravity and distance',context=[full(87,77,344),(87,260,344,576,667)])
add(g,1,[(87,56,357,258,425)]); add(g,2,[(87,56,425,258,557)])

def reviews(topic,title,page_numbers,kind='Section review',expected=None):
    g=group(topic,kind,title)
    for p in page_numbers:
        left=63 if (p-5)%2 else 48
        for x0,x1,anchor in [(left-4,left+243,left),(left+254,576,left+258)]:
            starts=[]
            for line in LINES[p]:
                m=re.match(r'^(\\d+)\\.\\s',line['text'])
                if m and abs(line['xMin']-anchor)<2 and 40<line['yMin']<715:
                    starts.append((int(m[1]),line['yMin']))
            starts.sort(key=lambda v:v[1])
            for i,(n,y) in enumerate(starts):
                end=starts[i+1][1]-3 if i+1<len(starts) else 715
                boxes=[(p,x0,y-3,x1,end)]
                if p==103:
                    boxes=[(p,x0,y-3,x1,min(end,577))]
                    if n==4: boxes.append(full(103,577,709))
                add(g,n,boxes)
    g['questions'].sort(key=lambda q:int(q['label']))
    assert [int(q['label']) for q in g['questions']]==list(range(1,expected+1)),title
    return g

reviews('3.1','3.1 Review: force of gravity',[88,89],expected=9)
g=group('3.2','Warm-up','Friction: warm-up'); add(g,'Warm-up',[full(90,116,147)])
g=group('3.2','Sample prompt','Sample 3.2.1: kinetic friction'); add(g,'3.2.1',[full(92,390,421)])
g=group('3.2','Practice','Practice 3.2.1: kinetic friction')
for n,a,b in [(1,79,115),(2,187,407),(3,524,562)]: add(g,n,[full(93,a,b)])
g=group('3.2','Investigation','Investigation 3-2, Part 1: friction and weight',context=[full(94,77,702),full(95,60,149)])
for n,a,b in [(1,162,190),(2,189,206),(3,203,232),(4,230,276)]: add(g,n,[full(95,a,b)])
g=group('3.2','Challenge','Investigation 3-2: a different surface',context=[full(94,77,702),full(95,60,149)])
add(g,1,[full(95,290,307)])
g=group('3.2','Investigation','Investigation 3-2, Part 2: friction and contact area',context=[full(95,309,680),full(96,60,285)])
add(g,1,[full(96,299,341)]); add(g,2,[full(96,340,359)])
reviews('3.2','3.2 Review: friction',[97],expected=6)
g=group('3.3','Warm-up',"Hooke's law: warm-up"); add(g,'Warm-up',[full(98,124,164)])
spring_graph=(98,178,444,576,724)
g=group('3.3','Quick check','Spring constant: quick check',shared=[spring_graph])
for n,a,b in [(1,222,241),(2,384,403),(3,546,565)]: add(g,n,[full(99,a,b)])
g=group('3.3','Investigation','Investigation 3-3: another way to weigh',context=[full(100,77,678),full(101,60,434)])
add(g,1,[full(101,446,501)]); add(g,2,[full(101,500,532)])
g=group('3.3','Challenge','Investigation 3-3: make a letter weigher',context=[full(100,77,678),full(101,60,434)])
add(g,1,[full(101,546,579)])
g=reviews('3.3',"3.3 Review: Hooke's law",[102],expected=5); g['shared']=[spring_graph]
reviews('Chapter review','Chapter 3 Review Questions',[103,104],kind='Chapter review',expected=10)
reviews('Extra practice','Chapter 3 Extra Practice',[105],kind='Extra practice',expected=18)
assert sum(len(g['questions']) for g in GROUPS)==79

'''
tail=source[source.index('CACHE={}'):]
tail=tail.replace("TOPICS=[('2.1','2.1 Speed and velocity'),('2.2','2.2 Acceleration'),('2.3','2.3 Uniform acceleration'),('2.4','2.4 Gravity and free fall'),('Chapter review','Chapter review'),('Extra practice','Extra practice')]", "TOPICS=[('3.1','3.1 Force of gravity'),('3.2','3.2 Friction'),('3.3',\"3.3 Hooke's law\"),('Chapter review','Chapter review'),('Extra practice','Extra practice')]")
tail=tail.replace("'Investigation','Section review'","'Investigation','Challenge','Section review'")
tail=tail.replace('Chapter 2','Chapter 3').replace('Kinematics','Forces').replace('101 question','79 question').replace('Printed pages 38-74','Printed pages 76-100').replace('Try golf ball, graph, or 2.3','Try gravity, friction, or 3.3')
tail=tail.replace('Every warm-up, quick check, practice problem, review question, and extra-practice problem, plus sample-problem prompts and investigation questions.', 'Every warm-up, quick check, practice problem, section and chapter review, and extra-practice problem, plus the sample-problem prompt, investigation questions, and challenges.')
tail=tail.replace('Answers use g = 9.81 m/s² unless the supplied equation or graph uses 9.8. Graph readings are approximate. Printing includes the answers you have revealed.', 'Answers use g = 9.81 N/kg and G = 6.67 × 10⁻¹¹ N·m²/kg² unless stated otherwise. Graph readings are approximate. Missing units and source misprints are explained in the affected answers. Printing includes the answers you have revealed.')
tail=tail.replace("output=ROOT/'bc-kinematics-questions.html'", "output=ROOT/'bc-forces-questions.html'").replace("manifest=ROOT/'content/bc-kinematics-questions.json'", "manifest=ROOT/'content/bc-forces-questions.json'").replace('chapter=2','chapter=3')
tail=tail.replace("(ROOT/'tools/bc-kinematics-homework.js').read_text()", "(ROOT/'tools/bc-kinematics-homework.js').read_text().replace('bc-physics11-ch2','bc-physics11-ch3').replace('Kinematics','Forces').replace('Chapter 2','Chapter 3').replace('bc-kinematics-questions.html','bc-forces-questions.html').replace('kinematics-homework','forces-homework')")
tail=tail.replace("(ROOT/'tools/bc-kinematics-homework-ai.js').read_text()", "(ROOT/'tools/bc-kinematics-homework-ai.js').read_text().replace('kinematics-difficulty','forces-difficulty')")
Path('tools/build_bc_forces_questions.py').write_text(head+groups+tail)
