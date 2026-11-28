@title: Why does a glass sing?
@subtitle: Vibrating walls, water, and the mass–spring model behind Warm-up 6.1.

# Why does a glass sing?

## 1 Start with the sound
This is **optional further reading for Warm-up 6.1 in Section 1 of Wave Motion Notes**. You can complete the Physics 11 notes without this page. Prerequisites for the model are Newton’s second law, Hooke’s law, frequency, and algebra. Section 3 additionally uses second derivatives and the differentiation of cosine; it is a calculus extension beyond Physics 11.

**An empty glass can ring.** Its elastic walls deform and vibrate, pushing and pulling on nearby air. The resulting pressure disturbances travel to your ear as sound. The glass vibrates about its equilibrium shape; the air transmits the sound away.

Adding water generally lowers the ringing frequency and therefore the pitch, because the moving walls also set some water in motion. Compare the same glass at different fill levels, with the same holding and rubbing technique.

The short explanation above develops the notes’ worked answer. The mathematical model below is an additional idealization, rather than a derivation supplied by the original warm-up.

GLASS_MODE_FIGURE

## 2 Model one vibration as a mass and a spring
A real glass has many possible patterns of vibration, called **modes**. Focus on one dominant ringing mode at small amplitude. Its pattern is fixed in this approximation: a single coordinate x(t) measures its deformation from equilibrium, in metres. Choose x positive when a selected point on the rim moves outward; the restoring force then acts in the negative direction. Other points need not move in the same direction at that instant.

The system is the vibrating glass together with the water participating in this mode. Represent its elastic resistance and inertia by two effective quantities:

- **k_eff**, effective stiffness, in N/m: resistance to deformation in the chosen mode.
- **m_eff**, effective mass, in kg: inertia participating in that same deformation. It is not necessarily the total mass on a scale.

For small deformations, approximate the restoring force by F_restore = −k_eff x, like Hooke’s law. Ignore damping and the finger’s driving force initially. The model’s undamped natural frequency is:

```text
f₀ = (1 / 2π) √(k_eff / m_eff)
```

Here f₀ is measured in hertz (Hz = cycles/s). A stiffer system oscillates faster; a system with more inertia oscillates more slowly. For weak damping, a sustained ringing tone is usually close to this natural frequency.

## 3 Optional calculus: why the frequency formula works
**Calculus extension.** Newton’s second law says that the restoring force produces acceleration. With x measured from equilibrium, the linearized equation of motion is:

```text
m_eff d²x/dt² = −k_eff x
m_eff d²x/dt² + k_eff x = 0
```

Try a sinusoidal oscillation, x(t) = A cos(ωt), starting at maximum positive deformation. A is amplitude in metres, t is time in seconds, and ω is angular frequency in rad/s. Differentiating twice gives:

```text
dx/dt = −Aω sin(ωt)
d²x/dt² = −Aω² cos(ωt) = −ω²x
```

Substitute into the equation of motion:

```text
−m_eff ω²x + k_eff x = 0
(k_eff − m_eff ω²)x(t) = 0
```

For a nonzero oscillation, x(t) is not identically zero. Therefore its constant coefficient must vanish; we do not divide by x at an instant when x = 0.

```text
k_eff − m_eff ω² = 0
ω² = k_eff / m_eff
ω = √(k_eff / m_eff)
```

One cycle corresponds to 2π radians. Since ω = 2πf₀:

```text
f₀ = ω / (2π) = (1 / 2π) √(k_eff / m_eff)
```

**Unit check:** (N/m)/kg = s⁻². Taking its square root gives s⁻¹, as required for a frequency. The factor 2π converts angular frequency to cycles per second.

## 4 Why adding water lowers the pitch
Moving some water along with the walls increases the mode’s inertia. A simple added-mass approximation is:

```text
m_eff = m_g + αm_w
```

- **m_g** is the effective mass of the empty-glass mode, in kg, for the chosen coordinate x.
- **m_w** is the water’s total mass, in kg.
- **α** is a dimensionless participation factor: αm_w is the effective added mass due to the water’s motion. It is not simply a measured fraction of water moving rigidly with the glass.

Assume that the effective stiffness and glass-mode description stay approximately unchanged. Apply the same frequency formula to the empty and water-filled glass, then divide:

```text
f_empty = (1 / 2π) √(k_eff / m_g)
f_water ≈ (1 / 2π) √[k_eff / (m_g + αm_w)]

f_water / f_empty ≈ √[m_g / (m_g + αm_w)]
```

When αm_w is positive, the denominator inside the square root is larger than the numerator, so the ratio is below 1. The oscillation takes longer to complete each cycle, giving a lower frequency and pitch.

**Limiting check:** if the effective added mass approaches zero, the frequency ratio approaches 1. The empty-glass result is recovered.

### Example · An effective mass that doubles
Suppose the participating water adds effective mass equal to m_g, so αm_w = m_g. This is a hypothetical model condition, not a claim that equal total masses of water and glass will produce this result.

```text
f_water / f_empty ≈ √[m_g / (2m_g)]
                     = 1/√2 ≈ 0.707

For f_empty = 800 Hz:
f_water ≈ 800/√2 Hz ≈ 566 Hz
```

Doubling effective mass lowers the frequency to about 71% of its original value. It does not halve the frequency.

## 5 Why rubbing keeps it ringing
A tapped glass gradually becomes quiet because vibration energy leaves through sound radiation, internal losses, and interactions with the water and support. The [UNSW Music Acoustics FAQ](https://newt.phys.unsw.edu.au/jw/musFAQ.html) explains how finger friction can sustain a glass’s vibration through a stick–slip process, similar to a violin bow.

With suitable moisture, pressure, and motion, the moving finger briefly grips and then slips over the rim. Energy from your hand feeds the vibration. The ringing frequency is governed mainly by the glass–water system; it is not the number of times your finger circles the rim each second.

A schematic driven, damped version of the model is:

```text
m_eff d²x/dt² + b dx/dt + k_eff x = F_rub(t)
```

Here b is a positive damping coefficient in kg/s. The damping force is −b dx/dt: it opposes motion. F_rub(t), measured in newtons, represents the finger’s effective driving force on this mode. Actual friction depends on the finger–glass motion, so this equation is a simplified description rather than a prescribed sinusoidal driving mechanism.

At a steady amplitude, the finger supplies as much energy per cycle as the system loses. When you stop rubbing, that supply stops and the sound fades. Stronger damping can also shift the observed frequency away from the undamped model value.

## 6 What the model can and cannot predict
The added-mass model explains the **usual downward trend** in frequency when water is added. A real glass’s shape, wall thickness, water depth, holding position, and mode pattern affect the result. α can vary with fill level; stiffness and the mode pattern need not stay fixed. Water mass alone therefore does not determine an exact ringing frequency.

The main oscillator in this activity is the glass wall coupled to the liquid. Do not use an air-column length formula to predict its tone: blowing across a bottle’s opening excites a different kind of oscillator.

For a fuller experimental and theoretical treatment of the coupled glass–liquid vibration, see Jundt and colleagues’ [Vibrational modes of partly filled wine glasses](https://phys.unsw.edu.au/music/people/publications/Jundtetal2006.pdf). The schematic model and numerical example here are explanations, not measured results or publisher-verified worked answers.
