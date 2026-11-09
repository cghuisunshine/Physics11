#!/usr/bin/env python3
"""Build the Chapter 7 optics study notes and Quick Review."""
from bc_study_pages import Chapter, build_study_pages

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
    (4, 'Vertex, focus, and centre of curvature', 218, (60, 182, 549, 311),
     'A concave mirror with the centre of curvature, principal focus, vertex, and principal axis marked.',
     'Figure 7.2.2 · In the spherical model, F lies about halfway from V to C.'),
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
)

if __name__ == '__main__':
    build_study_pages(CHAPTER)
