"""Small, self-contained ray diagrams for the Chapter 7 worked solutions."""
from html import escape

RAY = '#096a70'
SECOND_RAY = '#4863a1'
OBJECT = '#8a4528'
IMAGE = '#91396d'


def diagram(caption, drawing, view='0 0 410 180'):
    return (f'<figure class="answer-graph"><svg viewBox="{view}" role="img" '
            f'aria-label="{escape(caption, quote=True)}">{drawing}</svg>'
            f'<figcaption>{escape(caption)}</figcaption></figure>')


def path(points, color, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ''
    coords = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2"{dash}/>'


def label(x, y, text, color='#203440'):
    return f'<text x="{x:g}" y="{y:g}" fill="{color}">{escape(text)}</text>'


def ray_diagram(device, object_distance, *, diverging=False, caption):
    """Paraxial construction with distances in focal lengths and the optic at x = 0."""
    focal_length = -1 if diverging else 1
    mirror = device == 'mirror'
    real_side = -1 if mirror else 1
    d = object_distance
    at_focus = d == focal_length
    di = None if at_focus else 1 / (1 / focal_length - 1 / d)
    xi = 0 if at_focus else real_side * di
    magnification = 0 if at_focus else -di / d

    left = min(-2.6, -d - .35, xi - .4)
    right = max(1.3 if mirror and not diverging else 2.6, xi + .4)
    scale = 348 / (right - left)
    optical_x = 30 - scale * left
    axis_y = 79
    h = min(27, 54 / max(1, abs(magnification)))
    obj = (optical_x - d * scale, axis_y - h)
    img = (optical_x + xi * scale, axis_y - h * magnification)
    refraction_y = (obj[1], axis_y)
    if mirror:
        bend = 13 if diverging else -13
        optic = (f'<path d="M{optical_x+bend:.1f} 17Q{optical_x-bend:.1f} 79 '
                 f'{optical_x+bend:.1f} 141" fill="none" stroke="#203440" stroke-width="2"/>')
    else:
        bulge = 14 if not diverging else -8
        optic = (f'<path d="M{optical_x-5:.1f} 17Q{optical_x-5-bulge:.1f} 79 {optical_x-5:.1f} 141'
                 f'H{optical_x+5:.1f}Q{optical_x+5+bulge:.1f} 79 {optical_x+5:.1f} 17Z" '
                 'fill="#e8f4f6" stroke="#203440" stroke-width="1.5"/>')

    drawing = [path([(20, axis_y), (388, axis_y)], '#a8b5bb'), optic]
    focus_positions = [(-focal_length, 'F'), (-2 * focal_length, 'C')] if mirror else [(-1, 'F₁'), (1, 'F₂')]
    for offset, name in focus_positions:
        x = optical_x + offset * scale
        drawing.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="2.3" fill="#203440"/>')
        drawing.append(label(x - 6, axis_y + 17, name))

    for hit_y, color in zip(refraction_y, (RAY, SECOND_RAY), strict=True):
        hit = (optical_x, hit_y)
        drawing.append(path([obj, hit], color))
        end_x = 27 if mirror else 381
        if at_focus:
            slope = h / (scale * d) * real_side
        else:
            slope = (img[1] - hit_y) / (img[0] - optical_x)
        # End each ray at the viewport border, if its slope would take it past the frame.
        end_y = hit_y + slope * (end_x - optical_x)
        if not 9 <= end_y <= 149:
            end_y = min(149, max(9, end_y))
            end_x = optical_x + (end_y - hit_y) / slope
        drawing.append(path([hit, (end_x, end_y)], color))
        if di is not None and di < 0:
            drawing.append(path([hit, img], color, dashed=True))

    def arrow(point, color):
        x, y = point
        foot = 5 if y < axis_y else -5
        return path([(x, axis_y), point, (x - 4, y + foot), point, (x + 4, y + foot)], color)

    drawing.append(arrow(obj, OBJECT))
    if di is not None:
        drawing.append(arrow(img, IMAGE))
    drawing.append(label(26, 169, 'Object', OBJECT))
    if di is not None:
        drawing.append(label(103, 169, 'Image', IMAGE))
    drawing.append(label(176, 169, 'Dashed lines are extensions' if di is not None and di < 0 else 'Solid lines show light paths', RAY))
    return diagram(caption, ''.join(drawing))


def pinhole():
    return diagram(
        'Rays from the top and bottom of the object cross at the pinhole and form an inverted image.',
        path([(44, 38), (199, 83), (351, 127)], RAY)
        + path([(44, 115), (199, 83), (351, 52)], SECOND_RAY)
        + path([(199, 24), (199, 77)], '#203440')
        + path([(199, 89), (199, 143)], '#203440')
        + path([(351, 25), (351, 146)], '#a8b5bb')
        + label(21, 159, 'Object') + label(176, 159, 'Pinhole') + label(329, 159, 'Screen'),
    )


def periscope():
    return diagram(
        'Two parallel 45° reflecting faces turn the light down, then horizontally toward the eye.',
        path([(341, 48), (207, 48), (207, 132), (70, 132)], RAY)
        + path([(239, 16), (239, 80), (175, 80), (239, 16)], '#a8b5bb')
        + path([(175, 100), (239, 100), (175, 164), (175, 100)], '#a8b5bb')
        + label(277, 38, 'Light in ←') + label(51, 120, '← To eye'),
    )


def apparent_depth():
    return diagram(
        'Rays leaving water bend away from the normal. Extend them backward to locate a shallower virtual image.',
        path([(25, 69), (385, 69)], '#506b80')
        + path([(180, 145), (180, 69), (180, 22)], RAY)
        + path([(180, 145), (219, 69), (256, 18)], SECOND_RAY)
        + path([(219, 69), (180, 123)], SECOND_RAY, dashed=True)
        + label(24, 62, 'Air') + label(24, 94, 'Water')
        + label(112, 128, 'Virtual') + label(125, 150, 'Coin'),
    )
