@chapter: Physics 11
@title: Energy
@subtitle: Work, power, machines, mechanical energy, temperature, heat transfer, and measuring thermal energy.

# Energy

## 1 Energy and work
### What energy means
**Energy is the capacity to do work.** It can be stored or transferred in different forms: kinetic, gravitational potential, elastic potential, chemical, electrical, nuclear, thermal, light, and sound.

A bouncing ball links many of these forms. During a fall, gravitational potential energy becomes kinetic energy. During contact, the ball deforms and briefly stores elastic energy. Some energy spreads into thermal energy and sound, so the rebound is lower.

### When a force does work
Work measures energy transferred by a force acting through a displacement. For a constant force parallel to the displacement:
```
W = Fd
1 J = 1 N·m = 1 kg·m²/s²
```
- W: work, in joules (J)
- F: force, in newtons (N)
- d: displacement along the force, in metres (m)

More generally, use the component of force parallel to the displacement:
```
W = Fd cos θ
```
The angle θ is between the force and displacement. Work is **positive** when the force helps the motion, **negative** when it opposes it, and **zero** when force and displacement are perpendicular or there is no displacement. Work and energy are scalars.

### Sample problem 5.1.1: lifting a golf ball
A golfer lifts a **46 g** ball through **0.95 m** at a steady speed. How much work does the golfer do? Textbook p. 132.

**Worked answer**
```
m = 46 g = 0.046 kg
F = mg = (0.046)(9.81) = 0.45126 N
W = Fd = (0.45126)(0.95) = 0.428697 J
```
The golfer does **0.43 J** of positive work. Gravity does **−0.43 J** of work. The net work is zero because the ball's speed stays constant.

### Practice 5.1.1: pushing and climbing
1. A steady **25 N** force pushes a concrete block **4.3 m** along a floor in the direction of the force. Find the work done by this force.
2. A **70.0 kg** person climbs stairs with a vertical rise of **25.0 m** at a steady pace. Find the increase in gravitational potential energy.
3. You push a stuck car with **300.0 N** for **10.0 s**, but it does not move. Find the mechanical work done on the car. Textbook p. 133.

**Worked answer**
```
1. W = Fd = (25)(4.3) = 107.5 J ≈ 1.1 × 10² J
2. ΔEₚ = mgh = (70.0)(9.81)(25.0)
         = 17 167.5 J ≈ 1.72 × 10⁴ J
3. W = Fd = (300.0)(0) = 0 J
```
For the stairs, use the **vertical rise**, not the length of the staircase. For the stuck car, a person can expend chemical energy without doing mechanical work on the stationary car.

### Source and conventions
These lessons adapt **BC Science Physics 11, Chapter 5: Energy**, printed pp. **132–172** (PDF pages **137–177**). They cover sections 5.1–5.4, selected textbook questions, and the main investigations. Extra explanations and review examples support the textbook material.

Use **g = 9.81 m/s²** unless a question states otherwise. Use the textbook value **c = 4200 J/(kg·°C)** for water. Convert grams to kilograms, centimetres to metres, minutes to seconds, and kilojoules to joules before substituting.

## 2 Power and horsepower
### Energy per second
**Power is the rate at which work is done or energy is transferred.** Two motors may lift the same load through the same height, doing the same useful work, but the faster motor has greater useful power.
```
P = W / Δt = ΔE / Δt
W = PΔt
1 W = 1 J/s
1 kW = 1000 W
1 MW = 1 000 000 W
```
The letter W represents **work** in an equation; the unit W represents a **watt**. A joule is an amount of energy, while a watt is a rate of energy transfer.

### Sample problem 5.1.2: a toy motor
A motor does **4200 J** of work in **70.0 s**. Find its average power output. Textbook p. 133.

**Worked answer**
```
P = W / Δt = 4200 / 70.0 = 60 W
```
The motor transfers **60 J of useful mechanical energy each second**, on average.

### Practice 5.1.2: baggage and a light bulb
1. A baggage handler raises **42 bags**, averaging **24 kg** each, through **1.6 m** in **3.6 min**. Calculate useful average power.
2. How much energy does a **150 W** light bulb transfer in **1.0 h**? Textbook p. 134.

