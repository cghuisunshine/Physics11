@chapter: Physics 11 · Chapter 8
@title: Special Relativity
@subtitle: Inertial frames, the speed of light, time dilation, length contraction, relativistic momentum, and mass–energy equivalence.

# Special Relativity

## 1 Reference frames and relative velocity
### Specify what velocity is relative to
A **reference frame** gives positions and times using coordinates and clocks. The riverbank, a drifting boat, and a bird can each provide a frame. At ordinary speeds, add signed velocities along the same line.
```
v(A relative to C) = v(A relative to B) + v(B relative to C)
v(A relative to B) = −v(B relative to A)
```
An **inertial frame** is one in which a free object moves at constant velocity. A vehicle cruising straight at steady speed is a useful approximation. A ball tossed straight up in the vehicle also moves forward in the road frame, where its path is a parabola.

### Example · A boat in a current
Take downstream as positive. A boat moves 10 km/h downstream relative to the water. The water moves 5.0 km/h downstream relative to Earth. Find the boat’s Earth-frame velocity and the riverbank’s velocity relative to the boat.

**Worked answer**

Add the two velocities to get **+15 km/h** for the boat relative to Earth. Reverse the sign to get **−15 km/h** for the riverbank relative to the boat. Each answer names a different frame.

## 2 Einstein’s postulates and the speed of light
### Two rules for inertial observers
- The laws of physics have the same form in all inertial frames.
- Every inertial observer measures the same speed **c** for light in vacuum, regardless of the source’s motion.
```
c = 299 792 458 m/s ≈ 3.00 × 10⁸ m/s
```
A wave’s frequency can depend on the observer’s motion. The vacuum speed c stays the same. Light also travels more slowly through materials such as water or glass.

### The interferometer test
Michelson and Morley’s 1887 experiment split light from a laboratory lamp into perpendicular round trips. Rotating the apparatus tested whether their relative travel times changed with orientation. The measured fringe shift was far smaller than the stationary-ether model predicted. The textbook’s star diagram illustrates an idea about motion and light speed. The historical setup is described in the original paper linked at the end of these notes.

### Example · A headlight in vacuum
A spaceship moves at 0.50c and shines light forward. What speed does the pilot measure for the beam? What speed does an inertial observer outside measure?

**Worked answer**

Both measure **c** in their own frames. Adding 0.50c to c using the ordinary low-speed rule would give the wrong result.

## 3 Events, clocks, and simultaneity
### Separate an event from when its signal arrives
An **event** is a particular occurrence at a place and time, such as a flash or a clock tick. A distant observer receives light from that event later. To compare assigned event times, a frame uses synchronized clocks and accounts for travel time.

Two events that are simultaneous at different positions in one frame can occur at different times in another. For frames moving along x, with the primed frame moving at +v relative to the unprimed frame:
```
Δt′ = γ(Δt − vΔx/c²)
γ = 1/√(1 − v²/c²)
```
For events simultaneous in the unprimed frame, Δt = 0. The second term can still give Δt′ ≠ 0 when the locations differ along the motion.

### Example · Two flashes beside a passing train
Two platform lamps flash simultaneously in the platform frame. Lamp B is farther forward along the train’s direction than lamp A. Which emission occurs first in the train frame?

**Worked answer**

For B minus A, Δt = 0, Δx > 0, and v > 0. Thus Δt′ < 0, so **B flashes first in the train frame**. The result refers to the assigned emission times, which account for signal travel.

## 4 The Lorentz factor and a light clock
### How a longer light path changes the measured time
Define β = v/c. The **Lorentz factor γ** is 1 at rest and grows as speed approaches c.
```
β = v/c               γ = 1/√(1 − β²)
```
Imagine a clock with two mirrors separated by height h, perpendicular to the ship’s motion. A tick starts when light leaves the bottom mirror and ends when it returns to the same mirror. In the ship, each leg is vertical. In the outside frame, the mirrors move sideways during each leg, giving a diagonal path. Both frames use c.
```
h = cΔτ/2
(cΔt/2)² = h² + (vΔt/2)²
Δt = Δτ/√(1 − β²) = γΔτ
```
Here Δτ is the **proper time** measured by one clock present at both events. The textbook writes it as t₀.

