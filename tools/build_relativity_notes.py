#!/usr/bin/env python3
"""Build the Chapter 8 study notes and printable Quick Review."""
from bc_relativity_inventory import LIGHT_CLOCK, RIVER, VAN
from bc_study_pages import Chapter, build_study_pages

REFERENCES = [
    ('260–263', 265), ('262–265, 273', 269), ('265–267', 270),
    ('265–267', 271), ('267–269, 274–275', 272), ('268–269', 273),
    ('269–270, 275', 274), ('269, 276, 278', 274), ('265, 278', 283),
    ('271–273, 277', 276), ('271, 276–278', 276), ('274–278', 279),
]
FIGURES = [
    (1, 'Specify what velocity is relative to', RIVER[0], RIVER[1:],
     'The river and boat move left. Wind blows right. The bird flies left relative to the air. Each arrow is labelled with its own reference frame.',
     'Figure 8.1.1 · Read each arrow with its stated frame.'),
    (1, 'Specify what velocity is relative to', VAN[0], VAN[1:],
     'A roadside observer and a passenger in a van travelling to the right each toss a ball upward.',
     'Figure 8.1.4 · The van travels at 50 km/h relative to the road.'),
    (4, 'How a longer light path changes the measured time', 271, (162, 48, 566, 208),
     'Inside the ship, the path of light is vertical between the two mirrors.',
     'Figure 8.1.6 · The clock’s rest frame. Use a full round trip for one tick.'),
    (4, 'How a longer light path changes the measured time', LIGHT_CLOCK[0], LIGHT_CLOCK[1:],
     'In the outside frame, light follows a diagonal path because the spaceship moves between reflections.',
     'Figure 8.1.7 · The outside observer measures a longer light path at the same speed c.'),
]
HERO = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true">
<path d="M35 155H222M35 56V155" fill="none" stroke="#b8cfd2" stroke-width="2"/>
<path d="M43 152 124 65 207 152" fill="none" stroke="#087cff" stroke-width="3.5"/>
<path d="M43 152H207M124 65V152" fill="none" stroke="#086b72" stroke-width="2" stroke-dasharray="4 4"/>
<path d="M109 63H139M28 154H58M192 154H222" stroke="#086b72" stroke-width="4"/>
<text x="154" y="101" fill="#087cff" font-size="16">light</text>
<text x="79" y="180" fill="#086b72" font-size="15">ship moves →</text>
</svg>'''

CHAPTER = Chapter(
    slug='relativity', title='Special Relativity', number=8, first_page=264, last_page=283,
    references=REFERENCES, figures=FIGURES, hero=HERO, search_hint='Try “muon” or “proper time”',
    worked_answers=12, review_labels=['Frames', 'Time dilation', 'Length contraction',
                                     'Muons and trips', 'Velocity addition', 'Momentum', 'Energy'],
    sources=(
        ('https://www.gutenberg.org/files/70888/70888-h/70888-h.htm',
         'Michelson and Morley’s 1887 experiment, original paper'),
        ('https://www.fourmilab.ch/etexts/einstein/specrel/www/',
         'Einstein’s 1905 special relativity paper, English translation'),
    ),
)

if __name__ == '__main__':
    build_study_pages(CHAPTER)