**Worked answer**
```
1. Δt = 3.6 × 60 = 216 s
   W = 42mgh = (42)(24)(9.81)(1.6) = 15 821.568 J
   P = W / Δt = 73.248 W ≈ 73 W

2. Δt = 3600 s
   E = PΔt = (150)(3600) = 540 000 J = 0.54 MJ
```
The light bulb's energy output includes both light and thermal energy.

### Sample problem 5.1.3: horsepower
A motor lifts a **650 N** load vertically through **12 m** in **11 s**. Find output power in watts and horsepower. Textbook pp. 134–135.
```
1 hp ≈ 746 W
```

**Worked answer**
```
W = Fd = (650)(12) = 7800 J
P = 7800 / 11 = 709.09 W ≈ 7.1 × 10² W
Power in hp = 709.09 / 746 = 0.9505 hp ≈ 0.95 hp
```
Use the conversion factor provided in a question if it rounds one horsepower differently.

## 3 Pulleys, work, and mechanical advantage
### Trading force for distance
A pulley system can reduce the effort force needed to lift a load. The trade-off is that you pull a greater length of rope. An ideal machine **does not reduce the work required**.
```
Wᵢₙ = Fₑdₑ                 Wₒᵤₜ = Fₗdₗ
Ideal machine: Fₑdₑ = Fₗdₗ
Actual mechanical advantage, AMA = Fₗ / Fₑ
Ideal mechanical advantage, IMA = dₑ / dₗ
```
- Fₑ and dₑ: effort force and effort distance
- Fₗ and dₗ: load force and load distance

For a simple ideal pulley system, count the rope segments **supporting the moving load assembly**. Equal rope tension means that n supporting segments can share the load, giving IMA = n. A fixed pulley can simply change the direction of the pull.

### Investigation 5-1A: getting work done with pulleys
The textbook compares arrangements that lift a **2.0 N** load by **0.100 m**. For each arrangement, measure effort force and effort distance, then compare input and output work. Textbook pp. 136–137.

### Practice example: a two-segment lift
In an ideal pulley system with **two supporting rope segments**, lift that 2.0 N load by 0.100 m. Find effort force, effort distance, and work.

**Worked answer**
```
IMA = 2
Fₑ = Fₗ / 2 = 1.0 N
dₑ = 2dₗ = 0.200 m
Wᵢₙ = (1.0)(0.200) = 0.20 J
Wₒᵤₜ = (2.0)(0.100) = 0.20 J
```
The effort is halved, but the pulling distance doubles. Real pulleys require extra input work because of friction and other transfers.

### Investigation 5-1B: a small motor
A motor winds a string to raise a measured mass through height h. Measure the lifting time, repeat several trials, and calculate useful output power:
```
Pₒᵤₜ = mgh / Δt
```
This measures the power delivered to the load, rather than the electrical input power. Record the mass, height, time, and trial-to-trial variation. Textbook p. 138.

## 4 Kinetic energy and the work-energy theorem
### Energy of motion
An object with **kinetic energy** can do work because it is moving. For the ordinary speeds used in this chapter:
```
Eₖ = ½mv²
```
Use mass in kilograms and speed in metres per second. Doubling mass doubles Eₖ; doubling speed **quadruples** Eₖ. Kinetic energy is nonnegative and does not indicate direction.

### Why the equation contains one half
For a constant net force accelerating an object from rest, combine Newton's second law with the kinematics equation:
```
Wₙₑₜ = Fₙₑₜd = mad
v² = 2ad  →  ad = v²/2
Wₙₑₜ = ½mv²
```
If the object is already moving, compare its final and initial kinetic energies:
```
Wₙₑₜ = ΔEₖ = ½mv²f − ½mv²i
```
Use the **net work of all forces**. Positive net work increases speed; negative net work reduces speed. The work of a single force need not equal ΔEₖ when other forces also do work.

### Quick check: doubling mass or speed
The textbook asks whether doubling a golf club's mass or doubling its striking speed has the greater effect on its kinetic energy. Textbook p. 143.

