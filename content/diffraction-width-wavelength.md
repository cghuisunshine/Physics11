@title: Why does opening width affect diffraction?
@subtitle: Derive the spreading angle by pairing waves across one opening, then compare patterns for different width-to-wavelength ratios.

## 1 The model and the question
This is **optional further reading for Section 9 of Wave Motion Notes**. Prerequisites are wavelength, phase, superposition, algebra, and the sine ratio. The optional intensity derivation also introduces phase arrows and angles in radians. No calculus is needed, and the main Physics 11 notes can be completed without this page.

Consider a single long slit of width **b**, illuminated normally by a wave with uniform amplitude and phase across the opening. Let **λ** be its wavelength in the medium beyond the opening. Measure the observation angle **θ from the normal** pointing straight through the opening. Lengths such as b and λ use the same units, normally metres; b/λ has no units.

We use an ideal scalar **far-field** model: contributions from across the opening travel in nearly parallel directions toward a distant observation point. Near the central direction, useful screen-distance conditions are **L ≫ b** and **L ≫ b²/λ**, where L is the perpendicular distance to the screen. The second condition keeps wavefront-curvature corrections small compared with a wavelength. Real water waves and sound also depend on the opening shape and boundary conditions; the model explains the width-to-wavelength trend, rather than every detail of a ripple tank or doorway.

The question is: **At what angle do contributions from different parts of the opening first cancel completely?** That angle marks the edge of the central diffraction maximum in this model.

## 2 Pair points in the two halves of the opening
By the wavelet model, different parts of the opening contribute waves that must be added at the observer. At θ = 0 they have equal path lengths in the far-field approximation, so their oscillations reinforce. At an angle, their paths differ.

Pair every small strip in the upper half with the strip **b/2 below it** in the lower half. The two strips have equal widths and, in this uniform-illumination model, equal arriving amplitudes. Their separation projected onto the outgoing direction gives the path difference:

DIFFRACTION_PAIR_FIGURE

```
Δr_pair ≈ (b/2) sin θ
```
This is the same right-triangle projection used for the double-slit path difference, now applied to two parts of one opening. The projection itself is exact; replacing the finite path difference by that projection uses the far-field approximation.

Two equal contributions cancel when one has travelled an extra half-wavelength: its crests arrive with the other’s troughs. The corresponding phase difference is half a cycle, or π radians. At the **first minimum**, impose that condition on every pair:
```
(b/2) sin θ₁ = λ/2
b sin θ₁ = λ
sin θ₁ = λ/b
θ₁ = arcsin(λ/b)                       for b > λ
```
The first equality is within the far-field model. Every upper strip has a cancelling partner, so the sum across the whole slit vanishes. Cancellation is not caused by just the two edges: at this first minimum the edge-to-edge path difference is one whole wavelength, while each paired half-slit separation gives half a wavelength.

For higher minima, split the opening into 2m equal strips and pair adjacent strips at corresponding positions. Their separation b/(2m) gives a half-wavelength path difference when **b sin θ_m = mλ**, with m = 1, 2, 3, …, wherever the resulting angle exists. The pattern is symmetric at negative angles.

MINIMUM_SOURCE

## 3 Why the ratio b/λ controls spreading
Rearrange the first-minimum condition to isolate the ratio:
```
(b/λ) sin θ₁ = 1
sin θ₁ = 1/(b/λ)
```
A larger b/λ reaches cancellation at a smaller angle. The bright central region is therefore narrower. A smaller b/λ needs a larger angle before the same phase difference can build up across the opening, so reinforcement persists over a wider range of directions.

- **b = 10λ:** θ₁ = arcsin(0.100) ≈ 5.74°.
- **b = 5λ:** θ₁ = arcsin(0.200) ≈ 11.5°.
- **b = 2λ:** θ₁ = arcsin(0.500) = 30.0°.
- **b = λ:** the ideal first zero reaches θ = 90°, the grazing-direction boundary.
- **b < λ:** λ/b > 1, so there is no first cancellation minimum in the forward angular range. The pattern is broad; this does not mean diffraction disappears or that the wave has equal intensity in every direction.

