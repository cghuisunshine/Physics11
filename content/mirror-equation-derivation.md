@title: Why does one mirror equation work for both shapes?
@subtitle: Optional further reading: a two-ray proof using reflection, similar triangles, and signed distances.

## 1 Set up one sign convention
This optional proof extends Topic 6 of Light and Geometric Optics Notes. **Prerequisites:** the law of reflection, principal rays, similar triangles, and algebra with negative numbers. No calculus is needed. You can complete the Physics 11 notes without this proof.

Use a real, upright object in front of a spherical mirror. Work in the **near-axis (paraxial) model**: rays make small angles with the principal axis, and the mirror's small depth is neglected when measuring their horizontal distances. In this model, a ray arriving parallel to the axis reflects through F, or its backward extension passes through F. This ray rule defines the focal point independently of the mirror equation we are about to derive.

Let **V be the origin**. The horizontal coordinate s is positive in front of the mirror (left in both drawings); vertical height is positive upward. The lengths dₒ, dᵢ, and f use the same unit. Heights hₒ and hᵢ also use one common length unit.

- Object tip O has coordinates **(dₒ, hₒ)**, with dₒ > 0 and hₒ > 0.
- Image tip I has coordinates **(dᵢ, hᵢ)**. A virtual image has dᵢ < 0; an inverted image has hᵢ < 0.
- Focus F has coordinates **(f, 0)**. Concave means f > 0; convex means f < 0.
- The parallel ray meets the mirror at P, approximated by **(0, hₒ)** in the near-axis model.

CONCAVE_DERIVATION_FIGURE

CONVEX_DERIVATION_FIGURE

Solid arrows show actual light; dashed lines behind the convex mirror extend the reflected rays backward. They are not light transmitted through the mirror. Both rays start at the same object tip and locate the same image tip.

## 2 The vertex ray gives the first height equation
The teal ray strikes V. At V the normal is the principal axis, so the law of reflection makes the incoming and reflected angles equal. The object and image triangles therefore have equal height-to-horizontal-distance ratios in magnitude.

For the concave real image drawn above, the image is below the axis, so hᵢ is negative. Equal triangle ratios give hₒ/dₒ = (−hᵢ)/dᵢ. For a virtual image, extend the reflected ray behind the mirror: dᵢ becomes negative and hᵢ becomes positive. Both cases are represented by the same signed relation:
```
hᵢ/dᵢ = −hₒ/dₒ

hᵢ/hₒ = −dᵢ/dₒ                         (A)
```
This is also the magnification equation. The minus sign follows from reflection at V; it does not need to be changed for a convex mirror.

## 3 The parallel ray gives a second height equation
The orange ray arrives at P parallel to the axis. After reflection, its straight line passes through **P = (0, hₒ)** and **F = (f, 0)**. For a convex mirror it is the backward extension of the ray that passes through F, but the same straight-line geometry applies.

From P to F, the signed horizontal change is f and the vertical change is −hₒ. From P to the image tip I, the corresponding changes are dᵢ and hᵢ − hₒ. Equal slopes, or similar right triangles with signed changes, give:
```
(hᵢ − hₒ)/dᵢ = (0 − hₒ)/f

hᵢ − hₒ = −hₒdᵢ/f
hᵢ = hₒ(1 − dᵢ/f)

hᵢ/hₒ = 1 − dᵢ/f                       (B)
```
In the convex example shown, f and dᵢ are both negative and 0 < dᵢ/f < 1. The equation therefore describes an upright image smaller than the object. No extra sign is inserted into the equation.

## 4 Set the two height equations equal
Equations (A) and (B) describe the **same image tip**, so their expressions for hᵢ/hₒ must agree:
```
−dᵢ/dₒ = 1 − dᵢ/f

dᵢ/f = 1 + dᵢ/dₒ

1/f = 1/dᵢ + 1/dₒ
```
In the final step, divide by the finite, nonzero image distance dᵢ. We obtain the familiar equation:
```
1/f = 1/dₒ + 1/dᵢ
```
Nothing in this step required f to be positive. **The same proof therefore covers concave and convex mirrors, and both real and virtual images within the stated model.** The signs belong to the distances, not to separate versions of the equation.

To isolate the image distance, use a common denominator and invert:
```
1/dᵢ = 1/f − 1/dₒ
     = (dₒ − f)/(f dₒ)

dᵢ = f dₒ/(dₒ − f)                      dₒ ≠ f
```

## 5 Check both shapes with the same object distance
These illustrative checks use dₒ = +100 cm and focal-length magnitude 20.0 cm. They are model calculations, not new measured data or publisher-verified answers.

### Concave mirror: f = +20.0 cm
```
dᵢ = (+20.0 cm)(100 cm)/(100 cm − 20.0 cm)
   = +25.0 cm

m = −(+25.0 cm)/(100 cm) = −0.250
```
Positive dᵢ means a real image in front. Negative m means inverted; its magnitude makes the image one quarter as tall. Check: 1/20.0 = 1/100 + 1/25.0, with every term in cm⁻¹.

### Convex mirror: f = −20.0 cm
```
dᵢ = (−20.0 cm)(100 cm)/(100 cm − (−20.0 cm))
   = −16.7 cm approximately

m = −(−16.7 cm)/(100 cm) ≈ +0.167
```
Negative dᵢ means a virtual image behind. Positive m means upright; its magnitude makes the image about one sixth as tall. Using the unrounded image distance, −16⅔ cm, gives −1/20 = 1/100 − 3/50 = −0.0500 cm⁻¹, as required.

For any real object and convex mirror, write f = −a with a > 0. Then dᵢ = −a dₒ/(dₒ + a) is always negative, and m = a/(dₒ + a) lies between 0 and 1. This explains why the convex image is always virtual, upright, and reduced for a real object.

## 6 What the derivation assumes
The equation is exact within the ideal near-axis model. A spherical mirror does not bring all rays far from the axis to a single focus: spherical aberration limits the approximation. We did not derive the separate near-axis relation f ≈ R/2 here; the proof uses the focus determined by the parallel-ray rule.

If dₒ = f for a concave mirror, equations (A) and (B) cannot agree at any finite image point. The reflected rays are parallel and there is no finite image distance. The rearranged formula must not be evaluated by dividing by zero.

For a very distant object, dᵢ approaches f. For a convex mirror, the denominator dₒ − f is always positive when dₒ > 0, so the image stays behind the mirror. The reciprocal equation has units of inverse length, and f dₒ/(dₒ − f) has units of length. These are useful checks on both the algebra and the signs.
