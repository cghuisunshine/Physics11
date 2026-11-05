@chapter: Physics 11
@title: Vectors
@subtitle: Scalars, components, vector operations, and relative velocity.

# Vectors

## 1 Scalars and vectors
### Scalars
Measurable quantities are either scalars or vectors. **Scalars have only magnitude (size).**
- Height = 170 cm
- Mass = 60 kg
- Age = 17 years

### Vectors
**Vectors have both magnitude and direction.**
- Velocity = 5 m/s east
- Acceleration = 9.8 m/s² down

### Representing vectors
A vector can be represented by an arrow. The magnitude of the vector is represented by the length of the arrow. The direction of the vector is represented by the direction of the arrow.

## 2 Directions and components
### Example: locations relative to Vancouver
- Whistler: 120 km north
- Seattle: 200 km south
- Kamloops: 350 km, 30° north of east

60° east of north is also correct for Kamloops, but the convention in these notes is to use the smaller angle.

### Splitting a vector into components
A vector at an angle can be split into horizontal and vertical components.

### Worked example: Vancouver to Kamloops
The displacement is **d = 350 km at 30° north of east**.
```
cos 30° = dₓ / d
dₓ = d cos 30°
   = 350 cos 30°
   ≈ 303 km east

sin 30° = dᵧ / d
dᵧ = d sin 30°
   = 350 sin 30°
   = 175 km north
```
Kamloops is **303 km east and 175 km north of Vancouver**.

### Practice example
Determine the horizontal and vertical components of the following vector: **56 m/s, 25° west of south**.

**Worked answer**

Choose east and north as positive. The angle is measured from south, so the horizontal component uses sine and the vertical component uses cosine.
```
vₓ = −56 sin 25° = −23.7 m/s
vᵧ = −56 cos 25° = −50.8 m/s
```
The components are **24 m/s west and 51 m/s south**, to two significant figures.

## 3 Vector addition: head-to-tail method
### Method
Vectors can be added using the **head-to-tail method**.
1. Draw the first vector.
2. Draw the second vector with its tail at the head of the first vector.
3. Draw the **resultant vector** from the tail of the first vector to the head of the second vector.

```
a⃗ + b⃗ = c⃗
```

### Practice example: Aaron's walk
Aaron walks **2.5 km east**, then **3.0 km, 35° north of east**. What is his total displacement?

**Worked answer**

Draw the second arrow from the head of the first. The resultant joins the starting point to the final point. Calculate its size and direction using the right triangle formed by its components:
```
dₓ = 2.5 + 3.0 cos 35° = 4.957 km east
dᵧ = 3.0 sin 35° = 1.721 km north
d = √(4.957² + 1.721²) = 5.248 km
θ = tan⁻¹(1.721 / 4.957) = 19.14°
```
Total displacement: **5.2 km, 19° north of east**. A scale drawing should give approximately the same result.

## 4 Vector addition: component method
### Method
Vectors can also be added using the **component method**.
1. Split vectors into horizontal and vertical components.
2. Add horizontal and vertical components separately to determine the components of the resultant vector.
3. Use the Pythagorean theorem and tangent to determine the magnitude and direction of the resultant vector.

When adding three or more vectors, the component method is more efficient.

### Practice example: Aaron's walk
Aaron walks **2.5 km east**, then **3.0 km, 35° north of east**. What is his total displacement?

**Worked answer**

Choose east as positive x and north as positive y. Add the corresponding components of the two displacements:
```
d₁ₓ = 2.5 km; d₁ᵧ = 0 km
d₂ₓ = 3.0 cos 35° = 2.457 km
d₂ᵧ = 3.0 sin 35° = 1.721 km

dₓ = 2.5 + 2.457 = 4.957 km
dᵧ = 0 + 1.721 = 1.721 km
d = √(dₓ² + dᵧ²) = 5.248 km
θ = tan⁻¹(dᵧ / dₓ) = 19.14°
```
Total displacement: **5.2 km, 19° north of east**. This is the same resultant found by the head-to-tail method.

## 5 Vector subtraction
### Adding the opposite
To subtract a vector, **add its opposite**.
```
a⃗ − b⃗ = c⃗
a⃗ + (−b⃗) = c⃗
```

Vector subtraction is most often used to determine the change in a vector quantity.
```
Δx⃗ = x⃗f − x⃗i    (displacement)
Δv⃗ = v⃗f − v⃗i    (change in velocity)
```

### Practice example: the dog's displacement
A stationary observer is monitoring the movement of a dog. Initially, the dog is seen **5.0 m east** of the observer. A few seconds later, the dog is **10.0 m, 45° north of east**. What is the displacement of the dog?

**Worked answer**

Choose east and north as positive. Subtract the initial position from the final position, component by component:
```
xᵢ = 5.0 m; yᵢ = 0 m
x_f = 10.0 cos 45° = 7.071 m
y_f = 10.0 sin 45° = 7.071 m

Δx = 7.071 − 5.0 = 2.071 m east
Δy = 7.071 − 0 = 7.071 m north
|Δr| = √(2.071² + 7.071²) = 7.368 m
θ = tan⁻¹(2.071 / 7.071) = 16.32°
```
Displacement: **7.4 m, 16° east of north** (equivalently 74° north of east).

## 6 Relative velocity: planes
### Frame of reference
The velocity of an object depends on the **frame of reference of the observer**.
```
v⃗PA + v⃗AG = v⃗PG
```

### Plane relative to air: v⃗PA
- Velocity of the plane relative to air
- Airspeed of the plane
- Velocity in still air
- Direction the plane is aimed

### Air relative to ground: v⃗AG
- Velocity of air relative to ground
- Wind velocity

### Plane relative to ground: v⃗PG
- Velocity of the plane relative to ground
- Ground speed of the plane
- Resultant velocity with wind redirection

## 7 Relative velocity: boats
### Boat, water, and shore
```
v⃗BW + v⃗WS = v⃗BS
```

### Boat relative to water: v⃗BW
- Velocity of the boat relative to water
- Rowing speed
- Velocity in still water
- Direction the boat is aimed

### Water relative to shore: v⃗WS
- Velocity of water relative to shore
- Current velocity

### Boat relative to shore: v⃗BS
- Velocity of the boat relative to shore
- Resultant velocity with current redirection

### Practice example: a river flowing west
A river flows **west at 4.0 km/h**. What would be the velocity of a boat relative to the shore if the boat aims:
1. West at 10.0 km/h?
2. East at 10.0 km/h?
3. South at 10.0 km/h?

**Worked answer**

Add the boat's velocity relative to water to the water's velocity relative to shore.
1. Aiming west: both velocities point west, so **14 km/h west**.
2. Aiming east: 10.0 east − 4.0 west gives **6.0 km/h east**.
3. Aiming south: the shore-frame components are **10.0 km/h south and 4.0 km/h west**.
```
v = √(10.0² + 4.0²) = 10.77 km/h
θ = tan⁻¹(4.0 / 10.0) = 21.80°
```
For the southward heading, the resultant is **10.8 km/h, 22° west of south**.
