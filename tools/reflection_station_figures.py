#!/usr/bin/env python3
"""Generate exact geometric SVG teaching diagrams for reflection stations A–C."""
from html import escape
from math import cos, sin, radians
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/wave-motion-notes'
INK, MUTED, INCIDENT, REFLECTED = '#182e3c', '#526875', '#086b72', '#ad4e16'


def text(x, y, value, size=24, color=INK, weight=400, anchor='start'):
    return (f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def path(points, color=INCIDENT, width=3, extra=''):
    return f'<path d="{points}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


def ray(a, b, reflected=False):
    marker = 'reflected-head' if reflected else 'incident-head'
    return path(f'M{a[0]:.3f},{a[1]:.3f}L{b[0]:.3f},{b[1]:.3f}',
                REFLECTED if reflected else INCIDENT, 3.5, f'marker-end="url(#{marker})"')


def make_svg(answer=False):
    title = 'Reflection stations · worked answer' if answer else 'Reflection stations · sketch and predict'
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1140" viewBox="0 0 1200 1140" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">Three top-view ripple-tank diagrams: circular fronts at a flat barrier, a straight-front ray incident at 35 degrees to the normal, and straight fronts approaching a parabolic barrier along its axis. {'Reflected fronts and rays are orange; dashed extensions locate the virtual source. The reflected angle is 35 degrees and parallel incident rays reflect toward the focus.' if answer else 'Sketch the reflected fronts in A, the leaving ray and angle in B, and the reflected paths toward the marked focus in C.'}</desc>
<defs><clipPath id="circular-water"><rect x="60" y="200" width="500" height="200"/></clipPath>
<marker id="incident-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="{INCIDENT}" stroke-width="1.8"/></marker>
<marker id="reflected-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="{REFLECTED}" stroke-width="1.8"/></marker></defs>
<rect width="1200" height="1140" rx="16" fill="white"/>
<g font-family="system-ui,-apple-system,sans-serif">
<rect x="40" y="125" width="540" height="495" rx="14" fill="#f4f9fa" stroke="#d6e2e5"/>
<rect x="620" y="125" width="540" height="495" rx="14" fill="#f4f9fa" stroke="#d6e2e5"/>
<rect x="40" y="650" width="1120" height="445" rx="14" fill="#f4f9fa" stroke="#d6e2e5"/>
''', text(40, 55, title, 34, weight=750),
        text(40, 96, 'Top views · crest lines are perpendicular to travel rays', 25, MUTED),
        text(65, 169, 'A · Circular fronts', 28, weight=700),
        '<rect x="60" y="200" width="500" height="200" fill="#e4f2f4"/>',
        '<rect x="60" y="405" width="500" height="155" fill="#f0f1f1"/>',
        text(76, 230, 'Water', 22, MUTED), text(76, 461, 'Behind barrier', 21, MUTED),
        '<g clip-path="url(#circular-water)" fill="none">']
    for radius in (38, 76, 114, 152, 190, 228):
        parts.append(f'<circle cx="300" cy="270" r="{radius}" stroke="{INCIDENT}" stroke-width="2.5"/>')
    if answer:
        for radius in (152, 190, 228):
            parts.append(f'<circle cx="300" cy="530" r="{radius}" stroke="{REFLECTED}" stroke-width="3"/>')
    parts.extend(['</g>', path('M60 400H560', INK, 9),
                  '<circle cx="300" cy="270" r="6" fill="#182e3c"/>',
                  text(312, 259, 'S', 23, weight=700), ray((335, 311.364), (410, 400)),
                  text(76, 429, 'Flat barrier', 21, INK, 600)])
    if answer:
        parts.extend([ray((410, 400), (520, 270), True),
                      path('M410 400L300 530', REFLECTED, 2, 'stroke-dasharray="7 6"'),
                      path('M300 282V518', MUTED, 1.5, 'stroke-dasharray="4 6"'),
                      '<circle cx="300" cy="530" r="6" fill="#ad4e16"/>',
                      text(313, 542, 'S′ (virtual)', 22, REFLECTED, 650),
                      text(66, 593, 'S and S′: equal distances from the barrier.', 22)])
    else:
        parts.extend([text(66, 587, 'Sketch reflected fronts and their', 23),
                      text(66, 612, 'apparent source position.', 23)])

    # Flat reflection: both rays are 35 degrees from the vertical normal.
    angle = radians(35)
    px, py, length = 900, 480, 230
    incoming = (px - length * sin(angle), py - length * cos(angle))
    outgoing = (px + length * sin(angle), py - length * cos(angle))
    parts.extend([text(645, 169, 'B · Straight fronts', 28, weight=700),
                  path('M650 480H1130', INK, 9),
                  path('M900 220V480', MUTED, 2, 'stroke-dasharray="8 7"'),
                  text(915, 240, 'Normal', 23, MUTED),
                  text(646, 268, 'Incident ray', 22, INCIDENT, 600),
                  ray(incoming, (px, py)),
                  '<circle cx="900" cy="480" r="5" fill="#182e3c"/>',
                  text(911, 507, 'P', 22, weight=700),
                  text(650, 516, 'Flat barrier', 22),
                  path('M900 450H930V480', MUTED, 1.5)])
    for distance in (80, 135, 190):
        x, y = px - distance * sin(angle), py - distance * cos(angle)
        dx, dy = 26 * cos(angle), -26 * sin(angle)
        parts.append(path(f'M{x-dx:.3f},{y-dy:.3f}L{x+dx:.3f},{y+dy:.3f}', INCIDENT, 2))
    radius = 66
    arc_x, arc_y = px - radius * sin(angle), py - radius * cos(angle)
    parts.extend([path(f'M900 414A66 66 0 0 0 {arc_x:.3f} {arc_y:.3f}', INCIDENT, 2),
                  text(844, 397, '35°', 25, INCIDENT, 650)])
    if answer:
        parts.append(ray((px, py), outgoing, True))
        parts.append(path(f'M900 414A66 66 0 0 1 {px+radius*sin(angle):.3f} {arc_y:.3f}', REFLECTED, 2))
        parts.extend([text(927, 397, '35°', 25, REFLECTED, 650),
                      text(645, 559, 'Leaves at 35° to the normal.', 23, REFLECTED, 650),
                      text(645, 591, 'That is 55° to the barrier.', 23)])
        for distance in (80, 135, 190):
            x, y = px + distance * sin(angle), py - distance * cos(angle)
            dx, dy = 26 * cos(angle), 26 * sin(angle)
            parts.append(path(f'M{x-dx:.3f},{y-dy:.3f}L{x+dx:.3f},{y+dy:.3f}', REFLECTED, 2))
    else:
        parts.extend([text(645, 559, 'Draw the ray leaving P.', 23),
                      text(645, 591, 'Label its angle to the normal.', 23)])

    # Left-opening parabola x = vertex - (y-axis_y)^2/(4*focal_length).
    vertex, axis_y, focal_length = 1000, 875, 80
    focus = (vertex - focal_length, axis_y)
    parts.extend([text(65, 697, 'C · Straight fronts approaching a parabolic barrier', 28, weight=700),
                  text(75, 737, 'Parallel incident fronts', 22, INCIDENT, 600),
                  path('M140 875H1090', MUTED, 1.5, 'stroke-dasharray="8 7"'),
                  text(145, 904, 'Axis', 22, MUTED)])
    for x in (220, 310, 400, 490, 580, 670, 760):
        parts.append(path(f'M{x} 750V1020', INCIDENT, 2))
    for dy in (-120, -60, 60, 120):
        y = axis_y + dy
        x = vertex - dy * dy / (4 * focal_length)
        parts.append(ray((160, y), (x, y)))
        if answer:
            mid = ((x + focus[0]) / 2, (y + focus[1]) / 2)
            parts.append(path(f'M{x:.3f},{y}L{mid[0]:.3f},{mid[1]:.3f}L{focus[0]},{focus[1]}',
                              REFLECTED, 3, 'marker-mid="url(#reflected-head)"'))
    curve = 'M' + 'L'.join(f'{vertex - dy*dy/(4*focal_length):.3f},{axis_y+dy}' for dy in range(-145, 146, 2))
    parts.extend([path(curve, INK, 9),
                  '<circle cx="920" cy="875" r="6" fill="#182e3c"/>',
                  text(889, 909, 'F', 25, weight=700),
                  text(1015, 842, 'Parabolic', 20), text(1015, 868, 'barrier', 20),
                  text(75, 1071, 'Reflected rays converge toward the focus F.' if answer else
                       'Trace the reflected rays. What happens near F?', 25,
                       REFLECTED if answer else INK, 650),
                  text(40, 1127, 'Orange: reflected waves. Dashed extensions behind the barrier are constructions.' if answer else
                       'Sketches are schematic. Water depth and barrier position remain fixed.', 21, MUTED),
                  '</g></svg>'])
    return '\n'.join(parts) + '\n'


def build_reflection_station_figures():
    OUT.mkdir(parents=True, exist_ok=True)
    for kind in ('question', 'answer'):
        (OUT / f'reflection-stations-{kind}.svg').write_text(make_svg(kind == 'answer'))
    print('Built reflection-stations question and answer SVGs.')


if __name__ == '__main__':
    build_reflection_station_figures()
