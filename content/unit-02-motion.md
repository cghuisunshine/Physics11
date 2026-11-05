@chapter: Physics 11 · Unit 2
@title: Unit 2: Motion
@subtitle: Describe one-dimensional motion with words, vectors, graphs, and constant-acceleration equations.

## 2.1 Position, displacement, distance, and average velocity

### Learning goal
Distinguish the length of a path from a signed change in position.

### Understand the model
Choose an origin and a positive direction. Position x locates an object relative to that origin. Displacement Δx is final position minus initial position; it depends only on the endpoints. Distance is the total path length and is nonnegative. A trip that returns to its start has zero displacement, but can have a large distance.

Average velocity is displacement divided by elapsed time. Average speed is distance divided by elapsed time. These can differ whenever direction changes. The time interval must include the whole trip being described. Changing the origin shifts both positions by the same amount and leaves displacement unchanged; reversing the positive axis reverses the signs of vector components.

### Equations and units
```text
Δx = x_f - x_i
v_avg = Δx/Δt
speed_avg = total distance/Δt
```

### Worked example
A student walks from x = 2.0 m to x = 12.0 m, then to x = 5.0 m. The full trip takes 8.0 s.

1. Displacement: 5.0 - 2.0 = +3.0 m.
2. Distance: |12.0 - 2.0| + |5.0 - 12.0| = 10.0 + 7.0 = 17.0 m.
3. Average velocity is +3.0/8.0 = +0.38 m/s to two significant figures. Average speed is 17.0/8.0 = 2.1 m/s.

### Common mistakes
A zero average velocity does not mean the object stayed still. Distance and displacement have the same unit but describe different quantities.

### Your turn
1. A cyclist completes a 400 m loop in 80 s. Find average velocity and speed.
2. An object moves from -3 m to -8 m. Find its displacement.

### Solutions and reasoning
**1.** The displacement is zero, so average velocity is 0 m/s. Average speed is 400/80 = 5.0 m/s.

**2.** Δx = -8 - (-3) = -5 m. Its final position and displacement are both negative here, but they are different quantities.

### Textbook reading
Section 2-1, PDF page 49 (printed page 13).

## 2.2 Instantaneous velocity and interpreting position graphs

### Learning goal
Use a local graph slope to infer velocity and recognize a turning point.

### Understand the model
Average velocity describes an interval. Instantaneous velocity describes motion at a particular moment and is estimated by the slope of a tangent to a position-time curve. A steep tangent means a large speed; an upward tangent means positive velocity and a downward tangent means negative velocity. A horizontal tangent means zero instantaneous velocity.

A straight position-time line describes constant velocity. A curved line indicates changing velocity. At a smooth maximum or minimum of position, the velocity can be zero as the object reverses direction. A flat interval means the position stays fixed throughout that interval. Two objects at an intersection of their position-time curves are at the same position at that time, but need not have the same velocity.

### Equations and units
```text
v at an instant ≈ slope of tangent to x-t graph
speed = |v|
```

### Worked example
A tangent at t = 4.0 s passes through the graph points (2.0 s, 1.0 m) and (6.0 s, 9.0 m). Find the instantaneous velocity at 4.0 s.

1. Use points on the tangent line, not two widely separated points on the curved trajectory.
2. v = (9.0 - 1.0)/(6.0 - 2.0) = +2.0 m/s.
3. This is the local velocity estimate at 4.0 s. The positive sign describes direction; the instantaneous speed is 2.0 m/s.

### Common mistakes
Position being zero says only that the object is at the origin. It does not imply zero velocity. A graph can slope downward while all its position values remain positive.

### Your turn
1. A position-time graph is horizontal at x = 5 m from 2 to 6 s. Describe the motion.
2. A curve rises but becomes less steep. Is the object speeding up?

### Solutions and reasoning
**1.** The object rests at x = 5 m throughout that interval; v = 0.

**2.** No. Its positive velocity decreases in magnitude, so it slows while continuing in the positive direction.

### Textbook reading
Section 2-2, PDF page 54 (printed page 18).

## 2.3 Acceleration and the signs of motion

### Learning goal
Calculate acceleration and decide whether speed increases or decreases.

### Understand the model
Acceleration is the rate at which velocity changes. Its unit m/s² means that the velocity changes by a certain number of m/s each second. Average acceleration uses the total velocity change over an interval; instantaneous acceleration is the tangent slope on a velocity-time graph.

In one dimension, an object speeds up when velocity and acceleration have the same sign and slows when they have opposite signs. A negative acceleration can therefore speed up an object moving negatively. At the moment a ball turns around, its velocity can be zero while its acceleration remains nonzero. A change in direction is also a change in velocity even if the speed before and after has the same magnitude.

### Equations and units
```text
a_avg = (v_f - v_i)/Δt
Δv = v_f - v_i
```

### Worked example
A cart changes velocity from -4.0 m/s to -10.0 m/s in 3.0 s. Find acceleration and describe its speed.

1. Δv = -10.0 - (-4.0) = -6.0 m/s.
2. a_avg = -6.0/3.0 = -2.0 m/s².
3. Its speed increases from 4.0 to 10.0 m/s. Both velocity and acceleration point along the negative axis.

