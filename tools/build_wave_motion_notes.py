#!/usr/bin/env python3
"""Build the Wave Motion study notes, Quick Review, and optional derivations."""
import base64
from html import escape
from tempfile import TemporaryDirectory
from pathlib import Path

from bc_study_pages import ROOT, Chapter, build_study_pages, render_outline

DERIVATION = 'double-slit-path-difference'
DERIVATION_LABEL = 'Deriving the path difference d sin θ'
DOPPLER_DERIVATION = 'doppler-sonic-boom-derivations'
DOPPLER_LABEL = 'Deriving the Doppler formulas and the Mach-cone angle'
DIFFRACTION_DERIVATION = 'diffraction-width-wavelength'
DIFFRACTION_LABEL = 'Why opening width and wavelength control diffraction'
SINGING_GLASS = 'singing-glass'
SINGING_GLASS_LABEL = 'Why does a glass sing, and why does water lower its pitch?'
RIPPLE_TANK = 'ripple-tank-animation'
RIPPLE_TANK_LABEL = 'Animate the ripple tank and its bright crest lines'


def build_singing_glass():
    template = (ROOT / f'tools/{SINGING_GLASS}-template.html').read_text()
    with TemporaryDirectory(prefix='singing-glass-') as directory:
        page = render_outline(f'{SINGING_GLASS}.md', template, Path(directory))
    data = base64.b64encode((ROOT / 'assets/wave-motion-notes/singing-glass-mode.svg').read_bytes()).decode()
    figure = (f'<figure><img src="data:image/svg+xml;base64,{data}" width="900" height="360" '
              'alt="Top view of a glass rim: two exaggerated oval shapes show opposite phases '
              'of one ringing mode around the dashed circular equilibrium. A mass and spring '
              'represent the mode’s effective inertia and stiffness, not a literal spring in the glass.">'
              '<figcaption>One mode can be described by a single deformation coordinate. '
              'The rim’s deformation is exaggerated; the mass–spring drawing is an equivalent '
              'model, not the glass’s physical construction.</figcaption></figure>')
    marker = '<p>GLASS_MODE_FIGURE</p>'
    assert page.count(marker) == 1
    page = page.replace(marker, figure)
    for label, url in (
        ('UNSW Music Acoustics FAQ', 'https://newt.phys.unsw.edu.au/jw/musFAQ.html'),
        ('Vibrational modes of partly filled wine glasses',
         'https://phys.unsw.edu.au/music/people/publications/Jundtetal2006.pdf'),
    ):
        marker = f'[{label}]({url})'
        assert page.count(marker) == 1
        page = page.replace(marker, f'<a href="{url}">{label}</a>')
    (ROOT / f'{SINGING_GLASS}.html').write_text(page)
    print(f'Built {SINGING_GLASS}.html: optional glass vibration explanation.')


