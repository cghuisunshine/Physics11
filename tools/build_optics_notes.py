#!/usr/bin/env python3
"""Build the Chapter 7 optics study notes and Quick Review."""
import base64
from html import escape

from bc_study_pages import ROOT, Chapter, build_study_pages
from optics_mirror_position_figures import CASES, build_mirror_position_figures
from optics_focus_figures import build_focus_figures


def embed_mirror_equation_solution():
    """Connect the numerical result to a ray diagram inside the worked answer."""
    path = ROOT / 'optics-notes.html'
    page = path.read_text()
    marker = '<p>MIRROR_EQUATION_SOLUTION_FIGURE</p>'
    assert page.count(marker) == 1
    svg = ROOT / 'assets/optics-notes/mirror-equation-solution.svg'
    data = base64.b64encode(svg.read_bytes()).decode()
    alt = ('A concave mirror with its upright object 100 cm in front of V. '
           'The real image is 25.0 cm in front, between F at 20.0 cm and C at 40.0 cm. '
           'Two reflected rays cross at the inverted image tip. The image arrow '
           'is one quarter as tall as the object, matching magnification −0.250. '
           'Both distance guides start at V.')
    caption = ('Worked-example diagram · Positive image distance puts this real image '
               'in front of the mirror. Negative magnification makes it inverted; '
               '|m| = 0.250 makes it one quarter as tall. The arrow heights are illustrative.')
    figure = (f'<figure class="diagram mirror-equation-solution">'
              f'<img src="data:image/svg+xml;base64,{data}" width="960" height="510" '
              f'alt="{escape(alt, quote=True)}" loading="lazy">'
              f'<figcaption>{escape(caption)}</figcaption></figure>')
    path.write_text(page.replace(marker, figure))


def embed_focus_figures():
    """Keep the focus comparison beside the corresponding explanation, offline."""
    path = ROOT / 'optics-notes.html'
    page = path.read_text()
    for name, alt, caption in (
        ('concave',
         'Light arrives from the left. A concave mirror reflects parallel rays back '
         'to a real focus F in front of the mirror. The axis order is C, F, V. '
         'VF is about half VC; C is the sphere centre, not the focus.',
         'Concave mirror · Follow the solid arrows to the real focus F. '
         'Both C and F are in front of the mirror.'),
        ('convex',
         'Light arrives from the left. A convex mirror reflects parallel rays back '
         'to the left, spreading apart. Dashed backward extensions meet at a virtual '
         'focus F behind the mirror. The axis order is V, F, C; VF is about half VC.',
         'Convex mirror · Solid arrows stay in front. Only dashed backward extensions '
         'meet at F behind the mirror; light does not follow those dashed lines.'),
    ):
        marker = f'<p>{name.upper()}_FOCUS_FIGURE</p>'
        assert page.count(marker) == 1
        data = base64.b64encode((ROOT / f'assets/optics-notes/{name}-focus.svg').read_bytes()).decode()
        figure = (f'<figure class="diagram {name}-focus">'
                  f'<img src="data:image/svg+xml;base64,{data}" width="960" height="490" '
                  f'alt="{escape(alt, quote=True)}" loading="lazy">'
                  f'<figcaption>{escape(caption)}</figcaption></figure>')
        page = page.replace(marker, figure)
    path.write_text(page)


def embed_mirror_height_solution():
    """Keep the explanatory ray diagram inside the example's hidden answer."""
    path = ROOT / 'optics-notes.html'
    page = path.read_text()
    marker = '<p>MINIMUM_MIRROR_HEIGHT_SOLUTION_FIGURE</p>'
    assert page.count(marker) == 1
    svg = ROOT / 'assets/optics-notes/minimum-mirror-height-solution.svg'
    data = base64.b64encode(svg.read_bytes()).decode()
    alt = ('Light from the head top A reflects at the upper edge U into the eye E; '
           'light from the feet B reflects at the lower edge L into E. Dashed '
           'backward extensions reach virtual image points equally far behind '
           'the mirror. The equal horizontal distances make U and L vertical '
           'midpoints, so their separation is half the student height: 0.880 m.')
    caption = ('Side-view construction · U is halfway in height between eye and head top; '
               'L is halfway between eye and feet. A shorter mirror would cut off '
               'one of these limiting rays. The eye height shown is illustrative.')
    figure = (f'<figure class="diagram mirror-height-solution">'
              f'<img src="data:image/svg+xml;base64,{data}" width="1000" height="810" '
              f'alt="{escape(alt, quote=True)}" loading="lazy">'
              f'<figcaption>{escape(caption)}</figcaption></figure>')
    path.write_text(page.replace(marker, figure))


