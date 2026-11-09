"""Worked solutions to Chapter 9 questions, in textbook order."""
from bc_kinematics_answers import graph, paragraphs as p, parts, table

SUPERSCRIPT = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SUBSCRIPT = str.maketrans('-0123456789', '₋₀₁₂₃₄₅₆₇₈₉')


def nuclide(a, z, symbol):
    return f'{str(a).translate(SUPERSCRIPT)}{str(z).translate(SUBSCRIPT)}{symbol}'


HELIUM = nuclide(4, 2, 'He')
ELECTRON = nuclide(0, -1, 'e')
NEUTRON = nuclide(1, 0, 'n')
ANTINEUTRINO = 'ν̄ₑ'


def alpha(a, z, parent, daughter):
    return f'{nuclide(a, z, parent)} → {nuclide(a - 4, z - 2, daughter)} + {HELIUM}'


def beta(a, z, parent, daughter):
    return f'{nuclide(a, z, parent)} → {nuclide(a, z + 1, daughter)} + {ELECTRON} + {ANTINEUTRINO}'


RN_DECAY = alpha(226, 88, 'Ra', 'Rn')
LEAD_DECAY = beta(214, 82, 'Pb', 'Bi')
FUSION = f'{nuclide(2, 1, "H")} + {nuclide(3, 1, "H")} → {HELIUM} + {NEUTRON} + energy'

REACTOR_COMPARISON = table(
    ('Type', 'Where steam forms', 'Moderator and primary coolant'),
    [
        ('Boiling-water reactor (BWR)', 'Water boils in the reactor vessel. Its steam goes to the turbine.',
         'Ordinary water serves as coolant and moderator.'),
        ('Pressurized-water reactor (PWR)', 'Primary water stays liquid and transfers heat to a separate steam loop.',
         'Ordinary water serves as coolant and moderator.'),
        ('CANDU', 'Primary coolant carries heat to steam generators and a separate ordinary-water steam loop.',
         'Heavy water in the moderator vessel slows neutrons. Separate pressurized heavy water flows through the fuel channels.'),
    ],
)

TURBINE_LABELS = [
    ('Right, fan-shaped component', 'Steam turbine'),
    ('Far right, driven by the turbine shaft', 'Electrical generator'),
    ('Lower right, where steam gives up heat', 'Condenser, with its own cooling-water path'),
    ('Lower return pipe', 'Feedwater pump and return to the steam source'),
]

LAB_CURVE = graph(
    'Expected results for 100 fair dice, with one face removed per roll',
    [('Expected survivors', [(n, 100 * (5 / 6)**n) for n in range(13)], '#096a70')],
    xmax=12, ymin=0, ymax=100, xlabel='Number of rolls', ylabel='Undecayed dice',
    xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 25, 50, 75, 100], dots=True,
)

