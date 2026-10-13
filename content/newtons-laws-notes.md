# Newton's Laws of Motion Notes

Understand how forces change motion, identify interacting objects, and use momentum and impulse to explain collisions. These notes follow BC Science Physics 11 Chapter 4, with diagrams, guided examples, and all 121 original question entries. Try each question before opening its worked answer.

## 1 Inertia and mass

### Why motion resists change
**Inertia** is an object's tendency to maintain its velocity. An object at rest stays at rest unless a net force changes that state. A moving object continues at the same speed and in the same direction unless a net force acts. Inertia is a property of matter; it is not an extra force on a free-body diagram.

An object's **mass** measures its inertia. For the same net force, a larger mass changes velocity more slowly. Starting, stopping, and turning a logging truck therefore require more force than producing the same acceleration in a bicycle.

### Turning in a car
The car turns because a sideways force changes its velocity. Your body initially tends to keep moving along its original straight path. The seat, door, or seatbelt must exert a force toward the turn to make you follow the car. The sensation of leaning outward does not require an outward force in the road's reference frame.

### Mass and weight are different
Mass is measured in kilograms and remains the same when an object is moved to a place with a different gravitational field. Weight is the gravitational force on that mass, measured in newtons. An astronaut in orbit still has mass and inertia; apparent weightlessness occurs because the astronaut and station fall together.

```text
mass m: kilograms (kg), a measure of inertia
weight F_g = mg: newtons (N), a gravitational force
near Earth's surface: g ≈ 9.81 N/kg
```

## 2 Newton's first law and balanced forces

### Constant velocity requires zero net force
In an inertial reference frame, Newton's first law says that an object maintains constant velocity when the vector sum of its forces is zero. Constant velocity includes rest. A car moving steadily along a straight road can have several forces on it: forward traction balances resistance, and vertical support balances weight.

```text
F_net = ΣF = 0  ⇒  a = 0  ⇒  velocity is constant
```

### Speed and direction both matter
A moving object does not need a continuing net force to maintain its velocity. It needs a net force to **change** velocity. Slowing down, speeding up, and turning all involve acceleration. If a car on ice loses the sideways friction needed to turn, it tends to continue along a straight path tangent to the intended curve.

### Ideal conditions and real motion
The textbook often assumes negligible friction to isolate a law of motion. A real coasting bicycle slows because resistive forces act on it. Zero net force does not mean zero individual forces, and zero velocity at one instant does not imply zero acceleration.

### Guided example: a steady cart
A cart moves right at a constant 2.0 m/s on a level floor. A student pulls right with 12 N. What horizontal friction force acts on the cart? State its acceleration.

**Worked answer**
Constant velocity means zero net force. Choose right as positive:
```text
F_net = +12 N + F_fr = 0
F_fr = −12 N: 12 N to the left
a = 0 m/s²
```

## 3 Investigation 4-1: investigating inertia

### Problem 1: how a seatbelt works
The toy passenger in Figure 4.1.2 continues forward when the vehicle hits an obstruction. Taping the passenger to the vehicle provides a force that changes the passenger's velocity with the vehicle. A real seatbelt restrains the occupant and helps prevent a second collision with the interior or road. Use the toy model to compare the two cases.

### Problem 2: air has inertia
The inflated bag in Figure 4.1.3 contains air with mass. When the bag is jerked sideways, the air initially resists the change in motion. When the bag stops, the moving air tends to continue. The bag's deformation provides evidence of inertia even though the air is difficult to see.

### Problem 3: a glider on an air track
The air cushion in Figure 4.1.4 reduces contact friction. On a level track, weight and vertical support balance. After a brief push ends, a glider with negligible horizontal resistance travels with nearly constant velocity. A tilted track introduces a component of gravity along the track and changes the result.

### Problem 4: leaving a curved train track
The track guides the train by exerting a force that changes its direction. When the train leaves the open end in Figure 4.1.5, that guiding force ends. Its initial path is along the **tangent** at the departure point, rather than continuing in a circle or moving radially outward. Later friction can slow it.

### Problem 5: a slow pull and a sudden pull
Figure 4.1.6 compares identical hanging masses and strings. With a slow pull, the upper string supports the weight plus the extra pull and typically breaks first. A sharp tug can break the lower string before the large mass accelerates appreciably. The precise result depends on the strings and pull duration; inertia explains why the two methods differ.

