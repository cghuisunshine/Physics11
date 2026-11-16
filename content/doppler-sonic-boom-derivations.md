@title: Deriving the Doppler effect and sonic booms
@subtitle: Follow successive wave crests to derive the sound-frequency formulas, then use a right triangle to find the Mach-cone angle.

## 1 Model, symbols, and prerequisites
This is **optional further reading for Section 12 of Wave Motion Notes**. Prerequisites are speed = distance/time, period and frequency, the wave equation, algebra, and right-triangle trigonometry. No calculus is required. You can complete the main notes without this page.

Use a uniform medium at rest, such as still air. Sound travels at speed **c relative to the medium**, independently of the source’s speed in this model. The source emits at a constant frequency **f_s**, with period **T_s = 1/f_s**. The observer receives frequency **f_o**, with arrival period **T_o = 1/f_o**. Frequencies are in hertz (Hz), times in seconds (s), speeds in metres per second (m/s), and wavelengths in metres (m).

For the Doppler derivations, motion is along the source–observer line, the source is subsonic, and the observer does not overtake the wave crests. Speeds of moving objects are measured relative to the medium. These are classical **sound** formulas; light needs a different, relativistic treatment.

## 2 Moving source: derive the changed wavelength
First hold the observer still and let the source move right at speed **u_s**, with 0 ≤ u_s < c. It emits one crest, waits one period T_s, then emits the next. In that interval, the first crest travels cT_s while the source advances u_sT_s. Subtract those distances ahead of the source and add them behind it.

DOPPLER_SPACING_FIGURE

### Ahead: the source approaches a stationary observer
The second crest starts closer to the first, so the forward wavelength is shorter:
```
λ_ahead = cT_s − u_sT_s
        = (c − u_s)T_s
        = (c − u_s)/f_s
```
The crests still pass the stationary observer at speed c. Use received frequency = crest speed / crest spacing:
```
f_o = c/λ_ahead
    = c / [(c − u_s)/f_s]
    = f_s c/(c − u_s)                 approaching source
```
The denominator is smaller than c, so f_o > f_s. Equivalently, the arrival period is T_o = λ_ahead/c = T_s(1 − u_s/c).

### Behind: the source recedes from a stationary observer
The source moves away from the earlier backward-going crest, increasing the spacing:
```
λ_behind = cT_s + u_sT_s = (c + u_s)/f_s
f_o = c/λ_behind = f_s c/(c + u_s)     receding source
```
Here f_o < f_s. The sound speed in still air remains c on both sides; the moving source changes the wavelength, not that propagation speed.

## 3 Moving observer: derive the crest encounter rate
Now hold the source still. The wavelength in the medium is **λ₀ = c/f_s**. Let the observer move at speed **u_o**, with 0 ≤ u_o < c. A moving observer does not change the emitted crest spacing.

When the observer moves toward the source, the observer and the arriving crests approach each other at c + u_o. In the time T_o between encounters, their relative motion closes one wavelength:
```
(c + u_o)T_o = λ₀
T_o = λ₀/(c + u_o)
f_o = 1/T_o = (c + u_o)/λ₀
    = f_s(c + u_o)/c                 approaching observer
```
When the observer moves away in the same direction as the arriving sound, the crests catch up at c − u_o instead:
```
(c − u_o)T_o = λ₀
f_o = f_s(c − u_o)/c                 receding observer
```
**c ± u_o is a speed relative to the observer.** It does not replace c as the sound speed relative to the medium. Source motion changes the spacing; observer motion changes how quickly that spacing is crossed.

## 4 Combine the motions with an explicit sign convention
Choose **+x along the sound’s travel direction from source to observer** for the segment being studied. Let **v_s** and **v_o** be the signed source and observer velocities along this same axis, relative to the medium. A positive source velocity follows the outgoing sound; a positive observer velocity runs away with it. Require |v_s| < c and |v_o| < c here.

The crest spacing is (c − v_s)/f_s. The speed at which crests overtake the observer is c − v_o. Combining the two results gives:
```
λ = (c − v_s)/f_s
f_o = (c − v_o)/λ
    = f_s(c − v_o)/(c − v_s)
```
If the source moves toward the observer at speed u_s and the observer moves toward the source at speed u_o, then v_s = +u_s and v_o = −u_o. Therefore f_o = f_s(c + u_o)/(c − u_s). If both move away from one another, the corresponding result is f_s(c − u_o)/(c + u_s).

These signs refer to the chosen direction of sound travel, not a memorized rule that every velocity is positive. Do not use this one-dimensional derivation unchanged for a passing source at an arbitrary angle. Source and observer motion relative to the medium matter separately; their relative speed alone is insufficient for the general sound problem.

