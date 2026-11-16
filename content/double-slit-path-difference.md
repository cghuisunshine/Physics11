@title: Why is the path difference d sin θ?
@subtitle: An optional mathematical derivation for Young’s double slit, using right-triangle geometry and algebra.

## 1 Set up the geometry
This optional tutorial extends Section 11 of Wave Motion Notes. **Prerequisites:** the sine ratio in a right triangle, Pythagoras, and the idea of path difference. No calculus is needed. The core notes can be completed without this page.

Two narrow slits A and B are separated by a centre-to-centre distance **d**. The screen is a perpendicular distance **L** from the slit plane. Its centre O lies directly opposite the midpoint of the slits. A point P on the screen has a signed vertical offset **y** from O.

Measure **θ from the central normal** (the line from the slit midpoint to O) toward P. Positive y and θ point toward slit A. Let r_A and r_B be the distances AP and BP. Define the signed path difference **Δr = r_B − r_A**. Above the centre, B is farther from P, so Δr is positive. All distances use the same units, normally metres; θ may be expressed in degrees or radians.

The geometric path difference does not require in-phase sources. To connect it to the usual bright and dark bands, assume coherent, in-phase sources of the same wavelength in a uniform medium.

## 2 Draw the small right triangle
For a distant observation point, the paths AP and BP are nearly parallel. Draw two **parallel construction rays** in the direction θ, one from each slit. From A, draw a perpendicular to the lower construction ray, meeting it at C.

PATH_DIFFERENCE_FIGURE

Triangle ABC is right-angled at C. Its hypotenuse AB is d. The angle at B, between BA and BC, is 90° − θ. Therefore the angle at A, between AB and AC, is θ: the two acute angles of a right triangle add to 90°.

The side opposite angle θ at A is BC. Apply the sine ratio before making any wave assumptions:
```
sin θ = opposite / hypotenuse = BC / AB
sin θ = BC / d
BC = d sin θ
```
In the parallel-ray model, A and C lie on the same line perpendicular to the travel direction. Their remaining forward distances to a common distant wavefront are equal. The lower path includes the extra segment BC, so **Δr ≈ BC = d sin θ** for a distant screen. The triangle identity is exact; treating its projection as the difference of the two finite paths is the approximation.

**Why sine rather than cosine?** θ is measured from the normal to the slit plane, not from the slit separation AB. BC is opposite θ in this triangle. If an angle α were measured from AB instead, the same projection would be d cos α, with α = 90° − θ.

## 3 Check it with exact finite-distance algebra
Choose coordinates with the slit midpoint at (0, 0), horizontal x toward the screen, and vertical y toward A. Then A = (0, d/2), B = (0, −d/2), and P = (L, y). Pythagoras gives the exact path lengths:
```
r_A = √[L² + (y − d/2)²]
r_B = √[L² + (y + d/2)²]
Δr = r_B − r_A
```
Multiply by the conjugate to turn the difference of square roots into a difference of squares:
```
Δr = (r_B − r_A)(r_B + r_A) / (r_B + r_A)
   = (r_B² − r_A²) / (r_B + r_A)
   = [(y + d/2)² − (y − d/2)²] / (r_B + r_A)
   = [(y² + yd + d²/4) − (y² − yd + d²/4)] / (r_B + r_A)
   = 2yd / (r_B + r_A)                  exact
```
Let **R = √(L² + y²)** be the distance from the slit midpoint to P. When the slit spacing is much smaller than this distance, **d ≪ R**, both path lengths are approximately R. Thus r_B + r_A ≈ 2R. In the large screen triangle, sin θ = y/R, so:
```
Δr ≈ 2yd / (2R)
   = d(y/R)
   = d sin θ                           distant-screen result
```
This derivation also handles negative y: the signed path difference is negative below the centre. If path difference means the nonnegative difference of lengths, write **|Δr| ≈ d |sin θ|**.

## 4 Connect the geometry to the bright bands
For in-phase sources, reinforcement occurs when the extra distance is a whole number of wavelengths. For cancellation, it is an odd half-wavelength; complete darkness also requires equal arriving amplitudes in the ideal model. With λ the wavelength and m the nonnegative order on the upper side:
```
Bright:  Δr = mλ          → d sin θ ≈ mλ
Dark:    Δr = (m + ½)λ    → d sin θ ≈ (m + ½)λ
m = 0, 1, 2, …
```
The familiar equations d sin θ = mλ and d sin θ = (m + ½)λ use the distant-screen model. **A distant screen does not by itself require a small θ.** The additional small-angle approximation is needed for the usual fringe-position shortcut. From the large screen triangle:
```
tan θ = y/L                              exact geometry
sin θ = y/√(L² + y²)                     exact geometry
For |y| ≪ L: sin θ ≈ tan θ ≈ y/L
Bright bands: d(y/L) ≈ mλ → y ≈ mλL/d
```

## 5 Worked example and checks
**AI-authored example.** Let d = 0.250 mm, L = 2.00 m, and y = 4.80 mm, the same geometry as the notes example. First use the screen triangle to find θ, then project the slit spacing:
```
d = 2.50 × 10⁻⁴ m; y = 4.80 × 10⁻³ m
θ = arctan(y/L) = arctan(0.00240) ≈ 0.1375°
Δr ≈ d sin θ ≈ 6.00 × 10⁻⁷ m = 600 nm
```
If this point is the first bright band, m = 1 and λ ≈ Δr = 600 nm. Here d/R ≈ 1.25 × 10⁻⁴ and |y|/L = 0.00240, consistent with both approximations.

- **Units:** sin θ has no units, so d sin θ is a length, as a path difference must be.
- **Centre:** θ = 0 gives Δr = 0; the two exact paths are equal.
- **Symmetry:** changing y to −y reverses Δr but preserves its magnitude.
- **Magnitude:** |d sin θ| ≤ d, consistent with the fact that the difference between distances to two points cannot exceed their separation.
