@title: Why is the path difference d sin θ?
@subtitle: An optional mathematical derivation for Young’s double slit, using right-triangle geometry and algebra.

## 1 Set up the geometry
This optional tutorial extends Section 11 of Wave Motion Notes. **Prerequisites:** the sine ratio in a right triangle, Pythagoras, and the idea of path difference. No calculus is needed. The core notes can be completed without this page.

Two narrow slits A and B are separated by a centre-to-centre distance **d**. The screen is a perpendicular distance **L** from the slit plane. Its centre O lies directly opposite the midpoint of the slits. A point P on the screen has a signed vertical offset **y** from O.

Measure **θ from the central normal** (the line from the slit midpoint to O) toward P. Positive y and θ point toward slit A. Let r_A and r_B be the distances AP and BP. Define the signed path difference **Δr = r_B − r_A**. Above the centre, B is farther from P, so Δr is positive. All distances use the same units, normally metres; θ may be expressed in degrees or radians.

The geometric path difference does not require in-phase sources. To connect it to the usual bright and dark bands, assume coherent, in-phase sources of the same wavelength in a uniform medium.

## 2 Project the slit separation onto MP
Mark **M, the midpoint of the two slits**, and **P, the point where both paths arrive on the screen**. Draw AP, BP, and MP. The angle between MP and the central normal MO is θ. Put **C on MP so that AC is perpendicular to MP**, and put **D on the backward extension of MP so that BD is also perpendicular to MP**. Thus D, M, C, and P lie on the same straight line in the illustrated arrangement.

PATH_DIFFERENCE_FIGURE

### The projection CD is exactly d sin θ
Triangle AMC is right-angled at C, with hypotenuse AM = d/2. The angle between AM and AC is θ: these lines are perpendicular to the central normal and MP, respectively. Apply the sine ratio:
```
sin θ = MC/AM
MC = (d/2) sin θ
```
By symmetry, triangle BMD gives the same projected length on the other side of M:
```
MD = (d/2) sin θ
CD = CM + MD
   = (d/2) sin θ + (d/2) sin θ
   = d sin θ                           exact projection
```
**Why sine rather than cosine?** The viewing angle θ is measured from the normal to the slit plane. In triangle AMC, MC is opposite θ and AM is the hypotenuse. If the viewing angle were measured from the slit plane instead, the complementary angle would give the same projection using cosine.

### The actual paths are slightly longer than their projections
The coloured paths AP and BP meet at P. The dashed line MP contains their projected lengths CP and DP. Because AC and BD are perpendicular to MP, Pythagoras gives:
```
AP² = AC² + CP²
BP² = BD² + DP²
```
Thus **AP > CP** and **BP > DP** when the perpendicular legs are nonzero. Neither equality is exact at a finite screen. The same factorization explains why each difference becomes small as P gets farther away:
```
AP − CP = AC²/(AP + CP)
BP − DP = BD²/(BP + DP)
```
Here AC = BD = (d/2) cos θ. The perpendicular legs remain bounded by d/2 while the denominators grow with distance.

### Now make the distant-screen approximation
The figure shows P above the centre, with MP > d/2, so both projection feet lie before P along the line from D to P. Therefore DP = DC + CP. For a distant P, replace each actual path by its projected length:
```
AP ≈ CP,  BP ≈ DP
Δr = BP − AP
   ≈ DP − CP
   = CD
   = d sin θ
```
**CD = d sin θ is exact geometry; Δr ≈ CD uses the distant-screen approximation.** In this construction C and D lie on MP, not on the actual path BP. The coordinate derivation below checks the approximation directly without assuming either path equals its projection. Negative viewing angles are handled by the signed algebra in Section 3.

### Another interpretation: parallel rays with your annotated sketch
The sketch below gives a second way to visualize the same projection. **Its point C belongs to this separate construction:** it lies on the lower green ray, rather than on MP as in the diagram above.

PARALLEL_SKETCH_FIGURE

**Choose both green rays parallel to MP.** The upper green ray starts at A and approximates the direction of AP; the lower green ray starts at B and approximates the direction of BP. When **MP ≫ d**, the directions of AP and BP differ only slightly from the midpoint direction MP. Replacing both by that common direction is the **parallel-ray, or distant-screen, approximation**.

Both green rays therefore make the same angle θ with a horizontal normal, and the blue segment AC is perpendicular to them. In right triangle ABC, AB = d and BC is opposite θ at A. Therefore:
```
sin θ = BC/AB = BC/d
BC = d sin θ                           exact construction
```
The red overlay adds **M, the slit midpoint**, **P, a finite screen point**, and AP, MP, and CP. It makes the approximation visible: the actual paths meet at P, while the green rays keep the common direction parallel to MP. The sketch is schematic; θ is the angle of this chosen common direction.

Your added **E and F** make the approximate path lengths explicit. Draw **EF through P, perpendicular to MP and both green rays**. Let E lie on the upper green ray and F on the lower green ray. EF is an auxiliary perpendicular line through the observation point, not the vertical screen itself.

The finite path AP ends at P, while its parallel-ray replacement AE ends at E. Similarly, BP is replaced by BF. Triangles AEP and BFP are right-angled at E and F:
```
AP² = AE² + EP²
BP² = BF² + FP²
```
For a distant P, EP and FP are small compared with the long forward distances AE and BF. Therefore:
```
AP ≈ AE
BP ≈ BF
```
Since AC and EF are both perpendicular to the green rays, the segments **AE and CF are exactly equal**. B, C, and F lie on the same lower green ray, so:
```
AE = CF                               exact construction
BF = BC + CF
BF − AE = BC
```
Now substitute the approximate path lengths into the actual path difference:
```
Δr = BP − AP
   ≈ BF − AE
   = (BC + CF) − AE
   = BC
   = d sin θ
```
**The upper green length AE approximates AP, and the lower green length BF approximates BP. Their difference is exactly BC in the construction.** The equality AE = CF is exact; the replacements AP ≈ AE and BP ≈ BF use the distant-screen approximation. At finite distance, E and F remain different points from P, and C lies on BF rather than generally on the actual path BP. This gives the same far-distance result as the midpoint-projection interpretation above.

## 3 Check it with exact finite-distance algebra
Choose coordinates with the slit midpoint at (0, 0), horizontal x toward the screen, and vertical y toward A. Then A = (0, d/2), B = (0, −d/2), and P = (L, y).

EXACT_GEOMETRY_FIGURE

The dashed horizontal legs end at **Q_A = (L, d/2)** and **Q_B = (L, −d/2)** on the screen. Each horizontal leg has length L. The vertical legs to P have lengths **|y − d/2|** and **|y + d/2|**; squaring removes the absolute values. The diagram shows y > d/2 for clarity, but the algebra below also applies to points between the slit heights or below the centre. The two paths meet at the same finite point P and are not parallel.

Pythagoras gives the exact path lengths:
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
Let d = 0.250 mm, L = 2.00 m, and y = 4.80 mm, the same geometry as the notes example. First use the screen triangle to find θ, then project the slit spacing:
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
