#!/usr/bin/env python3
"""Build Chapter 9 study notes and the printable Quick Review."""
from bc_nuclear_inventory import DECAY_SERIES
from bc_study_pages import Chapter, build_study_pages

REFERENCES = [
    ('279–281', 285), ('281–284', 287), ('285–287', 290), ('288–290', 294),
    ('288–290, 295', 293), ('292–293', 298), ('290–292', 296), ('294', 299),
    ('296–297', 301), ('297–298', 303), ('298–300, 305–306', 304), ('301, 305–306', 306),
]

# Bounds are in PDF points measured from the upper left.
FIGURES = [
    (2, 'Compare the three emissions', 287, (148, 48, 373, 165),
     'Alpha stops after a thin layer. Beta penetrates farther. Gamma passes into lead and is attenuated.',
     'Figure 9.1.1 · The sketch compares typical penetration. Actual attenuation depends on energy and material.'),
    (2, 'Magnetic separation', 287, (150, 516, 493, 705),
     'A beam passes between magnet poles. Alpha and beta tracks curve in opposite directions while gamma continues straight.',
     'Figure 9.1.2 · Use the charge signs to explain the opposite deflections.'),
    (3, 'What scattering revealed', 290, (166, 519, 553, 691),
     'An alpha source points toward a thin gold foil. A movable screen records particles scattered through different angles.',
     'Figure 9.1.4 · Large deflections reveal concentrated positive charge.'),
    (4, 'Read the upper and lower numbers', 294, (179, 98, 527, 210),
     'Hydrogen, deuterium, and tritium each have one proton. Their nuclei contain zero, one, and two neutrons respectively.',
     'Figure 9.1.6 · The three hydrogen isotopes differ in neutron number.'),
    (6, 'Follow the arrows', DECAY_SERIES[0], DECAY_SERIES[1:],
     'The decay chart connects uranium-238 to lead-206 through successive alpha and beta-minus steps.',
     'Figure 9.1.8 · The vertical axis is atomic number and the horizontal axis is mass number.'),
    (7, 'Halve the parent count repeatedly', 296, (190, 47, 541, 351),
     'A carbon-14 curve starts at 8000 atoms and halves the parent count approximately every 5700 years.',
     'Figure 9.1.7 · Each halving takes the same time, even as the number lost per interval decreases.'),
    (10, 'One fission event can start another', 303, (160, 54, 440, 315),
     'An incoming neutron excites a uranium-235 nucleus. In this illustrated channel the nucleus splits into barium and krypton and releases three neutrons.',
     'Figure 9.2.1 · The figure shows a different possible fragment pair from the worked example below.'),
    (11, 'Trace heat and steam separately', 304, (175, 543, 561, 700),
     'In the boiling-water reactor schematic, steam goes from the reactor vessel directly to the turbine.',
     'Figure 9.2.2 · BWR. Locate the steam outlet on the reactor vessel.'),
    (11, 'Trace heat and steam separately', 305, (160, 124, 540, 297),
     'In the pressurized-water reactor schematic, the primary loop transfers heat to a secondary steam loop.',
     'Figure 9.2.3 · PWR. Trace the primary loop and the separate turbine steam loop.'),
    (11, 'Trace heat and steam separately', 305, (159, 450, 558, 653),
     'The CANDU reactor schematic shows horizontal fuel channels in a moderator vessel and a separate steam circuit.',
     'Figure 9.2.4 · CANDU. Locate the horizontal fuel channels, steam generator, and condenser.'),
]
HERO = '''<svg class="hero-art" viewBox="0 0 260 210" aria-hidden="true">
<g fill="none" stroke="#9ebac0" stroke-width="2">
<circle cx="90" cy="105" r="34"/><circle cx="191" cy="61" r="24"/><circle cx="195" cy="151" r="21"/>
<path d="M30 105H53m-7-5 7 5-7 5M124 91l41-25m-9-1 9 1-4 8M124 119l45 27m-4-8 4 8-9 1"/>
</g>
<g fill="#086b72"><circle cx="80" cy="91" r="8"/><circle cx="100" cy="95" r="8"/><circle cx="88" cy="116" r="8"/>
<circle cx="186" cy="54" r="7"/><circle cx="196" cy="70" r="7"/><circle cx="191" cy="146" r="8"/></g>
<g fill="#318ac1"><circle cx="21" cy="105" r="6"/><circle cx="75" cy="110" r="7"/><circle cx="105" cy="113" r="7"/>
<circle cx="199" cy="54" r="6"/><circle cx="202" cy="155" r="6"/><circle cx="226" cy="39" r="5"/>
<circle cx="233" cy="112" r="5"/><circle cx="225" cy="174" r="5"/></g>
</svg>'''

CHAPTER = Chapter(
    slug='nuclear', title='Nuclear Fission and Fusion', number=9, first_page=284, last_page=311,
    references=REFERENCES, figures=FIGURES, hero=HERO, search_hint='Try “half-life” or “reactor”',
    worked_answers=12, review_labels=['Radiation', 'Isotopes', 'Nuclear equations',
                                     'Half-life', 'Energy and fission', 'Reactors', 'Fusion'],
    sources=(
        ('https://www.nobelprize.org/prizes/chemistry/1908/rutherford/lecture/',
         'Ernest Rutherford’s Nobel lecture on radioactive transformations'),
        ('https://www.nist.gov/news-events/news/2014/02/toward-new-precision-measuring-neutron-lifetime',
         'NIST on the free neutron’s lifetime and decay products'),
        ('https://www.nndc.bnl.gov/nudat3/', 'Brookhaven National Laboratory’s evaluated nuclear data'),
        ('https://www.nrc.gov/public-involve/conference-symposia/ric/past/2020/docs/posters/5_oversight_medical_radioisotpes.pdf',
         'U.S. Nuclear Regulatory Commission on the six-hour half-life of technetium-99m'),
        ('https://www.nrc.gov/cdn/legacy/reading-rm/training/reactor-concepts-training-course.pdf',
         'U.S. Nuclear Regulatory Commission on BWR and PWR designs'),
        ('https://www.cnsc-ccsn.gc.ca/eng/reactors/power-plants/nuclear-power-plant-safety-systems/',
         'Canadian Nuclear Safety Commission on CANDU heat transport and decay heat'),
        ('https://www.energy.gov/science/doe-explainsfusion-reactions',
         'U.S. Department of Energy on deuterium–tritium fusion'),
    ),
)

if __name__ == '__main__':
    build_study_pages(CHAPTER)