def embed_mirror_position_figures():
    """Show prediction setups first and keep the ray constructions in the answer."""
    path = ROOT / 'optics-notes.html'
    page = path.read_text()

    def figure(slug, width, height, alt, caption):
        svg = ROOT / f'assets/optics-notes/mirror-image-positions-{slug}.svg'
        data = base64.b64encode(svg.read_bytes()).decode()
        return (f'<figure class="diagram mirror-positions-{slug}">'
                f'<img src="data:image/svg+xml;base64,{data}" width="{width}" height="{height}" '
                f'alt="{escape(alt, quote=True)}" loading="lazy">'
                f'<figcaption>{escape(caption)}</figcaption></figure>')

    question = figure(
        'question', 1000, 884,
        'Six prediction setups with upright object arrows: five concave-mirror positions '
        'beyond C, at C, between C and F, at F, and inside F; then a convex security mirror. '
        'C, F and V are labelled. Images are not shown.',
        'Prediction setups · O is the object. For the concave cases C and F lie in front '
        'of the mirror; for the convex mirror they lie behind it. Predict before opening the answer.')
    answers = ''.join(figure(
        slug, 960, 454, f'{title}. {prediction}. {screen} '
        'Dark arrow: object; magenta arrow: image. Solid arrows show light; '
        'dashed rays behind the mirror are backward extensions.',
        f'{title} · {prediction}. {screen}')
        for slug, title, ratio, sign, prediction, screen in CASES)
    for marker, figures in (
        ('MIRROR_IMAGE_POSITIONS_QUESTION_FIGURE', question),
        ('MIRROR_IMAGE_POSITIONS_ANSWER_FIGURES', answers),
    ):
        token = f'<p>{marker}</p>'
        assert page.count(token) == 1
        page = page.replace(token, figures)
    path.write_text(page)


