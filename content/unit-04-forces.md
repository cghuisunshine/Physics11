@chapter: Physics 11 · Unit 4
@title: Unit 4: Forces
@subtitle: Use interactions and free-body diagrams to explain motion, contact forces, friction, and apparent weight.

## 4.1 Newton’s first and second laws

### Learning goal
Relate net force to acceleration and distinguish balanced motion from rest.

### Understand the model
Newton’s first law says an object maintains constant velocity when its net external force is zero in an inertial frame. Constant velocity includes rest and straight-line motion at a steady speed. Mass measures inertia: more mass requires more net force for the same acceleration. A force is an interaction with another object, not something an object carries because it moves.

Newton’s second law relates the vector sum of external forces to acceleration. Add forces by components before dividing by mass. A single force can be large while the net force is zero because another force balances it. These introductory calculations assume constant mass and an approximately inertial frame; Earth’s surface is an adequate approximation for the examples here.

### Equations and units
```text
ΣF⃗ = ma⃗
ΣFₓ = maₓ; ΣFᵧ = maᵧ
1 N = 1 kg·m/s²
```

### Worked example
A 4.00 kg cart is pulled right with 18.0 N and left with 6.00 N. Find acceleration.

1. Choose right as positive. The horizontal net force is 18.0 - 6.00 = +12.0 N.
2. aₓ = 12.0/4.00 = +3.00 m/s².
3. If the cart initially moves left, this rightward acceleration initially slows it. Force gives acceleration, not the current velocity.

### Common mistakes
Constant speed along a straight line does not require a forward net force. In ordinary motion a driving force may be needed to balance resistance, leaving the net force zero.

### Your turn
1. A 2.0 kg object has acceleration -3.0 m/s². Find net force.
2. Can an object move when its net force is zero?

### Solutions and reasoning
**1.** ΣFₓ = (2.0)(-3.0) = -6.0 N.

**2.** Yes. It can maintain a nonzero constant velocity. Zero net force means zero acceleration, not necessarily zero velocity.

### Textbook reading
Section 5-1, PDF page 130 (printed page 94).

## 4.2 Free-body diagrams and interaction pairs

### Learning goal
Draw only forces acting on the chosen object and identify Newton’s third-law pairs.

### Understand the model
Choose one object, represent it as a dot or simple outline, and draw each external force with its tail on that object. Label the source of each force: Earth supplies gravity, a surface supplies normal force or friction, a rope supplies tension, and a spring supplies spring force. Add coordinate axes chosen to simplify the problem. Velocity and acceleration can be shown separately, but they are not forces.

Newton’s third law states that the force of A on B is equal in magnitude and opposite in direction to the force of B on A. The pair acts on different objects, so it does not cancel in the free-body diagram of either object alone. Weight and normal force on the same block are not a third-law pair even when they balance.

### Equations and units
```text
F⃗_A on B = -F⃗_B on A
ΣFₓ = maₓ; ΣFᵧ = maᵧ
```

### Worked example
Draw the forces on a book resting on a table and identify the partner of each force.

1. On the book: gravity mg downward from Earth and normal force N upward from the table. There is no horizontal force if no horizontal interaction is present.
2. Because aᵧ = 0, N - mg = 0. Their equality comes from equilibrium, not the third law.
3. The partner of Earth’s force on the book is the book’s gravitational force on Earth. The partner of the table’s normal force on the book is the book’s contact force on the table.

### Common mistakes
Do not put the book’s force on the table into the book’s own free-body diagram. Do not add an extra “motion force” or “ma force” to the diagram.

### Your turn
1. A truck and a small car interact during a collision. Which exerts the larger interaction force?
2. Why do weight and normal force not form an action-reaction pair?

### Solutions and reasoning
**1.** Their interaction forces have equal magnitudes and opposite directions. Their accelerations can differ because their masses differ.

**2.** Both act on the same object. A third-law pair must act on two different objects.

### Textbook reading
Section 5-1, PDF page 130 (printed page 94); Section 5-3, PDF page 142 (printed page 106).

