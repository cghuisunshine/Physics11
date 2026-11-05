@chapter: Physics 11 · Unit 3
@title: Unit 3: Projectiles
@subtitle: Separate horizontal and vertical motion, then reconnect them through a shared flight time.

## 3.1 Vertical motion and free fall

### Learning goal
Solve upward and downward motion with a consistent sign convention.

### Understand the model
Free fall means gravity is the only significant force after release. Near Earth’s surface, use approximately constant downward acceleration g = 9.81 m/s² unless the problem assigns another value. If upward is positive, aᵧ = -g for the entire flight: ascent, peak, and descent. Mass does not appear in the ideal kinematic equations.

An upward-moving ball slows because its velocity and acceleration oppose one another. At the highest point vᵧ = 0, but aᵧ remains -g. During descent both are negative, so the ball speeds up. Use the displacement between the stated initial and final levels, and do not assume that the landing level equals the launch level.

### Equations and units
```text
vᵧ = v₀ᵧ - gt
Δy = v₀ᵧt - ½gt²
vᵧ² = v₀ᵧ² - 2gΔy
```

### Worked example
A ball is thrown straight up at 14.0 m/s. Find the time to the peak and the height gained.

1. At the peak, vᵧ = 0. Thus t = 14.0/9.81 = 1.43 s.
2. 0 = 14.0² - 2(9.81)Δy, giving Δy = 9.99 m.
3. If it later returns to the launch level with negligible drag, the total time is 2.85 s and the returning velocity is -14.0 m/s. The symmetry applies only between equal heights.

### Common mistakes
Gravity does not switch off at the peak. The acceleration does not change sign when the ball changes direction. Real air resistance can spoil the mass independence and symmetry.

### Your turn
1. A ball is dropped from rest through 20.0 m. Find fall time and impact speed.
2. At the highest point of a vertical throw, what are v and a?

### Solutions and reasoning
**1.** With upward positive, -20.0 = -½gt², so t = 2.02 s. vᵧ = -19.8 m/s and speed is 19.8 m/s.

**2.** v = 0 for that instant, while a = 9.81 m/s² downward in the ideal model.

### Textbook reading
Section 2-5, PDF page 63 (printed page 27).

## 3.2 Independent components and horizontal launches

### Learning goal
Find flight time vertically and range horizontally for a horizontal launch.

### Understand the model
A projectile is an object moving after launch under gravity alone in the ideal model. Resolve its motion into perpendicular axes. Gravity supplies vertical acceleration but no horizontal acceleration, so the horizontal velocity remains constant while the vertical velocity changes. Both components use the same time because they describe the same object.

For a horizontal launch, v₀ᵧ = 0. Use the height to determine the time to land, then multiply that time by the horizontal velocity. A ball dropped and a ball launched horizontally from the same height land together under the ideal assumptions, even though their horizontal positions differ. The initial push is not a force that continues acting throughout flight.

### Equations and units
```text
aₓ = 0; aᵧ = -g
Δx = v₀ₓt
Δy = v₀ᵧt - ½gt²
for horizontal launch from height h: t = √(2h/g)
```

### Worked example
A ball leaves a 1.25 m high table horizontally at 4.00 m/s. How far from the edge does it land?

1. Set the launch point at y = 0 and the floor at y = -1.25 m.
2. Vertical motion gives -1.25 = -½(9.81)t², so t = 0.505 s.
3. Δx = (4.00)(0.505) = 2.02 m. The horizontal speed changes the range, not the fall time in this model.

### Common mistakes
Do not use the total launch speed as a vertical initial speed. Do not invent a horizontal acceleration when air resistance is neglected.

### Your turn
1. A horizontal launch speed doubles from the same height. What happens to flight time and range?
2. A ball launches horizontally at 6.0 m/s from 5.0 m high. Find the range.

### Solutions and reasoning
**1.** Flight time is unchanged; range doubles.

**2.** t = √(10.0/9.81) ≈ 1.01 s; range ≈ 6.1 m.

### Textbook reading
Section 4-3, PDF page 103 (printed page 67); Section 4-4, PDF page 106 (printed page 70).

## 3.3 Angled launches and equal-height range

### Learning goal
Resolve an angled launch and identify when the shortcut range formula applies.

### Understand the model
For launch speed v₀ at angle θ above horizontal, use v₀ₓ = v₀ cos θ and v₀ᵧ = v₀ sin θ. Vertical motion determines when the object reaches a chosen height. Horizontal motion then determines where it is. At the peak, only the vertical component is zero; an angled projectile normally retains horizontal speed.

If landing and launch heights are equal, the nonzero root of Δy = 0 gives t = 2v₀ sin θ/g. Substitution into Δx = v₀ cos θ × t gives R = v₀² sin(2θ)/g. The ideal range is largest at 45°, and complementary launch angles have equal ranges. These conclusions require equal heights, fixed launch speed, uniform gravity, and negligible drag.

### Equations and units
```text
v₀ₓ = v₀ cos θ; v₀ᵧ = v₀ sin θ
t_flight = 2v₀ sin θ/g  (equal heights)
R = v₀² sin(2θ)/g  (equal heights)
h_max above launch = v₀² sin²θ/(2g)
```

### Worked example
Launch a ball at 20.0 m/s and 30.0°. It lands at the launch height. Find time, range, and maximum height.

