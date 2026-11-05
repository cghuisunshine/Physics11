@chapter: Physics 11 · Unit 1
@title: Unit 1: Math Tools & Measurement
@subtitle: Build the measurement, algebra, graphing, and trigonometry habits that every later unit uses.

## 1.1 SI units and dimensional reasoning

### Learning goal
Convert a measurement to SI units and check whether an equation has consistent dimensions.

### Understand the model
A physical quantity combines a numerical value with a unit. A length of 2.0 m and a time of 2.0 s have different meanings even though the numbers match. In this course the main base units are metre (m), kilogram (kg), second (s), ampere (A), and kelvin (K). Derived units combine them: velocity uses m/s, acceleration uses m/s², and force uses N = kg·m/s².

A conversion factor is a ratio of equal physical amounts, so it equals one. Put the unit you want to cancel on the opposite side of the fraction. For an area or volume, raise the entire length conversion to the appropriate power. Dimensional checks can reject an equation with incompatible units, but cannot determine a missing numerical factor or prove that the physics is correct.

### Equations and units
```text
v = Δx/Δt  [m/s]
a = Δv/Δt  [m/s²]
1 N = 1 kg·m/s²
1 J = 1 N·m
1 W = 1 J/s
```

### Worked example
Convert 72.0 km/h to m/s and 250 cm² to m².

1. Write 72.0 km/h × (1000 m/1 km) × (1 h/3600 s). Both unwanted units cancel.
2. The speed is 20.0 m/s. A speed equation that adds metres to seconds would fail a dimensional check.
3. For area, 250 cm² × (1 m/100 cm)² = 0.0250 m² if 250 has three significant figures. The squared factor is 1/10 000, not 1/100.

### Common mistakes
Use kilograms rather than grams in mechanical equations. Keep prefixes case-sensitive: m means milli while M means mega. Never convert a squared unit using only a first-power length factor.

### Your turn
1. Convert 3.50 ms to seconds.
2. Does Δx = v₀t + at have consistent units?

### Solutions and reasoning
**1.** Milli means 10⁻³. The time is 3.50 × 10⁻³ s.

**2.** No. v₀t has units m, while at has units m/s. The constant-acceleration displacement term is ½at², with units m.

### Textbook reading
Section 1-1, PDF page 37 (printed page 1); Section 1-2, PDF page 41 (printed page 5); Section 1-3, PDF page 42 (printed page 6).

## 1.2 Scientific notation and significant figures

### Learning goal
Report a calculation to a precision justified by its measurements.

### Understand the model
Scientific notation writes a number as a × 10ⁿ, with 1 ≤ |a| < 10. It makes very large and very small quantities manageable and makes the stated precision visible. Leading zeros locate the decimal point; they are not significant. Zeros between nonzero digits are significant. Trailing zeros after a decimal point are significant. A value written simply as 1200 has ambiguous precision; 1.20 × 10³ is unambiguous.

For multiplication and division, round the final result to the fewest significant figures among the measured inputs. For addition and subtraction, round to the least precise decimal place. Exact counts and defined conversion factors do not limit precision. Keep extra digits through intermediate steps, then round once at the end. These rules are a reporting convention, not a substitute for a full uncertainty analysis.

### Equations and units
```text
(a × 10ᵐ)(b × 10ⁿ) = ab × 10ᵐ⁺ⁿ
(a × 10ᵐ)/(b × 10ⁿ) = (a/b) × 10ᵐ⁻ⁿ
```

### Worked example
A runner travels 12.40 m in 3.2 s. Report the average speed. Then add 12.40 m and 0.6 m.

1. The calculator gives 12.40/3.2 = 3.875 m/s.
2. The time has two significant figures, so report the speed as 3.9 m/s.
3. The sum is 13.00 m before rounding. The 0.6 m measurement is precise only to tenths, so the reported sum is 13.0 m.

### Common mistakes
Do not round every intermediate line. Do not report a long calculator display as though the experiment measured all those digits. Written zeros matter: 3.0 has two significant figures.

### Your turn
1. How many significant figures are in 0.004050?
2. Calculate (2.50 × 10³)(4.0 × 10⁻²).

### Solutions and reasoning
**1.** Four: 4, the internal 0, 5, and the final decimal 0.

**2.** The unrounded product is 100. The reported result is 1.0 × 10², with two significant figures.

### Textbook reading
Section 1-1, PDF page 37 (printed page 1).

## 1.3 Accuracy, precision, and uncertainty

### Learning goal
Describe the quality of data and judge whether an experimental result agrees with a model.