**Worked answer**
Doubling mass gives **2Eₖ**. Doubling speed gives **4Eₖ**. Doubling speed has the greater effect on the club's kinetic energy. The ball's resulting motion also depends on the collision.

### Quick check: slowing a vehicle
A **1200 kg** vehicle slows from **80 km/h** to **50 km/h**. Find the net work done on it. Textbook p. 143.

**Worked answer**
```
vᵢ = 80 / 3.6 = 22.222… m/s
vf = 50 / 3.6 = 13.888… m/s
Wₙₑₜ = ½(1200)[(13.888…)² − (22.222…)²]
       = −180 555.6 J ≈ −1.8 × 10⁵ J
```
The negative work removes kinetic energy. Braking and resistive forces transfer that energy mainly into thermal energy of the brakes, tires, road, and surroundings.

## 5 Gravitational potential energy and reference levels
### Energy associated with height
Lifting a mass slowly near Earth's surface requires an upward force approximately equal to its weight. The work increases the gravitational potential energy of the object–Earth system:
```
Eₚ = mgh
ΔEₚ = mg(hf − hᵢ)
```
Here h is **vertical height above the chosen zero level**. The formula assumes g is approximately constant. Travelling farther along a ramp does not increase the height gained.

### Choosing zero potential energy
You may choose the floor, a tabletop, or the lowest point of a swing as zero. State your choice and keep it throughout the calculation. Only **changes** in potential energy affect the prediction.

For a **1.0 kg** book held **0.50 m above a 1.0 m table**, using g = 9.8 m/s² gives **4.9 J relative to the table** or **14.7 J relative to the floor**. The change in energy from the tabletop to the raised position is 4.9 J in either reference system.

### From stored energy to motion
The source basketball diagram shows potential energy changing into kinetic energy as a released ball falls. Choose the floor as zero height. A ball held at rest initially has Eₖ = 0; just before reaching the floor, its gravitational potential energy approaches zero.

### Quick check: lifting a television
It takes **620 J** of work against gravity to raise a television **2.5 m**, with no change in speed. Find its mass. Textbook p. 144.

**Worked answer**
```
W = mgh
m = W / (gh) = 620 / [(9.81)(2.5)]
  = 25.28 kg ≈ 25 kg
```
This assumes all the stated work increases gravitational potential energy.

### Quick check: lifting twice as high
A box gains a certain gravitational potential energy when lifted **5 m**. What happens if it is lifted another **5 m**? Textbook p. 144.

**Worked answer**
With approximately constant g, the second 5 m lift adds **the same amount** of potential energy as the first. The total gain from the initial position is doubled.

## 6 Conservation of mechanical energy
### Track the whole energy balance
**Energy cannot be created or destroyed.** It can transfer between objects and change form. In an isolated system, total energy stays constant.

Mechanical energy is the sum of kinetic and potential energies. When drag and friction are negligible and no external agent adds energy:
```
Eₘ = Eₖ + Eₚ
Eₖᵢ + Eₚᵢ = Eₖf + Eₚf
½mv²i + mghᵢ = ½mv²f + mghf
```
This equation applies to falls, swings, and frictionless tracks. The path can curve: it is the **change in vertical height** that matters. For release from rest through a vertical drop Δh:
```
v = √(2gΔh)
```
The mass cancels. The result gives speed; find the direction from the path.

### Sample problem 5.2.1: a pendulum
A pendulum bob is raised **0.36 m** above its lowest position and released from rest. Find its speed at the bottom, ignoring resistance. Textbook p. 146.

**Worked answer**
```
Choose Eₚ = 0 at the bottom.
mgh = ½mv²
v = √(2gh) = √[(2)(9.81)(0.36)]
  = 2.6577… m/s ≈ 2.7 m/s
```
Use the vertical rise of the bob, rather than the string length or arc length.

### Practice 5.2.1: a web swing
A person swings from rest on a **9 m** web line, starting **3.0 m above** the lowest point. Find the bottom speed. Textbook p. 147.

**Worked answer**
```
v = √(2gΔh) = √[(2)(9.81)(3.0)]
  = 7.672… m/s ≈ 7.7 m/s
```
The 9 m line length is not the height lost. The ideal model assumes the line remains taut and resistance is negligible.