def build_derivation():
    """Keep the optional proof separate from the core notes in every mode."""
    template = (ROOT / f'tools/{DERIVATION}-template.html').read_text()
    with TemporaryDirectory(prefix='double-slit-') as directory:
        page = render_outline(f'{DERIVATION}.md', template, Path(directory))
    svg = (ROOT / f'assets/wave-motion-notes/{DERIVATION}.svg').read_bytes()
    data = base64.b64encode(svg).decode()
    figure = (f'<figure><img src="data:image/svg+xml;base64,{data}" width="940" height="720" '
              'alt="Exact paths AP and BP meet at screen point P. M is the slit midpoint; '
              'MP makes angle θ with the central normal. AC and BD are perpendicular to MP '
              'at C and D, with D, M, C, P collinear. The projected separation CD is d sin θ '
              'exactly. For distant P, AP is approximately CP and BP is approximately DP.">'
              '<figcaption>Both slits are projected onto MP: AC and BD are perpendicular '
              'to this midpoint direction. The orange segment CD equals d sin θ exactly. '
              'Using AP ≈ CP and BP ≈ DP for a distant P makes the path difference '
              'approximately CD. Slit spacing is enlarged for clarity.</figcaption></figure>')
    assert page.count('<p>PATH_DIFFERENCE_FIGURE</p>') == 1
    page = page.replace('<p>PATH_DIFFERENCE_FIGURE</p>', figure)
    sketch = ROOT / 'assets/wave-motion-notes/double-slit-parallel-rays-annotated.jpg'
    data = base64.b64encode(sketch.read_bytes()).decode()
    figure = (f'<figure><img src="data:image/jpeg;base64,{data}" width="1280" height="871" '
              'alt="User-annotated parallel-ray sketch: green rays from A and B are chosen '
              'parallel to MP and approximate the directions of AP and BP for a distant P; '
              'AC is perpendicular to them and the orange segment BC equals d sin θ. '
              'Red lines add the midpoint M, screen point P, and AP, MP, and CP. '
              'The added line EF passes through P perpendicular to MP, meeting the upper '
              'green ray at E and the lower at F. AE approximates AP; BF approximates BP. '
              'C is on the lower construction ray, not generally on the actual path BP.">'
              '<figcaption>Your updated sketch places E and F on a common line through P '
              'perpendicular to the green rays and MP. For distant P, AE ≈ AP and BF ≈ BP. '
              'Since AE = CF, their difference BF − AE equals BC = d sin θ. '
              'This local point C differs from '
              'the projection foot C in the first diagram.</figcaption></figure>')
    assert page.count('<p>PARALLEL_SKETCH_FIGURE</p>') == 1
    page = page.replace('<p>PARALLEL_SKETCH_FIGURE</p>', figure)
    data = base64.b64encode((ROOT / 'assets/wave-motion-notes/double-slit-exact-geometry.svg').read_bytes()).decode()
    figure = (f'<figure><img src="data:image/svg+xml;base64,{data}" width="900" height="690" '
              'alt="Coordinate graph: slits A at (0, d/2) and B at (0, −d/2) connect to '
              'P at (L, y) by exact paths r_A and r_B. Each right triangle has horizontal '
              'leg L; its vertical leg is |y − d/2| or |y + d/2|. The dashed midpoint path '
              'has length R and angle θ to the central normal.">'
              '<figcaption>The coloured paths converge at P on a finite '
              'screen. The dashed horizontal legs show the two right triangles used by '
              'Pythagoras; the dashed diagonal is R = √(L² + y²). '
              'Slit spacing is enlarged for clarity.</figcaption></figure>')
    assert page.count('<p>EXACT_GEOMETRY_FIGURE</p>') == 1
    page = page.replace('<p>EXACT_GEOMETRY_FIGURE</p>', figure)
    (ROOT / f'{DERIVATION}.html').write_text(page)
    print(f'Built {DERIVATION}.html: optional geometry and algebra derivation.')


def build_doppler_derivation():
    template = (ROOT / f'tools/{DOPPLER_DERIVATION}-template.html').read_text()
    with TemporaryDirectory(prefix='doppler-') as directory:
        page = render_outline(f'{DOPPLER_DERIVATION}.md', template, Path(directory))
    figures = (
        ('DOPPLER_SPACING_FIGURE', 'doppler-crest-spacing', 900, 500,
         'A source moving right compresses the forward crest spacing and stretches the backward '
         'spacing. An observer moving toward a stationary source meets unchanged crests faster.',
         'The marks are one-dimensional cross-sections of crests emitted one period apart. '
         'Source motion changes their spacing; observer motion changes their encounter rate.'),
        ('MACH_CONE_FIGURE', 'mach-cone-geometry', 840, 600,
         'Right triangle OAS: OA is the sound-front radius c Δt, OS is source travel u_s Δt, '
         'and SA is tangent to the front at A. Angle μ at S has sine OA divided by OS.',
         'The cone surface is tangent to an earlier sound front. Its radius meets the surface '
         'at a right angle, making sin μ = c/u_s. This is a cross-section of a three-dimensional cone.'),
    )
    for marker, slug, width, height, alt, caption in figures:
        data = base64.b64encode((ROOT / f'assets/wave-motion-notes/{slug}.svg').read_bytes()).decode()
        figure = (f'<figure><img src="data:image/svg+xml;base64,{data}" width="{width}" '
                  f'height="{height}" alt="{alt}"><figcaption>'
                  f'{caption}</figcaption></figure>')
        assert page.count(f'<p>{marker}</p>') == 1
        page = page.replace(f'<p>{marker}</p>', figure)
    (ROOT / f'{DOPPLER_DERIVATION}.html').write_text(page)
    print(f'Built {DOPPLER_DERIVATION}.html: optional Doppler and Mach-cone derivations.')


