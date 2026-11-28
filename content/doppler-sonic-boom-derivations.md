@title: Deriving the Doppler effect and sonic booms
@subtitle: Follow two successive wave crests, measure their distances, then build a Mach cone from expanding circles.

## 1 Model, symbols, and prerequisites
This is **optional further reading for Section 12 of Wave Motion Notes**. Prerequisites are speed = distance/time, period and frequency, the wave equation, algebra, and right-triangle trigonometry. No calculus is required. You can complete the main notes without this page.

Use a uniform medium at rest, such as still air. Sound travels at speed **c relative to the medium**, independently of the source’s speed in this model. The source emits at a constant frequency **f_s**, with period **T_s = 1/f_s**. The observer receives frequency **f_o**, with arrival period **T_o = 1/f_o**. Frequencies are in hertz (Hz), times in seconds (s), speeds in metres per second (m/s), and wavelengths in metres (m).

For the Doppler derivations, motion is along the source–observer line, the source is subsonic, and the observer does not overtake the wave crests. Speeds of moving objects are measured relative to the medium. These are classical **sound** formulas; light needs a different, relativistic treatment.

## 2 Moving source: why the wavelength changes
Imagine a horn that moves right at speed u_s while the air and both listeners are stationary. Each crest travels at sound speed c, not c + u_s. A crest is a moving pressure maximum; a circle in a top-view drawing is a cross-section of its spherical wavefront.

### Step 1 — Emit the first crest
At time t = 0, the horn is at x = 0 and emits crest 1. The next crest will be emitted exactly one source period later: T_s = 1/f_s.

### Step 2 — Wait one period
At t = T_s, crest 1 has expanded to radius cT_s. Its right edge is at x = cT_s and its left edge is at x = −cT_s. Meanwhile the horn has moved to x = u_sT_s and emits crest 2 there. Crest 2 initially has zero radius. The old crest does not move with the horn.

DOPPLER_SPACING_FIGURE

### Step 3 — Measure the wavelength ahead
A wavelength is the separation of adjacent crests in the direction of wave travel, measured at the same instant. Just as crest 2 is emitted, its forward edge is at the horn; crest 1 is farther right. Subtract their positions.
```
λ_ahead = x₁ − x₂
        = cT_s − u_sT_s
        = (c − u_s)T_s
        = (c − u_s)/f_s
```
After another small time interval, both forward crests advance equally at c, so this spacing remains unchanged. It is not the distance travelled by the horn.

### Step 4 — Convert spacing into received frequency
At a stationary listener, the first crest must move one wavelength farther before the next crest reaches the listener. The time between arrivals is T_o = λ_ahead/c. Frequency is the reciprocal of this arrival time.
```
f_o = 1/T_o = c/λ_ahead
    = c / [(c − u_s)/f_s]
    = f_s c/(c − u_s)
```
The wavelength is shorter, so more crests arrive per second and the pitch increases.

### Step 5 — Repeat behind the moving source
The left edge of crest 1 is at −cT_s, and crest 2 starts at +u_sT_s. The distance between them is now the sum of the two distances.
```
λ_behind = u_sT_s − (−cT_s)
         = (c + u_s)T_s
         = (c + u_s)/f_s
f_o = c/λ_behind = f_s c/(c + u_s)
```
Behind the horn the wavelength is longer, so fewer crests arrive per second.

### Quick numerical picture
Use c = 300 m/s, u_s = 100 m/s and f_s = 100 Hz. In 0.010 s the crest travels 3 m and the horn travels 1 m. The front gap is 3 − 1 = 2 m; the rear gap is 3 + 1 = 4 m. A stationary listener ahead receives 300/2 = 150 Hz and one behind receives 300/4 = 75 Hz.

## 3 Moving observer: why the encounter rate changes
Now the horn stays still and the listener moves. Successive crests have the same spacing λ₀ = cT_s = c/f_s everywhere along the ray. The listener cannot change that spacing by moving.

### Step 1 — Start when one crest reaches the listener
At t = 0, the listener meets crest 1. The next crest (crest 2) is exactly one wavelength λ₀ to the left. All crests travel right.

### Step 2 — Follow the next crest and the listener
The listener moves left at speed u_o (toward the horn). At the next meeting, the second crest has moved right by cT_o and the listener has moved left by u_oT_o. Together they have closed the original gap λ₀.

OBSERVER_FIGURE

```
distance covered by crest + distance covered by listener = gap
cT_o + u_oT_o = λ₀
(c + u_o)T_o = λ₀
T_o = λ₀/(c + u_o)
```

### Step 3 — Turn arrival time into frequency
```
f_o = 1/T_o
    = (c + u_o)/λ₀
    = (c + u_o)/(c/f_s)
    = f_s(c + u_o)/c
```
The sound still moves at c in the air. The closing speed c + u_o is relative to the listener, not a new sound speed.

### Step 4 — What if the listener moves away?
The crest must catch up with a listener moving in the same direction. The crest travels cT_o, but the listener moves an additional u_oT_o away.
```
cT_o = λ₀ + u_oT_o
(c − u_o)T_o = λ₀
f_o = f_s(c − u_o)/c
```
For example, c = 300 m/s, f_s = 100 Hz and u_o = 100 m/s give λ₀ = 3 m. Moving toward the horn gives f_o = 400/3 ≈ 133 Hz; moving away gives 200/3 ≈ 66.7 Hz. The 3 m spacing never changes.

## 4 Combine the motions with an explicit sign convention
Choose **+x along the sound’s travel direction from source to observer** for the segment being studied. Let **v_s** and **v_o** be the signed source and observer velocities along this same axis, relative to the medium. A positive source velocity follows the outgoing sound; a positive observer velocity runs away with it. Require |v_s| < c and |v_o| < c here.

First use the source velocity to calculate the actual crest spacing in the air. Next use the observer velocity to calculate the rate at which those crests pass the observer. Do not add both speeds to the sound speed. Combining the two results gives:
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
### Step 1 — Freeze the motion at the current time
Imagine an aircraft moving right at twice the speed of sound. It emits disturbances at successive positions. At the current instant S, each earlier disturbance is a circle in the drawing (a sphere in 3D). Older circles are larger because they have had longer to expand. Their centres stay at the original emission positions, not at the aircraft.

### Step 2 — Connect the outside edges
The aircraft is outside all the earlier circles because u_s > c. A straight line from S can touch the outside edge of every circle without cutting through it. These two common tangent lines make the V-shaped cross-section of the Mach cone.

### Step 3 — Select one circle and draw a right triangle
Choose the earlier emission point O, and let Δt be the time since emission. The source travelled OS = u_sΔt. The sound travelled equally in every direction from O, giving radius OA = cΔt. A is where the upper tangent touches that circle.

MACH_CONE_FIGURE

### Step 4 — Apply the sine ratio
A radius drawn to a tangent is perpendicular to the tangent, so OA is perpendicular to SA. The right angle is at A, and OS is the hypotenuse. The angle μ is at S, between the backward horizontal direction SO and the cone surface SA. The side opposite μ is OA. Therefore:
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