### Practice 5.2.1: a runaway hill
A vehicle enters a runaway hill at **90 km/h (25 m/s)**. Ignoring friction, how far does it rise vertically before stopping? Textbook p. 147.

**Worked answer**
```
½mv² = mgh
h = v² / (2g) = 25² / [(2)(9.81)]
  = 31.855… m ≈ 32 m
```
This is vertical rise, rather than distance along the hill. Friction would make the stopping height smaller.

### Practice 5.2.1: a roller coaster
A **500 kg** car travels at **10 m/s** at the bottom. What is the maximum height it can reach without added work, ignoring friction? Textbook p. 147.

**Worked answer**
```
h = v² / (2g) = 10² / 19.62 = 5.0968… m ≈ 5.1 m
```
At this limiting height its speed is zero. For the car to **pass over** a hill with some speed remaining, the crest must be lower than this limit, or more energy must be supplied.

## 7 Friction, rebounds, and energy accounting
### Mechanical energy can decrease
When a cart rubs against a track or a ball deforms during impact, mechanical energy can become thermal energy, sound, and deformation energy. Total energy is still conserved when all stores and transfers are included.

For a system that includes the moving object, Earth, and the rubbing surfaces, a useful model is:
```
Eₘᵢ + Wₑₓₜ = Eₘf + ΔEₜₕ
```
Here Wₑₓₜ is work added from outside the system; ΔEₜₕ is the increase in thermal energy within it. If sound leaves the system, include that energy transfer as well.

For constant sliding friction against a stationary surface:
```
Work by friction on the object: Wf = −fₖd
Thermal energy increase of object + surface: ΔEₜₕ ≈ fₖd
```
Count the friction effect once. Use either its work on the chosen object or the thermal increase of the larger system consistently.

### Practice example: a rough track
A **2.00 kg** cart starts from rest **3.00 m** above the bottom. The cart–track–Earth system gains **10.0 J** of thermal energy during the descent. Find the bottom speed. Additional review example.

**Worked answer**
```
Eₘᵢ = mgh = (2.00)(9.81)(3.00) = 58.86 J
Eₖf = 58.86 − 10.0 = 48.86 J
vf = √(2Eₖf/m) = √[(2)(48.86)/2.00]
   = 6.99 m/s
```
Without friction, the speed would be 7.67 m/s. The smaller speed reflects conversion into thermal energy.

### Review: a bouncing ball
A ball falls from **2.0 m** and rebounds to **1.6 m**. What fraction of its initial mechanical energy remains at the top of the rebound? Adapted from section 5.2 review, p. 149.

**Worked answer**
```
Eᵢ = mg(2.0)       Ef = mg(1.6)
Ef / Eᵢ = 1.6 / 2.0 = 0.80
```
**80% remains as mechanical energy; 20% has changed into other forms or left the ball–Earth mechanical system.** The mechanical-energy loss is not the same as saying 20% of total energy disappeared.

### Review: a cart's spring bumper
A **2.6 kg** cart moves at **2.0 m/s** into a barrier and momentarily stops as its bumper spring compresses **0.12 m**. Ignoring losses, find the stored elastic energy and the average force magnitude during compression. Section 5.2 review, p. 149.

**Worked answer**
```
Eelastic = Eₖᵢ = ½mv² = ½(2.6)(2.0)² = 5.2 J
Faverage = Eelastic / d = 5.2 / 0.12 ≈ 43 N
```
The cart's kinetic energy becomes **elastic potential energy** in the spring, another form of mechanical energy. The spring force changes during compression, so this is the average magnitude rather than its final value. An ideal spring can return that stored energy as it expands.

### Connecting mechanics to thermal energy
The section 5.2 warm-up asks you to shake a container of sand and compare its temperature before and after. Work done by your hand can increase the internal energy of the sand and container. Any measured change also depends on energy transfer to the surroundings.

## 8 Particles, temperature, thermal energy, and heat
### The kinetic molecular picture
Matter consists of atoms or molecules in motion. Depending on the material and molecular structure, particles can have **translational, rotational, and vibrational motion**. Interactions between particles also store potential energy.

