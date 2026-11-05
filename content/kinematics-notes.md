@chapter: Physics 11
@title: Kinematics
@subtitle: Motion, acceleration, free fall, motion graphs, and projectiles.

# Kinematics

## 1 Position, displacement, and distance
### The study of motion
**Kinematics is the study of motion.**

### Position and displacement
**Position** is a vector describing where an object is relative to an origin.

**Displacement** is the change in position. It is represented by a vector joining the initial and final positions.

### Distance
**Distance** is the length of a path. Distance is a scalar.

For a straight path travelled without reversing direction, distance is equal to the **magnitude of the displacement**. This makes the source's comparison between a scalar and a vector precise.

### Practice example: a dog around a city block
A dog walks from corner to corner around a square city block of side length **100 m**. Calculate the distance travelled and the displacement.

The source diagram shows the dog travelling along two adjacent sides: up the left side and right across the top.

**Worked answer**

Distance follows the two sides: **100 + 100 = 200 m**. Displacement is the diagonal from the starting corner to the opposite corner.
```
|Δr| = √(100² + 100²) = 141.4 m
θ = tan⁻¹(100 / 100) = 45°
```
Displacement: **about 141 m, 45° above the horizontal to the right**, with components 100 m right and 100 m up in the diagram.

## 2 Speed, velocity, and uniform motion
### Speed
**Speed** is the rate at which distance is travelled. Speed is a scalar.
```
v = d / t
```
- v: speed, in m/s
- d: distance, in m
- t: time, in s

If speed is not constant, this equation gives **average speed**.

### Velocity
**Velocity** is the rate at which an object changes its position. Velocity is a vector.
```
v⃗ = d⃗ / t
```
- v⃗: velocity, in m/s
- d⃗: displacement, in m
- t: time, in s

If velocity is not constant, this equation gives **average velocity**.

### Uniform motion
**Uniform motion** refers to motion at a constant velocity.

### Practice example: sunlight
Light from the Sun takes **8½ minutes** to reach Earth. If light travels at **3.00 × 10⁸ m/s**, how far away is the Sun?

**Worked answer**

```
t = 8.5 × 60 = 510 s
d = vt = (3.00 × 10⁸)(510)
  = 1.53 × 10¹¹ m
```
The Sun is **approximately 1.53 × 10¹¹ m away**, or 1.53 × 10⁸ km.

### Practice example: four laps
A student completes **four laps** around a **400 m track** in **390 s**. What are the student's average speed and velocity?

**Worked answer**

```
Distance = 4 × 400 = 1600 m
Average speed = 1600 / 390 = 4.10 m/s
Displacement = 0 m
Average velocity = 0 / 390 = 0 m/s
```
Average speed is **4.1 m/s**. Average velocity is **0 m/s**, because the student finishes at the starting point.

## 3 Acceleration
### Change in velocity
**Acceleration** is the rate of change of velocity. Acceleration is a vector.
```
a⃗ = Δv⃗ / t = (v⃗f − v⃗i) / t
```
**Delta (Δ)** means change in: final minus initial.
- a⃗: acceleration, in m/s²
- Δv⃗: change in velocity, in m/s
- v⃗f: final velocity, in m/s
- v⃗i: initial velocity, in m/s
- t: elapsed time, in s

## 4 Motion with constant acceleration
### Average velocity
For motion with constant acceleration, the average velocity can be expressed in the following forms:
```
v_avg = d / t
v_avg = (v_i + v_f) / 2
```
If acceleration is not constant, **v_avg = (v_i + v_f) / 2 does not generally apply**.

- v_avg: average velocity, in m/s
- v_i: initial velocity, in m/s
- v_f: final velocity, in m/s
- d: displacement, in m
- t: elapsed time, in s

### Four useful equations
Using the three basic equations for motion with constant acceleration, we can form four useful equations:
```
v_f = v_i + at
d = [(v_i + v_f) / 2]t
v_f² = v_i² + 2ad
d = v_i t + ½at²
```
a is acceleration, in m/s². The other symbols have the meanings listed above. These equations use **signed quantities along one chosen axis**.

### Practice example: a sprinter
A sprinter, starting from rest, accelerates at **1.1 m/s²** for the entirety of a **100 m dash**. What is his final velocity?

