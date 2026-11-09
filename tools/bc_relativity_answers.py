"""Worked solutions to Chapter 8 questions in textbook order."""
from math import sqrt

from bc_kinematics_answers import graph, paragraphs as p, parts, table


def dilated_time(beta, result):
    return p(f'Δt = Δτ/√(1 − β²) = (5.0 s)/√(1 − {beta}²) ≈ <strong>{result}</strong>. '
             'The outside frame assigns the longer interval.')


def contracted_length(beta, result):
    return p(f'L = L₀√(1 − β²) = (100 m)√(1 − {beta}²) ≈ <strong>{result}</strong>. '
             'The length is measured along the direction of motion.')


speeds = (.10, .50, .87, .9999)
momentum_rows = [
    (f'{beta:g}c', f'{beta:g} mc', f'{beta / sqrt(1 - beta**2):.3g} mc')
    for beta in speeds
]
momentum_rows.append(('c', 'mc (formal Newtonian result)', 'No finite value for a massive electron'))


answer_groups = [
    # 8.1 warm-up and two reference-frame quick checks
    [p('Yes. If the neighbouring cars move forward, the distance from you to them increases. With only those cars as a reference, your brain may interpret this as your car rolling backward. Compare your position with a fixed roadside object to tell the difference.')],
    [
        parts('<strong>10 km/h downstream (left)</strong> relative to the water, as marked on the diagram.',
              'Add the river’s 5.0 km/h downstream speed to get <strong>15 km/h downstream</strong> relative to Earth.'),
        parts('<strong>25 km/h left</strong> relative to the air.',
              'The bird’s Earth-frame velocity is 25 − 20 = 5 km/h left, the same as the river. It is at <strong>0 km/h</strong> relative to the water.',
              '<strong>5 km/h left</strong> relative to Earth. The wind blows 20 km/h to the right.'),
        p('The river and bird both move left at 5 km/h relative to Earth. Subtract their velocities to get <strong>0 km/h</strong> relative to the bird.'),
        p('The boat moves left at 15 km/h relative to Earth and the bird at 5 km/h left. The person therefore moves <strong>10 km/h downstream (left)</strong> relative to the bird.'),
        p('The question describes a <strong>geostationary</strong> view, with the camera fixed over a point on the rotating Earth. In the Earth-fixed map used by the camera, the local ground is stationary, so the local Earth-relative velocities are unchanged. These are the boat at 15 km/h left, river and bird at 5 km/h left, and wind at 20 km/h right. The diagram’s boat-relative-to-water and bird-relative-to-air velocities describe the same pairwise motion.'),
    ],
    [
        p('Observer A stands at the roadside, so their road-relative velocity is <strong>0 km/h</strong>.'),
        p('The ball keeps the van’s steady horizontal velocity after release. In the road frame it moves forward while rising and falling under gravity. Draw a <strong>parabola</strong> opening downward, with the catch farther along the road. In the van frame the throw is straight up and down.') +
        graph('One possible road-frame path, with illustrative distances',
              [('Ball travels right', [(x, 1.8 - .2 * (x - 3)**2) for x in (0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6)], '#096a70')],
              xmax=6, ymin=0, ymax=2, xlabel='Forward distance (m)', ylabel='Height above release (m)'),
    ],
    # Sample and practice 8.1.1
    [p('With β = 0.500, γ = 1/√(1 − 0.500²) ≈ 1.1547. Thus <strong>Δt ≈ 1.155 Δτ</strong> for the same clock interval. An hour on board corresponds to about 69.3 min outside, about <strong>9.3 min longer</strong>.')],
    [
        dilated_time('0.65', '6.6 s'),
        dilated_time('0.866', '10 s'),
        dilated_time('0.995', '5.0 × 10¹ s'),
        dilated_time('0.999', '1.1 × 10² s'),
    ],
    # Sample and practice 8.1.2
    [p('The stick’s proper length is 1.00 m. Its length measured parallel to its motion is (1.00 m)√(1 − 0.995²) ≈ <strong>0.100 m, or 10.0 cm</strong>. Record both endpoint positions at the same time in your frame. The speed in the question is 0.995c.')],
    [
        contracted_length('0.63', '78 m'),
        contracted_length('0.866', '50 m'),
        contracted_length('0.999', '4.5 m'),
    ],
    # Momentum quick check
    [
        parts('0.10mc', '0.50mc', '0.87mc', '0.9999mc', 'mc') +
        p('These follow by formally substituting into p = mv. The Newtonian model is an approximation for low speeds and its c result is only a formal value.'),
        p('Use p/(mc) = β/√(1 − β²), where m is the invariant mass. At c the formula has no finite value for an electron. The momentum grows without bound as v approaches c from below.') +
        table(('Speed', 'Newtonian p', 'Relativistic p'), momentum_rows),
        p('The average net force in the chosen frame is Δp/Δt. From rest, Δp = γmv. At any fixed finite time t, the required average force grows without bound as v approaches c. <strong>No finite force can bring an electron to c in finite time.</strong>'),
    ],
    # 8.1 Review
    [
        parts('The laws of physics have the same form in all inertial frames.',
              'All inertial observers measure the same speed c for light in vacuum, regardless of the motion of its source.'),
        p('The light passes at <strong>c ≈ 3.00 × 10⁸ m/s</strong> in the spaceship frame. Moving toward the star can change the frequency you measure.'),
        parts('The 10 a on the astronaut’s clock is proper time. Δt = 10/√(1 − 0.65²) ≈ <strong>13.2 years</strong> in the Earth frame.',
              'L = (50.0 m)√(1 − 0.65²) ≈ <strong>38.0 m</strong>. Measure the two endpoints simultaneously in the Earth frame.'),
        p('With β = ½, Δt = t₀/√(1 − ¼) = <strong>2t₀/√3 ≈ 1.155t₀</strong>. The bus clock measures the proper interval for an event pair at the same location in the bus.'),
        p('Set L/L₀ = ½ = √(1 − β²). Then β² = ¾, so <strong>v = (√3/2)c ≈ 0.866c</strong>.'),
        p('The ratio is 5 m/10 m = 0.5. Then v/c = √(1 − 0.5²) = <strong>0.866</strong>. The bus travels at 0.866c.'),
        p('<strong>Choice (c).</strong> The light has taken time to reach Earth, so it carries information about the star when the light was emitted. For example, a star 10 light-years away is seen roughly 10 years in the past in the Earth frame.'),
        p('In the idealized model, Earth ages by 2520 − 2020 = 500 years. The traveller can spend at most 75 − 25 = 50 years on board, so γ must be at least 10. At γ = 10, v = c√(1 − 1/100) ≈ <strong>0.995c</strong>. This assumes equal cruising speeds on the outward and return legs with negligible time spent turning around.'),
        p('1 mg = 1 × 10⁻⁶ kg. E₀ = mc² ≈ (1 × 10⁻⁶)(3.00 × 10⁸)² = <strong>9 × 10¹⁰ J</strong> if all of that mass is converted.'),
        parts('Convert 46 g to 0.046 kg. E₀ = (0.046)(3.00 × 10⁸)² ≈ <strong>4.1 × 10¹⁵ J</strong>.',
              '16 kWh/day = 5.76 × 10⁷ J/day. Dividing 4.14 × 10¹⁵ J by that rate gives about 7.19 × 10⁷ days, or <strong>2.0 × 10⁵ years</strong>, under complete conversion and lossless storage.'),
        p('Use your own monthly reading B in kWh. The monthly energy is B × 3.6 × 10⁶ J. Full conversion of 1 g gives (0.001)(3.00 × 10⁸)² = 9.0 × 10¹³ J, or <strong>2.5 × 10⁷ kWh</strong>. Divide 2.5 × 10⁷ by B for the number of months. A reading of 600 kWh would give about 4.2 × 10⁴ months.'),
    ],
    # Extension
    [
        p('For invariant mass m, p = γmv. As v approaches c, γ increases without bound and so does the required momentum. Total energy E = γmc² also grows without bound. An electron can be accelerated very close to c, but cannot reach c with finite energy.'),
        p('Special relativity describes physics in flat spacetime. It can also describe an accelerating object by tracking its motion in that spacetime. General relativity describes gravity through spacetime curvature produced by matter and energy. Freely falling objects follow geodesics, and clocks can accumulate different proper times when they follow different paths or remain at different heights in a gravitational field.'),
    ],
    # Extra practice
    [
        p('<strong>Choice (b), 9.95 m.</strong> L = (10 m)√(1 − 0.1²) = 9.94987 m before rounding. This is a small contraction.'),
        p('<strong>Choice (c), 8 years and 4 months.</strong> The traveller ages 5 years. At 0.8c, γ = 1/0.6 = 5/3, so the Earth-frame duration is (5/3)(5 years) = 8⅓ years. Treat the turnaround as brief and use 0.8c as the speed on both legs.'),
        p('Use the electron rest mass m ≈ 9.11 × 10⁻³¹ kg. E₀ = mc² ≈ (9.11 × 10⁻³¹)(3.00 × 10⁸)² = <strong>8.20 × 10⁻¹⁴ J</strong>. None of the printed choices matches. Choice (d) has the right coefficient and an exponent one power of ten too small.'),
        p('<strong>Choice (a), c.</strong> The observer still measures c for light in vacuum. Their motion toward the source changes the received frequency.'),
        p('<strong>Choice (b), 5:16 a.m.</strong> At 0.6c, 1/γ = √(1 − 0.6²) = 0.800. The spaceship watch advances by 0.800 × 20 min = 16 min over the 20 min Earth-frame interval.'),
        p('<strong>Choice (c), 0.89c.</strong> For a forward launch at 0.5c relative to the ship, u = (0.7c + 0.5c)/(1 + 0.7 × 0.5) ≈ 0.889c in the outside frame. A backward launch would require a negative signed launch velocity and give a different answer.'),
    ],
]
