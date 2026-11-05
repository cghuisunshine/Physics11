@chapter: Physics 11 · Unit 6
@title: Unit 6: Energy & Thermal Physics
@subtitle: Track work and energy in a defined system, calculate power and efficiency, and apply energy conservation to heating.

## 6.1 Work and force-displacement graphs

### Learning goal
Determine the sign and magnitude of work, including work by a changing force.

### Understand the model
Work is energy transfer by a force acting through displacement. For a constant force, only the component parallel to displacement contributes. A forward pull can do positive work, friction on a sliding block negative work, and a perpendicular normal force zero work along a level surface. Work is a scalar measured in joules.

If force changes with position, compute the signed area under the graph of the force component parallel to displacement. A rectangular area represents constant force; a triangular area represents a linear rise from zero. This graphical method gives the algebra-level meaning of the textbook’s integral. Holding a load stationary involves no mechanical work on that load because displacement is zero, even though a person uses metabolic energy.

### Equations and units
```text
W = Fd cos θ  (constant force)
W = signed area under F_parallel-versus-position graph
1 J = 1 N·m
```

### Worked example
A 30.0 N pull acts 60.0° above a horizontal displacement of 4.00 m. Separately, find work for a force rising linearly from 0 to 20.0 N over 0.500 m.

1. Constant-force work: W = (30.0)(4.00) cos 60.0° = +60.0 J.
2. The perpendicular component does no work along the horizontal displacement.
3. For the changing force, the triangular graph area is ½(0.500)(20.0) = 5.00 J. Using the final force for the whole distance would incorrectly give 10.0 J.

### Common mistakes
The angle belongs between force and displacement. A force being present is not sufficient for nonzero work on the chosen object.

### Your turn
1. A 10 N friction force opposes 3.0 m of sliding. Find its work on the block.
2. What work does a normal force do during horizontal motion on a level rigid surface?

### Solutions and reasoning
**1.** W = (10)(3.0) cos 180° = -30 J.

**2.** Zero in the simple model, because the normal force is perpendicular to displacement.

### Textbook reading
Section 7-2, PDF page 187 (printed page 151); Section 7-5, PDF page 198 (printed page 162).

## 6.2 Kinetic energy and the work-energy theorem

### Learning goal
Use net work to calculate a change in speed without first finding time.

### Understand the model
Kinetic energy is the energy associated with motion. For speeds far below the speed of light, K = ½mv². Speed is squared, so kinetic energy is nonnegative and does not encode direction. Doubling speed quadruples kinetic energy at the same mass.

The net work on a particle equals its change in kinetic energy. Add the work of all forces, not just the applied force. Positive net work increases kinetic energy; negative net work reduces it. This method is useful when displacement and forces are known but time is not. It does not directly determine a velocity direction, so interpret the final speed using the motion and geometry.

### Equations and units
```text
K = ½mv²
W_net = ΔK = K_f - K_i
v_f² = v_i² + 2W_net/m
```

### Worked example
A 2.00 kg cart initially travels at 3.00 m/s. Its net work over a track segment is +16.0 J. Find final speed.

1. K_i = ½(2.00)(3.00)² = 9.00 J.
2. K_f = 9.00 + 16.0 = 25.0 J.
3. v_f = √(2K_f/m) = √(50.0/2.00) = 5.00 m/s. No elapsed time was needed.

### Common mistakes
Use net work, not the work of one selected force unless it is the only force doing work. A speed increase does not identify the direction of the final velocity.

### Your turn
1. At fixed mass, how does kinetic energy change if speed triples?
2. A 1.00 kg object at 4.00 m/s receives -6.00 J of net work. Find its final speed.

### Solutions and reasoning
**1.** K increases by a factor of 3² = 9.

**2.** K_i = 8.00 J and K_f = 2.00 J, so v_f = √4.00 = 2.00 m/s.

### Textbook reading
Section 7-1, PDF page 185 (printed page 149); Section 7-2, PDF page 187 (printed page 151).

## 6.3 Potential energy and conservative forces

### Learning goal
Choose a potential-energy reference and calculate gravitational or spring energy changes.

### Understand the model
Potential energy belongs to a system of interacting objects. Near Earth, the object-Earth system has gravitational potential energy U_g = mgh relative to a chosen zero height. The zero is arbitrary; only changes in potential energy influence predictions. A spring stores elastic potential energy ½kx², measured from the relaxed state. Extension and compression of equal magnitude store equal energy.

For a conservative force, work depends on endpoints rather than the path, and its work is the negative change in potential energy. Gravity does positive work during descent while gravitational potential energy decreases. Stretching a spring requires positive work by the external agent while the spring itself does negative work. Avoid counting both gravitational work and the corresponding potential-energy change twice in the same energy bookkeeping.

### Equations and units
```text
U_g = mgh; ΔU_g = mgΔh
U_s = ½kx²
W_conservative = -ΔU
```

