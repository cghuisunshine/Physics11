@title: Why does opening width affect diffraction?
@subtitle: Connect circular and nearly straight crest lines to wave phase, then derive how opening width and wavelength control the spreading.

## 1 The model and the question
This is **optional further reading for Section 9 of Wave Motion Notes**. Prerequisites are wavelength, phase, superposition, algebra, and the sine ratio. The optional intensity derivation also introduces phase arrows and angles in radians. No calculus is needed, and the main Physics 11 notes can be completed without this page.

Consider a single long slit of width **b**, illuminated normally by a wave with uniform amplitude and phase across the opening. Let **λ** be its wavelength in the medium beyond the opening. Measure the observation angle **θ from the normal** pointing straight through the opening. Lengths such as b and λ use the same units, normally metres; b/λ has no units.

We first examine the spatial wavefronts in a scalar-wave model, including the region near the opening. The later cancellation and intensity formulas use an ideal **far-field** model: contributions from across the opening travel in nearly parallel directions toward a distant observation point. Near the central direction, useful screen-distance conditions are **L ≫ b** and **L ≫ b²/λ**, where L is the perpendicular distance to the screen. The second condition keeps wavefront-curvature corrections small compared with a wavelength. Real water waves and sound also depend on the opening shape and boundary conditions; the model explains the width-to-wavelength trend, rather than every detail of a ripple tank or doorway.

There are two related questions: **Why do the crest lines look circular or nearly straight?** And **over what range of directions is the outgoing wave strong?** A wavefront is a line of equal phase; an intensity graph tells us its strength in different directions. We need both to explain the ripple-tank picture.

## 2 Why the crests look circular or nearly straight
### A crest line is a line of equal phase
Take a top view, with x pointing through the opening and y running across it. Let u be the wave displacement at position (x, y) and time t. Define **k = 2π/λ**, **ω = 2πf**, and **v = fλ**. The argument of the cosine is the wave’s phase; points with phase 0, 2π, 4π, … are at crest phase.

For an ideal plane wave travelling along +x:
```
u(x, y, t) = A cos(kx − ωt)
Crest phase: kx − ωt = 2πm
x = vt + mλ
```
At a fixed time, each crest has **one constant x for every y**. Its top-view shape is therefore a straight line. Here m is an integer labelling successive crests.

For a small source at the centre of the opening, let **r = √(x² + y²)**. Its outgoing wave has approximately radial phase:
```
u(x, y, t) ≈ A(r) cos(kr − ωt)
Crest phase: kr − ωt = 2πm
r = vt + mλ
x² + y² = (vt + mλ)²
```
At a fixed time this is **a circle**, with the transmitted part forming an arc or approximately a semicircle beyond the barrier. A constant source-phase offset would shift the crest radii without changing their circular shape. A(r) allows the amplitude to decrease with distance; it is the radial phase that gives the circle.

### Why a narrow opening approaches the small-source case
Contributions from the opening begin in phase. Their path-length differences toward a distant direction are at most about b, so the phase difference across the opening has magnitude:
```
|Δφ| ≈ (2π/λ) b |sin θ|
|Δφ| ≤ 2πb/λ
```
If **b ≪ λ**, the contributors occupy a region too small to create large phase differences in any forward direction. Seen from distances large compared with b, they act approximately like one small source. Reinforcement is spread over a broad range of directions, revealing a broad circular crest. When b is merely comparable to λ, the pattern is already broad but is not a perfect point-source pattern; the circular appearance becomes clearer as b/λ decreases.

### Why a wide opening keeps a nearly straight central part
A wide opening contains many wavelength-sized portions of the incoming, in-phase wavefront. Near its centre, the combined wave can closely resemble transmission through an unlimited straight front. For an unlimited uniform front, every y position is equivalent, so the displacement has no y dependence: **u ≈ A cos(kx − ωt)**. That gives the straight crest lines derived above.