### Three terms to keep separate
- **Temperature** describes thermal state. In the ideal-gas model it is proportional to average translational kinetic energy per particle.
- **Thermal energy**, as used in this chapter, is the microscopic energy associated with the particles and their interactions. Its amount depends on the quantity and kind of material as well as its state and temperature.
- **Heat** is energy transferred because of a temperature difference. It flows spontaneously from a hotter object to a colder one.

An object contains internal energy; it does not contain a stored quantity of “heat.” Heat names a transfer. Thermal equilibrium means the objects have the **same temperature** and no net heat transfer between them.

### Quick check: a drop and a bucket
A drop and a bucket of water are both at **100°C**. Which has the higher temperature and which has more thermal energy? Based on p. 151.

**Worked answer**
They have **the same temperature**. The bucket has much more thermal energy because it contains far more water. For the same material and state, a larger amount of material at the same temperature has more microscopic energy.

### Quick check: a hot nail in water
A small red-hot nail is dropped into a large pot of near-boiling water. Which way does heat flow, and what is equal when they reach equilibrium? Textbook p. 152.

**Worked answer**
Initially, the nail has the higher temperature, so heat flows **from the nail to the water**. At equilibrium they have the same temperature, but they need not have equal internal energies. Mass, material, and microscopic energy storage also matter.

## 9 Celsius, kelvins, and absolute zero
### Temperature scales
On the Celsius scale, water freezes at about **0°C** and boils at about **100°C at standard atmospheric pressure**. Absolute zero is **0 K**, equivalent to **−273.15°C**.
```
T(K) = T(°C) + 273.15
T(°C) = T(K) − 273.15
ΔT in kelvins = ΔT in degrees Celsius
```
A kelvin and a Celsius degree have the same size. Write **K**, not “°K.” The textbook often rounds 273.15 to **273**.

### Why gas-energy ratios need kelvins
For an ideal gas, average translational kinetic energy is proportional to **absolute temperature in kelvins**. Doubling a Celsius temperature does not generally double this energy.

Absolute zero is the lower limit of thermodynamic temperature. The classical model takes translational thermal kinetic energy toward zero there; it does not justify the claim that all microscopic quantum motion must vanish.

### Quick check: helium at 20°C
One helium sample is at **20°C**. In a second sample, atoms have **twice the average translational kinetic energy**. Find the second temperature in kelvins and degrees Celsius. Textbook p. 152.

**Worked answer**
```
T₁ = 20 + 273.15 = 293.15 K
T₂ = 2T₁ = 586.30 K
T₂ in °C = 586.30 − 273.15 = 313.15°C
```
Approximately **586 K or 313°C**. Using the textbook's rounded 273 gives the same whole-number result. Doubling 20°C to 40°C would be incorrect.

### Practice example: a temperature change
Water warms from **20.0°C to 60.0°C**. Find the temperature change in Celsius degrees and kelvins. Additional review example.

**Worked answer**
```
ΔT = 60.0 − 20.0 = 40.0°C = 40.0 K
```
Add 273.15 to convert an absolute temperature; **do not add it to a temperature change**.

## 10 Conduction, convection, radiation, and insulation
### Conduction
**Conduction transfers energy through microscopic interactions without bulk flow of the material.** A heated end of a rod passes energy along it. Metals conduct well partly because mobile electrons help transfer energy.

A metal surface can feel colder than wood at the same room temperature because it transfers energy away from your hand faster. Touch measures the effect of heat transfer as well as temperature.

### Convection
**Convection transfers energy by the bulk movement of a fluid**, such as water or air. A warmed region often expands, becomes less dense, and rises through cooler fluid. Cooler, denser fluid moves in to replace it, creating circulation.

A kettle heats water efficiently through convection even though water conducts poorly. Ordinary convection requires fluid motion; it cannot carry energy across empty space.

### Radiation
**Radiation transfers energy by electromagnetic waves** and can travel through a vacuum. This is how energy from the Sun reaches Earth. Objects also emit thermal radiation; net radiative transfer is from hotter to colder surroundings.

Dark, matte surfaces commonly absorb radiation more effectively than shiny metallic surfaces. Absorption depends on wavelength and material, so visible colour alone does not determine every infrared property.