### Problem 6: the pop-up coaster
The ball launched from the moving cart in Figure 4.1.7 already has the cart's horizontal velocity. With negligible air resistance, gravity changes only its vertical motion while its horizontal velocity remains constant. If the cart also maintains constant horizontal velocity, the ball returns to the cannon. A changing cart speed or air resistance can make it miss.

### What to record
For each demonstration, identify the object, its velocity before the change, and the forces that change that velocity. Distinguish an observation from your explanation. The original procedures and investigation questions appear below each practice-set heading.

## 4 Newton's second law: net force and acceleration

### The net force sets the acceleration
Newton's second law relates the **vector sum** of all forces on one object to its acceleration. For constant mass, acceleration is in the direction of the net force. A single applied force can be only one contribution to that sum.

```text
F_net = ΣF = ma
a = F_net / m
m = F_net / a
1 N = 1 kg·m/s²
```

At fixed mass, doubling the net force doubles the acceleration. At fixed net force, doubling the mass halves the acceleration. Use kilograms, newtons, and metres per second squared together.

### Acceleration need not point along velocity
A car moving right can accelerate left while braking. Its speed then decreases until it stops. If the leftward net force continues after it stops, it starts moving left. Force determines how velocity changes, rather than always pointing in the direction of travel.

### Guided example: comparing masses
A 3.00 kg cart experiences a 6.00 N net force to the right. Find its acceleration. What is the acceleration if the mass is doubled while the net force remains the same?

**Worked answer**
```text
a = F_net / m = 6.00 N / 3.00 kg = 2.00 m/s² right
with m = 6.00 kg: a = 6.00 N / 6.00 kg = 1.00 m/s² right
```
The greater mass has greater inertia; it does not experience a greater net force in this comparison.

## 5 Free-body diagrams and multiple forces

### Draw forces on one chosen object
Figure 4.2.1 shows a block pushed across a floor. Its free-body diagram contains weight downward, normal force upward, applied force left, and kinetic friction right. Label each force by its source. Leave forces exerted **by** the block on other objects out of the block's diagram.

### A reliable solution method
1. Choose the object or system and draw all external forces on it.
2. Choose axes and state the positive directions.
3. Sum forces along each axis, with signs, and set each sum equal to the corresponding mass times acceleration.
4. Use friction or kinematics relations when needed, then solve with consistent units.
5. Check whether the sign and magnitude fit the physical situation.

For a horizontal push on a level floor with no vertical acceleration, F_N = mg. This equality follows from vertical force balance; it is not a universal definition of the normal force. An angled pull, an incline, or vertical acceleration can change it. Choose the positive horizontal direction along the push for the equations below.

```text
vertical: F_N − mg = 0
kinetic friction magnitude: F_fr = μ_k F_N
horizontal: F_applied − F_fr = ma
```

### Guided example: push with friction
A 5.00 kg block slides on a level floor with μ_k = 0.200. A horizontal 20.0 N push acts right. Find its acceleration using g = 9.81 N/kg.

**Worked answer**
```text
F_N = mg = (5.00 kg)(9.81 N/kg) = 49.05 N
F_fr = μ_k F_N = (0.200)(49.05 N) = 9.81 N left
F_net = 20.0 − 9.81 = 10.19 N right
a = 10.19 N / 5.00 kg = 2.04 m/s² right
```
Kinetic friction applies because the block is sliding. For a block at rest, static friction adjusts up to its maximum; it is not automatically μ_s F_N.

## 6 Investigation 4-2: testing the second law

### Read the cart and hanging-mass setup
Figure 4.2.2 compares eight setups. A string over a pulley connects the cart to a hanging mass. For the whole moving system, the hanging mass's weight supplies the driving force once resistance is compensated. The accelerating mass includes **both** the cart and hanging masses. The hanging weight is not generally equal to the string tension during acceleration.

In setups (a)–(d), masses are transferred from the cart to the hanger. The total moving mass stays constant while the driving force increases from about 2.0 N to 8.0 N. In setups (e)–(h), the hanging weight stays approximately 2.0 N while the moving mass increases from one to four mass units.

The textbook slightly tilts the track so that a component of gravity compensates resistance, checked by steady motion. Follow the teacher's setup when using the apparatus. Small remaining friction, pulley inertia, or an inaccurate tilt can affect the measurements.

