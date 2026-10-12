@chapter: Physics 11 · BC Science Chapter 3
@title: Forces Notes
@subtitle: Understand gravity, friction, and springs, then practise with all 79 questions from the chapter collection.

# Forces Notes

## 1 Forces and gravitational fields
### What a force does
A **force** describes an interaction: a push or pull exerted by one object on another. It can change an object's speed, direction, or shape. A force has a magnitude and a direction, so it is a vector. Its SI unit is the **newton**, N.

Identify both the object experiencing the force and the object producing it. A hand pushes a book; a floor supports a box; Earth attracts a falling ball. Several forces can act at once. Their combined effect depends on their directions, not just their sizes.

### Contact forces and action at a distance
Friction and spring forces require contact. Gravity acts between masses even when they do not touch. Around a mass, a **gravitational field** describes the gravitational force that another mass would experience.

Gravity is attractive. Near Earth's surface its direction is approximately downward, toward Earth's centre. The strength of the field is the gravitational force per kilogram of mass:
```
g = F_g / m
near Earth's surface: g ≈ 9.81 N/kg
1 N/kg = 1 m/s²
```
The two units describe the same physical quantity in different contexts: force per unit mass or the acceleration of an object acted on by gravity alone.

### Why paper and a book fall differently
The paper-and-book warm-up separates **gravity** from **air resistance**. Thin paper has a large exposed area relative to its mass. Air resistance can therefore have a substantial effect on its motion. A book underneath the paper can shield it from much of that resistance.

With negligible air resistance, objects released from the same height with the same initial velocity have the same gravitational acceleration. A larger mass experiences a larger gravitational force, but it also requires more force for a given acceleration.

### Check your reasoning
Do not infer that a moving object must have a force pointing in its direction of travel. Forces describe interactions and changes in motion. A falling object can experience both downward gravity and upward air resistance.

## 2 Mass, weight, and measuring gravity
### Mass and weight are different quantities
**Mass** describes inertia and is measured in kilograms. **Weight** is the gravitational force on an object and is measured in newtons. Changing location changes weight if the gravitational field changes; it does not change the object's mass.
```
F_g = mg
m = F_g / g
g = F_g / m
```
Here F_g is the magnitude of the gravitational force. Its direction must be stated separately, usually downward near Earth's surface.

### Worked example: weight on Earth
Find the weight of a **60.0 kg** person on Earth, using g = 9.81 N/kg.

**Worked answer**
```
F_g = mg = (60.0 kg)(9.81 N/kg)
    = 588.6 N ≈ 589 N downward
```
The kilograms cancel, leaving newtons. The person's mass is still 60.0 kg.

### Worked example: a different planet
A **4.00 kg** object has a weight of **14.8 N** on another planet. Find the gravitational field strength there.

**Worked answer**
```
g = F_g / m = 14.8 N / 4.00 kg
  = 3.70 N/kg
```
The object's mass is 4.00 kg on either planet. On Earth the same object would weigh about 39.2 N.

### What a spring balance measures
A spring balance responds to a force through its stretch. For an object hanging at rest, the upward spring force balances the downward gravitational force, so the balance can measure weight. A scale marked in kilograms converts that force using an assumed value of g.

This interpretation assumes the object is in equilibrium. A support-force reading need not equal weight when the object accelerates. Chapter 4 develops those situations further.

### Common mistakes
- Convert grams to kilograms before using g in N/kg.
- Do not report a force in kilograms or a mass in newtons.
- Use the gravitational field strength at the specified location.
- Distinguish a force reading from a mass-equivalent scale display.

## 3 Universal gravitation and distance
### The attraction between two masses
Newton's law of universal gravitation gives the magnitude of the attraction between two point masses. It also applies outside a spherically symmetric body when its mass is treated as concentrated at its centre:
```
F_g = Gm₁m₂ / r²
G = 6.67 × 10⁻¹¹ N·m²/kg²
```
The masses m₁ and m₂ are in kilograms. The separation r is in metres and is measured **between the centres**, not between the nearest surfaces. The force on each object has the same magnitude; each points toward the other object.

### Cavendish's measurement
The attraction between ordinary laboratory masses is extremely small. Cavendish used the twist of a suspended rod to detect that attraction. The apparatus illustrates why air currents and other unwanted influences had to be minimized. Measuring this attraction allowed the gravitational constant G to be determined.

### How changing mass or distance changes the force
At fixed separation, doubling one mass doubles the force; doubling both masses multiplies the force by four. Distance enters as a square:
```
F_new / F_old = (m₁,new / m₁,old)(m₂,new / m₂,old)(r_old / r_new)²
double r: F_new = F_old / 4
triple r: F_new = F_old / 9
halve r: F_new = 4F_old
```
Use ratios when the question asks how a force changes. You often do not need to calculate either force separately.

