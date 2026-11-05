@chapter: Physics 11 · Unit 5
@title: Unit 5: 2D Forces & Simple Machines
@subtitle: Resolve forces on ramps, analyze connected objects, and explain how simple machines exchange force for distance.

## 5.1 Angled forces and equilibrium

### Learning goal
Apply Newton’s second law independently along two axes.

### Understand the model
In two dimensions the same vector law becomes two scalar equations. Resolve every angled force along the chosen axes, keeping signs. If the object is in equilibrium, both acceleration components are zero, so both component sums vanish. Two forces with cancelling horizontal components can still have vertical components that add.

For a box pulled upward at an angle on a horizontal floor, the upward pull reduces N. If the pull points downward it increases N. This also changes friction. Work from the free-body diagram rather than memorizing N = mg. The angle in a component formula must refer to the axis that defines the adjacent side.

### Equations and units
```text
ΣFₓ = maₓ; ΣFᵧ = maᵧ
Fₓ = F cos θ; Fᵧ = F sin θ
level floor, aᵧ = 0, upward pull: N = mg - F sin θ
```

### Worked example
A 10.0 kg box is pulled with 40.0 N at 30.0° above horizontal on a frictionless level floor. Find N and horizontal acceleration.

1. Fₓ = 40.0 cos 30.0° = 34.6 N; Fᵧ = 20.0 N upward.
2. Vertical balance gives N = 98.1 - 20.0 = 78.1 N.
3. Horizontal dynamics gives aₓ = 34.641/10.0 = 3.46 m/s². The smaller N would also reduce friction if friction were present.

### Common mistakes
Do not use the full angled force in both component equations. Components reconstruct one force; they are not extra forces to add alongside it.

### Your turn
1. Two equal ropes make 30° with the horizontal and hold a 20.0 N load symmetrically. Find each tension.
2. What equations describe translational equilibrium?

### Solutions and reasoning
**1.** Horizontal components cancel. 2T sin 30° = 20.0 N gives T = 20.0 N.

**2.** ΣFₓ = 0 and ΣFᵧ = 0. An extended body may also require zero net torque for rotational equilibrium.

### Textbook reading
Section 3-1, PDF page 76 (printed page 40); Section 5-3, PDF page 142 (printed page 106).

## 5.2 Inclined planes without friction

### Learning goal
Choose axes along a ramp and resolve gravity relative to those axes.

### Understand the model
For a ramp tilted by θ above horizontal, choose x down the ramp and y perpendicular outward. Gravity is vertical, but its components in these rotated axes are mg sin θ down the ramp and mg cos θ into the ramp. This choice avoids resolving the normal force: it lies entirely along the perpendicular axis.

If the block remains on a straight fixed ramp, its perpendicular acceleration is zero. With no other perpendicular force, N = mg cos θ. On a frictionless ramp the downslope equation gives a = g sin θ, independent of mass. The expression becomes zero for a level ramp and approaches g for a nearly vertical ramp, useful limiting checks.

### Equations and units
```text
F_g,parallel = mg sin θ
F_g,perpendicular = mg cos θ
N = mg cos θ  (no other perpendicular forces)
a_down = g sin θ  (frictionless)
```

### Worked example
A 4.00 kg block slides down a frictionless 25.0° ramp. Find N and acceleration.

1. Perpendicular balance gives N = (4.00)(9.81) cos 25.0° = 35.6 N.
2. Downslope gravity is (4.00)(9.81) sin 25.0° = 16.6 N.
3. a = 16.584/4.00 = 4.15 m/s² down the ramp. Gravity still points vertically; the components are bookkeeping along rotated axes.

### Common mistakes
N is not mg on a ramp. Do not draw mg sin θ and mg cos θ as extra forces in addition to mg; show either the original force or a clear component decomposition.

### Your turn
1. What is acceleration down a frictionless 30.0° ramp?
2. Does doubling block mass double the ramp acceleration?

### Solutions and reasoning
**1.** a = 9.81 sin 30.0° = 4.91 m/s².

**2.** No. Both the downslope gravitational force and inertia double, leaving a = g sin θ unchanged.

### Textbook reading
Section 5-3, PDF page 142 (printed page 106); Section 6-1, PDF page 160 (printed page 124).

## 5.3 Friction on ramps and the threshold of slipping

### Learning goal
Decide whether a block remains at rest and calculate acceleration after sliding begins.

### Understand the model
A resting block on a ramp tends to slide down because of mg sin θ. Static friction acts up the ramp to prevent that tendency if it can supply enough force. Under the simple ramp model, the threshold is mg sin θ = μₛmg cos θ, giving tan θ = μₛ. Below the threshold, actual friction is mg sin θ rather than its maximum.

If a block slides down, kinetic friction points up the ramp and the acceleration along the downward axis is g(sin θ - μₖ cos θ). If it slides up, kinetic friction points down, so gravity and friction both oppose the upward velocity. The direction of kinetic friction comes from the current sliding direction, not from a memorized picture.

### Equations and units
```text
rest possible if mg sin θ ≤ μₛmg cos θ
tan θ_threshold = μₛ
sliding down: a = g(sin θ - μₖ cos θ)
```

### Worked example
A block has μₛ = 0.50 and μₖ = 0.30 on a 30.0° ramp. Released from rest, does it slide? Find its acceleration if it does.

1. tan 30.0° = 0.577, which exceeds μₛ = 0.50, so static friction cannot hold it.
2. Once sliding down, a = 9.81[sin 30.0° - 0.30 cos 30.0°].
3. a = 2.36 m/s² down the ramp. The static coefficient determines the onset, while the kinetic coefficient determines this sliding acceleration.

