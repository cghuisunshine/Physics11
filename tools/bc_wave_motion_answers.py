"""Worked solutions in the order of the Chapter 6 source sets."""
from html import escape
from bc_kinematics_answers import paragraphs as p, parts


def sketch(label, paths, extras='', view='0 0 390 125'):
    return (
        f'<figure class="answer-graph"><svg viewBox="{view}" role="img" '
        f'aria-label="{escape(label, quote=True)}">'
        f'<path d="{paths}" fill="none" stroke="#096a70" stroke-width="2"/>'
        f'{extras}</svg><figcaption>{escape(label)}</figcaption></figure>'
    )


def pulses(destructive):
    lower = 'M235 66H275Q285 66 293 47T313 47Q322 66 332 66H365'
    if destructive:
        lower = 'M235 66H275Q285 66 293 85T313 85Q322 66 332 66H365'
    label = ('An upward pulse meets an equal downward pulse. Their displacements cancel during exact overlap.'
             if destructive else 'Two identical upward pulses meet. At exact overlap their height doubles.')
    return sketch(label, 'M25 66H65Q75 66 83 47T103 47Q112 66 122 66H155 ' + lower,
                  '<text x="75" y="106">→</text><text x="286" y="106">←</text>')


wave_labels = sketch(
    'A crest is a maximum, a trough is a minimum, λ spans successive crests, and A spans equilibrium to a crest.',
    'M20 64Q40 7 60 64T100 64T140 64T180 64T220 64T260 64 '
    'M40 23H120M37 23l6 -3m-6 3 6 3M123 23l-6 -3m6 3 -6 3M120 36V64',
    '<path d="M20 64H260" stroke="#75868d" stroke-dasharray="4 3"/>'
    '<text x="74" y="18">λ</text><text x="127" y="54">A</text>'
    '<text x="30" y="113">crest at top · trough at bottom</text>',
    '0 0 290 125',
)

diffracted_fronts = sketch(
    'Plane fronts reach a narrow gap and emerge as spreading arcs.',
    'M35 18V107M61 18V107M87 18V107M136 44a18 18 0 0 1 0 36'
    'M136 26a36 36 0 0 1 0 72M136 10a52 52 0 0 1 0 104',
    '<path d="M136 5V56M136 69V120" stroke="#2b3940" stroke-width="5"/>',
    '0 0 224 125',
)