### Example · Work with β directly
Find γ for v = 0.80c. If one light-clock tick lasts 3.0 ns in the ship, how long does it take in the outside frame?

**Worked answer**
```
β = 0.80
γ = 1/√(1 − 0.80²) = 1/0.60 ≈ 1.667
Δt = γΔτ ≈ 5.0 ns
```

## 5 Time dilation and proper time
### Choose the clock that is present at both events
A clock travelling with an object can measure the proper interval between two ticks on that clock. A frame in which the clock moves assigns the longer coordinate interval Δt = γΔτ. The relation also works backward. Use Δτ = Δt/γ when the outside interval is given.

For two inertial observers in uniform relative motion, either one can describe the other’s moving clock as slow. Each comparison uses its own frame’s simultaneous times.

### Sample 8.1.1 · One hour aboard
A clock moving at 0.500c records one hour between two ticks. Find the outside interval and the difference between them.

**Worked answer**

γ = 1/√(1 − 0.500²) ≈ 1.1547. The outside interval is **1.155 h**, about **69.3 min**. The difference is about **9.3 min** for that one-hour proper interval.

## 6 Muons as travelling clocks
### One decay, two descriptions
A muon is an unstable particle. An average lifetime describes a population. Individual muons can decay earlier or later. In the Earth frame, time dilation increases the mean lifetime of fast-moving muons. In a frame moving with a particular muon, the atmosphere is length-contracted along the motion. The two descriptions agree about whether that muon reaches the ground.

### Example · A muon moving at 0.998c
Use the textbook’s illustrative proper mean lifetime of 2.0 μs. Find the Earth-frame mean lifetime and mean distance at 0.998c. How far away is the ground in the muon frame when the Earth-frame altitude is 7.0 km?

**Worked answer**
```
γ = 1/√(1 − 0.998²) ≈ 15.8
Earth-frame mean lifetime = γ(2.0 μs) ≈ 31.6 μs
Earth-frame mean distance = (0.998c)(31.6 μs) ≈ 9.5 km
Muon-frame distance to the ground = 7.0 km/γ ≈ 0.44 km
```
The textbook discussion switches from 0.988c in the setup to 0.998c in the calculation. Using **0.988c** throughout gives γ ≈ 6.47 and a mean distance of about **3.8 km**. That shorter mean still allows some muons to survive the trip.

## 7 Length contraction
### Measure both endpoints at the same time
The **proper length L₀** is the length measured in the object’s rest frame. To measure its length in a frame where the object moves, record both endpoint positions simultaneously in that measuring frame.
```
L = L₀/γ = L₀√(1 − β²)
β = √(1 − (L/L₀)²)
```
Only the component parallel to the motion contracts. A photograph also depends on when light from different parts arrives at the camera. Use simultaneous positions for the length calculation.

### Sample 8.1.2 · The moving metre stick
A metre stick passes you lengthwise at 0.995c. What length do you measure?

**Worked answer**

L = (1.00 m)√(1 − 0.995²) ≈ **0.100 m**, about 10.0 cm. The stick’s proper length is still 1.00 m. Use the speed from the problem statement, 0.995c, in the substitution.

## 8 Round trips and different ages
### Compare clocks when they meet again
In a round trip the traveller changes direction and switches between inertial cruising frames. The Earth clock follows a different path through spacetime. When the clocks reunite, their elapsed times can be compared directly.

For a simplified trip with a brief turnaround, calculate the traveller’s proper time on each cruise leg using its Earth-frame duration divided by γ. Add the proper times. If the speed has the same magnitude on both legs, one γ applies to their combined cruise time.

### Example · An out-and-back journey
Earth measures 10.0 years for an out-and-back trip at a cruising speed of 0.80c. Ignore the time spent turning around. How much does the traveller age?

**Worked answer**