def build_diffraction_derivation():
    from diffraction_figures import build_pattern, build_wavefronts
    build_pattern()
    build_wavefronts()
    template = (ROOT / f'tools/{DIFFRACTION_DERIVATION}-template.html').read_text()
    with TemporaryDirectory(prefix='diffraction-') as directory:
        page = render_outline(f'{DIFFRACTION_DERIVATION}.md', template, Path(directory))
    figures = (
        ('DIFFRACTION_WAVEFRONTS_FIGURE', 'diffraction-wavefront-shapes', 1050, 800,
         'Calculated displacement snapshots for openings of 0.5λ and 5λ at the same spatial scale. '
         'The narrow opening gives curved crest arcs. The wide opening has nearly straight '
         'central crests and curved waves near its edges. Black lines mark crest phase.',
         'Spatial wavefronts, not an intensity-versus-angle graph. These scalar-wave model '
         'snapshots show the same wavelength; colours are normalized separately for visibility. '
         'The field calculation includes the near-opening region, where the far-field formula is not used.'),
        ('DIFFRACTION_PAIR_FIGURE', 'diffraction-pair-cancellation', 900, 620,
         'Contributions from points Q and Q prime separated by b/2 have projected path '
         'difference (b/2) sin θ. At the first minimum this is λ/2, so every pair cancels.',
         'Pair the two halves of one opening. The orange projection is the extra distance '
         'for one representative pair, not the full edge-to-edge path difference.'),
        ('DIFFRACTION_PATTERN_FIGURE', 'diffraction-width-pattern', 960, 580,
         'Normalized intensity versus angle for b/λ of 0.5, 1, and 5. The smaller ratios '
         'produce broader patterns. For b = 5λ, the first minimum is at about 11.5 degrees.',
         'Calculated ideal single-slit patterns: [sin β/β]² with β = π(b/λ) sin θ. '
         'Each curve is normalized to its own central intensity; absolute transmitted power is not compared.'),
    )
    for marker, slug, width, height, alt, caption in figures:
        data = base64.b64encode((ROOT / f'assets/wave-motion-notes/{slug}.svg').read_bytes()).decode()
        figure = (f'<figure><img src="data:image/svg+xml;base64,{data}" width="{width}" '
                  f'height="{height}" alt="{alt}"><figcaption>{caption}</figcaption></figure>')
        assert page.count(f'<p>{marker}</p>') == 1
        page = page.replace(f'<p>{marker}</p>', figure)
    for marker, section, title in (
        ('WAVEFRONT_SOURCE', '1-6-huygenss-principle', 'Huygens’s Principle'),
        ('MINIMUM_SOURCE', '4-1-single-slit-diffraction', 'Single-Slit Diffraction'),
        ('INTENSITY_SOURCE', '4-2-intensity-in-single-slit-diffraction', 'Intensity in Single-Slit Diffraction'),
    ):
        citation = (f'<p class="reference">Reference: <a href="https://openstax.org/books/'
                    f'university-physics-volume-3/pages/{section}">OpenStax · {title}</a>.</p>')
        assert page.count(f'<p>{marker}</p>') == 1
        page = page.replace(f'<p>{marker}</p>', citation)
    (ROOT / f'{DIFFRACTION_DERIVATION}.html').write_text(page)
    print(f'Built {DIFFRACTION_DERIVATION}.html: optional diffraction-width derivation.')