### Turn ticker tape into acceleration
Use the timer's actual frequency to convert dots into elapsed time. At 60 Hz, six timing intervals represent 0.10 s; count the gaps between dots when measuring a time interval. Measure successive displacements, calculate each interval's average speed, and plot that speed at the interval's midpoint. The slope of the speed-versus-time graph gives acceleration. Convert cm/s² to m/s² by dividing by 100 when using SI equations.

### Three graphs to test the model
These illustrative graphs use SI values, rather than measured class data. With fixed mass, acceleration against net force is a straight line through the origin with slope 1/m. With fixed net force, acceleration against mass is a decreasing curve. Plotting acceleration against reciprocal mass makes that relationship linear, with slope F_net.

On a small screen, swipe a wide graph sideways to read its axes and labels.

```text
fixed mass: a = (1/m)F_net
fixed net force: a = F_net/m = F_net(1/m)
```

Compare repeated trials, record the actual total moving mass, and describe experimental limitations instead of forcing measured points onto a perfect line.

## 7 Newton's third law: interaction pairs

### Equal forces on different objects
When object A exerts a force on B, B simultaneously exerts an equal-magnitude force in the opposite direction on A. Both forces are the same kind of interaction: gravitational, contact, or another interaction. Neither waits for the other to happen.

```text
F_(A on B) = −F_(B on A)
```

The two forces act on **different objects**, so they do not cancel in either object's individual free-body diagram. Equal interaction forces also do not imply equal accelerations: acceleration depends on each object's mass.

### The horse and cart
Figure 4.3.1 labels the force of the horse on the cart and the force of the cart on the horse. Those are a third-law pair. The horse pushes backward on the ground; the ground pushes forward on the horse. That forward external force can accelerate the combined horse-and-cart system if it exceeds external resistance. The harness forces are internal to that combined system.

### Weight and normal force are not a pair
For a book resting on a table, Earth pulls the book down and the table pushes the book up. Those two forces balance on the book, but they have different interaction partners. The reaction to Earth's gravitational pull on the book is the book's gravitational pull on Earth. The reaction to the table's upward push is the book's downward push on the table.

### Guided example: unequal carts
Cart A has mass 1.00 kg and cart B has mass 3.00 kg. During a spring interaction, A pushes B right with 6.00 N. Neglect other horizontal forces. Find each cart's acceleration.

**Worked answer**
```text
force on B from A = +6.00 N
force on A from B = −6.00 N
a_B = +6.00 N / 3.00 kg = +2.00 m/s²
a_A = −6.00 N / 1.00 kg = −6.00 m/s²
```
The interaction forces are equal and opposite. The lighter cart has the larger acceleration magnitude.

## 8 Investigation 4-3: observing the third law

### Part 1: exploding carts
Figure 4.3.2 shows carts with spring bumpers. Compress the bumpers and release the carts on a level surface. The carts exert equal and opposite forces on one another at each instant. With equal masses, their acceleration magnitudes match. Adding mass to one cart makes its acceleration smaller relative to the other cart's; it does not destroy the equality of the interaction forces.

For the same initial spring compression, changing a cart's mass can alter how the force changes with time. The third law guarantees equal opposing forces **within each trial**, rather than an identical force history in different trials.

### Part 2: a car on a movable road
The toy car in Figure 4.3.3 travels on a light board supported by an air table. Its driven wheels push the board backward. The board pushes the car forward, so the car and its movable road move in opposite directions. With negligible external horizontal force, their total horizontal momentum stays constant. A heavier board recoils less for the same transferred momentum.

### Part 3: tug of war with spring balances
Figure 4.3.4 places two spring balances in series. With a light string and balances held steadily, each reads the same tension T. If each person pulls with 10 N, each balance reads 10 N, not 20 N. Adding a third balance in series gives the same reading under the same conditions. These readings measure tension; each balance is in equilibrium because the forces at its ends balance.

### Name the interaction partners
For every observation, write “force of ___ on ___” twice with the objects reversed. Then choose one object's diagram to predict its acceleration. This keeps an interaction pair separate from two forces that balance on the same object.

## 9 Momentum: mass times velocity

### Momentum has direction
Momentum combines an object's mass and velocity. Two objects with the same speed can have different momentum if their masses differ. Equal masses moving in opposite directions have opposite momenta, even though both have positive speed.

```text
p = mv
momentum units: kg·m/s
total momentum: p_total = p_A + p_B + …
```