1. v₀ₓ = 17.3 m/s and v₀ᵧ = 10.0 m/s.
2. Flight time is 2(10.0)/9.81 = 2.04 s; range is 17.3205 × 2.0387 = 35.3 m.
3. The maximum height above launch is 10.0²/[2(9.81)] = 5.10 m. At the peak the speed is still 17.3 m/s.

### Common mistakes
The 45° maximum-range statement is conditional. Never apply the equal-height range formula to a cliff launch without checking the geometry.

### Your turn
1. For fixed speed at equal heights, compare 25° and 65° launches.
2. A 10.0 m/s launch at 45.0° returns to its starting height. Find range.

### Solutions and reasoning
**1.** They have equal ideal ranges because sin 50° = sin 130°. The 65° launch has a greater height and flight time.

**2.** R = 10.0² sin 90°/9.81 = 10.2 m.

### Textbook reading
Section 4-4, PDF page 106 (printed page 70).

## 3.4 Unequal launch and landing heights

### Learning goal
Solve the vertical quadratic and select the physical flight time.

### Understand the model
When landing height differs from launch height, begin with the full vertical displacement equation. Rearrange it to a quadratic in time. The quadratic may describe crossings of a height both before and after the peak, or may produce a negative time outside the chosen motion interval. Read the roots in the context of the question.

Once time is known, find horizontal displacement using the horizontal component. Do not replace the vertical displacement by the distance travelled up and down; kinematics uses endpoints. If a projectile lands above its launch point, first check whether its maximum height is high enough to reach that level. A negative discriminant means the chosen height is unreachable within the ideal model.

### Equations and units
```text
½gt² - v₀ᵧt + Δy = 0
t = [v₀ᵧ ± √(v₀ᵧ² - 2gΔy)]/g
Δx = v₀ₓt
```

### Worked example
A ball leaves a platform 10.0 m above the ground at 15.0 m/s and 30.0° above horizontal. Find its landing distance.

1. Components: v₀ₓ = 15.0 cos 30.0° = 12.99 m/s; v₀ᵧ = 7.50 m/s. The ground has Δy = -10.0 m.
2. Solve 4.905t² - 7.50t - 10.0 = 0. Roots are about 2.38 s and -0.855 s.
3. The future landing uses t = 2.38 s. Range is 12.99 × 2.385 ≈ 31.0 m. The negative root is outside the flight after launch.

### Common mistakes
Landing below the start means Δy is negative if up is positive. Do not automatically reject one of two positive roots: they may represent ascent and descent through the same height.

### Your turn
1. A ball is launched vertically at 10.0 m/s. Can it reach 6.0 m above launch?
2. A horizontal projectile lands 20.0 m away after 2.00 s. Find launch speed and drop height.

### Solutions and reasoning
**1.** No. h_max = 100/(2 × 9.81) = 5.10 m, which is below 6.0 m.

**2.** v₀ₓ = 20.0/2.00 = 10.0 m/s. h = ½(9.81)(2.00)² = 19.6 m.

### Textbook reading
Section 4-4, PDF page 106 (printed page 70).

## 3.5 Velocity during flight and evaluating the model

### Learning goal
Reconstruct the velocity vector at a chosen time and explain ideal-model limitations.

### Understand the model
The velocity vector points tangent to the trajectory. Its horizontal component stays constant in the ideal model and its vertical component changes linearly. Use the components to calculate the speed and an angle above or below horizontal. The trajectory curves because the direction of velocity changes, while acceleration remains downward.

The textbook’s projectile model treats the object as a particle and neglects air resistance. It works best when drag and lift are small relative to weight. A feather, a spinning ball, and a fast lightweight object can differ substantially from this model. An experiment should report those limitations, separate uncertainty in measurements from systematic model disagreement, and avoid claiming that a single trial proves the ideal law.

### Equations and units
```text
vₓ = v₀ₓ
vᵧ = v₀ᵧ - gt
speed = √(vₓ² + vᵧ²)
velocity angle: tan φ = vᵧ/vₓ  (check signs)
```

### Worked example
A horizontal projectile has v₀ₓ = 8.00 m/s. Find its velocity 0.600 s after launch, assuming it is still airborne.

1. vₓ = +8.00 m/s; vᵧ = 0 - (9.81)(0.600) = -5.89 m/s.
2. Speed is √(8.00² + 5.886²) = 9.93 m/s.
3. φ = tan⁻¹(5.886/8.00) = 36.3° below horizontal. State both magnitude and direction to specify the velocity.

### Common mistakes
The horizontal velocity is not the whole speed except when vᵧ = 0. A trajectory drawing is a position picture, not a velocity-time graph.

### Your turn
1. What is acceleration at the peak of an angled ideal projectile?
2. What observation would suggest drag matters?

### Solutions and reasoning
**1.** aₓ = 0 and aᵧ = -g; the full acceleration is downward and nonzero.

**2.** A systematic decline of horizontal speed after release, beyond measurement uncertainty, contradicts the no-drag assumption.

### Textbook reading
Section 4-2, PDF page 100 (printed page 64); Section 4-4, PDF page 106 (printed page 70).

## 3.6 Investigate and reflect

### Inquiry task
Use a soft ball rolling off a low surface, with an adult or teacher supervising the setup. Predict its landing distance from height and horizontal launch speed. Record several trials and compare with the no-drag model. Discuss uncertainty in the launch point and speed. An alternative is to collect simulated data from the trajectory explorer and clearly label it as model data, not an experiment.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

