#!/usr/bin/env python3
"""Draw two signed principal-ray constructions for the optional mirror proof."""
from html import escape
from math import atan2, cos, pi, sin, sqrt
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/optics-notes'


def build_focus_reflection_figure():
    """Use exact circle normals and specular reflection; the focus is approximate."""
    v, axis, radius, height = 700., 260., 320., 50.
    centre, focus = v-radius, v-radius/2
    px, py = centre+sqrt(radius**2-height**2), axis-height
    theta = atan2(height, px-centre)
    reflected_end_x = 430.
    reflected_end_y = py+(px-reflected_end_x)*sin(2*theta)/cos(2*theta)

    def arc(start_angle, end_angle, r):
        a=(px+r*cos(start_angle),py+r*sin(start_angle))
        b=(px+r*cos(end_angle),py+r*sin(end_angle))
        return f'M{a[0]:.3f} {a[1]:.3f}A{r} {r} 0 0 0 {b[0]:.3f} {b[1]:.3f}'

    edge=centre+sqrt(radius**2-110**2)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="470" viewBox="0 0 960 470" role="img" aria-labelledby="title desc">
<title id="title">The law of reflection sends a near-axis parallel ray toward the focus</title>
<desc id="desc">A parallel ray strikes a concave spherical mirror at P. The radius PC is normal to the surface. The incident ray and reflected ray make equal angles theta with PC. The normal is tilted theta to the horizontal, so the reflected ray is tilted twice theta to the axis. It crosses the axis near F, about halfway from C to V.</desc>
<defs><marker id="orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:20px;fill:#203440}}.title{{font-size:26px;font-weight:700;fill:#075d64}}.small{{font-size:17px}}.guide{{stroke:#91a5ab;stroke-width:1.4;fill:none}}.normal{{stroke:#526875;stroke-width:2;stroke-dasharray:7 5;fill:none}}</style></defs>
<rect width="960" height="470" fill="#fff"/><rect x="12" y="12" width="936" height="446" rx="12" fill="none" stroke="#cadbdd" stroke-width="2"/>
<text x="32" y="51" class="title">The normal sets the reflected direction</text>
<text x="32" y="86" class="small">Concave spherical mirror · both angles at P are measured from the radius PC.</text>
<rect x="747" y="112" width="177" height="215" rx="8" fill="#eef3f4"/>
<text x="760" y="145" class="small">Behind mirror</text>
<path d="M70 {axis}H925" class="guide"/>
<text x="75" y="290" class="small">Principal axis</text>
<path d="M120 {py}H{px}" stroke="#b24c20" stroke-width="3" fill="none"/>
<path d="M280 {py}H420" stroke="#b24c20" stroke-width="3" marker-end="url(#orange)"/>
<text x="120" y="185" fill="#b24c20">Incoming: parallel to axis</text>
<path d="M{px} {py}L{reflected_end_x} {reflected_end_y}" stroke="#086b72" stroke-width="3" fill="none"/>
<path d="M650 {py+(px-650)*sin(2*theta)/cos(2*theta)}L605 {py+(px-605)*sin(2*theta)/cos(2*theta)}" stroke="#086b72" stroke-width="3" marker-end="url(#teal)"/>
<path d="M{centre} {axis}L{px} {py}" class="normal"/>
<text x="326" y="136" class="small">Normal = radius PC</text>
<path d="M430 142L482 {py+(px-482)*height/(px-centre)}" class="guide"/>
<path d="{arc(pi,pi-theta,120)}" stroke="#b24c20" stroke-width="2" fill="none"/>
<path d="{arc(pi-theta,pi-2*theta,120)}" stroke="#086b72" stroke-width="2" fill="none"/>
<text x="{px+154*cos(pi-theta/2)-6}" y="{py+154*sin(pi-theta/2)+5}">θ</text>
<text x="{px+154*cos(pi-1.5*theta)-6}" y="{py+154*sin(pi-1.5*theta)+5}">θ</text>
<path d="M{edge} 150A{radius} {radius} 0 0 1 {edge} 370" stroke="#075d64" stroke-width="6" fill="none"/>
<circle cx="{px}" cy="{py}" r="4" fill="#203440"/>
<text x="{px+13}" y="{py-8}" font-weight="700">P</text>
<path d="M{px} {py}H731M731 {py}V{axis}M725 {axis}H737" class="guide"/>
<text x="737" y="240">h</text>
<circle cx="{centre}" cy="{axis}" r="4" fill="#203440"/><text x="{centre}" y="289" text-anchor="middle" font-weight="700">C</text>
<circle cx="{focus}" cy="{axis}" r="4" fill="#203440"/><text x="{focus}" y="292" text-anchor="middle" font-weight="700">F</text>
<circle cx="{v}" cy="{axis}" r="4" fill="#203440"/><text x="{v}" y="289" text-anchor="middle" font-weight="700">V</text>
<text x="330" y="328" class="small">Reflected ray: angle 2θ to the axis</text>
<path d="M{focus} 352V364M{focus} 358H{v}M{v} 352V364" class="guide"/>
<text x="{(focus+v)/2}" y="348" text-anchor="middle">f ≈ R/2</text>
<path d="M{centre} 392V404M{centre} 398H{v}M{v} 392V404" class="guide"/>
<text x="{(centre+v)/2}" y="388" text-anchor="middle">R</text>
<text x="32" y="437" class="small">Exact reflection at the drawn point P; the shared focus F is a near-axis approximation.</text>
</svg>'''
    ASSETS.mkdir(exist_ok=True)
    (ASSETS/'mirror-derivation-reflection-focus.svg').write_text(svg+'\n')


def build_derivation_figures():
    build_focus_reflection_figure()
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
    print('Built reflection-normal diagram and concave/convex two-ray constructions.')


if __name__ == '__main__':
    build_derivation_figures()