At 0.80c, γ = 5/3. Each 5.0-year Earth-frame leg takes 3.0 years on the ship. The traveller ages **6.0 years** in total, while the Earth clock advances by 10.0 years.

## 9 Adding velocities near c
### Use signed velocities in the same direction
For a ship moving at v relative to Earth and an object launched at u′ relative to the ship, the Earth-frame velocity u along the same line is:
```
u = (u′ + v)/(1 + u′v/c²)
```
Use a negative u′ for a launch in the opposite direction. At low speeds the denominator is close to 1. For a forward light pulse, u′ = c gives u = c. This rule is needed for the last Extra Practice question.

### Example · A probe launched forward
A ship moves at 0.70c relative to Earth and launches a probe forward at 0.50c relative to itself. Find the probe speed in the Earth frame.

**Worked answer**

u = (0.70c + 0.50c)/(1 + 0.70 × 0.50) ≈ **0.889c**. Adding the two speeds without the denominator would incorrectly give 1.20c.

## 10 Relativistic momentum and the speed limit
### Invariant mass stays fixed
For a particle of invariant mass m, momentum is p = γmv. Momentum and energy increase as the particle speeds up. The mass m stays the same.
```
p = γmv
p/(mc) = γβ
Average net force = Δp/Δt in the chosen frame
```
At low speed, γ ≈ 1 and p ≈ mv. As v approaches c from below, γ grows without bound. A massive particle cannot reach c with finite energy.

### Example · Compare two momentum models
Find p in units of mc for a particle moving at 0.87c. Compare the Newtonian and relativistic results.

**Worked answer**

Newtonian p/(mc) = **0.87**. Relativistic p/(mc) = 0.87/√(1 − 0.87²) ≈ **1.76**. The relativistic value is about twice as large at this speed.

## 11 Rest energy, total energy, and kinetic energy
### Use the energy formula that matches the question
A particle at rest has **rest energy** E₀ = mc². A moving particle has total energy E = γmc². Kinetic energy is the increase above rest energy.
```
E₀ = mc²           E = γmc²
K = E − E₀ = (γ − 1)mc²
1 kWh = 3.6 × 10⁶ J
```
When a system loses rest mass, the associated energy difference is ΔE = Δmc². For example, a reaction can release energy as radiation and kinetic energy while conserving total energy.

### Example · Mass equivalent and electricity
If 1.00 mg of mass could be fully converted into usable energy, how many joules and kilowatt-hours would it provide?

**Worked answer**
```
m = 1.00 × 10⁻⁶ kg
E = (1.00 × 10⁻⁶)(3.00 × 10⁸)² = 9.00 × 10¹⁰ J
E = (9.00 × 10¹⁰)/(3.6 × 10⁶) ≈ 2.50 × 10⁴ kWh
```
This is an energy equivalent under the stated complete-conversion assumption.

## 12 Applying the models
### Work from the measurement
1. Name the reference frame and the two events or endpoints.
2. Identify the proper time or proper length, if either is given.
3. Compute β and γ. Check that a massive object has |β| < 1.
4. Compare directions and units. Moving-clock coordinate time is larger than proper time, and longitudinal moving length is smaller than proper length.

Special relativity describes clocks and motion in flat spacetime, including accelerated paths. General relativity accounts for gravity through curved spacetime. A clock comparison in a gravitational field can depend on the paths or heights of the clocks.

### Example · Identify the frame before calculating
A 60 m ship passes Earth at 0.80c. The 60 m length comes from an Earth-frame measurement. During a separate clock test the ship records 12 s between two ticks. Find the proper length and the Earth-frame interval.

**Worked answer**

γ = 5/3. The **proper length is 100 m**, since L₀ = γL. The **Earth-frame interval is 20 s**, since Δt = γΔτ. The two given measurements belong to different frames.

### Chapter scope
These notes follow BC Science Physics 11 Chapter 8, printed pp. 259–278. The measurement of simultaneous endpoints, the light-clock derivation, and the velocity-addition example connect the chapter’s formulas to the reference frames in which they apply.