### Understand the model
Accuracy concerns closeness to a suitable reference value. Precision concerns the spread of repeated measurements. Repeated readings can cluster tightly while all being shifted by a calibration error. Random effects vary between trials; systematic effects shift results in a consistent way. Repeating measurements can reduce the uncertainty in an average caused by random variation, but cannot by itself remove a systematic bias.

State an uncertainty with its method. For an analogue ruler, half the smallest division is a common reading estimate, but alignment and edge placement can contribute more. A digital last-digit resolution is only one part of the total uncertainty. Report a value and uncertainty at matching decimal places. When comparing with a reference, percent error describes relative disagreement; it does not identify its cause.

### Equations and units
```text
relative uncertainty = absolute uncertainty / |measured value|
percent uncertainty = relative uncertainty × 100%
percent error = |experimental - reference| / |reference| × 100%
```

### Worked example
A length is (25.0 ± 0.2) cm. A gravity experiment gives 9.60 m/s²; compare it with the assigned reference 9.81 m/s².

1. The length percent uncertainty is (0.2/25.0) × 100% = 0.8%.
2. The gravity percent error is |9.60 - 9.81|/9.81 × 100% ≈ 2.1%.
3. Agreement cannot be judged fully from percent error alone. Compare the discrepancy with the experiment’s uncertainty and discuss timing, height measurement, and model assumptions.

### Common mistakes
Avoid writing “human error” without identifying a mechanism. Reaction-time variation, parallax, and a ruler zero offset are specific sources that suggest specific improvements.

### Your turn
1. Readings are 10.1, 10.1, and 10.2 cm, but the reference is 11.0 cm. Describe the data.
2. What is the percent uncertainty of (4.0 ± 0.1) s?

### Solutions and reasoning
**1.** They are relatively precise but inaccurate against that reference. Investigate calibration or a consistent method error.

**2.** 0.1/4.0 × 100% = 2.5%.

### Textbook reading
Section 1-1, PDF page 37 (printed page 1); Section 1-2, PDF page 41 (printed page 5).

## 1.4 Algebra and a repeatable problem-solving method

### Learning goal
Rearrange a physical equation before substituting values and evaluate the result.

### Understand the model
A successful solution starts with a model: identify the object or system, choose axes, list the given quantities with units, and name the unknown. Sketch the situation before choosing an equation. Rearranging symbolically helps expose which quantities matter and catches errors that numerical substitution can hide. Every operation must affect both sides of the equation.

After substituting SI values, carry units through the arithmetic. End with a signed answer or a magnitude and direction, as appropriate. Check whether the answer is physically plausible: a stopping time should be positive, a passive efficiency should not exceed 100%, and a component cannot have a magnitude larger than its vector. A quadratic equation may have two mathematical roots; decide which roots belong to the time interval and situation being studied.

### Equations and units
```text
v = v₀ + at  →  t = (v - v₀)/a
v² = v₀² + 2aΔx  →  Δx = (v² - v₀²)/(2a)
```

### Worked example
A cart moves at +12.0 m/s and brakes at -3.00 m/s². Find the time and displacement until it first stops.

1. Choose the initial motion as positive. The stopping velocity is 0, and the stated acceleration is constant.
2. t = (0 - 12.0)/(-3.00) = 4.00 s.
3. Δx = (0² - 12.0²)/(2 × -3.00) = +24.0 m. The cart keeps moving forward while slowing; it does not have negative displacement.

### Common mistakes
A negative acceleration does not always mean slowing down. It means the acceleration points along the negative axis. Do not take the square root of a velocity-squared result without considering direction.

### Your turn
1. Rearrange P = E/t for E.
2. A cart starts at -6.0 m/s with acceleration +2.0 m/s². When does it stop?

### Solutions and reasoning
**1.** Multiply both sides by t: E = Pt.

**2.** t = [0 - (-6.0)]/2.0 = 3.0 s. Velocity and acceleration are opposite, so it slows.

### Textbook reading
Section 2-4, PDF page 59 (printed page 23).

## 1.5 Graphing, slope, and area

### Learning goal
Extract physical meaning and correct units from the slope or area of a graph.

### Understand the model
Label each axis with the quantity and unit, choose a scale that uses the available space, and plot measurements clearly. A best-fit line follows the trend of noisy data; it need not pass through every point. Use well-separated points on that line to calculate its slope. The slope unit is the vertical-axis unit divided by the horizontal-axis unit. A nonzero intercept can describe a real starting value or a systematic offset.

On a position-time graph, slope gives velocity. On a velocity-time graph, slope gives acceleration and signed area gives displacement. On an acceleration-time graph, signed area gives change in velocity. Area below the time axis is negative. Interpolation estimates within the measured range; extrapolation extends beyond it and relies more strongly on the model remaining valid.

