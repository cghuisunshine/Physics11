#!/usr/bin/env python3
"""Draw introductory spherical-mirror focus diagrams in the small-angle model."""
from html import escape
from math import sqrt
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/optics-notes'


def build_focus_figure(concave):
    name = 'concave' if concave else 'convex'
    sign = 1 if concave else -1
    vertex, axis, radius = 600, 230, 320
    centre = vertex - sign * radius
    focus = vertex - sign * radius / 2
    title = ('Concave: reflected rays meet at F' if concave
             else 'Convex: reflected rays appear to come from F')
    description = ('Light arrives from the left, parallel to the principal axis. '
                   'Orange arrows show incoming light; teal arrows show reflected light. '
                   + ('The reflected rays cross at the real focus F in front of the mirror. '
                      'The order is C, F, V.' if concave else
                      'The reflected rays spread apart in front of the mirror. Dashed backward '
                      'extensions meet at the virtual focus F behind it. The order is V, F, C.')
                   + ' F is halfway between V and C. The shaded area is behind the mirror.')
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="490"
 viewBox="0 0 960 490" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
<marker id="incoming" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="reflected" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>
text{{font-family:Arial,Helvetica,sans-serif;font-size:20px;fill:#203440}}
.title{{font-size:27px;font-weight:700;fill:#075d64}}
.small{{font-size:18px}}.label{{font-size:23px;font-weight:700}}
.axis{{stroke:#879da4;stroke-width:1.5}}.dimension{{stroke:#647a84;stroke-width:1.5;fill:none}}
.in{{stroke:#b24c20;stroke-width:3;fill:none}}
.out{{stroke:#086b72;stroke-width:3;fill:none}}
.extension{{stroke:#086b72;stroke-width:2;stroke-dasharray:7 6;fill:none}}
</style></defs>
<rect width="960" height="490" rx="12" fill="#fff"/>
<rect x="14" y="14" width="932" height="462" rx="12" fill="none" stroke="#cadbdd" stroke-width="2"/>
<text x="32" y="52" class="title">{escape(title)}</text>
<text x="32" y="86" class="small">Solid arrows: actual light</text>
<rect x="638" y="108" width="292" height="225" rx="8" fill="#eef3f4"/>
<text x="56" y="132">In front of mirror</text>
<text x="665" y="132">Behind mirror</text>
<path d="M48 {axis}H932" class="axis"/>
<text x="55" y="258" class="small">Principal axis</text>''']
    for offset in (-48, 48):
        hit_x = centre + sign * sqrt(radius**2 - offset**2)
        hit_y = axis + offset
        # The curve is spherical; reflected paths use the near-axis common-focus model.
        end_x = 150 if concave else 290
        slope = offset / (hit_x - focus)
        end_y = hit_y + slope * (end_x - hit_x)
        parts += [f'<path d="M65 {hit_y}H{hit_x:.3f}" class="in"/>',
                  f'<path d="M220 {hit_y}H330" class="in" marker-end="url(#incoming)"/>',
                  f'<path d="M{hit_x:.3f} {hit_y}L{end_x} {end_y:.3f}" class="out"/>']
        # Place the arrow before the focus for concave, before the left edge for convex.
        t1, t2 = (.12, .27) if concave else (.45, .65)
        p = (hit_x + t1*(end_x-hit_x), hit_y + t1*(end_y-hit_y))
        q = (hit_x + t2*(end_x-hit_x), hit_y + t2*(end_y-hit_y))
        parts.append(f'<path d="M{p[0]:.3f} {p[1]:.3f}L{q[0]:.3f} {q[1]:.3f}" '
                     'class="out" marker-end="url(#reflected)"/>')
        if not concave:
            parts.append(f'<path d="M{hit_x:.3f} {hit_y}L{focus} {axis}" class="extension"/>')
    # A circular arc bulges toward V for concave and away from V for convex.
    edge_x = centre + sign * sqrt(radius**2 - 105**2)
    sweep = 1 if concave else 0
    parts.append(f'<path d="M{edge_x:.3f} {axis-105}A{radius} {radius} 0 0 {sweep} '
                 f'{edge_x:.3f} {axis+105}" fill="none" stroke="#075d64" stroke-width="7"/>')
    for label, x in (('C', centre), ('F', focus), ('V', vertex)):
        parts += [f'<circle cx="{x}" cy="{axis}" r="5" fill="#203440"/>',
                  f'<text x="{x+13 if label == "V" else x}" y="{axis+29}" '
                  f'text-anchor="middle" class="label">{label}</text>']
    if concave:
        parts += ['<text x="312" y="315">Real focus</text>',
                  f'<path d="M410 295L{focus-5} {axis+8}" class="dimension"/>']
    else:
        parts += ['<text x="672" y="305">Virtual focus</text>',
                  '<text x="654" y="352" class="small">Dashed: backward extensions</text>']
    for x, y, label in ((focus, 383, 'VF = |f|'), (centre, 425, 'VC = R')):
        lo, hi = sorted((x, vertex))
        parts += [f'<path d="M{lo} {y-6}V{y+6}M{lo} {y}H{hi}M{hi} {y-6}V{y+6}" class="dimension"/>',
                  f'<text x="{(lo+hi)/2}" y="{y-10}" text-anchor="middle" class="small">{label}</text>']
    parts += ['<text x="32" y="459" class="small">Near-axis model: F is about halfway from V to C.</text>', '</svg>']
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / f'{name}-focus.svg').write_text('\n'.join(parts) + '\n')


def build_focus_figures():
    for concave in (True, False):
        build_focus_figure(concave)
    print('Built concave and convex introductory focus SVGs.')


if __name__ == '__main__':
    build_focus_figures()