def embed_ripple_measurement_figures():
    """Keep the question visible and its solution diagram inside the hidden answer."""
    path = ROOT / 'wave-motion-notes.html'
    page = path.read_text()
    for kind, width, height, alt, caption in (
        ('question', 1000, 740,
         'Question: six consecutive bright crest lines numbered 1 to 6 span 0.200 m '
         'in the tank at 5.00 Hz. Find wavelength and speed, then predict wavelength '
         'at 10.0 Hz assuming unchanged speed and depth. The stated span is corrected '
         'for projection magnification.',
         'Illustrative question data. Count gaps between the six lines; the labelled '
         '0.200 m is the actual tank distance, not an uncorrected screen length.'),
        ('answer', 1000, 900,
         'Answer: six crests enclose five gaps, so wavelength is 0.200 divided by 5, '
         'or 0.0400 m. At 5.00 Hz the speed is 0.200 m/s. Assuming that speed at '
         '10.0 Hz gives wavelength 0.0200 m: eleven crests enclose ten gaps over '
         'the same 0.200 m tank span.',
         'Both patterns use the same horizontal scale and 0.200 m tank span. '
         'The 10.0 Hz pattern is a prediction under the constant-speed assumption.'),
    ):
        svg = ROOT / f'assets/wave-motion-notes/ripple-measurement-{kind}.svg'
        data = base64.b64encode(svg.read_bytes()).decode()
        marker = f'<p>RIPPLE_MEASUREMENT_{kind.upper()}_FIGURE</p>'
        assert page.count(marker) == 1
        figure = (f'<figure class="diagram ripple-measurement-{kind}">'
                  f'<img src="data:image/svg+xml;base64,{data}" width="{width}" height="{height}" '
                  f'alt="{escape(alt, quote=True)}" loading="lazy">'
                  f'<figcaption>{escape(caption)}</figcaption></figure>')
        page = page.replace(marker, figure)
    path.write_text(page)


def embed_reflection_station_figures():
    path = ROOT / 'wave-motion-notes.html'
    page = path.read_text()
    for kind, alt, caption in (
        ('question',
         'Three reflection tasks. A: circular incident fronts from source S approach '
         'a flat barrier; sketch reflected fronts and locate their apparent source. '
         'B: a ray approaches point P at 35 degrees to a dashed normal perpendicular '
         'to the flat barrier; draw the leaving ray and label its angle. '
         'C: straight fronts and parallel rays approach a parabolic barrier along '
         'its axis; trace their reflected paths near marked focus F.',
         'Top views for tasks A–C. Teal lines show incident crests and arrows show '
         'travel directions. Complete the reflected paths before opening the answer.'),
        ('answer',
         'A: orange reflected circular arcs appear to spread from virtual source S prime, '
         'the mirror image of S behind the flat barrier. B: the leaving ray is on the '
         'other side of the normal at 35 degrees to it, or 55 degrees to the barrier; '
         'crest lines are perpendicular to the rays. C: orange reflected rays from '
         'the parabolic barrier converge toward focus F.',
         'Orange shows reflected fronts or rays. The virtual source behind the flat '
         'barrier is a construction. All reflection angles are measured from the normal.'),
    ):
        data = base64.b64encode((ROOT / f'assets/wave-motion-notes/reflection-stations-{kind}.svg').read_bytes()).decode()
        marker = f'<p>REFLECTION_STATIONS_{kind.upper()}_FIGURE</p>'
        assert page.count(marker) == 1
        figure = (f'<figure class="diagram reflection-stations-{kind}">'
                  f'<img src="data:image/svg+xml;base64,{data}" width="1200" height="1140" '
                  f'alt="{escape(alt, quote=True)}" loading="lazy">'
                  f'<figcaption>{escape(caption)}</figcaption></figure>')
        page = page.replace(marker, figure)
    path.write_text(page)


def embed_refraction_depth_figure():
    """Preserve the supplied perspective image and clarify its angle annotation."""
    path = ROOT / 'wave-motion-notes.html'
    page = path.read_text()
    marker = '<p>REFRACTION_DEPTH_FIGURE</p>'
    assert page.count(marker) == 1
    data = base64.b64encode((ROOT / 'assets/wave-motion-notes/refraction-deep-shallow-user.png').read_bytes()).decode()
    alt = ('Perspective view of a ripple tank with deep water on the left and a raised '
           'block making shallow water on the right. The incoming teal ray bends toward '
           'the horizontal dashed normal as it enters the shallow region. The vertical '
           'dashed line marks the depth boundary. The supplied teal arc is drawn to '
           'the boundary rather than to the normal.')
    caption = ('The raised block makes the water shallower on the right. '
               'Horizontal dashed line: normal; vertical dashed line: depth boundary. '
               'Measure both ray angles from the horizontal normal. The teal arc in '
               'this supplied illustration is drawn to the boundary, so it does not '
               'show the angle of incidence. Ray directions and depths are schematic; '
               'use the top-view diagram above for the numerical angles.')
    figure = (f'<figure class="diagram refraction-depth-figure">'
              f'<img src="data:image/png;base64,{data}" width="1752" height="897" '
              f'alt="{escape(alt, quote=True)}" loading="lazy">'
              f'<figcaption>{escape(caption)}</figcaption></figure>')
    path.write_text(page.replace(marker, figure))