## 5 What changes at and above Mach 1?
Define the **Mach number M = u_s/c**, where u_s is now the positive source speed through the medium. The sonic-boom discussion uses a source moving steadily along a straight line in otherwise uniform, still air.

- **M < 1:** an earlier sound front can advance ahead of the source. The source remains inside each earlier spherical front.
- **M = 1:** the ideal forward crest spacing (c − u_s)T_s reaches zero. The fronts meet at the source’s forward position in the ideal geometry.
- **M > 1:** the source outruns the earlier sound fronts. Their common envelope trails the source as a cone, called the Mach cone.

The approaching-source Doppler formula has a denominator tending to zero as u_s approaches c. **That is a limit of the subsonic periodic-wave model, not a prediction of an infinitely high audible pitch or a formula for a sonic boom.** Supersonic motion requires a different wavefront geometry. A real aircraft produces pressure disturbances and shocks; the construction below models their Mach-cone geometry using the ambient sound speed c, rather than calculating shock strength.

## 6 Derive the Mach-cone half-angle
Choose an earlier source position O and the current position S. Let **Δt > 0** be the elapsed time since the source was at O. A small sound disturbance emitted at O has expanded to a sphere of radius **r = cΔt**. Meanwhile the source has moved **OS = u_sΔt**.

In a cross-section through the flight path, draw a tangent from S to that circle, touching it at A. The radius OA is perpendicular to the tangent SA. Triangle OAS is therefore right-angled at A. Define **μ as the half-angle between the backward flight axis SO and the cone surface SA**.

MACH_CONE_FIGURE

In triangle OAS, OA is opposite μ and OS is the hypotenuse. Apply the sine ratio:
```
sin μ = OA/OS
      = cΔt/(u_sΔt)
      = c/u_s
      = 1/M

μ = arcsin(1/M), for M > 1
```
The elapsed time cancels, so disturbances emitted at different earlier times share the same cone angle for constant u_s and c. Rotating the two tangent lines around the flight axis produces the three-dimensional cone. **μ is the half-angle; the full opening angle is 2μ.** It is not measured from a line perpendicular to the flight path.

For M < 1, 1/M > 1, so no real tangent-cone angle exists. As M approaches 1 from above, μ approaches 90° in this ideal model; as M increases, μ gets smaller and the cone becomes narrower.

## 7 Why an observer hears a boom
The cone moves with the supersonic source. An observer hears a sonic boom when the associated shock surface sweeps across their position, causing a rapid pressure change. **A boom is not emitted only at the instant the source first passes Mach 1:** steady supersonic flight can keep producing a shock pattern, which different observers encounter at different times.

The cone is behind the source, so a ground observer can hear the boom after the aircraft has passed overhead. The Mach-angle derivation predicts geometry, not the loudness, pressure jump, or detailed waveform of a real boom. Aircraft shape and atmospheric conditions affect those details.

## 8 Worked examples and checks
### A moving horn
A 500 Hz horn moves at 30.0 m/s through still air with c = 343 m/s. Both listeners are stationary. Use the changed wavelength because the source is moving:
```
Ahead:  λ = (343 − 30.0)/500 = 0.626 m
        f_o = 343/0.626 ≈ 548 Hz
Behind: λ = (343 + 30.0)/500 = 0.746 m
        f_o = 343/0.746 ≈ 460 Hz
```
For comparison, a stationary 500 Hz source and an observer moving toward it at 30.0 m/s give f_o = 500(343 + 30.0)/343 ≈ 544 Hz. The closing speed is the same as in the approaching-source example, but the sound-frequency shifts differ because different objects move relative to the medium.

### A source at Mach 2
With c = 343 m/s and u_s = 686 m/s, first find M, then the cone half-angle:
```
M = u_s/c = 686/343 = 2.00
sin μ = 1/M = 0.500
μ = 30.0°; full opening angle = 60.0°
```
After Δt = 1.00 s, an earlier disturbance has radius 343 m and the source has travelled 686 m. Their ratio is 0.500, confirming the same angle.

- **Dimensions:** every Doppler speed ratio is dimensionless, leaving f_o in Hz; c/u_s is dimensionless, as sin μ must be.
- **Stationary limit:** setting both velocities to zero gives f_o = f_s.
- **Shared motion:** v_o = v_s gives f_o = f_s for this collinear, uniform-motion model.
- **Directions:** approaching raises frequency; receding lowers it under the stated subsonic assumptions.
- **Cone limit:** doubling a supersonic Mach number reduces sin μ; it does not increase the cone half-angle.