**Worked answer**

Take the running direction as positive.
```
v_f² = v_i² + 2ad
v_f = √[0² + 2(1.1)(100)]
    = 14.83 m/s
```
Final velocity: **15 m/s in the running direction**.

### The source's five solving steps
1. Identify your unknown along with three givens.
2. Choose the equation with the unknown and three givens.
3. Simplify by plugging in any zeros.
4. Algebraically solve for the unknown.
5. Plug in values.

### Practice example: Rammus
Rammus is powerballing with an acceleration of **1.4 m/s²**. If he starts from rest and powerballs for **7.0 s**, how far does he travel?

**Worked answer**

```
d = v_i t + ½at²
  = 0 + ½(1.4)(7.0)²
  = 34.3 m
```
He travels **34 m**, to two significant figures.

### Practice example: a police car
A police car increases its speed from **50 km/h to 90 km/h** in **2.5 s**. What was its acceleration?

**Worked answer**

Assume straight-line motion without a change in direction. Convert the speed change to m/s before dividing by seconds.
```
Δv = (90 − 50) / 3.6 = 11.11 m/s
a = Δv / t = 11.11 / 2.5 = 4.444 m/s²
```
Acceleration: **4.4 m/s² in the direction of travel**.

## 5 Free fall and problem-solving tips
### Acceleration due to gravity
**Acceleration due to gravity, g**, is the acceleration of free fall due to gravitational force.

On the surface of Earth, **g = 9.8 m/s² down**. The signed acceleration can be positive or negative, depending on the chosen positive direction.

### Choose a direction convention
Before listing your givens, decide on one direction to be positive. All vectors in the opposite direction will be negative.

### Givens that are not explicitly stated
- Free fall: a = 9.8 m/s² down.
- Starts at rest: v_i = 0 m/s.
- Object is dropped from a stationary position: v_i = 0 m/s.
- An object moving vertically in free fall reaches its peak: v_f = 0 m/s.
- An object initially moving upwards returns to its original position or height: v_f = −v_i.

The peak and return-to-height statements above refer to **vertical velocity**. For a projectile with horizontal motion, horizontal velocity can remain nonzero at the peak.

### Impact velocity
If you are asked for the velocity at which an object hits the ground, you are looking for its velocity **before stopping**, so v_f is not zero.

### Practice example: a hammer
How far will a hammer fall after **2.0 s** if it is dropped from rest?

**Worked answer**

Choose down as positive and use g = 9.8 m/s².
```
d = ½gt² = ½(9.8)(2.0)² = 19.6 m
```
The hammer falls **about 20 m**.

### Practice example: an upward bullet
A bullet is fired from a gun upwards at **700 m/s**. What maximum height will it reach?

**Worked answer**

Use the notes' ideal model with no air resistance and constant gravity. Choose up as positive, so a = −9.8 m/s² and the vertical velocity at the peak is zero.
```
v_f² = v_i² + 2ah
0 = 700² − 2(9.8)h
h = 700² / [2(9.8)] = 25 000 m
```
Maximum height above the launch point: **2.5 × 10⁴ m (25 km)** in this ideal model.

### Practice example: a ball returning to a hand
A boy throws a ball upwards at a speed of **15 m/s**. How long does it take to return to his hand?

**Worked answer**

At the original height, the final velocity is −15 m/s if up is positive.
```
t = (v_f − v_i) / a
  = (−15 − 15) / (−9.8)
  = 3.061 s
```
The ball returns in **3.1 s**. The upward and downward parts each take about 1.53 s.

## 6 Position versus time graphs
### Reading straight segments
Position versus time graphs can also be labelled displacement versus time graphs.
- An upward straight segment shows motion in the positive direction at a steady speed.
- A horizontal segment shows an object at rest.
- A downward straight segment shows motion back in the negative direction at a steady speed.

### Slope gives velocity
The **slope of a d versus t graph is equal to velocity**.

Average velocity is the slope of a straight line joining two points on a d versus t graph.

### Practice example: piecewise motion
Calculate the velocity for each part of the position versus time graph from source page 12.

The graph rises from **(0 s, 0 m) to (2 s, 20 m)**, remains at **20 m until 4 s**, and then decreases to **about 5 m at 8 s**.