### Worked example: changing the separation
Two objects attract with a force F. Both masses remain unchanged, but the separation increases to **three times** its original value. What is the new force?

**Worked answer**
```
F_new / F = (r / 3r)² = 1/9
F_new = F/9
```
The force decreases to one ninth. It does not decrease to one third, because the law depends on r².

### Connecting universal gravity to weight
For a small object of mass m near a spherical planet of mass M, combine F_g = mg with the universal law:
```
mg = GMm / r²
g = GM / r²
at altitude h: r = R + h
```
The small object's mass cancels. The field strength depends on the planet's mass and the distance from its centre. At an altitude equal to the planet's radius, r doubles and g becomes one quarter of its surface value.

### A reliable calculation method
Convert to SI units, write the centre-to-centre separation, square it, substitute the masses and G, and check the power of ten. Very small forces between everyday objects are physically reasonable. G and g are different quantities with different units.

## 4 Investigating gravity
### Investigation 3-1A: falling-body demonstrations
Compare two steel balls of different masses dropped together from the same height. With little air resistance, their landing times should be almost the same. Then compare tissue paper with a steel ball: different air-resistance effects make the paper fall more slowly.

The coin-and-feather demonstration removes most of the air from a tube. When air resistance is negligible, both objects fall together. The final demonstration compares a ball launched horizontally with one dropped vertically at the same instant. Their vertical motions are the same if their initial vertical velocities, release heights, and gravitational acceleration are the same.

These results connect forces to the earlier kinematics model: horizontal motion does not change vertical free fall when air resistance is negligible. On the Moon, free fall has a smaller acceleration and takes longer from a given height, but the paired objects still share the same vertical acceleration.

### Connecting a weight graph to field strength
As an additional connection, a graph of **F_g vertically against m horizontally** has a useful slope:
```
slope = ΔF_g / Δm = g
slope units: N/kg
```
A straight line approximately through the origin supports F_g = mg. Use widely separated points on a best-fit line to estimate the slope. If you graph mass against force instead, the slope is 1/g and has units kg/N.

### Investigation 3-1B: force versus distance
For fixed masses, the universal law predicts F_g proportional to 1/r². A graph of force against distance is curved. Plotting **F_g against 1/r²** gives a straight line in the ideal model.
```
F_g = (Gm₁m₂)(1/r²)
slope of F_g versus 1/r² = Gm₁m₂
```
Use centre-to-centre distances. Compare ratios to the inverse-square prediction rather than assuming equal changes in distance produce equal changes in force.

### Writing an investigation conclusion
State the observed relationship, cite a slope or ratio from your own data, and connect it to the relevant equation. A conclusion should also explain discrepancies, such as balance zero error, uncertain distance measurements, or limited graph resolution.

The procedure and data tables accompany the original questions below. Investigation answers describe methods and may include illustrative values; use your measured results when completing an experiment.

## 5 Static friction and kinetic friction
### Why friction matters
Friction comes from interactions between contacting surfaces. Microscopic deformation and adhesion help explain why even smooth-looking surfaces can resist slipping. Friction can be useful: it allows walking, gripping, braking, and writing. It can also waste energy and wear down materials.

Air and water resistance are related examples of resistive forces, but the dry sliding-friction model used in this chapter should not be applied indiscriminately to fluids.

### Static friction adjusts to the situation
**Static friction** acts when the contacting surfaces are not sliding relative to one another. It opposes the tendency to slip and can take a range of values up to a maximum. A stationary box pushed gently can experience just enough static friction to balance the push.

For example, if a 5 N horizontal push does not move the box and no other horizontal force acts, static friction is 5 N in the opposite direction. It is not automatically equal to its maximum value.

### Kinetic friction acts during sliding
**Kinetic friction** acts when one surface slides over the other. It opposes the relative sliding at the contact. For many dry surface pairs, starting motion requires a larger force than maintaining steady sliding; the maximum static friction commonly exceeds the kinetic friction.

Avoid the blanket rule that friction always points opposite the object's overall motion. A moving conveyor belt, for example, can exert friction that accelerates an object in the belt's direction. Look at the relative sliding or the tendency to slide at the contact.

### Constant motion and balanced forces
A box sliding in a straight line at steady speed has balanced forces. The push or pull balances friction horizontally, while support balances weight vertically. Constant motion does not require an unbalanced forward force.

