@chapter: Physics 11 · Unit 7
@title: Unit 7: Electricity
@subtitle: Use charge and energy conservation to solve DC circuits, real batteries, and electrical power problems.

## 7.1 Charge, current, voltage, and resistance

### Learning goal
Explain each circuit quantity and connect its definition to its unit.

### Understand the model
Current is the rate at which charge passes a cross-section. Conventional current follows the direction a positive charge would move; conduction electrons in a metal drift in the opposite direction. Charge is not used up as it passes through a resistor. In a steady circuit the same current enters and leaves a single unbranched component.

Potential difference, or voltage, is energy change per unit charge between two points. A source transfers energy to charge carriers and components transfer energy to other forms. Resistance relates a component’s voltage to its current at the operating condition. It is measured in ohms. A closed path is needed for sustained current in the simple DC circuit model; an open switch breaks that path.

### Equations and units
```text
I = Δq/Δt  (steady current)
V = ΔE/q  (energy per charge)
R = V/I
1 A = 1 C/s; 1 V = 1 J/C; 1 Ω = 1 V/A
```

### Worked example
A steady current of 0.500 A flows for 12.0 s through a component with a 9.00 V drop. Find charge and transferred energy.

1. q = IΔt = (0.500)(12.0) = 6.00 C.
2. Energy transferred by those charges is E = qV = (6.00)(9.00) = 54.0 J.
3. The charges continue through the circuit. The component converts or transfers energy; it does not consume the charge.

### Common mistakes
Voltage is measured between two points, not “through” a component. Current flows through a component; voltage is across it. Do not confuse charge in coulombs with energy in joules.

### Your turn
1. A 2.0 A steady current flows for 5.0 s. How much charge passes?
2. A 12 V source supplies 36 J to charge. How much charge?

### Solutions and reasoning
**1.** q = It = 10 C.

**2.** q = E/V = 36/12 = 3 C.

### Textbook reading
Section 24-1, PDF page 721 (printed page 685); Section 26-1, PDF page 781 (printed page 745); Section 26-3, PDF page 788 (printed page 752).

## 7.2 Ohm’s law and electrical measurements

### Learning goal
Identify an ohmic component and infer resistance from a graph or circuit measurements.

### Understand the model
An ohmic component has approximately constant resistance over the operating range when physical conditions such as temperature stay fixed. Its V-I graph is a straight line through the origin, with slope R when voltage is vertical and current horizontal. Many devices, including filament lamps at changing temperature, are not ohmic over a broad range. The ratio V/I at one point does not prove constant resistance.

An ammeter measures current and connects in series. Its ideal resistance is zero so that it changes the current as little as possible. A voltmeter measures potential difference and connects in parallel across the component. Its ideal resistance is infinite, drawing no current. Real meters affect the circuit slightly; incorrect ammeter placement across a source can create a short circuit.

### Equations and units
```text
V = IR  (constant-R model)
R = slope of V-versus-I graph
I = slope of I-versus-V graph × V for a line through origin
slope of I-versus-V graph = 1/R
```

### Worked example
An ohmic resistor has measured points (0.100 A, 2.00 V) and (0.300 A, 6.00 V). Find R and current at 9.00 V.

1. R = ΔV/ΔI = (6.00 - 2.00)/(0.300 - 0.100) = 20.0 Ω.
2. Under the same conditions, I = 9.00/20.0 = 0.450 A.
3. A broad range of measured points would be needed to establish the linear model well. If temperature rises, resistance may change and the prediction may fail.

### Common mistakes
Check which quantity is on each graph axis. Do not place an ammeter directly across a battery. Resistance readings should be made on an unpowered, appropriately isolated component using the meter’s instructions.

### Your turn
1. A 6.0 V drop gives 0.20 A through an ohmic resistor. Find R.
2. Why might a lamp’s V-I curve bend?

### Solutions and reasoning
**1.** R = 6.0/0.20 = 30 Ω.

**2.** Its filament temperature changes with electrical heating, which changes resistance; the constant-R assumption fails.

### Textbook reading
Section 26-4, PDF page 792 (printed page 756); Section 27-3, PDF page 824 (printed page 788).

## 7.3 Series circuits

### Learning goal
Find equivalent resistance and distribute voltage along one unbranched current path.

### Understand the model
Components are in series when they lie on the same unbranched current path. Charge conservation gives the same current through every component. Energy conservation gives a source voltage equal to the sum of component voltage drops in an ideal resistive loop. Adding another series resistor increases total resistance and reduces current for a fixed ideal source.

Equivalent resistance replaces a combination while preserving the source’s voltage-current relationship. For series resistors, R_eq is their sum. First find total current from the source voltage and equivalent resistance, then calculate each drop using its resistance. A larger series resistance takes a larger share of the voltage. One open connection stops current through the entire series path.

### Equations and units
```text
R_eq = R₁ + R₂ + ...
I = V_source/R_eq
V_i = IR_i
V_source = V₁ + V₂ + ...
```