**Worked answer**

Velocity is the slope of each position-time segment.
1. From 0 to 2 s: (20 − 0)/(2 − 0) = **+10 m/s**.
2. From 2 to 4 s: (20 − 20)/(4 − 2) = **0 m/s**; the object is at rest.
3. From 4 to 8 s: (5 − 20)/(8 − 4) = **approximately −3.75 m/s**, in the negative direction.
The last value is approximate because the endpoint is read from the drawn graph. At a sharp corner, use the slope on the relevant side rather than assigning one instantaneous velocity to the corner.

### Curves and instantaneous velocity
A curve on a d versus t graph describes acceleration. For a curved graph, estimate the slope using a tangent line.

The slope of a tangent line on a d versus t graph is the **instantaneous velocity**.

## 7 Curved position graphs
### Four parts of the source curve
The diagram on source page 13 illustrates four types of motion:
1. Positive slope growing steeper: speeding up in the positive direction.
2. Positive slope becoming less steep: slowing down in the positive direction.
3. Negative slope growing steeper in magnitude: speeding up backwards.
4. Negative slope becoming less steep in magnitude: slowing down backwards.

For negative slopes, “increasing” and “decreasing” in the handwritten labels refer to **steepness or magnitude**. A slope becoming more negative has increasing magnitude.

### Practice example: instantaneous and average velocity
Using the curved position versus time graph on source page 13, determine the **instantaneous velocity at 4.0 s** and the **average velocity from 0 to 8.0 s**.

The graph rises from the origin towards approximately **20 m at 8 s**, with a slope that becomes less steep. Use the original graph to draw the required tangent and secant.

**Worked answer**

At 4.0 s, draw a tangent to the curve. An approximate tangent through (2 s, 11 m) and (6 s, 19 m) gives:
```
v(4.0 s) ≈ (19 − 11) / (6 − 2)
         ≈ +2 m/s
```
The instantaneous velocity is **approximately +2 m/s**. This is a graphical estimate; the handwritten curve does not specify an exact mathematical function.
For the whole interval, use the endpoints rather than the tangent:
```
v_avg = [d(8) − d(0)] / (8 − 0)
      ≈ (20 − 0) / 8
      ≈ +2.5 m/s
```
Average velocity: **approximately +2.5 m/s**.

## 8 Velocity versus time graphs
### Reading the source diagram
- Constant positive acceleration with positive velocity: speeding up forwards.
- A horizontal line: constant velocity.
- Constant negative acceleration with positive velocity: slowing down forwards.
- Constant negative acceleration with negative velocity: speeding up backwards.
- Constant positive acceleration with negative velocity: slowing down backwards.

### Slope and area
The **slope of a v versus t graph equals acceleration**.

The **signed area under a v versus t graph equals displacement**. Area above the time axis is positive displacement; area below the time axis is negative displacement.

### Practice example: a velocity graph
Use the graph from source page 15 to calculate:
1. The acceleration at t = 4 s.
2. The average acceleration from 0 to 14 s.
3. The total displacement.
4. The total distance travelled.
5. The average velocity from 0 to 14 s.
6. The average speed from 0 to 14 s.

The graph consists of straight segments from **(0 s, +10 m/s) to (8 s, −10 m/s)**, then to **(12 s, −10 m/s)**, then to **(14 s, 0 m/s)**. It crosses v = 0 at t = 4 s.

**Worked answer**

Use slopes for acceleration, signed areas for displacement, and the magnitudes of all areas for distance.
1. Acceleration at 4 s: (−10 − 10)/(8 − 0) = **−2.5 m/s²**. Velocity is zero at that instant, but acceleration is not.
2. Average acceleration: [v(14) − v(0)]/14 = (0 − 10)/14 = **−0.714 m/s²**.
3. Signed areas: +20 m from 0–4 s, −20 m from 4–8 s, −40 m from 8–12 s, and −10 m from 12–14 s. Total displacement = **−50 m**.
4. Total distance = 20 + 20 + 40 + 10 = **90 m**.
5. Average velocity = −50/14 = **−3.57 m/s**.
6. Average speed = 90/14 = **6.43 m/s**.

## 9 Projectile motion
### Independent components
The notes describe **projectile motion** as free-fall motion that has a horizontal component of velocity. Examples include an angled throw and an object launched horizontally from a ledge.