def link_derivations():
    # The outline generator renders inline Markdown links as plain text.
    # Resolve this page's authored link after building the shared notes layout.
    path = ROOT / 'wave-motion-notes.html'
    page = path.read_text()
    for slug, label in ((DERIVATION, DERIVATION_LABEL), (DOPPLER_DERIVATION, DOPPLER_LABEL),
                        (DIFFRACTION_DERIVATION, DIFFRACTION_LABEL),
                        (SINGING_GLASS, SINGING_GLASS_LABEL),
                        (RIPPLE_TANK, RIPPLE_TANK_LABEL)):
        marker = f'<p>Further reading: [{label}]({slug}.html).</p>'
        assert page.count(marker) == 1
        page = page.replace(marker, f'<p>Further reading: <a href="{slug}.html">{label}</a>.</p>')
    path.write_text(page)

REFERENCES = [
    ('173–174', 178), ('175', 180), ('175–176', 181), ('176, 179', 181),
    ('177–178, 197', 182), ('178, 180', 185), ('177, 189–190', 194),
    ('177, 190–191', 196), ('186, 191–192', 196), ('183–184, 192–193', 188),
    ('184–186', 189), ('187–188', 192),
]
# Coordinates are PDF points, with the origin at the upper left.
FIGURES = [
    (2, 'Reading a wave snapshot', 180, (180, 219, 555, 331),
     'Crests and troughs with a horizontal wavelength marker and a vertical amplitude marker.',
     'Figure 6.1.1 · Compare horizontal crest spacing with vertical displacement from equilibrium.'),
    (4, 'Compare the two directions', 181, (164, 483, 536, 632),
     'A spring carrying a sideways pulse above and a lengthwise compression pulse below.',
     'Figure 6.1.2 · Compare the motion of the coils with the travel direction of each pulse.'),
    (6, 'Reading the ripple tank', 183, (46, 435, 295, 702),
     'Side view of a ripple tank: a lamp above the water shines through its wavy surface and glass bottom. Crests concentrate light into bright lines on the screen below, while troughs spread the light out.',
     'Figure 6.1.4 · The projection is the light pattern on the white screen beneath the tank. Bright lines locate the water-wave crests.'),
    (6, 'Reading the ripple tank', 185, (61, 135, 398, 232),
     'A point source produces circular fronts, while a straight vibrating bar produces straight fronts.',
     'Figure 6.1.5 · Compare the wavefront shapes made by the two sources.'),
    (7, 'Investigation 6-2 · Stations 1–3', 194, (397, 403, 568, 526),
     'Top view of a wave tank with a generator and a tilted reflecting barrier.',
     'Figure 6.2.9 · Compare the incident and reflected wavefronts at the barrier.'),
    (8, 'Investigation 6-2 · Station 4', 196, (425, 82, 566, 208),
     'Top view of a ripple tank with an angled boundary between deep and shallow water.',
     'Figure 6.2.12 · Follow the straight wavefronts across the slanted boundary.'),
    (9, 'Investigation 6-2 · Station 5', 196, (304, 592, 566, 707),
     'Ripple-tank arrangements showing waves from a point source approaching an edge and a narrow doorway.',
     'Figure 6.2.13 · Look for waves spreading into the area behind the barriers.'),
    (10, 'Investigation 6-2 · Station 6', 197, (299, 510, 550, 677),
     'Two crests travel toward each other in the upper drawing. A crest and a trough approach in the lower drawing.',
     'Figure 6.2.14 · Compare the sum of the displacements in both cases.'),
    (11, 'From ripple patterns to light', 189, (168, 332, 417, 560),
     'A single slit illuminates a double slit. Circular fronts from the two slits overlap, producing bright and dark positions on a distant screen.',
     'Figure 6.2.3 · Both slits receive light from the same source.'),
    (12, 'Motion changes the rate of arrival', 192, (178, 282, 549, 532),
     'A moving vehicle has closely spaced wavefronts ahead and widely spaced wavefronts behind.',
     'Figure 6.2.6 · The spacing depends on the source’s position when each wavefront was emitted.'),
    (12, 'The sound barrier and the shock', 193, (46, 49, 544, 225),
     'Wavefronts crowd at the nose of a plane at the speed of sound. A faster plane produces a V-shaped shock in this two-dimensional view.',
     'Figure 6.2.7 · Compare the fronts at Mach 1 and above Mach 1.'),
]
HERO = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true">
<path d="M15 114H245M61 56H176M61 51V61M176 51V61" fill="none" stroke="#b8cfd2" stroke-width="2"/>
<path d="M32 114C46 67 75 67 90 114S134 161 148 114S192 67 206 114S234 156 244 136" fill="none" stroke="#086b72" stroke-width="4"/>
<path d="M176 80V114m-4-29 4-5 4 5m-8 24 4 5 4-5" fill="none" stroke="#087cff" stroke-width="2"/>
<text x="114" y="45" font-size="18" fill="#086b72">λ</text><text x="184" y="104" font-size="15" fill="#087cff">A</text>
</svg>'''

CHAPTER = Chapter(
    slug='wave-motion', title='Wave Motion', number=6, first_page=178, last_page=203,
    references=REFERENCES, figures=FIGURES, hero=HERO, search_hint='Try “wavelength” or “Doppler”',
    worked_answers=13, review_labels=['Wave types', 'Wave equation', 'Reflection', 'Refraction',
                                     'Diffraction', 'Interference', 'Doppler effect'],
    illustrations=((7, 'Flat and curved boundaries', 'assets/wave-motion-notes/reflection.svg',
                    'Top view of reflection at a flat barrier: incident and reflected rays each make 35° '
                    'with the dashed normal. Equally spaced wavefronts are perpendicular to the rays.',
                    'Arrows show travel directions; short lines show crests. '
                    'Both angles are measured from the normal, perpendicular to the barrier. '
                    'The reflected wave stays in the same medium, so its wavelength is unchanged.'),
                   (8, 'Across a boundary', 'assets/wave-motion-notes/refraction.svg',
                    'Top view of refraction from deep to shallow water: the incident ray at 45° '
                    'bends toward the normal to about 26°. Crest spacing drops from 4.0 to 2.5 cm '
                    'as speed drops from 0.20 to 0.125 m/s; frequency stays 5.0 Hz.',
                    'Lines show crests perpendicular to each ray; arrows '
                    'show travel. Measure wavelength perpendicular to the crests. The slower region '
                    'has closer crests and a smaller angle to the normal. Values match the example '
                    'below; the transmitted angle is rounded. Only the incident and transmitted waves are shown.'),
                   (9, 'Waves spread past edges', 'assets/wave-motion-notes/diffraction.svg',
                    'Top views of water waves travelling right through two openings: an opening about '
                    'one wavelength wide gives broad, nearly semicircular spreading; an opening five '
                    'wavelengths wide gives mostly straight fronts with curved edges.',
                    'Lines show crests, arrows show incoming travel, and dark bars form the barrier. '
                    'Opening width b is compared with the same wavelength λ in both panels. '
                    'These schematic transmitted wavefronts show wider spreading at the narrower gap. '
                    'Reflected waves are omitted; crest spacing stays unchanged in the same medium.'),
                   (10, 'Add signed displacements', 'assets/wave-motion-notes/interference.svg',
                    'Displacement versus position graphs at exact overlap: two upward pulses of '
                    'height A add to a pulse of height 2A; an upward and an equal downward pulse '
                    'add to zero at every position. All graphs use the same scales.',
                    'Each sum graph adds the signed displacements of '
                    'the two pulses at the same horizontal position. Zero is equilibrium; A is '
                    'the positive amplitude of each individual pulse. Complete cancellation lasts '
                    'only during exact overlap; ideal pulses continue afterward.')),
)

if __name__ == '__main__':
    from reflection_station_figures import build_reflection_station_figures
    build_reflection_station_figures()
    from build_ripple_tank_animation import build_ripple_tank_animation
    build_ripple_tank_animation()
    build_singing_glass()
    build_derivation()
    build_doppler_derivation()
    build_diffraction_derivation()
    build_study_pages(CHAPTER)
    embed_ripple_measurement_figures()
    embed_reflection_station_figures()
    embed_refraction_depth_figure()
    link_derivations()