In the wavelet picture, each individual contribution is curved; **the sum of many contributions**, rather than the shape of one contribution, determines the resulting crests. Across a wide opening, sideways contributions increasingly cancel while the forward contributions reinforce. There is a central region with nearly straight crests and curved waves near the two edges. A finite opening never eliminates edge diffraction.

DIFFRACTION_WAVEFRONTS_FIGURE

The two panels use the same wavelength and spatial scale. The narrower opening produces visibly curved crests across a broad region. The wider opening has nearly straight central crests, plus curved edge waves. The coloured regions show displacement at one instant, not intensity; the black lines identify equal crest phase.

**Distance matters as well as width.** The nearly plane central region is a description at suitable distances near a wide opening, not a promise that its wavefront remains straight forever. Far beyond a finite opening, the leading radial phase is approximately kr for both widths. The wide opening then illuminates mainly a narrow arc around straight ahead, and that small arc can look almost flat. Section 4 below quantifies this connection.

WAVEFRONT_SOURCE

## 3 Pair points in the two halves of the opening
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

## 4 Why the ratio b/λ controls spreading
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

### Why a narrow visible arc can look like a straight line
In the far field, take one circular crest with radius R and put its central point at x = R. At transverse position Y, the same circle has x = √(R² − Y²). Its backward deviation from the central tangent line is:
```
s = R − √(R² − Y²)
  = Y² / [R + √(R² − Y²)]
For |Y| ≪ R: s ≈ Y²/(2R)
```
Over a small angular half-width θ₁, Y/R ≈ θ₁. Using θ₁ ≈ λ/b for a wide opening:
```
s/R ≈ θ₁²/2 ≈ (λ/b)²/2
```
Thus the strongly visible part of the circular crest becomes a flatter-looking arc as b/λ increases. For b = 5λ, θ₁ ≈ 11.5° and the deviation at the edge of the central lobe is **s/R = 1 − cos θ₁ ≈ 0.020**, about 2% of the radius. For a narrow opening that illuminates a broad range of angles, much more of the circle is visible and its curvature is obvious.

This does not mean a wide opening changes every distant circle into an exact line. Near the opening the central wave can be approximately plane; far away the visible central arc is narrow. Both effects help explain the usual straight-versus-circular sketches.

## 5 A graph of the spreading
The graph shows the ideal normalized intensity for three ratios, each divided by its own central intensity. It compares **angular shape**, not the absolute amount of energy transmitted by different openings. The broad patterns for b = λ and b = 0.5λ contrast with the narrow central maximum for b = 5λ. Smaller side peaks remain outside the central region for the wider opening.

DIFFRACTION_PATTERN_FIGURE

The curves use the scalar aperture factor derived below. In particular, for widths comparable to or smaller than a wavelength, detailed angular factors and boundary effects can matter in a real experiment. The curves are model calculations, not measured water-wave data. For a small opening, broad angular strength makes a broad portion of the approximately circular crest visible. A wide opening gives a narrow strong arc in the far field. The intensity graph alone does not specify the crest shape, which also depends on phase and observation distance.

## 6 Optional: derive the intensity curve without calculus
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

## 7 Example matching the ripple-tank investigation
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

## 8 Checks and interpretation
- **Shape versus strength:** crest lines follow equal phase. Intensity tells us which parts are strong enough to see; it is not itself a map of crests.
- **Units:** λ/b and sin θ are dimensionless; Lλ/b is a length.
- **Central direction:** θ = 0 gives zero phase difference and maximum reinforcement.
- **Wide-opening limit:** b/λ grows, θ₁ shrinks, and the central pattern becomes more directional.
- **Small-opening limit:** b/λ decreases, the available phase differences across the opening shrink, and broad-angle cancellation becomes harder to obtain.
- **Unchanged medium:** changing the opening width does not by itself change frequency, wavelength, or wave speed; it changes the interference between contributions across the opening.
- **One opening versus two slits:** b is the width of one opening. The double-slit d is the separation between two openings. Similar projection geometry appears in both, but their minimum conditions follow different cancellation arguments.