The motion of a projectile can be analyzed by looking at horizontal and vertical components separately. Each direction is independent of the other.

### Horizontal motion
The horizontal component follows uniform motion:
```
v_x = constant
d_x = v_x t
```

### Vertical motion
The vertical component follows uniformly accelerated motion, with **a_y = 9.8 m/s² down**.
```
v_yf = v_yi + a_y t
d_y = [(v_yi + v_yf) / 2]t
v_yf² = v_yi² + 2a_y d_y
d_y = v_yi t + ½a_y t²
```

### Time links the components
**Time links the horizontal and vertical motion.** The trajectory is parabolic, and the horizontal displacement d_x is the range.

For a launch speed v_i at an angle θ above the horizontal:
```
v_x = v_i cos θ
v_yi = v_i sin θ
```

These are the source's ideal-motion equations: **air resistance is neglected and gravity is treated as constant**.

## 10 Worked example: a ball off a cliff
### The question
A soccer ball is kicked off a **100 m cliff** with a velocity of **20 m/s to the right**.
1. How long will it spend in the air?
2. How far from the base of the cliff will it land?
3. What will be its velocity right before it hits the ground?

### Direction convention and givens
The source chooses **right and down as positive**.
```
Horizontal: v_x = 20 m/s; t = ?; d_x = ?
Vertical:   v_yi = 0; a_y = +9.8 m/s²;
            d_y = +100 m; t = ?
```

### Part 1: time in the air
```
d_y = v_yi t + ½a_y t²
v_yi = 0, so d_y = ½a_y t²
t² = 2d_y / a_y
t = √(2d_y / a_y)
  = √[2(100) / 9.8]
  = 4.5175 s
  ≈ 4.5 s
```

### Part 2: horizontal distance
Use the unrounded time:
```
d_x = v_x t
    = (20)(4.5175)
    = 90.3508 m
    ≈ 90 m
```

### Part 3: vertical impact velocity
```
v_yf² = v_yi² + 2a_y d_y
v_yi = 0, so v_yf² = 2a_y d_y
v_yf = √(2a_y d_y)
     = √[2(9.8)(100)]
     = +44.2719 m/s (down)
```

The horizontal component remains **20 m/s right**. The vertical component is **44.2719 m/s down**.

### Combine the components
```
v_f² = v_x² + v_yf²
v_f = √(v_x² + v_yf²)
    = √[20² + 44.2719²]
    = 48.5798 m/s

tan θ = v_yf / v_x
θ = tan⁻¹(v_yf / v_x)
  = tan⁻¹(44.2719 / 20)
  = 65.69°
```
The source's rounded answer is **49 m/s, 66° below the horizontal to the right**.

## 11 Practice: a ball from level ground
### The question
A ball is thrown from level ground with a velocity of **12 m/s, 60° above the horizontal**.
1. How long will it spend in the air?
2. How far from the thrower will it land?
3. What will be its velocity right before it hits the ground?

### Worked answer: components
Choose the launch direction horizontally as positive x and up as positive y. Use a_y = −9.8 m/s² and neglect air resistance.
```
v_x = 12 cos 60° = 6.00 m/s
v_yi = 12 sin 60° = 10.392 m/s
```

### Part 1: time in the air
The ball lands at its original height, so vertical displacement is zero. Factor the vertical-motion equation and take the nonzero root:
```
0 = v_yi t − ½gt²
t = 2v_yi / g
  = 2(10.392) / 9.8
  = 2.121 s
```
Time in the air: **2.1 s**.

### Part 2: horizontal distance
Use the unrounded time.
```
d_x = v_x t = (6.00)(2.12088)
    = 12.725 m
```
The ball lands **13 m from the thrower**.

### Part 3: impact velocity
```
v_yf = v_yi − gt
     = 10.392 − (9.8)(2.12088)
     = −10.392 m/s
v_xf = +6.00 m/s

|v_f| = √(6.00² + 10.392²) = 12.0 m/s
θ = tan⁻¹(10.392 / 6.00) = 60°
```
Immediately before impact, the velocity is **12 m/s, 60° below the horizontal in the launch direction**. Its speed equals the initial speed, while its vertical component has reversed direction.
