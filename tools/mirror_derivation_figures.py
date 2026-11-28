#!/usr/bin/env python3
"""Draw two signed principal-ray constructions for the optional mirror proof."""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/optics-notes'


def build_derivation_figures():
    for sign, name in ((1, 'concave'), (-1, 'convex')):
        v, axis, do, ho = 600., 240., 320., 60.
        f = sign*120.
        di = f*do/(do-f)
        ox, image_x, image_y = v-do, v-di, axis+ho*di/do
        focus_x = v-f
        title = f'{name.capitalize()}: ' + ('f > 0, dᵢ > 0, hᵢ < 0' if sign>0 else 'f < 0, dᵢ < 0, hᵢ > 0')
        svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="490" viewBox="0 0 960 490" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Two rays from upright object tip O: an orange parallel ray reflects at P and a teal ray reflects at vertex V. Their reflected lines meet at image tip I, {'a real inverted image in front' if sign>0 else 'a virtual upright image behind, found with dashed backward extensions'}. Signed coordinate s increases toward the front, leftward. Vertical height is positive upward.</desc>
<defs>
<marker id="orange-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="teal-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:19px;fill:#203440}}.title{{font-size:26px;font-weight:700;fill:#075d64}}.small{{font-size:17px}}.label{{font-weight:700}}.axis{{stroke:#91a5ab;stroke-width:1.5;fill:none}}.orange{{stroke:#b24c20;stroke-width:2.5;fill:none}}.teal{{stroke:#086b72;stroke-width:2.5;fill:none}}.extension{{stroke-dasharray:7 5}}.image{{stroke:#8d315f;stroke-width:4;fill:none}}</style></defs>
<rect width="960" height="490" fill="#fff"/>
<rect x="12" y="12" width="936" height="466" rx="12" fill="none" stroke="#cadbdd" stroke-width="2"/>
<text x="32" y="50" class="title">{escape(title)}</text>
<text x="32" y="85" class="small">Positive s points left, in front of the mirror. Positive height points up.</text>
<rect x="636" y="110" width="287" height="213" rx="8" fill="#eef3f4"/>
<text x="667" y="137" class="small">Behind mirror: s &lt; 0</text>
<path d="M65 {axis}H925" class="axis"/>
<text x="68" y="269" class="small">Principal axis</text>''']

        def path(points, cls, arrow=False):
            d='M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in points)
            marker=f' marker-end="url(#{cls}-arrow)"' if arrow else ''
            return f'<path d="{d}" class="{cls}"{marker}/>'

        for cls, hit_y, slope, end_x in (
            ('orange', axis-ho, ho/f, 350. if sign>0 else 430.),
            ('teal', axis, ho/do, 350.),
        ):
            hit=(v,hit_y)
            end=(end_x,hit_y+slope*(v-end_x))
            svg += [path([(ox,axis-ho),hit],cls), path([hit,end],cls),
                    path([(ox+.25*do,axis-ho+.25*(hit_y-axis+ho)),
                          (ox+.5*do,axis-ho+.5*(hit_y-axis+ho))],cls,True)]
            a=tuple(hit[i]+.4*(end[i]-hit[i]) for i in (0,1))
            b=tuple(hit[i]+.6*(end[i]-hit[i]) for i in (0,1))
            svg.append(path([a,b],cls,True))
            if sign<0:
                end=(focus_x,axis) if cls=='orange' else (image_x+55,image_y-slope*55)
                svg.append(path([hit,end],cls+' extension'))
        bow=-5*sign
        svg.append(f'<path d="M{v+bow} 118Q{v-bow} 240 {v+bow} 340" stroke="#075d64" stroke-width="6" fill="none"/>')
        svg += [f'<path d="M{ox} {axis}V{axis-ho}M{ox-7} {axis-ho+12}L{ox} {axis-ho}L{ox+7} {axis-ho+12}" stroke="#203440" stroke-width="4" fill="none"/>',
                f'<text x="{ox-16}" y="{axis-ho-15}" class="label">O</text>',
                f'<text x="{ox-38}" y="{axis-ho/2+5}">hₒ</text>']
        direction=1 if image_y>axis else -1
        svg += [f'<path d="M{image_x} {axis}V{image_y}M{image_x-6} {image_y-direction*9}L{image_x} {image_y}L{image_x+6} {image_y-direction*9}" class="image"/>',
                f'<text x="{image_x+14}" y="{image_y+direction*19}" class="label">I</text>',
                f'<text x="{image_x-38}" y="{(axis+image_y)/2+5 if sign>0 else image_y-28}">hᵢ</text>',
                f'<circle cx="{focus_x}" cy="{axis}" r="4" fill="#203440"/>',
                f'<text x="{focus_x}" y="{axis+26}" text-anchor="middle" class="label">F</text>',
                f'<text x="{v+14}" y="{axis-ho-10}" class="label">P (0, hₒ)</text>',
                f'<text x="{v+14}" y="{axis+26}" class="label">V (0, 0)</text>']
        for start,end,y,label in ((ox,v,402,'dₒ > 0'),(v,image_x,367,'dᵢ > 0' if sign>0 else 'dᵢ < 0')):
            svg += [path([(start,y-5),(start,y+5)],'axis'),path([(start,y),(end,y)],'axis'),
                    path([(end,y-5),(end,y+5)],'axis'),
                    f'<text x="{(start+end)/2}" y="{y-10}" text-anchor="middle">{escape(label)}</text>']
        svg += ['<text x="32" y="450" class="small">Near-axis construction; mirror depth neglected. Diagram dimensions are illustrative.</text>',
                '</svg>']
        ASSETS.mkdir(exist_ok=True)
        (ASSETS/f'mirror-derivation-{name}.svg').write_text('\n'.join(svg)+'\n')
    print('Built concave and convex two-ray derivation diagrams.')


if __name__ == '__main__':
    build_derivation_figures()