## 6 Normal force and friction calculations
### The normal force is perpendicular to the surface
The **normal force**, F_N, is the support force exerted by a contacting surface. It acts perpendicular to that surface. On a horizontal surface with no vertical acceleration and no other vertical forces, F_N = mg.

On a slope, the normal force is not equal to the entire weight. An upward component of an applied pull can also reduce the support force; a downward push can increase it. Find the normal force from the actual forces before substituting into a friction equation.

### The coefficient of kinetic friction
For the chapter's approximate model of dry sliding surfaces:
```
F_fr = μ_k F_N
μ_k = F_fr / F_N
```
The coefficient μ_k is a dimensionless ratio. It depends on the materials and their condition, including lubrication and wetness. The textbook uses μ for the kinetic coefficient; the subscript k here makes the type of friction explicit.

### Approximate surface coefficients
These textbook values illustrate the effect of surface conditions. They are approximate, not universal constants.

### Worked example: steady-speed sliding
A wooden box weighs **450 N**. It slides across a level floor at steady speed under a horizontal push. The coefficient of kinetic friction is **0.30**. Find the required push.

**Worked answer**
There are no other vertical forces and no vertical acceleration, so F_N = 450 N.
```
F_fr = μ_k F_N = (0.30)(450 N) = 135 N
horizontal balance: F_push = F_fr
required push ≈ 1.4 × 10² N
```
The push is in the direction of sliding and friction is opposite. The final answer is rounded to two significant figures, as in Sample Problem 3.2.1.

### What changes friction in this model?
The normal force and the nature of the contacting surfaces have the largest effects. For otherwise comparable dry surfaces, changing the apparent contact area has little effect in this approximate model. It is not a rule covering every adhesive, deformable, or fluid-contact situation.

### A friction problem checklist
Identify whether the contact is static or sliding, draw the forces, determine F_N, calculate friction, and use the motion information to relate friction to an applied force. Do not use F_fr = μ_k mg unless the conditions justify F_N = mg.

When a static coefficient μ_s is supplied, the limiting friction is F_static,max = μ_s F_N. Before sliding, the actual static friction is only as large as needed, up to that limit. Once sliding begins, use the kinetic coefficient instead.

## 7 Investigating friction
### Investigation 3-2, Part 1: friction and weight
In Figure 3.2.3, the vertical spring balance on the left measures each block's weight. The four setups on the right show a horizontal balance pulling stacks of one, two, three, and four blocks. Add blocks on top of the same bottom block: **total weight changes while the contact area stays the same**.

Measure the pull needed to keep each stack sliding steadily. The steady pull estimates kinetic friction. A brief maximum at the start of motion is associated with overcoming static friction, not the steady sliding value.

Include both the block and any added load when finding the normal force. For the level, horizontally pulled setup, F_N equals their total weight. Graph **F_fr vertically against F_N horizontally**:
```
slope = ΔF_fr / ΔF_N = μ_k
```
The textbook labels the horizontal axis F_g; in this level setup, F_N = F_g. The slope has no units because it is a ratio of two forces. Repeat measurements and use a best-fit line rather than selecting a single reading.

### Changing the surface
Keep load and measurement method comparable while changing the contacting surfaces. A different slope indicates a different coefficient. In a fair comparison, do not change both the load and surface condition without accounting for their separate effects.

### Investigation 3-2, Part 2: contact area
Figure 3.2.4 uses the **same four blocks in every arrangement**. Read the diagrams as follows:
- **(a):** Four blocks stacked; one bottom face touches the bench, giving area A.
- **(b):** Two stacks of two blocks; two bottom faces touch the bench, giving area 2A.
- **(c):** Three bottom blocks with the fourth on top; three faces touch the bench, giving area 3A.
- **(d):** All four blocks side by side; four faces touch the bench, giving area 4A.

Here **contact area changes while total weight stays the same**. Use the horizontal spring balance to compare steady sliding forces. Similar readings support the approximate independence of dry friction from apparent contact area.

### Sources of experimental uncertainty
An angled pull changes the normal force; a changing speed makes the pulling force an unreliable estimate of friction alone. An unzeroed force meter, surface contamination, and uneven motion can also affect results. Describe how your method controlled these effects.

## 8 Hooke's law and spring graphs
### Extension is a change in length
A spring's **extension**, x, is its loaded length minus its unloaded length. It is not the spring's full length. A compressed spring is displaced in the opposite direction from its relaxed length.

Within a spring's linear elastic range, the magnitude of the applied force is proportional to the magnitude of the displacement:
```
F = kx
k = F / x
x = F / k
spring constant units: N/m
```
In these magnitude calculations x is a positive extension or compression. The spring's restoring force opposes the displacement; along a signed axis it can be written F_s = −kx. The minus sign expresses direction, not a negative spring constant.