## 4.3 Mass, gravity, and normal force

### Learning goal
Calculate gravitational force and determine the normal force from vertical dynamics.

### Understand the model
Mass is measured in kilograms and remains the same when an object changes location. Gravitational force near Earth has magnitude mg and points downward. A normal force is perpendicular to a contact surface and arises because the surface resists penetration. It is not defined as “equal to weight.”

For a block on a horizontal surface with no vertical acceleration, the vertical forces must sum to zero. If an upward applied force partly supports the block, the normal force is reduced. If a downward applied force presses the block into the surface, it increases. A simple nonadhesive surface can push but cannot pull the object downward; a computed negative N indicates that the assumed contact has failed.

### Equations and units
```text
F_g = mg
level surface with upward applied force: N + F_up - mg = maᵧ
for aᵧ = 0: N = mg - F_up
```

### Worked example
A 5.00 kg box on a level floor is pulled upward with 12.0 N while staying on the floor. Find the normal force.

1. Gravity is mg = (5.00)(9.81) = 49.05 N downward.
2. Vertical acceleration is zero, so N + 12.0 - 49.05 = 0.
3. N = 37.1 N after rounding. The floor provides the remaining support; it does not provide the full 49.1 N.

### Common mistakes
A scale commonly displays a mass-equivalent reading but responds to a support force. A normal force is not necessarily vertical: it is perpendicular to the surface.

### Your turn
1. A 2.00 kg block is pressed down with 10.0 N on a level floor. Find N.
2. A 3.0 kg object moves to a location where g = 1.6 m/s². Find its mass and gravitational force.

### Solutions and reasoning
**1.** N = mg + 10.0 = 29.6 N if the block has no vertical acceleration.

**2.** Mass remains 3.0 kg; gravitational force becomes 4.8 N.

### Textbook reading
Section 5-2, PDF page 138 (printed page 102).

## 4.4 Tension and spring forces

### Learning goal
Model an ideal rope and use Hooke’s law within a spring’s elastic range.

### Understand the model
A taut rope pulls an attached object along the rope; it does not push. In the ideal model a massless rope running over a massless frictionless pulley has one tension magnitude throughout. Real rope mass and pulley effects can make tensions differ, so state the idealization. A slack rope has no tension in this simple model.

A spring displaced from its relaxed length exerts a restoring force. Hooke’s law Fₛ = -kx says that the force opposes the signed extension or compression x. The spring constant k, measured in N/m, describes stiffness. This proportional model applies within an appropriate elastic range, not after permanent deformation or for every elastic object.

### Equations and units
```text
Fₛ = -kx  (signed force along spring axis)
|Fₛ| = k|x|
at rest for a hanging mass: T = mg
```

### Worked example
A vertical spring extends 0.0400 m when a 0.200 kg mass hangs at rest. Find its spring constant.

1. At equilibrium the upward spring force balances the downward gravitational force.
2. kx = mg, so k = mg/x = (0.200)(9.81)/0.0400 = 49.1 N/m.
3. Measure x from the relaxed spring length, not from its total stretched length. A force-extension graph has slope k when plotting the required holding-force magnitude.

### Common mistakes
Tension is not automatically equal to mg when a mass accelerates. The negative sign in Hooke’s law gives force direction; it does not mean that the spring constant is negative.

### Your turn
1. A spring has k = 200 N/m and extension +0.030 m. Find the signed restoring force.
2. A 1.00 kg hanging mass accelerates upward at 2.00 m/s². Find tension.

### Solutions and reasoning
**1.** Fₛ = -(200)(0.030) = -6.0 N along the chosen spring axis.

**2.** T - mg = ma, so T = m(g + a) = 11.8 N.

### Textbook reading
Section 5-2, PDF page 138 (printed page 102); Section 7-4, PDF page 195 (printed page 159).

## 4.5 Static and kinetic friction

### Learning goal
Choose the correct friction model and determine friction before assuming motion.