### Quick check: sea breezes
On a sunny day, land warms faster than nearby water. At night, land can cool faster. Predict the idealized near-surface breeze in each case. Textbook p. 154.

**Worked answer**
During the day, air warmed over land rises and cooler surface air moves **from sea to land**: a sea breeze. At night, if the sea is warmer, air rises over the sea and surface air moves **from land to sea**: a land breeze. Air returns in the opposite direction higher up, completing each circulation. Actual winds also depend on broader weather conditions.

### Quick check: a vacuum flask
Explain how a vacuum flask reduces all three routes of energy transfer. Textbook p. 154.

**Worked answer**
The **vacuum gap** greatly reduces conduction and prevents convection across the gap. **Reflective surfaces** reduce radiative transfer. An **insulating stopper** reduces conduction through the neck and limits fluid exchange and evaporation. No insulation stops every route completely.

### Quick check: dirty snow
Which usually melts faster in sunlight: fresh snow or snow darkened by dirt? Textbook p. 154.

**Worked answer**
Snow darkened by a thin layer of dirt generally absorbs more solar radiation and melts faster than clean, reflective snow under otherwise similar conditions. Absorbed radiation transfers energy into the snow.

## 11 Investigating heat transfer
### Investigation 5-3A: conduction
The textbook compares rods of different metals heated at one end or at a common junction. Wax holding small objects melts as energy travels along each rod. **Use the observed order to rank the tested conductors**, keeping rod dimensions and heating conditions comparable. Textbook pp. 155–156.

Another demonstration heats water near the top of a tube while ice remains at the bottom. The result shows that water is a poor conductor and that top heating does not readily establish a convection circulation down to the ice. Flame and hot-glass demonstrations belong in a supervised laboratory.

### Investigation 5-3B: convection
Food colouring traces circulation in a water-filled loop. The warmed water rises near the heated side while cooler water descends elsewhere. In the convection box, warm air above a candle rises out of one chimney, drawing cooler air into the other. Textbook p. 157.

### Investigation 5-3C: infrared absorption
Compare two otherwise similar containers: one black, one covered with shiny foil. Use equal water masses and initial temperatures, equal distances from the lamp, and the same exposure time. Record temperature every minute. Textbook p. 158.

The expected greater warming of the black container supports greater absorption under the test conditions. Keep container size and insulation comparable; different water masses could change the temperature rise even with equal absorbed energy.

### Practice example: interpreting an absorption experiment
Two containers each hold **0.100 kg** of water. Over the same exposure, the black container warms **4.0°C** and the shiny one **1.0°C**. Estimate the energy gained by each water sample. Additional review example.

**Worked answer**
```
Eblack = mcΔT = (0.100)(4200)(4.0) = 1680 J
Eshiny = mcΔT = (0.100)(4200)(1.0) = 420 J
```
The black container's **water gains four times as much energy**. This comparison uses water energy only; container heating and losses to the room also affect a full experimental balance.

## 12 Specific heat capacity and thermal calculations
### Energy needed for a temperature change
**Specific heat capacity, c**, is the energy required to raise the temperature of 1 kg of a substance by 1°C (or 1 K). A high c means a large energy transfer produces a relatively small temperature change.
```
Q = ΔE = mcΔT
ΔT = Tf − Tᵢ
c = Q / (mΔT)
```
- Q: heat transferred to the sample, in joules
- m: mass, in kilograms
- c: specific heat capacity, in J/(kg·°C) or J/(kg·K)
- ΔT: temperature change, in °C or K

In this simple model, **Q > 0** for warming and **Q < 0** for cooling. The magnitude of heat released is positive. Use this equation for temperature changes **without a phase change**, with c approximately constant. It does not describe the energy needed to melt or boil a sample at constant temperature.

### Textbook specific heat capacities
Selected values from Table 5.4.1, p. 160. Use the value supplied by a question when available.
```
Material        c, J/(kg·°C)
Water           4200
Methyl alcohol  2400
Ethylene glycol 2200
Ice             2100
Kerosene        2100
Steam           2100
Aluminum         920
Glass            840
Iron             450
Copper           430
Lead             130
```
These are the textbook's assigned values. A large body of water changes temperature slowly partly because water has a high specific heat capacity and the total mass is large. Water is also useful as a coolant because it can absorb substantial energy for a given temperature rise.