### Worked example
Raise a 3.00 kg object by 2.00 m and compress a spring of k = 200 N/m by 0.100 m. Find the stored energy changes.

1. ΔU_g = (3.00)(9.81)(2.00) = +58.9 J. The value is independent of where zero height was chosen.
2. U_s = ½(200)(0.100)² = 1.00 J, using the stated k as the model value.
3. Gravity does -58.9 J of work during the lift. The spring does -1.00 J of work while being compressed from its relaxed state.

### Common mistakes
Use metres for spring compression and height. Potential energy can be negative relative to a chosen reference without implying impossible physics.

### Your turn
1. How does spring energy change when compression doubles?
2. An object drops 5.0 m. Is ΔU_g positive or negative?

### Solutions and reasoning
**1.** It quadruples because U_s is proportional to x².

**2.** Negative: ΔU_g = mg(-5.0 m). Gravity’s work is positive.

### Textbook reading
Section 8-1, PDF page 213 (printed page 177); Section 7-4, PDF page 195 (printed page 159).

## 6.4 Conservation of energy with and without friction

### Learning goal
Choose a system boundary and include thermal energy when mechanical energy decreases.

### Understand the model
Mechanical energy is K + U. It stays constant when the system’s energy changes only through conservative transfers and no energy crosses the boundary. For a falling object-Earth system with negligible drag, gravitational potential energy becomes kinetic energy. This does not mean energy is always only mechanical.

When a block slides on a rough track, mechanical energy decreases while thermal energy of the block-track system increases. With that system chosen, use K_i + U_i + W_ext = K_f + U_f + ΔE_th. For simple constant dry friction and a stationary track, ΔE_th ≈ fₖd. If the track is outside the system, account for the energy transfer consistently rather than adding the same friction effect twice. Total energy conservation remains valid even when mechanical energy is not conserved.

### Equations and units
```text
frictionless isolated model: K_i + U_i = K_f + U_f
with thermal increase: K_i + U_i + W_ext = K_f + U_f + ΔE_th
ΔE_th ≈ fₖd  (simple sliding model)
```

### Worked example
A 2.00 kg cart starts from rest 3.00 m above the bottom of a track. The cart-track system gains 10.0 J of thermal energy. Find bottom speed.

1. Choose the bottom as U_g = 0 and include Earth and the track in the system.
2. Initial mechanical energy is mgh = 58.86 J. Final kinetic energy is 58.86 - 10.0 = 48.86 J.
3. v = √[2(48.86)/2.00] = 6.99 m/s. Without the thermal increase the speed would be √(2gh) = 7.67 m/s.

### Common mistakes
Friction does not destroy energy. It changes how energy is stored or transferred. State the system before writing a conservation equation.

### Your turn
1. A frictionless cart drops from rest through 1.25 m. Find speed.
2. A sliding friction force of 8.0 N acts over 2.5 m on a stationary track. Estimate thermal increase.

### Solutions and reasoning
**1.** v = √(2gh) = √(2 × 9.81 × 1.25) = 4.95 m/s.

**2.** ΔE_th ≈ fₖd = 20 J for the combined block-track system.

### Textbook reading
Section 8-2, PDF page 220 (printed page 184); Section 8-4, PDF page 227 (printed page 191); Section 8-5, PDF page 231 (printed page 195).

## 6.5 Power and efficiency

### Learning goal
Distinguish energy from its transfer rate and calculate useful output.

### Understand the model
Power is the rate at which energy is transferred or work is done. Two motors can lift the same load through the same height using the same useful energy, while the faster one has higher useful power. Average power uses the energy transferred over an interval. For a force acting parallel to velocity, instantaneous mechanical power is Fv.

Efficiency is useful output energy divided by total input energy, or useful output power divided by input power under corresponding conditions. A real machine often transfers energy into unwanted heating, sound, or deformation. A calculated efficiency above 100% indicates a mismatch of inputs and outputs, measurement problems, or an omitted energy source. A low efficiency does not violate total energy conservation.

### Equations and units
```text
P_avg = W/Δt = ΔE/Δt
P = Fv cos θ
η = E_useful/E_input × 100% = P_useful/P_input × 100%
1 W = 1 J/s
```

### Worked example
A motor lifts 20.0 kg by 5.00 m in 4.00 s while drawing 400 W. Find useful power and efficiency.

1. Useful energy is mgh = (20.0)(9.81)(5.00) = 981 J.
2. Useful average power is 981/4.00 = 245 W.
3. Input energy is 400 × 4.00 = 1600 J. Efficiency is 981/1600 × 100% = 61.3%, treating 400 W as the assigned input model value.

### Common mistakes
Watts are a rate; joules are an amount. Do not divide power by energy to calculate efficiency. Compare like quantities over the same interval.

### Your turn
1. A device transfers 600 J in 3.0 s. Find average power.
2. A 75% efficient motor receives 800 J. Find useful output and other energy.

### Solutions and reasoning
**1.** P = 600/3.0 = 200 W.