### Equations and units
```text
slope = rise/run = Δ(vertical quantity)/Δ(horizontal quantity)
rectangle area = base × height
triangle area = ½ × base × height
```

### Worked example
A velocity-time line rises from 2.0 m/s at 0 s to 8.0 m/s at 3.0 s. Find acceleration and displacement.

1. Slope: a = (8.0 - 2.0)/(3.0 - 0) = 2.0 m/s².
2. Area: a 3.0 s × 2.0 m/s rectangle gives 6.0 m, and a ½ × 3.0 s × 6.0 m/s triangle gives 9.0 m.
3. Total displacement is 15 m. The trapezoid method gives the same result: ½(2.0 + 8.0)(3.0) = 15 m.

### Common mistakes
The slope of a velocity-time graph is acceleration, not velocity. The height of a position-time graph is position, not speed. Do not automatically connect noisy experimental points with a zigzag line.

### Your turn
1. A position-time line falls 6.0 m over 2.0 s. What is its velocity?
2. A constant acceleration of -2.0 m/s² lasts 3.0 s. What does the graph area represent?

### Solutions and reasoning
**1.** v = -6.0/2.0 = -3.0 m/s.

**2.** Δv = (-2.0)(3.0) = -6.0 m/s, a change in velocity rather than a displacement.

### Textbook reading
Section 2-1, PDF page 49 (printed page 13); Section 2-2, PDF page 54 (printed page 18); Section 2-3, PDF page 56 (printed page 20); Section 2-6, PDF page 65 (printed page 29).

## 1.6 Trigonometry and vector components

### Learning goal
Resolve a vector into signed perpendicular components and reconstruct its magnitude and direction.

### Understand the model
A scalar has magnitude; a vector has magnitude and direction. Speed, mass, time, and energy are scalars. Displacement, velocity, acceleration, and force are vectors. A component is the signed projection of a vector along an axis. When the angle is measured counterclockwise from the positive x-axis, the x-component uses cosine and the y-component uses sine. If the angle is measured from another axis, identify adjacent and opposite sides again.

Add vectors by adding x-components separately from y-components. Subtraction means adding the reversed vector. Use the Pythagorean theorem to reconstruct the magnitude. The inverse tangent gives a reference angle; the component signs determine the quadrant. In this course set the calculator to degrees for stated degree angles.

### Equations and units
```text
Aₓ = A cos θ; Aᵧ = A sin θ
Rₓ = Aₓ + Bₓ; Rᵧ = Aᵧ + Bᵧ
R = √(Rₓ² + Rᵧ²)
tan θ = Rᵧ/Rₓ  (check quadrant)
```

### Worked example
A 20.0 N force acts 30.0° above the horizontal. Resolve it. Then find the resultant of 3.0 m east and 4.0 m north.

1. Fₓ = 20.0 cos 30.0° = 17.3 N; Fᵧ = 20.0 sin 30.0° = 10.0 N. Both components are positive.
2. The displacement components are Rₓ = 3.0 m and Rᵧ = 4.0 m, so R = √(3.0² + 4.0²) = 5.0 m.
3. θ = tan⁻¹(4.0/3.0) ≈ 53° north of east. The walked distance is 7.0 m, which differs from the displacement magnitude.

### Common mistakes
Do not add vector magnitudes unless the vectors are collinear in the same direction. Always state the axis from which an angle is measured.

### Your turn
1. Find the components of 10.0 m at 150° from +x.
2. What is the resultant of 8 N east and 3 N west?

### Solutions and reasoning
**1.** Aₓ = -8.66 m and Aᵧ = +5.00 m; the vector lies in quadrant II.

**2.** Take east as positive: 8 + (-3) = 5 N east.

### Textbook reading
Section 3-1, PDF page 76 (printed page 40); Section 3-2, PDF page 82 (printed page 46).

## 1.7 Investigate and reflect

### Inquiry task
Measure a small object five times with a ruler. State the ruler resolution, calculate the mean and spread, and distinguish repeated-reading variation from a possible zero error. Then time several walks over the same marked distance. Plot position against time, draw a best-fit line, and explain the slope with units. Change one method to reduce uncertainty and compare the evidence.

### Evidence checklist
- State the question and a testable prediction.
- Identify independent, dependent, and controlled variables.
- Record units, resolution, repeated trials, and a justified uncertainty estimate.
- Use a labelled graph or table and explain slope or area when relevant.
- Compare the result with the model and identify specific limitations.
- Explain an improvement and connect the result to a practical application.