### Sample problem 5.4.1: warming a water tank
Add **25 kJ** to **50.0 kg** of water initially at **20.0°C**. Find final temperature, assuming the water receives all the energy. Textbook p. 161.

**Worked answer**
```
Q = 25 000 J
ΔT = Q / (mc) = 25 000 / [(50.0)(4200)]
   = 0.1190…°C
Tf = 20.0 + 0.1190… = 20.1190…°C ≈ 20.1°C
```
Calculate the **change** first, then add it to the initial temperature.

### Practice 5.4.1: heating and cooling water
1. Find the heat needed to warm **90.0 kg** of water from **18°C to 80°C**.
2. Add **1.0 MJ** to **10.0 kg** of water initially at **15°C**. Find final temperature.
3. **12 kg** of water cools from **100°C to 20°C**. Find the heat released. Textbook p. 161.

**Worked answer**
```
1. ΔT = 80 − 18 = 62°C
   Q = (90.0)(4200)(62) = 23 436 000 J ≈ 23 MJ

2. ΔT = 1.0 × 10⁶ / [(10.0)(4200)] = 23.81…°C
   Tf = 15 + 23.81… ≈ 39°C

3. ΔT = 20 − 100 = −80°C
   Qwater = (12)(4200)(−80) = −4 032 000 J
   Heat released ≈ 4.0 MJ
```
Cooling gives a negative Q for the water and a positive transfer into its surroundings.

### Practice 5.4.1: identifying a heat capacity
It takes **1200 J** to warm **0.500 kg** of brass from **20.0°C to 26.2°C**. Find its specific heat capacity. Textbook p. 161.

**Worked answer**
```
ΔT = 26.2 − 20.0 = 6.2°C
c = Q / (mΔT) = 1200 / [(0.500)(6.2)]
  = 387.10… J/(kg·°C) ≈ 3.9 × 10² J/(kg·°C)
```
Using the final temperature instead of the temperature change would give the wrong result.

## 13 Heating power and efficiency
### Useful output compared with input
For a heat source, power is the rate of energy transfer. Efficiency compares the useful output with the total input:
```
P = ΔE / Δt
η = Euseful / Einput
η = Puseful / Pinput  (over the same interval)
Efficiency (%) = η × 100%
Euseful = ηEinput
```
Use η as a decimal in calculations: **80% = 0.80**. The part not counted as useful still goes somewhere, such as heating the device, warming the room, sound, or friction.

“Useful” depends on the purpose. Light is the useful output of a lamp; heating the water is the useful output of a kettle. Low useful efficiency does not contradict conservation of energy.

### Sample problem 5.4.2: a motorcycle ramp
A **1200 N** motorcycle is raised **1.3 m** using a ramp **2.4 m** long. The effort force along the ramp is **820 N**. Find the efficiency. Textbook p. 162.

**Worked answer**
```
Euseful = Fload × h = (1200)(1.3) = 1560 J
Einput = Feffort × d = (820)(2.4) = 1968 J
η = 1560 / 1968 = 0.79268…
Efficiency ≈ 79%
```
The effort acts through the **ramp distance**; useful gravitational energy depends on the **vertical rise**. This model assumes no change in the motorcycle's speed.

### Practice 5.4.2: pulleys, kettles, and bulbs
1. A pulley receives **500 J** to lift a **150 N** load by **3.0 m**. Find efficiency.
2. A **1200 W** kettle is **80% efficient**. Find the useful rate of energy transfer to water.
3. A **60 W** bulb is **5.0% efficient** at producing light. Find the light output power. Textbook p. 163.

**Worked answer**
```
1. Euseful = (150)(3.0) = 450 J
   η = 450 / 500 = 0.90 → 90%

2. Puseful = ηPinput = (0.80)(1200) = 960 W

3. Plight = (0.050)(60) = 3.0 W
```
For the bulb, the remaining 57 W is transferred mainly into thermal energy rather than useful light.

