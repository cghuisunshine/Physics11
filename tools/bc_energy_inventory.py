"""Source coordinates and complete Chapter 5 question inventory.

Coordinates use PDF points. Original numbering, including the missing quick-
check number 3 on printed p.154, is retained. Investigation procedures include
the activity predictions; concluding and challenge questions are separate entries.
"""
import re


def build_groups(lines):
    groups = []

    def group(topic, kind, title, shared=None, context=None):
        g = dict(id=f'set-{len(groups)+1}', topic=topic, kind=kind, title=title,
                 questions=[], shared=shared or [], context=context or [])
        groups.append(g)
        return g

    def add(g, label, boxes):
        texts = [l['text'] for page,x0,y0,x1,y1 in boxes for l in lines[page]
                 if x0 <= l['xMin'] < x1 and y0 <= l['yMin'] < y1]
        g['questions'].append(dict(label=str(label), boxes=boxes, text=' '.join(texts)))

    def full(page, y0, y1):
        return (page, 45, y0, 577, y1)

    def text_box(page,y0,y1,x0=45,x1=577):
        selected=[l for l in lines[page] if x0 <= l['xMin'] < x1 and y0 <= l['yMin'] < y1]
        assert selected,(page,y0,y1)
        return (page,x0,min(l['yMin'] for l in selected)-.4,x1,max(l['yMax'] for l in selected)+.4)

    def entries(g,page,ranges,x0=45,x1=577):
        for label,a,b in ranges:
            add(g,label,[text_box(page,a,b,x0,x1)])

    def reviews(topic,title,pages,expected,kind='Section review',shared=None):
        g=group(topic,kind,title,shared=shared)
        for page in pages:
            left=63 if (page-5)%2 else 48
            for x0,x1,anchor in [(left-4,left+243,left),(left+254,577,left+258)]:
                starts=[]
                for l in lines[page]:
                    m=re.match(r'^\s*(\d+)[.]\s+',l['text'])
                    if m and abs(l['xMin']-anchor)<2 and 40<l['yMin']<720:
                        starts.append((int(m[1]),l['yMin']))
                starts.sort(key=lambda pair:pair[1])
                for i,(label,y) in enumerate(starts):
                    end=starts[i+1][1]-.01 if i+1<len(starts) else 725
                    add(g,label,[(page,x0,y-.4,x1,end-.4)])
        g['questions'].sort(key=lambda q:int(q['label']))
        assert [int(q['label']) for q in g['questions']]==list(range(1,expected+1)),title
        return g

    g=group('5.1','Warm-up','Energy forms: bouncing-ball warm-up')
    add(g,'Warm-up',[text_box(137,128,142)])
    g=group('5.1','Sample prompt','Sample 5.1.1: calculating work')
    add(g,'5.1.1',[text_box(137,538,565)])
    g=group('5.1','Practice','Practice 5.1.1: calculating work')
    entries(g,138,[(1,82,96),(2,136,163),(3,204,232)])
    g=group('5.1','Sample prompt','Sample 5.1.2: calculating power')
    add(g,'5.1.2',[text_box(138,551,579)])
    g=group('5.1','Practice','Practice 5.1.2: calculating power')
    entries(g,139,[(1,82,110),(2,163,178),(3,231,273)])
    g=group('5.1','Sample prompt','Sample 5.1.3: calculating horsepower')
    add(g,'5.1.3',[text_box(140,76,104)])
    pulley_context=[full(141,60,724),full(142,60,251)]
    g=group('5.1','Investigation','Investigation 5-1A: work with pulleys',context=pulley_context)
    entries(g,142,[(1,278,305),(2,305,318),(3,319,399),(4,412,465),(5,466,493)])
    g=group('5.1','Challenge','Investigation 5-1A: pulley challenges',shared=[(142,445,512,566,701)],context=pulley_context)
    entries(g,142,[(1,514,554)],x1=445)
    entries(g,142,[(2,554,595)],x1=429)
    g=group('5.1','Investigation','Investigation 5-1B: power of a small motor',context=[full(143,60,549)])
    entries(g,143,[(1,567,580),(2,580,595)])
    reviews('5.1','5.1 Review: work, power, and machines',[144,145,146],11)

    g=group('5.2','Warm-up','Mechanical energy: shaking-sand warm-up')
    add(g,'Warm-up',[text_box(147,128,170)])
    g=group('5.2','Quick check','Kinetic energy and work: quick check')
    entries(g,148,[(1,85,153),(2,193,207),(3,260,274),(4,328,342)])
    g=group('5.2','Quick check','Gravitational potential energy: quick check')
    entries(g,149,[(1,252,280),(2,333,348),(3,414,429)])
    g=group('5.2','Sample prompt','Sample 5.2.1: conservation of energy')
    add(g,'5.2.1',[full(151,80,240)])
    g=group('5.2','Practice','Practice 5.2.1: conservation of energy')
    entries(g,152,[(1,82,125),(2,285,327),(3,487,531)])
    reviews('5.2','5.2 Review: mechanical energy',[153,154],8)

    g=group('5.3','Warm-up','Temperature and touch: warm-up')
    add(g,'Warm-up',[text_box(155,128,170)])
    g=group('5.3','Quick check','Temperature, heat, and kelvins: quick check')
    add(g,1,[text_box(156,499,608)])
    entries(g,157,[(2,64,173),(3,186,390)])
    g=group('5.3','Quick check','Conduction, convection, and radiation: quick check')
    add(g,1,[text_box(159,85,100)])
    add(g,2,[full(159,166,425)])
    entries(g,159,[(4,476,518),(5,598,613)])

    conduction_context=[full(160,60,710),(161,45,60,356,256),(161,356,60,577,340)]
    g=group('5.3','Investigation','Investigation 5-3A: conduction',context=conduction_context)
    entries(g,161,[(1,273,300),(2,300,327),(3,327,341)],x1=356)
    g=group('5.3','Challenge','Investigation 5-3A: keeping ice solid',context=conduction_context)
    add(g,1,[text_box(161,360,375)])
    convection_context=[full(162,60,87),(162,45,88,385,405),(162,385,88,577,637)]
    g=group('5.3','Investigation','Investigation 5-3B: convection',context=convection_context)
    entries(g,162,[(1,422,462),(2,462,518)],x1=385)
    radiation_context=[full(163,60,466)]
    g=group('5.3','Investigation','Investigation 5-3C: infrared absorption',context=radiation_context)
    entries(g,163,[(1,488,501),(2,502,516)])
    g=group('5.3','Challenge','Investigation 5-3C: infrared reflection',context=radiation_context)
    add(g,1,[full(163,534,722)])
    reviews('5.3','5.3 Review: temperature and heat transfer',[164],8)

    heat_table=full(165,454,612)
    g=group('5.4','Warm-up','Lakes and puddles: warm-up')
    add(g,'Warm-up',[text_box(165,128,157)])
    g=group('5.4','Sample prompt','Sample 5.4.1: specific heat capacity',shared=[heat_table])
    add(g,'5.4.1',[text_box(166,76,91)])
    g=group('5.4','Practice','Practice 5.4.1: specific heat capacity',shared=[heat_table])
    entries(g,166,[(1,394,412),(2,448,480),(3,515,548),(4,585,600),(5,623,656)])
    g=group('5.4','Sample prompt','Sample 5.4.2: efficiency')
    add(g,'5.4.2',[text_box(167,431,460)])
    g=group('5.4','Practice','Practice 5.4.2: efficiency')
    entries(g,168,[(1,82,110),(2,231,259),(3,379,394),(4,514,556)])
    g=group('5.4','Investigation','Investigation 5-4: heating power',context=[full(169,60,548)])
    entries(g,169,[(1,566,580),(2,580,619),(3,626,700),(4,707,722)])
    reviews('5.4','5.4 Review: thermal energy and efficiency',[170,171],9,shared=[heat_table])
    reviews('Chapter review','Chapter 5 Review Questions',[172,173,174,175],20,kind='Chapter review')
    # The shared diagram is required when exporting question 7 or 8 without 6.
    reviews('Extra practice','Chapter 5 Extra Practice',[176,177],24,kind='Extra practice',
            shared=[(176,318,114,577,337)])

    count=0
    for g in groups:
        for q in g['questions']:
            count+=1
            q['id']=f'q-{count}'
    return groups