### Worked example
Connect 2.00 Ω and 4.00 Ω in series across an ideal 12.0 V source. Find current and both voltage drops.

1. R_eq = 2.00 + 4.00 = 6.00 Ω.
2. I = 12.0/6.00 = 2.00 A through both resistors.
3. Drops are (2.00)(2.00) = 4.00 V and (2.00)(4.00) = 8.00 V. Their sum is 12.0 V, satisfying the loop rule.

### Common mistakes
Series resistors share current, not necessarily voltage. Geometric placement in a drawing does not define series; trace the nodes and current path.

### Your turn
1. Three 10.0 Ω resistors are in series across 15.0 V. Find total current.
2. Two series resistors carry 0.40 A. What current enters the second resistor?

### Solutions and reasoning
**1.** R_eq = 30.0 Ω and I = 0.500 A.

**2.** 0.40 A; current is not consumed by the first resistor.

### Textbook reading
Section 27-1, PDF page 807 (printed page 771).

## 7.4 Parallel circuits and mixed networks

### Learning goal
Recognize common nodes, find branch currents, and simplify a mixed circuit in stages.

### Understand the model
Parallel components connect across the same two nodes, so they have the same potential difference. Current divides among branches and recombines at a junction. A lower-resistance branch carries more current for the same voltage. The equivalent resistance of positive parallel resistors is smaller than the smallest branch resistance.

For a mixed circuit, identify a true series or parallel group, replace it with its equivalent, and continue until the source current can be found. Then reverse the simplification: recover the voltage across each parallel group and currents through each branch. Components that happen to sit beside each other in a drawing are not necessarily parallel; both endpoint nodes must match.

### Equations and units
```text
1/R_eq = 1/R₁ + 1/R₂ + ...
for two branches: R_eq = R₁R₂/(R₁ + R₂)
I_total = I₁ + I₂ + ...
I_branch = V_branch/R_branch
```

### Worked example
A 4.00 Ω resistor is in series with a parallel group of 6.00 Ω and 3.00 Ω across an ideal 12.0 V source.

1. The parallel equivalent is (6.00 × 3.00)/(6.00 + 3.00) = 2.00 Ω. Total resistance is 4.00 + 2.00 = 6.00 Ω.
2. Source current is 2.00 A. The series resistor drops 8.00 V, leaving 4.00 V across the parallel group.
3. Branch currents are 4.00/6.00 = 0.667 A and 4.00/3.00 = 1.33 A. Their unrounded sum is 2.00 A.

### Common mistakes
Do not give a parallel sub-group the full source voltage if another series element takes a voltage drop. Parallel branches share voltage, not current.

### Your turn
1. Find the equivalent of two 8.0 Ω resistors in parallel.
2. A 6.0 Ω and a 12 Ω resistor are each across 12 V. Find branch and total currents.

### Solutions and reasoning
**1.** R_eq = 4.0 Ω.

**2.** Branch currents are 2.0 A and 1.0 A; total is 3.0 A. Equivalent resistance is 4.0 Ω.

### Textbook reading
Section 27-2, PDF page 817 (printed page 781).

## 7.5 Kirchhoff’s junction and loop rules

### Learning goal
Write current and voltage equations with a consistent sign convention.

### Understand the model
The junction rule expresses charge conservation in a steady circuit: total current entering a node equals total current leaving it. The loop rule expresses energy conservation per unit charge: the algebraic sum of voltage changes around a closed loop is zero. These rules extend beyond circuits that reduce neatly into series and parallel groups.

Choose branch-current arrows, label every component, and choose a direction for each loop traversal. Across a resistor in the assumed current direction, the voltage change is -IR; going against it gives +IR. Across an ideal source from negative to positive terminal, the change is +ε, and the reverse crossing gives -ε. A negative solved current means the real direction opposes the assumed arrow, not that the solution is invalid.

### Equations and units
```text
ΣI_in = ΣI_out
ΣΔV around a closed loop = 0
resistor along current: ΔV = -IR
source from - to +: ΔV = +ε
```

### Worked example
Two opposing ideal sources of 12.0 V and 4.00 V share a single loop with 2.00 Ω and 6.00 Ω resistors. Find current.

1. Assume current in the direction driven by the 12.0 V source.
2. Loop equation: +12.0 - 4.00 - I(2.00) - I(6.00) = 0.
3. I = 8.00/8.00 = 1.00 A in the assumed direction. The resistor drops total 8.00 V, balancing the net source rise.

### Common mistakes
Do not count every possible loop equation as independent. Use enough independent junction and loop equations for the unknown currents and verify the remaining rules afterward.

### Your turn
1. A junction receives 3.0 A and 2.0 A, with one outgoing branch of 1.5 A. Find the other outgoing current.
2. A solved branch current is -0.20 A. What does that mean?

### Solutions and reasoning
**1.** 3.0 + 2.0 = 1.5 + I gives I = 3.5 A.