answer_groups = [
    # Vibrating glass warm-up
    [
        p('Adding water generally <strong>lowers the pitch</strong> of a rubbed glass. The moving water adds inertia to the vibration, so the resonant frequency decreases. Compare the same glass at different fill levels.'),
        p('<strong>Yes.</strong> A damp finger rubbing the rim can excite the glass itself. The vibrating glass sends sound waves through the air even when the glass is empty.'),
    ],
    # Frequency and period quick check
    [
        parts('f = N/Δt = 50.0/40.0 = <strong>1.25 Hz</strong>.', 'T = 1/f = 1/1.25 = <strong>0.800 s</strong>.'),
        parts('f = 7680/30 = <strong>256 Hz</strong>.', 'T = 1/256 = <strong>3.91 × 10⁻³ s</strong>.'),
        p('One complete back-and-forth cycle takes 4.0 s. f = 1/T = 1/4.0 = <strong>0.25 Hz</strong>.'),
    ],
    # Sample and practice 6.1.1
    [p('v = fλ = (256 Hz)(1.29 m) = 330.24 m/s ≈ <strong>330 m/s</strong>.')],
    [
        parts('At fixed speed, λ = v/f. Doubling f <strong>halves λ</strong>.', 'Halving f <strong>doubles λ</strong>.'),
        p('f = v/λ = (340 m/s)/(1.70 m) = <strong>200 Hz</strong>.'),
        p('λ = v/f = (3.0 m/s)/(2.0 Hz) = <strong>1.5 m</strong>.'),
    ],
    # Investigation 6-1A
    [
        p('Use your travel times over a known length. Compute v = distance/time for each spring and compare. Transverse speed increases with tension and decreases with mass per stretched metre. Diameter alone does not determine which spring is faster.'),
        p('Compare the travel times of a compression pulse over the same distance, or calculate distance/time for each spring. Longitudinal speed depends on the spring’s effective stiffness and inertia. Use your observations to rank the two springs.'),
        p('For small pulses at the same tension and stretch, speed is <strong>approximately independent of amplitude</strong>. Compare travel times. A very large pulse can alter the stretch and tension.'),
        p('<strong>Greater tension generally gives a faster transverse pulse.</strong> For an ideal stretched string, v = √(F/μ), where μ is the mass per unit length. Stretching the spring may change μ as well as the tension.'),
        p('The <strong>disturbance propagates</strong>. Each coil moves temporarily about its equilibrium position as the pulse passes. Track one marked coil to separate local motion from pulse motion.'),
        p('At a fixed end the transverse pulse <strong>inverts</strong>. A crest returns as a trough. At the boundary, the incoming and reflected displacements sum to zero.'),
    ],
    # Investigation 6-1B
    [
        p('In still water of uniform depth, a point pulse spreads at the same speed in every direction. A <strong>circular front</strong> stays centred on the source, so its radius is the same in every direction at a given time.'),
        p('Increasing f usually <strong>reduces the wavelength</strong> in this tank. Compare crest spacing for the same depth. The relation is λ = v/f. Exact inverse proportionality assumes the speed stays constant.'),
    ],
    # 6.1 Review
    [
        p('A <strong>disturbance</strong> starts a wave. A single disturbance can launch a pulse. Repeated vibrations of the source generate a periodic wave.'),
        p('The intended comparison is a <strong>single pulse</strong>, which has no repetition frequency and no periodic wavelength. A pulse does have an amplitude. A displacement amplitude of zero everywhere means there is no disturbance.'),
        p('107.3 MHz = <strong>1.073 × 10⁸ Hz</strong>, or 107.3 million oscillations per second.'),
        p('T = 1/f = 1/(25 Hz) = <strong>0.040 s</strong>.'),
        p('f = 1/T = 1/(2.0 s) = <strong>0.50 Hz</strong>.'),
        p('If 8 m describes the full trough-to-crest height, the amplitude is approximately <strong>4 m</strong>. Amplitude is measured from equilibrium to a crest or trough.'),
        p('One revolution takes 60 s. f = 1/60 s = <strong>0.0167 Hz</strong>.'),
        p('One revolution takes 12 h = 43 200 s. f = 1/43 200 s = <strong>2.31 × 10⁻⁵ Hz</strong>.'),
        p('T = 1/f. Tripling the frequency makes the period <strong>one-third</strong> of its original value.'),
        p('f = v/λ = (25 cm/s)/(2.5 cm) = <strong>10 Hz</strong>. The centimetres cancel.'),
        p('λ = c/f = (3.0 × 10⁸)/(3.0 × 10¹⁰) = <strong>1.0 × 10⁻² m = 1.0 cm</strong>.'),
        p('Successive crests arrive 6 s apart, so T = 6 s. v = λ/T ≈ 12/6 = <strong>2 m/s</strong>.'),
    ],
    # Overlapping ripples warm-up
    [p('Draw concentric crests around each splash. Mark X at intersections of two crest circles, where the upward displacements add. For simultaneous identical splashes, locations equally distant from both sources receive matching parts of the two ripples at the same time.') +
     sketch('Two expanding crest circles overlap. X marks a crest meeting a crest.',
            'M185 61a55 55 0 1 0 -110 0a55 55 0 1 0 110 0 M245 61a55 55 0 1 0 -110 0a55 55 0 1 0 110 0',
            '<circle cx="130" cy="61" r="3"/><circle cx="190" cy="61" r="3"/>'
            '<text x="156" y="20">X</text><text x="156" y="113">X</text>', '0 0 320 125')],
    # Investigation 6-2, stations 1–6
    [p('A rigid, lossless barrier that transmits no energy can reflect all incident energy in an ideal model. A real barrier can absorb, transmit, or scatter some energy, and a finite barrier lets waves pass around its ends. Reflected circular fronts appear to come from the mirror-image source behind a flat barrier.')],
    [
        p('<strong>θᵢ = θᵣ.</strong> Measure both ray angles from the normal. The angles between the wavefronts and the barrier are equal as well.'),
        p('The reflected waves remain in the same water at the same depth. Their <strong>speed, frequency, and wavelength stay the same</strong> in the ideal model. Amplitude can decrease.'),
    ],
    [
        p('Plane waves arriving along the axis reflect and <strong>converge toward the focus</strong>. A parabolic reflector can concentrate wave energy near that point.'),
        p('Waves spreading from the focus leave the ideal reflector as <strong>approximately straight, parallel wavefronts</strong> travelling along the axis. This reverses the focusing process.'),
    ],
    [
        p('In the ripple-tank model the waves <strong>slow down</strong> in shallower water, as shown by closer crest spacing at the same frequency.'),
        p('Use v = fλ and constant f. The ratio <strong>v(shallow)/v(deep) = λ(shallow)/λ(deep)</strong>. Measure several crest spacings in each region and divide by the number of intervals before taking the ratio.'),
        p('The generator fixes the number of crests per second. At a stationary boundary each incident cycle drives one transmitted cycle, so the frequency stays constant.'),
        p('If the fronts are parallel to the boundary, the direction of travel is along the normal. The waves <strong>continue straight</strong> while slowing and shortening their wavelength.'),
        p('At oblique incidence the ray <strong>bends toward the normal</strong> as it enters slower, shallow water. The refraction angle is smaller than the incidence angle. Equivalently, the transmitted crests make a smaller angle to the boundary.'),
        p('On returning to faster deep water, the ray <strong>bends away from the normal</strong>. If the two boundaries are parallel and the outer depths match, the final ray is parallel to the original. The exit refraction angle then equals the original incidence angle.'),
    ],
    [
        p('For a fixed gap or obstacle, diffraction is more noticeable with <strong>longer wavelengths</strong>. Compare wavelength with the size of the feature.'),
        p('For fixed wavelength, <strong>smaller openings</strong> give broader spreading when the opening is comparable to or smaller than λ. A very small opening can transmit less energy.'),
        p('Draw nearly <strong>semicircular wavefronts centred on the opening</strong>. The gap acts roughly like a point source when it is narrow compared with the wavelength.') +
        diffracted_fronts,
        parts('If the obstacle is very small relative to λ, the wave wraps around it with little persistent shadow.',
              'If its width is comparable to λ, the fronts curve appreciably around both edges.',
              'If the obstacle is much larger than λ, a clear shadow forms behind it, with some spreading at the edges.'),
        p('Examples include <strong>hearing someone around a corner</strong>, seeing ripples spread around a pier, and seeing a starburst when viewing a streetlight through fine mesh.'),
    ],
    [
        p('The displacements add. Equal crests of height A give a combined crest of <strong>2A</strong> during exact overlap.') + pulses(False),
        p('Equal and opposite displacements add to <strong>zero</strong> where they coincide. The original pulses continue after they pass through each other.') + pulses(True),
    ],
    [
        p('For equal amplitudes, a crest and trough cancel. The screen loses the alternating bright/dark crest pattern there, leaving a relatively steady region or <strong>nodal line</strong>.'),
        p('Crests add to crests, and troughs add to troughs. The displacement is larger and the projected pattern shows stronger variation at this <strong>maximum</strong>.'),
        p('The second distance must be a <strong>half-integer multiple of λ</strong>, such as (n ± ½)λ. In general the absolute path difference is (m + ½)λ for m = 0, 1, 2, …. Several distances are possible if the geometry allows them.'),
        p('The second distance can be <strong>any integer multiple of λ</strong> allowed by the geometry, including mλ itself. The path difference must be an integer multiple of λ, including zero.'),
    ],
    # 6.2 Review
    [
        p('<strong>Reflection.</strong> Put a virtual source the same distance behind the barrier as the real source is in front. Draw reflected circular arcs on the incident side of the barrier, centred on that virtual source.') +
        sketch('Solid arcs show reflected fronts. Their centre is the virtual source behind the barrier.',
               'M175 42A57 57 0 0 0 175 83M175 24A75 75 0 0 0 175 101M175 8A91 91 0 0 0 175 117',
               '<path d="M175 6V119" stroke="#2b3940" stroke-width="4"/>'
               '<circle cx="138" cy="63" r="3"/><text x="76" y="57">source</text>'
               '<circle cx="212" cy="63" r="3"/><text x="222" y="67">virtual source</text>'),
        p('<strong>Diffraction.</strong> Leave the straight incident fronts on the left. Draw spreading semicircular fronts centred on the narrow gap on the right.') +
        diffracted_fronts,
        p('<strong>Diffraction.</strong> The closely spaced threads act like a two-dimensional grating, spreading light into directions that can produce the starburst pattern.'),
        parts('<strong>Refraction</strong> at each boundary.', 'In shallow water the crest spacing is smaller, so λ and v decrease at fixed f. The fronts turn. At the parallel exit boundary they turn back to their original orientation if the two deep-water speeds are equal.'),
        parts('No. Like-signed equal pulses add.', 'No. The pulses have the same sign and unequal amplitudes.',
              '<strong>Yes.</strong> Mark the midpoint where the centres meet. Equal and opposite profiles sum to zero at exact overlap.',
              'No. Opposite signs alone are insufficient because the amplitudes differ.',
              'No. The two lobes arrive in opposite spatial order, so the profiles cannot cancel everywhere simultaneously.',
              '<strong>Yes.</strong> Mark the overlap location. The tall crest aligns with the deep trough and the shorter crest aligns with the shallower trough.'),
        p('<strong>All three</strong> can interfere. Sound pressure, the electric field of light, and water-surface displacement can each superpose.'),
        p('<strong>All three</strong> can exhibit a Doppler shift in measured frequency when source and observer move relative to each other along the line of travel. For waves in a medium, source and observer motion are measured relative to the medium.'),
        p('<strong>Yes.</strong> Moving toward a stationary source makes you encounter the wavefronts more often. Moving away makes you encounter them less often.'),
        p('The aircraft was <strong>supersonic</strong> when it generated the shock that reached you. The shock travels outward and can reach the ground after the aircraft has passed.'),
        p('The <strong>sound barrier</strong> refers to the aerodynamic effects near Mach 1, including compression and shock formation. A <strong>sonic boom</strong> is the sound heard when a shock from supersonic motion passes an observer.'),
        pulses(True),
    ],
    # Chapter 6 Review (the source skips 10)
    [
        p('A <strong>pulse</strong> is a single travelling disturbance. A <strong>periodic wave</strong> repeats regularly in time because the source repeats its motion.'),
        parts('A crest is a point of maximum upward displacement.', 'A trough is a point of maximum downward displacement.',
              'Wavelength is the distance between successive points at the same phase, such as crest to crest.',
              'Frequency is the number of complete oscillations per second at a point.',
              'Amplitude is the maximum displacement from equilibrium.') + wave_labels,
        p('<strong>1 Hz = one cycle per second = 1 s⁻¹</strong>.'),
        p('Frequency and period are reciprocals. <strong>f = 1/T</strong> and <strong>T = 1/f</strong>.'),
        parts('f = 50/20 = <strong>2.5 Hz</strong>.', 'T = 1/2.5 = <strong>0.40 s</strong>.'),
        p('For a <strong>transverse</strong> wave, the oscillation is perpendicular to the wave’s travel direction. For a <strong>longitudinal</strong> wave, it is parallel.'),
        p('<strong>v = fλ</strong>. A crest travels one wavelength in one period, so v = λ/T.'),
        p('λ = c/f = (3.0 × 10⁸)/60 = <strong>5.0 × 10⁶ m</strong>, or about 5000 km.'),
        p('λ = v/f = 330/512 ≈ <strong>0.645 m</strong> (about 0.64 m).'),
        p('<strong>Refraction</strong> is a change in direction as wave speed changes, as when an oblique light ray enters water. <strong>Diffraction</strong> is spreading around edges or through an opening, as when you hear a voice around a corner.'),
        parts('The wavelength decreases because λ = v/f.', 'The frequency stays the same at a stationary boundary.',
              'At oblique incidence the slower wave bends toward the normal.', 'At normal incidence the propagation direction is unchanged.'),
        parts('Constructive interference occurs when displacements reinforce, such as two crests meeting.',
              'Destructive interference occurs when opposite displacements reduce the sum. Equal and opposite displacements cancel completely.'),
        p('For two coherent, in-phase sources of equal amplitude, a <strong>nodal line</strong> forms where the path difference is (m + ½)λ. A <strong>maximum</strong> occurs where the difference is mλ, including zero. Here m is a nonnegative integer.'),
        p('The first mirror sends radiation from its focus into a nearly parallel beam. The facing mirror collects that beam and concentrates it at its focus, where the match absorbs energy.') +
        sketch('Radiation from the left focus reflects into a parallel beam, then converges at the right focus.',
               'M103 62L48 24H342L287 62L342 100H48L103 62 M189 20l8 4 -8 4M189 96l8 4 -8 4',
               '<path d="M54 9Q30 62 54 115M336 9Q360 62 336 115" fill="none" stroke="#263b40" stroke-width="3"/>'
               '<circle cx="103" cy="62" r="4"/><circle cx="287" cy="62" r="4"/>'
               '<text x="89" y="82">source</text><text x="271" y="82">match</text>'),
        p('v = fλ = (2.2 × 10⁶)(5.10 × 10⁻⁴) = 1122 m/s. The pulse travels down and back, so depth = vΔt/2 = (1122)(8.0)/2 ≈ <strong>4.5 × 10³ m</strong>, measured below the submarine.'),
    ],
    # Extra practice
    [
        p('Label a highest point <strong>crest</strong> and a lowest point <strong>trough</strong>. Mark amplitude vertically from the midline to a crest. Mark wavelength horizontally between adjacent crests or adjacent troughs.') + wave_labels,
        p('A is half the trough-to-crest height. A = 4.2/2 = <strong>2.1 m</strong>.'),
        p('λ = v/f = (3.4 × 10²)/256 ≈ <strong>1.3 m</strong>.'),
        p('610 nm = 6.10 × 10⁻⁷ m. f = c/λ = (3.00 × 10⁸)/(6.10 × 10⁻⁷) = <strong>4.92 × 10¹⁴ Hz</strong>.'),
        p('f = 3 Hz and v = 4 m/s. λ = v/f = 4/3 ≈ <strong>1.3 m</strong>.'),
        parts('f = 1/(100 s) = <strong>0.010 Hz</strong>.', 'f = 1/(0.5 s) = <strong>2 Hz</strong>.', 'f = 1/(1.0 × 10⁻² s) = <strong>1.0 × 10² Hz</strong>.'),
        parts('<strong>Wave 1</strong> has the longest period.', '<strong>Wave 1</strong> has the lowest frequency.',
              '<strong>Wave 4</strong> has the highest frequency.') +
        p('These comparisons assume the diagrams use a common time axis or show spatial snapshots of waves travelling at the same speed. Spatial spacing by itself gives wavelength.'),
        p('One revolution takes <strong>12 h = 43 200 s</strong>.'),
        p('One revolution takes <strong>60 s</strong>.'),
        parts('3.00 min = 180 s. f = 36/180 = <strong>0.200 Hz</strong>.', 'T = 1/f = <strong>5.00 s</strong>.'),
        p('The spider returns to the needle’s position after one revolution. T = (60 s)/33 ≈ <strong>1.8 s</strong>.'),
        p('Wavelength <strong>decreases</strong> when the source frequency increases, assuming the same wave speed. If speed is approximately constant, λ is inversely proportional to f.'),
        p('λ = v/f = 2.5/34 ≈ <strong>0.074 m = 7.4 cm</strong>.'),
        p('25 cm = 0.25 m and 5 km/h = 5/3.6 m/s ≈ 1.39 m/s. f = 1.39/0.25 ≈ <strong>5.6 Hz</strong> before rounding to the precision of the given speed.'),
        p('v = fλ = (200)(35) = <strong>7.0 × 10³ m/s</strong> from the given data. This is far above the speed of sound in room-temperature air.'),
        p('Using 250 wavelengths across 100 m gives λ ≈ 100/250 = <strong>0.40 m</strong>. If 100 m is measured from the first crest to the 250th crest, use 249 intervals and get 0.402 m, which also rounds to 0.40 m.'),
        p('600 nm = 6.00 × 10⁻⁷ m. f = (3.0 × 10⁸)/(6.00 × 10⁻⁷) = <strong>5.0 × 10¹⁴ Hz</strong>. A wavelength of 600 nm is approximately orange.'),
        p('<strong>Frequency</strong> stays the same across a stationary boundary, so the period also stays the same. Speed, wavelength, and amplitude can change.'),
        pulses(False),
    ],
]