### Understand the model
Dry friction acts along the contact surface. Static friction prevents relative sliding and adjusts to the force required for equilibrium, up to a maximum μₛN. Kinetic friction acts when surfaces slide relative to one another, and its magnitude is approximated by μₖN. Usually μₛ exceeds μₖ for the same pair of surfaces, but actual friction depends on conditions.

To decide whether a block moves, first calculate the static friction needed to keep it at rest, then compare with the maximum. If the required force exceeds that limit, switch to the kinetic model. Friction opposes relative sliding or its tendency; it does not always oppose an object’s overall motion. For example, static friction can propel a walking person or a driven tire forward.

### Equations and units
```text
0 ≤ fₛ ≤ μₛN
fₛ,max = μₛN
fₖ = μₖN
```

### Worked example
A 10.0 kg box has μₛ = 0.40 and μₖ = 0.30 on a level floor. Compare horizontal pushes of 25 N and 50 N.

1. N = mg = 98.1 N. Maximum static friction is 0.40 × 98.1 = 39.24 N.
2. For the 25 N push from rest, static friction is 25 N in the opposite direction and acceleration is zero.
3. A 50 N push exceeds the static limit. Once sliding, fₖ = 29.43 N, so a = (50 - 29.43)/10.0 ≈ 2.1 m/s².

### Common mistakes
The formula μₛN is the maximum static friction, not its automatic value. Calculate N from the actual forces; an angled pull can change it.

### Your turn
1. A resting box needs 8 N of friction, while μₛN = 12 N. What is fₛ?
2. A sliding block has N = 40 N and μₖ = 0.25. Find kinetic friction.

### Solutions and reasoning
**1.** fₛ = 8 N. The maximum is 12 N but the actual required force is smaller.

**2.** fₖ = 10 N, directed opposite the block’s sliding relative to the surface.

### Textbook reading
Section 6-1, PDF page 160 (printed page 124).

## 4.6 Elevators and apparent weight

### Learning goal
Predict a scale’s support force from acceleration rather than direction of travel.

### Understand the model
A person standing on a scale experiences gravity downward and a normal force upward. The scale responds to N, called apparent weight. With upward positive, N - mg = maᵧ. Upward acceleration makes N greater than mg; downward acceleration makes it smaller. Constant velocity in either direction gives N = mg.

An elevator travelling upward can have downward acceleration when it brakes, so the person then feels lighter. During ideal free fall the scale and person fall together; N becomes zero even though gravity remains present. Weightlessness in this sense means lack of support force, not absence of gravity. These statements use the ground as the approximately inertial reference frame.

### Equations and units
```text
N - mg = maᵧ
N = m(g + aᵧ)
free fall: aᵧ = -g → N = 0
```

### Worked example
A 60.0 kg person is in an elevator moving upward but slowing with a downward acceleration of 1.50 m/s². Find the scale force.

1. Choose upward positive. The acceleration is aᵧ = -1.50 m/s² even though velocity points up.
2. N = 60.0(9.81 - 1.50) = 498.6 N ≈ 499 N.
3. The ordinary support force is 589 N. The smaller reading follows from downward acceleration. Mass is still 60.0 kg.

### Common mistakes
Do not infer acceleration from the word “upward” alone. Read whether speed is increasing, decreasing, or constant.

### Your turn
1. A 50.0 kg person accelerates upward at 2.00 m/s². Find N.
2. An elevator moves downward at constant speed. How does N compare with mg?

### Solutions and reasoning
**1.** N = 50.0(9.81 + 2.00) = 591 N.

**2.** N = mg because the acceleration is zero.

### Textbook reading
Section 5-2, PDF page 138 (printed page 102); Section 5-3, PDF page 142 (printed page 106).

## 4.7 Investigate and reflect

### Inquiry task
Pull a block with a spring scale on a level surface. Record the largest force just before sliding and the force during nearly constant-speed sliding. Change the load while keeping the surfaces the same. Plot friction versus normal force and discuss the dry-friction model. Use small loads and keep hands clear of falling masses. Predict before measuring; explain a specific source of uncertainty.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.