Choose a positive direction before substituting numbers. Convert grams to kilograms and km/h to m/s. In a one-dimensional problem, a negative momentum means motion in the chosen negative direction.

### Momentum and the second law
For constant mass, Δp = mΔv. The average net force equals the momentum change divided by the time interval. This includes both starting from rest and slowing a moving object.

```text
F_net,avg = Δp / Δt = m(v_f − v_i) / Δt
```

Momentum alone does not determine how damaging an impact will be. Contact duration, contact area, deformation, and kinetic energy also matter.

## 10 Impulse and changing momentum

### A force acting over time
Impulse is the momentum change produced by the net force over an interval. For a constant force, it equals force multiplied by duration. For a varying force, use the average net force over the full interval. On a force-versus-time graph, the signed area gives impulse.

```text
J = F_net,avg Δt = Δp = m(v_f − v_i)
1 N·s = 1 kg·m/s
```

For the same momentum change, increasing the stopping time lowers the **average** net force. Airbags, padding, and bending your knees when landing use this principle. Peak forces depend on the shape of the force-versus-time curve and need not equal the average.

### Guided example: stopping a ball
A 0.200 kg ball moves right at 10.0 m/s and is brought to rest in 0.100 s. Find its impulse and average horizontal net force, taking right as positive.

**Worked answer**
```text
Δp = m(v_f − v_i) = (0.200 kg)(0 − 10.0 m/s)
J = −2.00 kg·m/s = −2.00 N·s
F_net,avg = −2.00 N·s / 0.100 s = −20.0 N
```
The impulse and average net force act left, opposite the initial velocity. If stopping takes 0.200 s instead, the impulse is unchanged but the average net force becomes −10.0 N.

## 11 Conservation of momentum

### Choose the system and check external impulse
The total momentum of a system remains constant when its net external impulse is zero or negligible over the event. Internal interaction forces transfer momentum between objects but cancel when all objects in the system are included. Individual objects can change momentum while the total stays constant.

```text
p_total,before = p_total,after
m_A v_Ai + m_B v_Bi = m_A v_Af + m_B v_Bf
```

These are signed velocities along one axis. For objects that stick together, replace both final velocities with the same v_f. Momentum conservation does not require kinetic energy to be conserved.

### Recoil and the third law
If two carts start at rest and separate with negligible external horizontal impulse, their momenta afterwards add to zero. Equal and opposite forces act over the same interaction interval, giving equal and opposite impulses. The more massive cart therefore has the smaller speed. This result concerns total momentum, rather than equal speeds or equal kinetic energies.

### Adding a load to a moving railway car
In textbook Sample 4.4.1, a moving railway car receives a load of sulphur. Include **both** the car and incoming sulphur in the system. Horizontal momentum is conserved if horizontal external impulse is negligible and the incoming sulphur has zero horizontal velocity. The load gains horizontal momentum while the car slows. Vertical forces need not vanish for horizontal momentum to be conserved.

### Guided example: carts stick together
A 0.500 kg cart moves right at 4.00 m/s toward a 1.50 kg cart at rest. They stick together. Neglect external horizontal impulse. Find their common final velocity.

**Worked answer**
```text
p_before = (0.500 kg)(4.00 m/s) + (1.50 kg)(0) = 2.00 kg·m/s
(0.500 + 1.50) kg × v_f = 2.00 kg·m/s
v_f = 1.00 m/s right
```
The combined mass is 2.00 kg. The final momentum equals the initial momentum, while some initial kinetic energy becomes other forms of energy.

## 12 Chapter review and extra practice

### Connect the ideas
Use the first law to recognize constant velocity and equilibrium. Use the second law to calculate acceleration from net force. Use the third law to identify forces on different objects. Use impulse for a momentum change over time, and conservation of momentum for a system with negligible external impulse.

### Check before opening an answer
1. Did you identify the object or system and label the forces acting on it?
2. Did you distinguish mass in kilograms from weight in newtons?
3. Did you sum forces with directions, rather than substitute one force for the net force?
4. Did you use signed velocities and subtract initial momentum from final momentum?
5. If you conserved momentum, did you state why external impulse is negligible along the chosen axis?
6. Does your answer include units, direction where needed, and a sensible physical interpretation?

The complete chapter review and extra practice follow. Original question numbering, figures, procedures, and worked answers are preserved throughout these notes.