For b > λ, the central maximum spans **−θ₁ to +θ₁**, so its full angular width between the first zeros is 2θ₁. When b ≫ λ, θ₁ is small and sin θ₁ ≈ θ₁ **in radians**:
```
Central half-width: θ₁ ≈ λ/b
Full angular width: 2θ₁ ≈ 2λ/b
```
Doubling the opening width roughly halves this angular width in the small-angle regime. Increasing wavelength at fixed width has the opposite effect. If both b and λ change by the same factor, the ideal angular pattern stays the same.

## 4 A graph of the spreading
The graph shows the ideal normalized intensity for three ratios, each divided by its own central intensity. It compares **angular shape**, not the absolute amount of energy transmitted by different openings. The broad patterns for b = λ and b = 0.5λ contrast with the narrow central maximum for b = 5λ. Smaller side peaks remain outside the central region for the wider opening.

DIFFRACTION_PATTERN_FIGURE

The curves use the scalar aperture factor derived below. In particular, for widths comparable to or smaller than a wavelength, detailed angular factors and boundary effects can matter in a real experiment. The curves are model calculations, not measured water-wave data. A broad angular distribution corresponds to strongly curved outgoing wavefronts; the intensity graph does not itself plot crest positions.

## 5 Optional: derive the intensity curve without calculus
The pair argument already explains the first minimum. To describe angles between minima, represent each small contribution by a **phase arrow**: its length is its amplitude and its direction records its oscillation phase. Add the arrows head to tail; the resulting arrow gives the combined amplitude.

The edge-to-edge path difference b sin θ corresponds to a total phase change Φ. For θ ≥ 0:
```
Φ = 2π (b sin θ)/λ                    radians
```
As the strips get very thin, successive arrows turn smoothly through this angle. Their head-to-tail chain approaches a circular arc. Let ρ be its radius. The total arrow length equals the on-axis amplitude A₀, because on axis the arrows all align. Arc length and chord length give:
```
A₀ = arc length = ρΦ
|A(θ)| = chord length = 2ρ |sin(Φ/2)|
|A(θ)|/A₀ = |sin(Φ/2)/(Φ/2)|
```
Define β = Φ/2 = π(b/λ) sin θ. Intensity is proportional to amplitude squared in this linear-wave model, so:
```
I(θ)/I(0) = [sin β / β]²
β = π(b/λ) sin θ
At θ = 0: I(θ)/I(0) = 1
```
The central value is the smooth limiting value, rather than a division by zero. Squaring makes the pattern symmetric for negative θ. Zeros occur at β = mπ for nonzero integers m, reproducing **b sin θ = mλ**. The formula depends on b and λ only through their ratio, which explains the graph’s scaling.

INTENSITY_SOURCE

## 6 Example matching the ripple-tank investigation
Keep λ = 2.0 cm, as in Section 9. Compare b = 2.0 cm and b = 10 cm using the ideal far-field first-minimum condition:
```
Narrow opening: b/λ = 2.0/2.0 = 1.0
sin θ₁ = 1.0 → ideal zero at 90°

Wide opening: b/λ = 10/2.0 = 5.0
sin θ₁ = 0.20 → θ₁ ≈ 11.5°
Full central angular width ≈ 23.1°
```
The narrower opening gives broad spreading across the forward region. The wider opening concentrates the central pattern closer to straight ahead. These numbers illustrate the ideal model; the qualitative comparison in the main notes does not require the tank to satisfy the far-field conditions.

For the wider opening, the small-angle screen estimate is **y₁ ≈ Lλ/b**, where y₁ is the distance from the centre to the first minimum. The full central width on that screen is approximately 2Lλ/b. Use y₁ = L tan θ₁ instead if the small-angle approximation is unsuitable and the far-field model still applies.

## 7 Checks and interpretation
- **Units:** λ/b and sin θ are dimensionless; Lλ/b is a length.
- **Central direction:** θ = 0 gives zero phase difference and maximum reinforcement.
- **Wide-opening limit:** b/λ grows, θ₁ shrinks, and the central pattern becomes more directional.
- **Small-opening limit:** b/λ decreases, the available phase differences across the opening shrink, and broad-angle cancellation becomes harder to obtain.
- **Unchanged medium:** changing the opening width does not by itself change frequency, wavelength, or wave speed; it changes the interference between contributions across the opening.
- **One opening versus two slits:** b is the width of one opening. The double-slit d is the separation between two openings. Similar projection geometry appears in both, but their minimum conditions follow different cancellation arguments.