**2.** The actual current is 0.20 A opposite the chosen arrow. The algebra has determined its direction.

### Textbook reading
Section 27-1, PDF page 807 (printed page 771); Section 27-2, PDF page 817 (printed page 781).

## 7.6 EMF, internal resistance, and terminal voltage

### Learning goal
Distinguish a battery’s energy-per-charge supply from the voltage delivered under load.

### Understand the model
Electromotive force ε is the energy supplied by a source per unit charge. Despite its name, EMF is measured in volts rather than newtons. An ideal battery has no internal resistance. A real battery is modeled as an ideal source in series with an internal resistance r.

While the battery discharges, some energy is transferred to thermal energy inside it, so the terminal voltage is ε - Ir. With no current, this model gives terminal voltage equal to EMF. A larger load current creates a larger internal drop. During charging, when current enters the positive terminal, the simple model requires an applied terminal voltage ε + Ir. The discharge expression must not be used with an unexamined current direction.

### Equations and units
```text
discharging: V_terminal = ε - Ir
I = ε/(R_load + r)
P_internal = I²r
P_source = εI; P_load = V_terminal I
```

### Worked example
A battery has ε = 12.0 V and r = 0.500 Ω. Connect a 5.50 Ω load. Find current, terminal voltage, and internal heating power.

1. Total resistance is 5.50 + 0.500 = 6.00 Ω, so I = 12.0/6.00 = 2.00 A.
2. V_terminal = 12.0 - (2.00)(0.500) = 11.0 V. Check: IR_load = (2.00)(5.50) = 11.0 V.
3. P_internal = (2.00)²(0.500) = 2.00 W. Source power is 24.0 W and load power 22.0 W, balancing the energy rate.

### Common mistakes
EMF is not a mechanical force. An unloaded voltage measurement and a loaded voltage measurement need not match. Never deliberately short a battery to test the model.

### Your turn
1. A 9.0 V battery with r = 1.0 Ω supplies 0.50 A while discharging. Find terminal voltage.
2. Why does terminal voltage drop with a larger discharge current?

### Solutions and reasoning
**1.** V_terminal = 9.0 - 0.50(1.0) = 8.5 V.

**2.** The internal resistive drop Ir increases; more energy per second is converted to thermal energy inside the source.

### Textbook reading
Section 27-1, PDF page 807 (printed page 771).

## 7.7 Electrical power, energy, and transmission

### Learning goal
Calculate electrical energy and explain why high-voltage transmission reduces resistive loss.

### Understand the model
Electrical power transferred to a component is P = VI. For a resistor obeying V = IR, substitution gives I²R or V²/R. A device using a constant power for time t transfers energy Pt. The kilowatt-hour is an energy unit: one kW operating for one hour transfers 3.6 × 10⁶ J. It is not a power unit.

A transmission line loses power as I²R_line. For a fixed delivered power, increasing transmission voltage allows lower current and therefore much smaller line loss. If voltage is increased by a factor of ten at the same transmitted power, current becomes one tenth and resistive loss becomes one hundredth. This energy argument applies to the resistive line model; actual grid equipment and voltage conversion require additional physics. Circuit breakers and fuses interrupt excessive current to limit overheating.

### Equations and units
```text
P = VI
for a resistor: P = I²R = V²/R
E = Pt
1 kWh = 3.6 × 10⁶ J
P_line loss = I²R_line
```

### Worked example
A 60.0 W device runs for 2.00 h. Find energy in kWh and joules. A line of total resistance 2.00 Ω carries 10.0 A; find its loss.

1. Device energy is (0.0600 kW)(2.00 h) = 0.120 kWh.
2. In joules, E = (60.0 J/s)(7200 s) = 432 000 J = 432 kJ.
3. Line loss is (10.0)²(2.00) = 200 W. The total line resistance should include the return path if the circuit has one.

### Common mistakes
Use hours with kW for kWh, and seconds with W for joules. Higher voltage does not directly reduce I²R loss unless current is correspondingly reduced for the same power transfer.

### Your turn
1. A 12.0 V resistor draws 2.00 A. Find power and energy in 30.0 s.
2. At fixed transmitted power, voltage doubles. What happens to resistive line loss?

### Solutions and reasoning
**1.** P = 24.0 W; E = 720 J.

**2.** Current halves, so I²R loss becomes one quarter if the line resistance is unchanged.

### Textbook reading
Section 26-5, PDF page 796 (printed page 760); Section 27-1, PDF page 807 (printed page 771).

## 7.8 Investigate and reflect

### Inquiry task
With a teacher-approved low-voltage battery circuit, measure current through and voltage across a resistor at several settings. Plot V versus I and compare the slope with resistance. Repeat with series and parallel combinations and test junction and loop rules within uncertainty. Use only low-voltage classroom equipment; never investigate a wall outlet. Connect an ammeter in series and a voltmeter across the component.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