### Common mistakes
Avoid treating “deceleration” as automatically negative. Use a chosen axis and signed velocity and acceleration. A zero velocity at one instant is not proof of zero acceleration.

### Your turn
1. Velocity changes from +5 m/s to -5 m/s in 2 s. Find average acceleration.
2. v = -6 m/s and a = +2 m/s². Is the object speeding up at this instant?

### Solutions and reasoning
**1.** Δv = -10 m/s; a_avg = -5 m/s². Equal initial and final speeds do not mean zero acceleration.

**2.** It is slowing because the signs are opposite. It may later stop and reverse if the acceleration continues.

### Textbook reading
Section 2-3, PDF page 56 (printed page 20).

## 2.4 Constant-acceleration equations and their derivation

### Learning goal
Choose and apply a kinematic equation under the constant-acceleration assumption.

### Understand the model
For constant acceleration, the velocity-time graph is a straight line. Its slope gives v = v₀ + at. Displacement is the area under that line: a rectangle v₀t plus a triangle ½at². This gives Δx = v₀t + ½at². The same area is a trapezoid with average height (v₀ + v)/2. Eliminating time between the equations produces v² = v₀² + 2aΔx.

List the five quantities v₀, v, a, t, and Δx. Select an equation containing the unknown and the known quantities while omitting a quantity that is unavailable. These equations apply to a single interval of constant acceleration. Divide a trip into intervals when acceleration changes, and carry the ending velocity and position of one interval into the next.

### Equations and units
```text
v = v₀ + at
Δx = v₀t + ½at²
v² = v₀² + 2aΔx
Δx = ½(v₀ + v)t
Δx = vt - ½at²
```

### Worked example
A bicycle starts at 3.0 m/s and accelerates uniformly at 1.5 m/s² for 4.0 s. Find final velocity and displacement.

1. v = 3.0 + (1.5)(4.0) = 9.0 m/s.
2. Δx = (3.0)(4.0) + ½(1.5)(4.0)² = 12 + 12 = 24 m.
3. Check with average velocity: ½(3.0 + 9.0)(4.0) = 24 m. The two methods agree because acceleration is constant.

### Common mistakes
The arithmetic mean of initial and final velocities is not generally the average velocity when acceleration varies. Δx is signed displacement, not automatically distance.

### Your turn
1. A car goes from rest to 20.0 m/s in 5.00 s with constant acceleration. Find a and Δx.
2. A cart has v₀ = 10.0 m/s, a = -2.00 m/s², and Δx = 16.0 m before turning. Find v.

### Solutions and reasoning
**1.** a = 4.00 m/s²; Δx = ½(0 + 20.0)(5.00) = 50.0 m.

**2.** v² = 100 - 64 = 36.0. Before turning it still moves positively, so v = +6.00 m/s.

### Textbook reading
Section 2-4, PDF page 59 (printed page 23).

## 2.5 Signed graph areas and multi-stage trips

### Learning goal
Calculate displacement and distance separately from a velocity-time graph.

### Understand the model
A velocity-time graph describes direction through its sign. The signed area above the time axis adds positive displacement; area below adds negative displacement. Total distance is the sum of the magnitudes of those areas. When a straight segment crosses zero velocity, split the area at the crossing before finding distance.

For multi-stage motion, keep a running record of time, position, and velocity. A moving object can travel far but finish near its start. An acceleration-time graph has a different area meaning: its area changes velocity. Starting velocity is needed to reconstruct a velocity graph from an acceleration graph, and starting position is needed to reconstruct position from velocity.

### Equations and units
```text
Δx = signed area under v-t graph
distance = area under |v|-t graph
Δv = signed area under a-t graph
```

### Worked example
An object travels at +4.0 m/s for 3.0 s, then at -2.0 m/s for 2.0 s. Find its displacement, distance, and average velocity.

1. The two displacements are (+4.0)(3.0) = +12 m and (-2.0)(2.0) = -4.0 m.
2. Net displacement is +8.0 m. Distance is 12 + 4.0 = 16 m.
3. The full elapsed time is 5.0 s, so average velocity is +8.0/5.0 = +1.6 m/s. The idealized abrupt reversal represents two separate intervals.

### Common mistakes
Do not cancel negative graph areas when calculating distance. Do not confuse the area under a position graph with displacement.

### Your turn
1. Velocity falls linearly from +6 m/s to -6 m/s over 4 s. Find displacement and distance.
2. a = +3 m/s² for 2 s, starting at v₀ = -1 m/s. Find v.

### Solutions and reasoning
**1.** The two triangles each have magnitude ½(2)(6) = 6 m. Displacement is 0; distance is 12 m.

**2.** Δv = 6 m/s. v = -1 + 6 = +5 m/s.

### Textbook reading
Section 2-6, PDF page 65 (printed page 29).

## 2.6 Investigate and reflect

### Inquiry task
Record a toy cart or walking motion against a measured background. Use several equally spaced times to build a position-time table, then estimate interval velocities. Identify a nearly uniform segment and an accelerating segment. Explain the effect of video frame rate, camera angle, and position resolution on the conclusion. Never infer constant acceleration from only two positions.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