### Reading a force-versus-extension graph
Plot force on the vertical axis and extension on the horizontal axis. The slope is the spring constant:
```
k = ΔF / Δx
1 N/cm = 100 N/m
```
A steeper force-versus-extension graph represents a stiffer spring. If the axes are reversed, the slope is 1/k. Check whether the extension axis uses metres or centimetres before interpreting the slope.

### Worked example: the textbook spring graph
Figure 3.3.1 shows a force of **1.0 N** for an extension of **0.75 cm**. Find the spring constant in N/m.

**Worked answer**
```
x = 0.75 cm = 0.0075 m
k = F / x = 1.0 / 0.0075
  ≈ 1.3 × 10² N/m
```
Equivalently, the slope is about 1.33 N/cm before rounding, which is about 133 N/m. An answer of 1.33 N/m would miss the centimetre-to-metre conversion.

### A hanging mass combines two models
For a mass hanging at rest, the spring's upward force balances its weight:
```
kx = mg
x = mg / k
```
Doubling the mass doubles the extension as long as the spring remains in the same linear range. Stretching it too far can produce nonlinear behaviour or permanent deformation. Rubber bands also need experimental checking; they do not necessarily behave as ideal springs over a broad range.

## 9 Elastic balances and calibration
### Investigation 3-3: another way to weigh
The textbook investigation uses a **metre stick clamped horizontally**, with 80.0 cm overhanging the bench. Known masses hang from the free end. Measure the end's vertical depression relative to its unloaded position, and convert each mass into a force using F_g = mg.

Graph **force against depression** and determine the effective stiffness from a best-fit slope. Include axis quantities and units. A relationship close to a straight line through the origin supports a Hooke-like elastic model over the measured range. Remove the masses to check that the stick returns to its initial position, and check that the clamp remains secure.

### Worked example: measuring an unknown mass
A calibrated elastic balance has an effective stiffness of **k = 200 N/m**. An unknown mass produces a deflection of **3.00 cm** while hanging at rest. Find the mass, using g = 9.81 N/kg.

**Worked answer**
```
x = 3.00 cm = 0.0300 m
F_s = kx = (200)(0.0300) = 6.00 N
mg = 6.00 N
m = 6.00 / 9.81 ≈ 0.612 kg
```
This method relies on equilibrium and the elastic support still behaving within its calibrated range. In the textbook investigation, compare the force inferred from the stick with a commercial spring balance.

### Making a letter weigher
The challenge replaces the metre stick with a strip of hacksaw blade. Use known masses to mark or calculate its scale. Check the unloaded zero, account for the holder's mass or tare it out, and check repeatability when adding and removing loads. A nonlinear or permanently deformed support will need a different calibration or replacement.

### Explaining your results
Use your measured slope and uncertainties in the final answer. Do not copy illustrative investigation data as if you measured it. If loading and unloading do not give the same extension, report that observation and discuss whether the ideal elastic model is adequate.

## 10 Chapter review and extra practice
### Choose the model before calculating
- **Weight or local field:** F_g = mg; use the specified g.
- **Attraction between two masses:** F_g = Gm₁m₂/r²; use centre-to-centre separation.
- **Planetary field:** g = GM/r²; at altitude, r = R + h.
- **Dry sliding friction:** F_fr = μ_k F_N; find the actual normal force first.
- **Spring deformation:** F = kx; measure the change in length within the linear range.
- **A hanging spring balance:** combine kx = mg when the load is at rest.

### Units that prevent common errors
Use kg, m, N, N/kg, and N/m consistently. Convert grams to kilograms, centimetres to metres, and kilometres to metres when necessary. Square the complete centre-to-centre distance in gravitation. Carry extra digits during calculation and round the final result appropriately.

### Graphs to recognise
F_g against mass has slope g. F_g against 1/r² has slope Gm₁m₂. Kinetic friction against normal force has slope μ_k. Spring force against extension has slope k. Always inspect the axis quantities and units: reversing the axes reverses the slope's physical interpretation.

### A bridge to Newton's laws
Extra Practice 11 asks about an accelerating desk. Its horizontal forces do not balance. Choose the push direction as positive, subtract the opposing friction, then use a = F_net / m. This is Newton's second law, developed in Chapter 4. A force of 1 N produces an acceleration of 1 m/s² in a 1 kg mass.

### Work through the chapter questions
Attempt each question before opening its answer. Include units and force directions when requested. For investigation questions, compare the explanation with your own procedure and data. The original chapter review and all 18 extra-practice questions follow below.