REFERENCES = [
    ('199–203', 204), ('204–207', 209), ('200, 208–211', 205),
    ('212–213, 219–221', 218), ('213–216, 222–225', 219), ('216–218', 222),
    ('226–228', 232), ('233, 237–238, 255', 238), ('229–230, 234', 234),
    ('230–231, 238', 235), ('232, 235–236', 240), ('239–242, 249', 246),
    ('242–244, 250–251', 247), ('244–246', 251), ('247–248, 251–253', 253),
]
# PDF coordinates have their origin at the upper left.
FIGURES = [
    (1, 'The electromagnetic spectrum', 205, (93, 541, 553, 706),
     'The spectrum runs from long radio wavelengths through visible light to short gamma wavelengths.',
     'Figure 7.1.1 · Frequency increases as vacuum wavelength decreases.'),
    (2, 'Draw a normal before measuring angles', 209, (165, 150, 480, 343),
     'An incident and reflected ray make the same angle with a vertical normal above a horizontal mirror.',
     'Figure 7.1.4 · Measure both angles from the normal.'),
    (2, 'A virtual image behind a plane mirror', 209, (165, 491, 548, 648),
     'Reflected rays reaching the viewer trace back through a mirror to an upright virtual image.',
     'Figure 7.1.5 · Follow the straight backward extensions behind the mirror.'),
    (3, 'A pinhole produces a real image', 205, (322, 95, 543, 215),
     'A cup has a small pinhole at one end and a translucent wax paper screen held over the open end.',
     'Textbook warm-up · The wax paper serves as the screen.'),
    (5, 'Trace two rays from the tip', 219, (162, 157, 550, 307),
     'Two rays from the top of a candle reflect from a concave mirror and cross below the principal axis.',
     'Figure 7.2.4 · The crossing locates the tip of a real, inverted image.'),
    (7, 'Speed changes at a boundary', 232, (178, 431, 549, 572),
     'A ray moves from vacuum into a higher-index material and makes a smaller angle with the normal.',
     'Figure 7.3.3 · Compare the angles to the vertical normal.'),
    (9, 'A ray can remain inside the higher-index material', 234, (180, 210, 558, 378),
     'One ray refracts out of water and partially reflects. The second reaches the interface at the critical angle.',
     'Figure 7.3.4 · At the critical angle, the refracted direction is along the surface.'),
    (10, 'Rainbows in raindrops', 235, (164, 514, 548, 697),
     'Sunlight follows different paths through drops to the observer. Red and violet leave at different angles.',
     'Figure 7.3.5 · Follow the refraction and internal reflection in the primary bow.'),
    (11, 'A direction for the electric field', 240, (88, 522, 555, 695),
     'A rope model compares passage of vertically polarized motion with blockage of horizontal motion.',
     'Figure 7.3.13 · The rope illustrates why orientation matters.'),
    (12, 'Converging and diverging lenses', 246, (57, 48, 556, 434),
     'A table compares a parallel ray, a focal ray, and a central ray for converging and diverging lenses.',
     'Table 7.4.1 · Compare how the three principal rays behave for each lens.'),
    (13, 'Investigation 7-4B · Predict and test', 256, (87, 248, 570, 368),
     'A converging lens forms a distant-source image near the focus and a closer-source image farther from the lens.',
     'Figure 7.4.17 · Compare the screen positions for parallel and diverging incident rays.'),
    (14, 'Accommodation and the retina', 251, (45, 125, 558, 253),
     'An eye focuses behind the retina in the first drawing. A converging lens corrects the focus in the second.',
     'Figure 7.4.6 · A converging lens can correct farsightedness.'),
    (14, 'Accommodation and the retina', 251, (122, 357, 558, 484),
     'An eye focuses in front of the retina in the first drawing. A diverging lens corrects the focus in the second.',
     'Figure 7.4.7 · A diverging lens can correct nearsightedness.'),
    (15, 'Match the instrument to the image', 253, (164, 126, 547, 257),
     'Parallel rays from a distant object enter the telescope objective. The eyepiece directs rays to the viewer.',
     'Figure 7.4.11 · The objective makes the intermediate image and the eyepiece magnifies the view.'),
]
HERO = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true">
<path d="M20 107H240" stroke="#b8cfd2" stroke-width="2"/>
<path d="M116 33Q86 107 116 181Q146 107 116 33Z" fill="#e7f3f3" stroke="#086b72" stroke-width="3"/>
<path d="M20 65H116L229 142M20 149H116L229 72" fill="none" stroke="#087cff" stroke-width="2.5"/>
<circle cx="178" cy="107" r="5" fill="#c86442"/><text x="173" y="130" font-size="15" fill="#086b72">F</text>
</svg>'''

CHAPTER = Chapter(
    slug='optics', title='Light and Geometric Optics', number=7, first_page=204, last_page=263,
    references=REFERENCES, figures=FIGURES, hero=HERO, search_hint='Try “Snell” or “critical angle”',
    worked_answers=16, review_labels=['Plane mirrors', 'Curved mirrors', 'Mirror equation', 'Refraction',
                                     'Critical angle and colour', 'Lenses', 'Optical instruments'],
    illustrations=((3, 'Small pinhole versus large pinhole',
                    'assets/optics-notes/pinhole-small-large-user.png',
                    'Two ray diagrams with trees on the right and camera screens on the left. '
                    'A small hole gives a sharp inverted tree. A larger hole lets rays from '
                    'each tree point reach a wider screen patch, producing overlapping, fuzzy images.',
                    'Small and large pinholes · Light travels from right to left. '
                    'A wider opening produces overlapping patches on the screen.'),
                   (3, 'Investigation 7-1B · Two mirrors and a periscope',
                    'assets/optics-notes/angled-mirror-images.svg',
                    'A point object centred between two mirrors at 60 degrees has five virtual '
                    'images. The object and images are equally far from the mirror vertex.',
                    'A · Five virtual images for a centred object at 60°. Solid orange dot: '
                    'object; dashed teal circles: virtual images.'),
                   (3, 'Investigation 7-1B · Two mirrors and a periscope',
                    'assets/optics-notes/parallel-mirror-images.svg',
                    'Two parallel facing mirrors produce repeated virtual images behind both '
                    'mirrors. More distant images are shown fainter because real reflections lose light.',
                    'B · Each mirror reflects images formed by the other. The sequence continues '
                    'in the ideal model; with real mirrors, images become fainter.'),
                   (3, 'Investigation 7-1B · Two mirrors and a periscope',
                    'assets/optics-notes/periscope-light-path.svg',
                    'A light ray enters from the left, turns downward at the upper mirror, and '
                    'turns right at the lower mirror toward the eye. Both parallel mirror faces '
                    'are at 45 degrees to the tube; dashed lines are normals.',
                    'C · Two reflections guide light through a periscope. At each mirror, '
                    'the angles of incidence and reflection are 45°, measured from the normal.'),
                   (3, 'Example · Mirror height and image count',
                    'assets/optics-notes/plane-mirrors-problem.png',
                    'Two question panels: a 1.76 m tall student faces a vertical plane mirror '
                    'of unknown minimum height; a top view shows an object on the angle '
                    'bisector between two mirrors meeting at 60 degrees.',
                    'Question setup · A: find the minimum mirror height. B: count the images '
                    'of the centred object. Schematic, not to scale.')),
)

if __name__ == '__main__':
    build_focus_figures()
    build_mirror_position_figures()
    build_study_pages(CHAPTER)
    embed_focus_figures()
    embed_mirror_equation_solution()
    embed_mirror_height_solution()
    embed_mirror_position_figures()
