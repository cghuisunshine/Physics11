#!/usr/bin/env python3
"""Draw the Grade 11 paraxial mirror constructions using the mirror equation."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/optics-notes'
CASES = (
    ('beyond-c', 'Concave · Object beyond C', 3.0, 1,
     'Between C and F · Real, inverted, reduced', 'A screen can receive this real image.'),
    ('at-c', 'Concave · Object at C', 2.0, 1,
     'At C · Real, inverted, same size', 'A screen can receive this real image.'),
    ('between-c-f', 'Concave · Object between C and F', 1.5, 1,
     'Beyond C · Real, inverted, enlarged', 'A screen can receive this real image.'),
    ('at-f', 'Concave · Object at F', 1.0, 1,
     'Parallel reflected rays · No finite image', 'No finite screen position brings the image into focus.'),
    ('inside-f', 'Concave · Object inside F', 0.6, 1,
     'Behind the mirror · Virtual, upright, enlarged', 'A screen cannot receive this virtual image.'),
    ('convex', 'Convex · Security mirror', 3.0, -1,
     'Between V and F, behind mirror · Virtual, upright, reduced',
     'Reflected rays diverge; their backward extensions locate the smaller image.'),
)


def text(x, y, value, cls='', anchor='start'):
    return (f'<text x="{x:g}" y="{y:g}" class="{cls}" '
            f'text-anchor="{anchor}">{escape(value)}</text>')


def line(points, cls, **attrs):
    d = 'M' + ' '.join(f'{x:.3f},{y:.3f}' for x, y in points)
    extra = ''.join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" class="{cls}"{extra}/>'


def svg_start(width, height, title, description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '''<defs>
<marker id="orange-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="teal-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>
text{font-family:Arial,Helvetica,sans-serif;font-size:19px;fill:#203440}
.title{font-size:25px;font-weight:700;fill:#075d64}.subtitle{font-size:20px;font-weight:700}
.small{font-size:17px}.point-label{font-size:18px;font-weight:700}
.axis{fill:none;stroke:#a4b8bc;stroke-width:1.4}.mirror{fill:none;stroke:#086b72;stroke-width:6;stroke-linecap:round}
.orange{fill:none;stroke:#b24c20;stroke-width:2.5}.teal{fill:none;stroke:#086b72;stroke-width:2.5}
.extension{stroke-dasharray:7 5}.object{fill:none;stroke:#203440;stroke-width:4}
.image{fill:none;stroke:#8d315f;stroke-width:4}.image-label{fill:#8d315f;font-weight:700}
.panel{fill:#fff;stroke:#cadbdd;stroke-width:2}.back{fill:#f0f5f5}
</style></defs>''', f'<rect width="{width}" height="{height}" fill="#fff"/>']


def arrow(x, base_y, tip_y, cls, virtual=False, element_id=None):
    """Keep object and image arrow heights proportional to magnification."""
    sign = 1 if tip_y > base_y else -1
    size = min(9, abs(tip_y - base_y) * .5)
    attrs = {'stroke_dasharray': '6 4'} if virtual else {}
    if element_id:
        attrs['id'] = element_id
    return (line([(x, base_y), (x, tip_y)], cls, **attrs)
            + line([(x-size*.55, tip_y-sign*size), (x, tip_y),
                    (x+size*.55, tip_y-sign*size)], cls))


def mirror(x, axis_y, sign, half_height=100):
    # A schematic curved face; ray intersections use the paraxial vertex plane.
    bow = -sign * 15
    result = (f'<path class="mirror" d="M{x+bow:g} {axis_y-half_height:g} '
              f'Q{x-bow:g} {axis_y:g} {x+bow:g} {axis_y+half_height:g}"/>')
    for offset in range(round(-half_height*.8), round(half_height*.8)+1, 20):
        face_x = x + bow * (offset / half_height)**2
        result += line([(face_x+4, axis_y+offset), (face_x+13, axis_y+offset-8)], 'axis')
    return result


def directed_segment(start, end, cls):
    p = tuple(start[i] + .42*(end[i]-start[i]) for i in (0, 1))
    q = tuple(start[i] + .60*(end[i]-start[i]) for i in (0, 1))
    return line([p, q], cls, marker_end=f'url(#{cls}-arrow)')


def build_question():
    width, height = 1000, 884
    svg = svg_start(width, height, 'Predict the images for six curved-mirror setups',
                    'Five concave mirror panels place an upright object beyond C, at C, '
                    'between C and F, at F, and inside F. A sixth panel places a real object '
                    'in front of a convex security mirror. Images are not shown.')
    svg += [text(24, 37, 'Predict first: where will the image form?', 'title'),
            text(24, 66, 'Object arrows are shown; image positions and orientations are left for you.', 'small')]
    for index, (_, title, ratio, sign, _, _) in enumerate(CASES):
        left, top = 14 + (index % 2)*494, 88 + (index // 2)*243
        x, y, f = left+305, top+145, 60*sign
        ox = x-ratio*60
        svg.append(f'<g id="setup-{index+1}"><rect class="panel" x="{left}" y="{top}" width="480" height="229" rx="12"/>')
        svg += [text(left+16, top+30, f'{index+1} · {title}', 'subtitle'),
                f'<rect class="back" x="{x+16}" y="{top+53}" width="145" height="151"/>',
                line([(left+23,y),(left+456,y)],'axis'), mirror(x,y,sign,55),
                arrow(ox,y,y-38,'object'),text(ox,y-50,'O','point-label','middle')]
        for label, px in (('C',x-2*f),('F',x-f),('V',x)):
            svg += [f'<circle cx="{px}" cy="{y}" r="3" fill="#647a84"/>',
                    text(px+(17 if label=='V' else 0),y+25,label,'point-label','middle')]
        svg += [text(left+24,top+205,'Reflecting side','small'),
                text(x+22,top+195,'Behind mirror','small'),'</g>']
    svg += [text(24, 851, 'C = centre of curvature · F = principal focus · V = vertex', 'small'),
            text(24, 875, 'Positions are illustrative. Open the worked answer after making your predictions.', 'small'),'</svg>']
    (ASSETS/'mirror-image-positions-question.svg').write_text('\n'.join(svg)+'\n')


def build_answer(case):
    slug, title, ratio, sign, prediction, screen = case
    x, y, h, unit_f = 620.0, 226.0, 36.0, 110.0
    f, do = sign*unit_f, ratio*unit_f
    di = None if ratio == 1 and sign == 1 else f*do/(do-f)
    ox, oy = x-do, y-h
    image_y = None if di is None else y+h*di/do
    description = (prediction + '. ' + screen + ' The object is a dark upright arrow. '
                   'The image is a magenta arrow. Solid rays show actual light; dashed '
                   'lines behind the mirror are backward extensions, not transmitted light.')
    svg = svg_start(960, 454, title, description)
    svg += [f'<rect x="12" y="12" width="936" height="430" rx="14" class="panel"/>',
            text(32,47,title,'title'),text(32,78,prediction,'subtitle'),
            f'<rect class="back" x="{x+18}" y="102" width="285" height="249" rx="7"/>',
            text(x+28,123,'Behind mirror','small'),
            line([(120,y),(910,y)],'axis'),
            '<g id="ray-construction" '
            f'data-f="{f}" data-do="{do}" data-di="{di}" data-height="{h}" data-v="{x}" data-axis="{y}">']
    # Two principal rays from the object tip: parallel to axis and through V.
    # Reflection at V preserves the vertical component and reverses horizontal motion.
    hits = ((x,y-h),(x,y))
    slopes = (h/f,h/do)  # screen-coordinate vertical change per unit travel left
    for index, (hit,slope,cls) in enumerate(zip(hits,slopes,('orange','teal'))):
        distance = min(480.0, (345-hit[1])/slope if slope>0 else (hit[1]-136)/(-slope))
        end = (x-distance,hit[1]+slope*distance)
        svg += [line([(ox,oy),hit],cls,id=f'incident-{index+1}'),
                line([hit,end],cls,id=f'reflected-{index+1}'),
                directed_segment((ox,oy),hit,cls),directed_segment(hit,end,cls)]
        if di is not None and di<0:
            svg.append(line([hit,(x-di,image_y)],cls+' extension',id=f'extension-{index+1}'))
    svg += [mirror(x,y,sign), arrow(ox,y,oy,'object',element_id='object'),
            text(ox-12,oy-14,'O','point-label','middle')]
    if di is not None:
        virtual = di<0
        svg += [arrow(x-di,y,image_y,'image',virtual,element_id='image'),
                text(x-di+14,image_y+(18 if image_y>y else -9),'I','image-label')]
    for label, px in (('C',x-2*f),('F',x-f),('V',x)):
        label_x = px+18 if label=='V' else px
        if di is not None and di>0 and abs(px-(x-di))<1:
            label_x -= 17
        svg += [f'<circle cx="{px}" cy="{y}" r="3" fill="#647a84"/>',
                text(label_x,y+23,label,'point-label','middle')]
    svg += ['</g>',text(32,377,screen,'small'),
            text(32,405,'O: object · I: image · Solid rays: light · Dashed rays: backward extensions','small'),
            text(32,431,'Ideal small-angle ray model; curved mirror faces are schematic.','small'),'</svg>']
    (ASSETS/f'mirror-image-positions-{slug}.svg').write_text('\n'.join(svg)+'\n')


def build_mirror_position_figures():
    ASSETS.mkdir(exist_ok=True)
    build_question()
    for case in CASES:
        build_answer(case)
    print('Built curved-mirror question overview and six ray-construction SVGs.')


if __name__ == '__main__':
    build_mirror_position_figures()