**2.** Useful output is 600 J; the remaining 200 J transfers into other forms or surroundings.

### Textbook reading
Section 7-6, PDF page 202 (printed page 166); Section 8-5, PDF page 231 (printed page 195).

## 6.6 Temperature, heat, and specific heat capacity

### Learning goal
Calculate energy transfer for a temperature change without a phase change.

### Understand the model
Temperature describes thermal state; it is not the total thermal energy of an object. A large cool object can contain more internal energy than a small hot object. Heat Q names energy transferred because of a temperature difference. Objects have internal energy; “heat” describes a transfer rather than an amount stored inside an object.

Specific heat capacity c is the energy needed per kilogram per degree of temperature change. Q = mcΔT assumes a suitable approximately constant c and no phase change over the interval. Q is positive for energy absorbed and negative for energy released. A change of 1 °C equals a change of 1 K, even though their absolute temperature scales differ. Use material data supplied by the problem, since values can vary with conditions.

### Equations and units
```text
Q = mc(T_f - T_i)
c unit: J/(kg·K) or J/(kg·°C)
T_K = T_°C + 273.15
ΔT_K = ΔT_°C
```

### Worked example
Heat 0.250 kg of water from 20.0 °C to 60.0 °C. Use c = 4180 J/(kg·°C). Find Q.

1. The temperature change is 60.0 - 20.0 = +40.0 °C.
2. Q = (0.250)(4180)(40.0) = 41 800 J = 41.8 kJ.
3. The positive sign means energy enters the water. Cooling the same mass through the same temperature interval releases the same energy magnitude in this model.

### Common mistakes
Do not insert an absolute temperature where the equation needs a temperature difference. Do not use Q = mcΔT across melting or boiling without separately accounting for phase change.

### Your turn
1. A 0.500 kg metal sample has c = 900 J/(kg·°C) and cools by 10.0 °C. Find Q.
2. Convert 25.0 °C to kelvin and a 25.0 °C rise to a kelvin rise.

### Solutions and reasoning
**1.** Q = (0.500)(900)(-10.0) = -4500 J using the stated model c.

**2.** Absolute temperature is 298.2 K after rounding to tenths. The temperature rise is 25.0 K.

### Textbook reading
Section 18-1, PDF page 550 (printed page 514); Section 18-4, PDF page 558 (printed page 522).

## 6.7 Thermal equilibrium and calorimetry

### Learning goal
Apply energy conservation to objects reaching a shared final temperature.

### Understand the model
Objects in thermal contact exchange energy until they reach thermal equilibrium, with a common temperature and no net heat transfer between them. For an insulated mixing system with no work or phase change, the signed heat transfers sum to zero. A warmer object has negative Q and a cooler object positive Q.

Include a calorimeter, thermometer, or other component when its heat capacity is significant. Heat leaking to the room violates the assumption that the selected system is isolated, not energy conservation itself. Conduction transfers energy through matter without bulk flow, convection involves bulk fluid motion, and radiation can transfer energy across a vacuum. Insulation changes the rate of transfer rather than creating energy.

### Equations and units
```text
ΣQ = 0  (insulated, no work or phase change)
m₁c₁(T_f - T₁) + m₂c₂(T_f - T₂) = 0
T_f = (m₁c₁T₁ + m₂c₂T₂)/(m₁c₁ + m₂c₂)
```

### Worked example
Mix 0.200 kg of water at 80.0 °C with 0.300 kg at 20.0 °C in an ideal insulated container. Find equilibrium temperature.

1. Both portions have the same c, so it cancels from the conservation equation.
2. 0.200(T_f - 80.0) + 0.300(T_f - 20.0) = 0 gives 0.500T_f = 22.0.
3. T_f = 44.0 °C. Hot-water transfer is -30 096 J and cool-water transfer is +30 096 J using c = 4180, so the energy balance checks.

### Common mistakes
Do not simply average temperatures unless the two heat capacities mc are equal. Use signed changes for every object; do not give both heat transfers positive signs.

### Your turn
1. Equal masses of the same material at 10 °C and 50 °C mix ideally. Find T_f.
2. If a cold metal is put in warm water, must they have equal internal energies at equilibrium?

### Solutions and reasoning
**1.** Their heat capacities are equal, so T_f = 30 °C.

**2.** No. They have a common temperature, but internal energies depend on mass, material, and state.

### Textbook reading
Section 18-1, PDF page 550 (printed page 514); Section 18-4, PDF page 558 (printed page 522); Section 18-6, PDF page 570 (printed page 534).

## 6.8 Investigate and reflect

### Inquiry task
Design an insulated warm-water/cool-water mixing investigation. Measure masses and initial temperatures, predict equilibrium temperature, then measure it. Account for the cup and thermometer if their heat capacities matter. Compare the prediction and data, identify heat leakage and timing limitations, and propose improvements. Use warm rather than boiling water. Relate insulation choices to an energy-efficient structure using a properly attributed, publicly shared community source.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