### Practice 5.1.2: a large lifting system
A lifting system is **25% efficient** and receives **1.5 × 10⁸ W** for **2.0 h**. Find useful work and the energy transferred into other forms. Textbook p. 134.

**Worked answer**
```
Δt = 2.0 × 3600 = 7200 s
Einput = PΔt = (1.5 × 10⁸)(7200) = 1.08 × 10¹² J
Euseful = (0.25)(1.08 × 10¹²) = 2.7 × 10¹¹ J
Eother = (0.75)(1.08 × 10¹²) = 8.1 × 10¹¹ J
```
Most of the other output is typically thermal energy. Use the same operating interval for input and useful output.

### Practice example: heating time with losses
An **80% efficient, 1200 W** kettle warms **0.500 kg** of water from **20.0°C to 60.0°C**. Find the heating time, assuming constant efficiency and no phase change. Additional review example.

**Worked answer**
```
Qwater = mcΔT = (0.500)(4200)(40.0) = 84 000 J
Pwater = (0.80)(1200) = 960 W
Δt = Qwater / Pwater = 84 000 / 960 = 87.5 s
```
Using the full 1200 W as useful water-heating power would underestimate the time.

## 14 Measuring heating power and reviewing the chapter
### Investigation 5-4: power of a hot plate
The textbook heats **0.300 kg** of water, recording temperature every **30 s** for up to **10 min**. Keep the thermometer away from the beaker bottom and stop the analysis before boiling. Plot temperature vertically and time horizontally. Textbook p. 164.

### Read a temperature-time graph
The slope tells you how quickly the water warms. Use a best-fit straight segment where heating is approximately steady:
```
Slope = ΔT / Δt        in °C/s
Pwater = mc(ΔT/Δt) = mc × slope
η = Pwater / Pinput
```
This measures **useful power absorbed by the water**. Some input energy heats the beaker, plate, and air. Heat loss can increase as the water gets hotter, causing the graph's slope to decrease.

### Practice example: from slope to power
A **0.300 kg** water sample warms from **20.0°C to 32.0°C in 120 s**. The heater input rating is **200 W**. Find average useful power and efficiency. Illustrative data for Investigation 5-4.

**Worked answer**
```
Slope = (32.0 − 20.0) / 120 = 0.100°C/s
Pwater = (0.300)(4200)(0.100) = 126 W
η = 126 / 200 = 0.630 → 63.0%
```
The water receives 15 120 J while the input supplies 24 000 J. The remaining 8880 J heats other parts of the apparatus or goes to the surroundings. The difference is not evidence that energy has been destroyed.

### Choose an equation by the question
- **Force through a displacement:** W = Fd cos θ.
- **Work or energy per time:** P = W/Δt or P = ΔE/Δt.
- **Moving object:** Eₖ = ½mv²; net work changes Eₖ.
- **Vertical height change:** ΔEₚ = mgΔh.
- **Negligible friction or drag:** Eₖᵢ + Eₚᵢ = Eₖf + Eₚf.
- **Warming or cooling:** Q = mcΔT, without a phase change.
- **Useful output and total input:** η = Euseful/Einput.
- **Heating graph:** Pwater = mc × slope.

### Final check: two ways to stop
Two identical vehicles move at speeds v and 2v. The same constant braking force stops each on a level road. How do the work needed and stopping distances compare? Additional chapter review example.

**Worked answer**
The faster vehicle has **four times the kinetic energy**. Each needs negative net work equal in magnitude to its initial kinetic energy. With the same braking-force magnitude, **Fd = Eₖ**, so the faster vehicle needs **four times the stopping distance** in this ideal model. Reaction distance is a separate part of a driver's total stopping distance.

### Before finishing a solution
State the system and assumptions, choose a reference height when needed, convert units, write the energy balance, and then substitute. Keep extra digits during calculations and round the final result to match the data. Check whether the result is a speed, an energy, a power, or a percentage.

For further practice, use the section reviews on pp. **139–141, 148–149, 159, and 165–166**, the Chapter 5 review on pp. **167–170**, and extra practice on pp. **171–172** of the source textbook.
