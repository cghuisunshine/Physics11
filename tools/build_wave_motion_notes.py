#!/usr/bin/env python3
"""Build the Wave Motion study notes and Quick Review."""
from bc_study_pages import Chapter, build_study_pages

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
)

if __name__ == '__main__':
    build_study_pages(CHAPTER)