### Common mistakes
Do not apply kinetic friction before checking whether the object slides. A downslope-moving block can slow down on a shallow ramp if friction exceeds the downslope weight component.

### Your turn
1. Find the threshold angle if μₛ = 0.40.
2. A block slides upward on a ramp. Which direction does friction act?

### Solutions and reasoning
**1.** θ = tan⁻¹(0.40) = 21.8° in this ideal dry-friction model.

**2.** Down the ramp, opposing upward sliding. Gravity’s parallel component also points down.

### Textbook reading
Section 6-1, PDF page 160 (printed page 124).

## 5.4 Connected masses and ideal pulleys

### Learning goal
Write one equation per body and use the rope constraint to solve a system.

### Understand the model
For a taut, inextensible rope over an ideal pulley, connected objects have matching acceleration magnitudes along the rope. Draw a separate free-body diagram for each mass. Choose a positive direction for each that agrees with one assumed system motion. The same tension magnitude appears in both equations under the massless-rope, massless-pulley, frictionless assumptions.

Adding the equations eliminates internal tension and gives the acceleration of the system. Substitute back to find tension. If the calculated acceleration is negative, the actual acceleration is opposite the assumed positive directions. Tension can differ from either mass’s weight because the masses accelerate.

### Equations and units
```text
Atwood system, m₂ > m₁:
m₂g - T = m₂a
T - m₁g = m₁a
a = (m₂ - m₁)g/(m₁ + m₂)
```

### Worked example
An ideal pulley connects m₁ = 2.00 kg and m₂ = 3.00 kg. Find acceleration and rope tension.

1. Assume m₂ accelerates down and m₁ up. Adding their equations gives (3.00 - 2.00)g = (3.00 + 2.00)a.
2. a = 1.962 m/s², so m₂ accelerates downward at 1.96 m/s².
3. T = m₁(g + a) = 2.00(9.81 + 1.962) = 23.5 N. Check m₂: m₂(g - a) gives the same tension.

### Common mistakes
The two masses have the same acceleration magnitude, not the same upward-signed acceleration. Keep each body’s chosen axis explicit. Do not set T equal to mg for an accelerating mass.

### Your turn
1. A 2.00 kg cart on a frictionless table connects to a 1.00 kg hanging mass. Find a and T.
2. In an ideal Atwood system with equal masses and no other forces, what is a?

### Solutions and reasoning
**1.** For the cart T = 2a; for the hanging mass 9.81 - T = a. Thus a = 3.27 m/s² and T = 6.54 N.

**2.** a = 0. The masses may remain at rest or move at constant speed if already moving.

### Textbook reading
Section 5-3, PDF page 142 (printed page 106).

## 5.5 Simple machines, mechanical advantage, and levers

### Learning goal
Relate force advantage to travel distance and use torque balance for an ideal lever.

### Understand the model
A simple machine changes the magnitude or direction of an applied force. Ramps, levers, pulleys, wedges, screws, and wheels with axles exchange force for distance. A smaller input force normally acts through a larger distance; an ideal machine conserves work rather than creating energy. Actual friction and deformation reduce useful output.

Mechanical advantage is output force divided by input force. Ideal mechanical advantage is input distance divided by output distance. A ramp has ideal advantage L/h. A frictionless movable pulley supporting a load with n equivalent vertical rope segments has ideal advantage n, and the pulling end must move n times the load’s rise. For a lever at rest, torque balance uses force times perpendicular moment arm. This is an algebra-level application of the textbook’s static equilibrium chapter.

### Equations and units
```text
MA = F_out/F_in
IMA = d_in/d_out
ideal ramp: IMA = L/h
τ = F × perpendicular moment arm
ideal lever: F_in r_in = F_out r_out
efficiency = (MA/IMA) × 100%
```

### Worked example
An ideal lever has an input arm of 0.80 m and output arm of 0.20 m. What input force balances a 200 N load?

1. Torque balance: F_in(0.80) = (200)(0.20).
2. F_in = 50 N, giving MA = 200/50 = 4.
3. For a small rotation the input moves four times as far as the load. If the load rises 0.050 m, ideal input travel is 0.20 m; both works equal 10 J.

### Common mistakes
Mechanical advantage greater than one does not imply efficiency greater than 100%. Use perpendicular moment arms, not an arbitrary distance to a force’s application point.

### Your turn
1. A ramp is 3.0 m long and 0.60 m high. Find ideal advantage and ideal force for a 300 N load.
2. A machine has IMA = 4.0 and MA = 3.0. Find efficiency.

### Solutions and reasoning
**1.** IMA = 3.0/0.60 = 5.0; ideal force = 300/5.0 = 60 N.

**2.** Efficiency = (3.0/4.0) × 100% = 75%.

### Textbook reading
Section 7-2, PDF page 187 (printed page 151); Section 7-6, PDF page 202 (printed page 166); Section 12-1, PDF page 363 (printed page 327); Section 12-2, PDF page 368 (printed page 332).

## 5.6 Investigate and reflect

### Inquiry task
Compare lifting a small load vertically with pulling it up a gentle ramp. Measure force and travel distance, then compare input work with the change in gravitational potential energy. Research an example of a simple machine using a publicly shared source from a local First Nation or an Indigenous-led organization. Cite the community and source, respect sharing protocols, and explain the mechanical principle without treating diverse First Peoples as one culture.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