answer_groups = [
    # 9.1 warm-up and discovery
    [p('The three-bladed <strong>radiation trefoil</strong> warns of ionizing radiation or radioactive material. An ionization smoke detector can contain a small sealed source, typically americium-241.')],
    [
        p('Becquerel was testing whether a fluorescent uranium compound emitted penetrating radiation like X-rays. The wrapped photographic plate darkened even when the compound had been stored in the dark. The emission came from the material itself.'),
        p('<strong>Marie Curie</strong> introduced the term <em>radioactivity</em> for the spontaneous emission.'),
        p('<strong>Ernest Rutherford</strong> distinguished and named alpha and beta radiation by their different penetration. <strong>Paul Villard</strong> detected the third, more penetrating component later called gamma radiation. Experiments later established what each component was.'),
    ],
    # Magnetic deflection and the nature of the three components
    [
        p('For a beam crossing the field, positive alpha and negative beta-minus particles deflect in opposite directions. Gamma photons have zero charge and travel straight in the field. The radius of a charged track also depends on its momentum, charge, and field strength.'),
        p('<strong>Henri Becquerel</strong> used deflection measurements to determine the charge-to-mass ratio of beta particles. Its negative sign and magnitude matched those of electrons measured in cathode rays.'),
        p('<strong>Rutherford and Edward Andrade</strong> used crystal diffraction. The crystal produced a diffraction pattern, as it does for X-rays, supporting the interpretation of gamma radiation as short-wavelength electromagnetic radiation.'),
    ],
    # Transmutation and atomic structure
    [
        p('<strong>Natural transmutation</strong> is the spontaneous change of one element into another when a nucleus decays and its proton number changes. Alpha and beta-minus decay can do this. Gamma emission leaves the element unchanged.'),
        p('Rutherford pictured hydrogen as a very small, dense, positive nucleus containing a single proton, with one negative electron outside it. Most of the atom’s volume lies outside the nucleus. Modern models describe the electron with a quantum state.'),
        p('A <strong>proton</strong> is a positively charged constituent of a nucleus. The <strong>atomic number Z</strong> counts its protons and determines the element.'),
        p('A free neutron is unstable. It undergoes beta-minus decay: <strong>n → p + e⁻ + ν̄ₑ</strong>. Its mean lifetime is about 15 minutes. Nuclear binding can make a neutron stable within a stable nucleus.'),
    ],
    # Isotopes and equations
    [
        p('Isotopes are nuclei of the <strong>same element</strong> with the same proton number but different neutron numbers. They have different mass numbers and may differ in nuclear stability. Neutral atoms of the same element have the same number of electrons.'),
        p('A <strong>radioisotope</strong> is an isotope with an unstable nucleus that can decay spontaneously.'),
        p(f'{nuclide(238, 92, "U")} is uranium with <strong>92 protons</strong> and <strong>238 nucleons</strong>. It contains 238 − 92 = <strong>146 neutrons</strong>. A neutral atom has 92 electrons.'),
        parts(f'<strong>{RN_DECAY}.</strong> The printed radon subscript is 88. Radon has Z = 86, which balances the equation with the emitted alpha particle.',
              f'<strong>{LEAD_DECAY}.</strong> The missing charged particle is the beta-minus electron.',
              f'<strong>{alpha(218, 84, "Po", "Pb")}.</strong> The daughter is lead-214.',
              f'<strong>{beta(210, 83, "Bi", "Po")}.</strong> The daughter is polonium-210.'),
    ],
    # Half-life sample and practice
    [p('Use the textbook half-life of 8.1 days. Since 1/16 = (1/2)⁴, four half-lives are needed. t = 4 × 8.1 = <strong>32.4 days</strong>, about 32 days to two significant figures. Iodine has atomic number <strong>53</strong>. The printed 63 should read 53.')],
    [
        p('144 d/24 d = 6 half-lives. The expected parent count is 4000(1/2)⁶ = 62.5, or <strong>about 63 thorium-234 atoms</strong>. An actual small sample can give a different count.'),
        p('1/32 = (1/2)⁵. Five half-lives take 26 years, so T½ = 26/5 = <strong>5.2 years</strong>.'),
    ],
    # Reading the decay series
    [
        p(f'<strong>{RN_DECAY}.</strong> Mass number drops by four and atomic number drops by two.'),
        p(f'<strong>{LEAD_DECAY}.</strong> Mass number stays 214 and atomic number increases from 82 to 83.'),
        p('The chart contains <strong>8 elements</strong> (U, Th, Pa, Ra, Rn, Po, Pb, and Bi) and <strong>15 distinct nuclides</strong>, counting uranium-238 at the start and stable lead-206 at the end. Follow the 14 arrows and count both endpoints.'),
    ],
    # Investigation 9-1
    [p('Take half the combined initial count and read where the class curve crosses that level. Record the number of rolls, interpolating between adjacent points if useful. The observed value depends on the class data. For fair dice the expected fraction after n rolls is (5/6)ⁿ, so the model half-life is ln(1/2)/ln(5/6) ≈ <strong>3.8 rolls</strong>.') + LAB_CURVE],
    # 9.1 Review
    [
        p('Becquerel’s radiation was invisible, passed through paper that blocked visible light, fogged photographic plates, and ionized air. The emission persisted without prior exposure to light. Different components later showed different penetration.'),
        p('Transmutation showed that radioactivity could change the identity of an element. A change in proton number comes from a <strong>nuclear process</strong>. The finding helped explain the appearance of daughter substances in a decaying sample.'),
        p('<strong>James Chadwick</strong> studied the neutral radiation produced when alpha particles struck beryllium. It knocked protons out of hydrogen-rich material such as paraffin. Recoil measurements supported a neutral particle with a mass close to that of the proton.'),
        p('The alpha particle is thousands of times more massive than an electron. An electron can give it only a small deflection. The observed large-angle scattering is explained by close approaches to a concentrated positive nucleus.'),
        p('A <strong>half-life</strong> is the time for the expected number of undecayed parent nuclei to fall to half its initial value. The activity of that parent isotope also halves if no additional parent nuclei are supplied.'),
        parts(f'<strong>{beta(14, 6, "C", "N")}.</strong> Nitrogen-14 has Z = 7. The electron must have charge number −1 to balance 6 = 7 − 1. The source shows a positive subscript.',
              f'<strong>{RN_DECAY}.</strong> The missing particle is {HELIUM}.',
              f'<strong>{alpha(225, 89, "Ac", "Fr")}.</strong> The parent has A = 225 and Z = 89.',
              f'<strong>{beta(209, 82, "Pb", "Bi")}.</strong> The parent is lead-209 and the emitted charged particle is a beta-minus electron.'),
        p('The fraction of parent carbon-14 left is (1/2)⁵ = 1/32. 4000 g/32 = <strong>125 g of carbon-14</strong>. The remaining material can include decay products.'),
    ],
    # 9.2 warm-up and review
    [p('<strong>Fission</strong> splits a heavy nucleus into lighter fragments. <strong>Fusion</strong> joins light nuclei to make a heavier nucleus. Both can release energy when the total product rest mass is lower.')],
    [
        parts('Cockcroft and Walton used accelerated protons to induce a reaction in lithium-7. The products were two helium-4 nuclei.',
              'The products had lower total rest mass. The mass difference released energy according to Q = (m(initial) − m(final))c², mostly as kinetic energy of the helium nuclei in this reaction.'),
        parts('Fission is the splitting of a heavy nucleus into lighter fragments, often after neutron absorption.',
              'It releases a large amount of energy, mainly first as kinetic energy of the fragments. Additional neutrons can also be emitted.',
              'Some emitted neutrons can cause further uranium-235 fissions, so the reaction can sustain itself.'),
        p('A uranium-235 fission generally emits several neutrons. If, on average, one causes another fission, the chain reaction is self-sustaining at steady power. The other neutrons can escape or be absorbed without producing fission.'),
        REACTOR_COMPARISON,
        table(('Benefits', 'Trade-offs'), [
            ('High energy yield from a relatively small amount of fuel. Low direct greenhouse-gas emissions during electricity generation.',
             'Used fuel and other radioactive waste require isolation and long-term management.'),
            ('Steady electricity generation while the plant is operating.',
             'Construction and decommissioning require substantial resources. Safety and cooling systems need continuing oversight.'),
        ]),
        p('The reactor controls the chain reaction by regulating how many neutrons produce new fissions. Neutron absorbers and independent shutdown systems can reduce that number. Coolant removes heat, including decay heat after shutdown, and containment helps limit releases. A conventional reactor is designed for controlled, steady operation.'),
    ],
    # Chapter review
    [
        p('Becquerel placed a uranium compound near a light-shielded photographic plate while studying fluorescence. The plate was exposed even when the compound had been kept in the dark. The observation revealed spontaneous radiation from the compound.'),
        p('Rutherford’s model placed positive charge and most of the mass in a tiny <strong>nucleus</strong>. Most of the atom’s volume was outside the nucleus. The negative electrons occupied the surrounding region.'),
        p('Early researchers observed effects such as skin burns as they worked with radioactive sources, but dose measurement and knowledge of long-term health effects were limited. Radiation protection developed as these effects became better understood.'),
        p('In this chapter a <strong>beta particle</strong> is a beta-minus electron, with negative charge and nonzero rest mass. A <strong>gamma ray</strong> is a photon emitted by the nucleus. It has zero charge and zero rest mass.'),
        p(f'{ELECTRON} is an <strong>electron</strong>, written this way when it is emitted in beta-minus decay. Its mass number is zero because it contains no nucleons. The lower −1 is its charge number.'),
        p('Both isotopes have 92 protons. Uranium-235 has 235 − 92 = <strong>143 neutrons</strong>, while uranium-238 has 238 − 92 = <strong>146 neutrons</strong>. Their mass numbers and nuclear properties differ.'),
        parts(f'<strong>{alpha(238, 92, "U", "Th")}.</strong>',
              f'<strong>{beta(234, 90, "Th", "Pa")}.</strong>'),
        p('The half-life is the time for the number of undecayed parent nuclei, or their activity, to fall to half its starting value. Repeat the halving for each additional half-life.'),
        p('52 years ÷ 5.2 years = 10 half-lives. Expected Co-60 left = 10⁶(1/2)¹⁰ ≈ <strong>977 atoms</strong>. About 999,023 of the original atoms have decayed, mainly to nickel-60.'),
        p('For the textbook example, choose a <strong>relatively short physical half-life</strong> that still allows preparation and enough time to record the scan. It gives a measurable signal during imaging and leaves less lingering activity afterward. The actual choice also depends on how the tracer behaves in the body.'),
        parts(f'<strong>{alpha(230, 90, "Th", "Ra")}.</strong> The missing daughter is radium-226.',
              f'<strong>{beta(234, 90, "Th", "Pa")}.</strong> The missing charged particle is a beta-minus electron.',
              f'<strong>{beta(14, 6, "C", "N")}.</strong> The missing daughter is nitrogen-14.',
              f'<strong>{alpha(218, 84, "Po", "Pb")}.</strong> The missing particle is an alpha particle.'),
        p('<strong>Fuel</strong> contains nuclei that undergo fission. A <strong>moderator</strong> slows neutrons in a thermal reactor. <strong>Control and shutdown absorbers</strong> capture neutrons. <strong>Coolant</strong> carries away heat. <strong>Shielding and containment</strong> limit radiation exposure and releases. In a power station, steam drives a <strong>turbine and generator</strong>, and a condenser returns the steam to water.'),
        p('The horizontal fuel channels identify a <strong>CANDU pressurized-heavy-water reactor</strong>. Its reactor coolant and turbine steam follow separate paths.') +
        table(('Location in the diagram', 'Label'), [
            ('Lower left, horizontal tubes in the core', 'Fuel channels in the moderator vessel'),
            ('Left loop between the core and upper vessel', 'Pressurized heavy-water coolant and its circulation pump'),
            ('Upper left, heated vessel above the core', 'Steam generator and steam outlet'),
            *TURBINE_LABELS,
        ]),
        p(f'<strong>Fusion</strong> joins light nuclei and can release energy. Example: <strong>{FUSION}</strong>. Deuterium and tritium are isotopes of hydrogen.'),
        p('Positive nuclei repel one another electrically. A fusion system must bring them close enough for the nuclear force to bind them. It needs a very hot plasma and enough density and confinement time for useful numbers of collisions, while limiting energy losses and handling the reaction products.'),
        p('Fusion could use abundant deuterium and would avoid a self-sustaining fission chain reaction. D–T fusion still requires tritium management and produces neutrons that can activate materials. Practical energy generation depends on meeting confinement, materials, maintenance, and energy-balance requirements.'),
        p('Light nuclei such as hydrogen isotopes can fuse and release energy. They need sufficient relative energy to approach despite electric repulsion, plus enough density and confinement time for a useful reaction rate. In stars, gravity provides confinement.'),
    ],
    # Extra practice
    [
        p('Absorber tests showed components with different penetrating abilities. A transverse field also separated the positive and negative components while a neutral component continued straight. These observations distinguished alpha, beta, and gamma radiation.'),
        p('The residual <strong>strong nuclear force</strong> binds nearby nucleons and can overcome proton–proton electric repulsion at nuclear distances. It acts over roughly <strong>a few femtometres</strong>, of order 10⁻¹⁵ m, and falls off rapidly beyond that range.'),
        p('An alpha particle is a <strong>helium-4 nucleus</strong> with two protons, two neutrons, and charge +2e.'),
        p(f'{HELIUM} denotes helium-4. Its upper 4 is the mass number and its lower 2 is the proton number. In a nuclear equation it can represent the emitted alpha particle.'),
        p('Rutherford received the <strong>1908 Nobel Prize in Chemistry</strong> for studying how elements disintegrate and investigating the chemistry of radioactive substances, including transformations between elements.'),
        parts('The curve reaches 50% at about <strong>20 million years</strong>.',
              'Three half-lives take about <strong>60 million years</strong>.',
              '80 million years ÷ 20 million years per half-life = <strong>4 half-lives</strong>. About 6.25% remains in the model.'),
        p('Using the problem’s stated 6.0 h, 24 h is four half-lives. The expected count is 64(1/2)⁴ = <strong>4 atoms</strong>. The isotope label in the textbook is inconsistent with evaluated decay data. The approximately six-hour half-life belongs to <strong>technetium-99m</strong>.'),
        parts(f'<strong>{alpha(222, 86, "Rn", "Po")}.</strong> The missing daughter is polonium-218.',
              f'<strong>{beta(210, 82, "Pb", "Bi")}.</strong> The missing charged particle is a beta-minus electron.',
              f'<strong>{beta(210, 83, "Bi", "Po")}.</strong> The missing daughter is polonium-210.'),
        p('This is a <strong>pressurized-water reactor (PWR)</strong>. The left reactor vessel and neighbouring steam generator are joined by the primary water circuit. The steam circuit is separate.') +
        table(('Location in the diagram', 'Label'), [
            ('Tall vessel on the left', 'Reactor vessel with fuel, moderator/coolant, and control rods'),
            ('Tall vessel to its right', 'Steam generator, where primary heat boils secondary water'),
            ('Upper line from that vessel to the turbine', 'Secondary steam line'),
            *TURBINE_LABELS,
        ]),
        p('This is a <strong>boiling-water reactor (BWR)</strong>. Steam produced in the reactor vessel goes directly to the turbine.') +
        table(('Location in the diagram', 'Label'), [
            ('Tall vessel on the left', 'Reactor vessel with fuel, moderator/coolant, and control rods'),
            ('Upper line from the vessel to the turbine', 'Steam line directly from the reactor vessel'),
            *TURBINE_LABELS,
        ]),
        p('A uranium-235 nucleus can absorb a neutron and form an excited uranium-236 nucleus. It can then split into two lighter fragments and release energy plus additional neutrons. The fragments transfer kinetic energy to their surroundings as heat. The released neutrons can cause further fissions.'),
        p('Fission splits a heavy nucleus into lighter ones. Fusion joins light nuclei. Either can release energy if the final products have less total rest mass.'),
        parts('Uranium-238 can capture a slow neutron to form <strong>uranium-239</strong>. Slow-neutron capture usually does not cause U-238 to fission.',
              'Uranium-235 can absorb a slow neutron and undergo <strong>fission</strong>, releasing energy, lighter fragments, and more neutrons. Some captures can occur without fission.'),
        p('<strong>Critical mass</strong> is the amount of fissile material needed for a self-sustaining chain reaction under specified conditions. In a nuclear weapon, the fission stage is brought from a subcritical state to a rapidly supercritical state, so successive neutron generations grow very quickly.'),
        p('A thermonuclear weapon uses energy from a fission stage to create the extreme conditions for light nuclei to fuse. The high temperature lets some nuclei approach closely enough to react.'),
        p('Fusion could provide useful energy from light nuclei, including deuterium. It offers a high energy yield per mass of fuel. A practical system must sustain the plasma and capture enough of the released energy while coping with losses and material damage.'),
        parts('Most stars consist mainly of <strong>hydrogen and helium</strong>.',
              '<strong>Nuclear fusion</strong> powers stars. For much of a star’s life, fusion converts hydrogen into helium.'),
    ],
]
