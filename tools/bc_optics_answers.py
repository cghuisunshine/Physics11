"""Worked answers for Chapter 7, grouped by the source inventory."""
from math import radians, sin
from bc_kinematics_answers import graph, paragraphs as p, parts, table
from bc_optics_diagrams import apparent_depth, diagram, label, path, periscope, pinhole, ray_diagram


def converging_cases(device, *cases):
    """Image-case table and the requested ray constructions."""
    mirror = device == 'mirror'
    real = 'in front of the mirror' if mirror else 'on the opposite side of the lens'
    virtual = 'behind the mirror' if mirror else 'on the object side of the lens'
    rows = [
        ('dₒ > 2f', f'Real, inverted, reduced. Between f and 2f {real}.', 2.6),
        ('dₒ = 2f', f'Real, inverted, same size. At 2f {real}.', 2),
        ('f < dₒ < 2f', f'Real, inverted, enlarged. Beyond 2f {real}.', 1.5),
        ('dₒ = f', 'Outgoing rays from each object point are parallel. No finite image.', 1),
        ('0 < dₒ < f', f'Virtual, upright, enlarged. {virtual.capitalize()}.', .65),
    ]
    return table(('Object position', 'Image'), [(rows[i][0], rows[i][1]) for i in cases]) + ''.join(
        ray_diagram(device, rows[i][2], caption=f'{rows[i][0]}. {rows[i][1]}') for i in cases
    )


convex_mirror = ray_diagram(
    'mirror', 2.2, diverging=True,
    caption='Convex mirror. Backward extensions meet behind the mirror between the vertex and F.',
)
diverging_lens = ray_diagram(
    'lens', 10 / 6, diverging=True,
    caption='Diverging lens. Backward extensions meet between the lens and the near focus.',
)

plane_mirror_height = diagram(
    'Rays from the head and feet meet the mirror halfway between those heights and eye level.',
    path([(70, 25), (317, 37), (70, 49)], '#096a70')
    + path([(70, 148), (317, 98.5), (70, 49)], '#4863a1')
    + path([(317, 36), (317, 100)], '#203440')
    + path([(70, 25), (70, 148)], '#a8b5bb')
    + label(17, 28, 'Head') + label(23, 54, 'Eye') + label(20, 151, 'Feet')
    + label(320, 73, 'Mirror'),
)

mirage = diagram(
    'Two facing concave mirrors return light through the opening and bring the rays together at a real image.',
    '<path d="M67 75.7Q130 35.8 193 32.3M217 32.3Q280 35.8 343 75.7M67 97.3Q205 184.7 343 97.3" '
    'fill="none" stroke="#203440" stroke-width="2"/>'
    + path([(205, 141), (112, 51.8), (112, 121.2), (205, 32)], '#096a70')
    + path([(205, 141), (298, 51.8), (298, 121.2), (205, 32)], '#4863a1')
    + label(220, 23, 'Image') + label(218, 157, 'Object'),
)

optical_pipe = diagram(
    'The solid ray follows the guide around a bend. Both incidence angles exceed the critical angle.',
    '<path d="M20 120H160A50 50 0 0 0 210 70V22H270V70A110 110 0 0 1 160 180H20Z" '
    'fill="#e8f4f6" stroke="#203440" stroke-width="2"/>'
    + path([(20, 146), (105, 180), (258.7, 118.5), (231.3, 22)], '#096a70'),
    '0 0 290 194',
)

answer_groups = [
    # 7.1 · Reflection
    [p('The screen shows a <strong>real, inverted image</strong> of the bulb. Rays travel in straight lines through the small hole. Rays from the top reach the lower screen and rays from the bottom reach the upper screen. Its size relative to the bulb depends on the two distances.') + pinhole()],
    [
        p('The minimum mirror height is <strong>1.0 m</strong>, half of 2 m. The extreme reflection points are halfway in height between the eye and the top of the head, and between the eye and the feet. The mirror must be mounted at the correct height.'),
        p('The glass reflects some indoor light all day. At night the view through the window is dark, so the reflection stands out. Daytime light transmitted from outdoors can swamp the faint indoor reflection.'),
        parts('Extend reflected rays backward to locate a virtual image.', 'It is <strong>behind the mirror</strong> as far as you are in front.', 'The image moves closer to the mirror by the same distance. Your separation from the image decreases twice as fast.'),
    ],
    # 7-1A · Location, reflected rays, and challenge
    [
        p('The unlit candle lines up with a <strong>virtual image behind the sheet</strong>. The image is as far behind the reflecting surface as the lit candle is in front. Check alignment from more than one viewing position to reduce parallax.'),
        p('Reflection occurs at the <strong>air–plastic interfaces</strong>. The front surface usually gives the brighter reflection. Light transmitted into the sheet can reflect at the back surface and emerge to give a faint offset image.'),
    ],
    [
        p('Measure perpendicular to the reflecting surface. The ideal result is <strong>equal distance magnitudes</strong>. Finite beam width, an inaccurate mirror line, and measurement errors can shift the measured intersection.'),
        p('Reflected rays diverge in front of the mirror. Extending them backward makes them appear to meet behind it. The light actually originates at the <strong>bulb filament in front</strong>.'),
        p('Each incident angle equals its reflected angle, measured from the normal. This is the same law used for wavefronts reflecting from a plane barrier. Report your observed differences and angle uncertainty.'),
    ],
    [p('Set the focus to about <strong>4 m</strong> if the camera is also 2 m from the mirror and next to your face. The virtual image is 2 m behind the mirror. In general add the appropriate object and camera distances for a head-on setup.')],
    # 7-1B · Multiple images and challenges
    [
        p('For the usual symmetric setup and when 360°/θ is an integer, the textbook model gives <strong>N = 360°/θ − 1</strong>. At 90° this gives 3 images. Finite mirrors can hide some images. For an odd integer ratio, moving the object off the bisector can change the count. Parallel facing mirrors can give a long chain of reflections.'),
        p('Four copies include the object, so 360°/θ = 4. The angle is <strong>90°</strong>.'),
    ],
    [
        p('With the object centred, opposing mirror walls reflect each other repeatedly. Each successive image is normally dimmer. The floor mirror also gives images below the apparent floor.'),
        p('Put two plane mirrors at 45° to the tube, with their reflective faces parallel and oriented to send the light down the tube and then toward the eye. Two reflections preserve the scene’s orientation.') + periscope(),
    ],
    # 7.1 Review
    [
        p('For electromagnetic radiation in vacuum, <strong>c = fλ</strong>. All bands have the same c, so higher frequency corresponds to shorter wavelength.'),
        p('The visible spectrum is the range detectable by the human eye, about <strong>380–760 nm</strong> using the textbook’s limits. Violet is at the short-wavelength end and red at the long-wavelength end.'),
        p('<strong>Infrared</strong> lies beyond red and is emitted by warm objects. <strong>Radio waves</strong> have longer wavelengths still and are used in broadcasting. Microwaves are another example.'),
        p('<strong>Infrared, microwaves, and radio waves</strong> all have lower frequencies than visible light.'),
        p('The incident and reflected angles are <strong>equal</strong> when measured from the normal at the point of reflection. The rays and normal lie in the same plane. A bathroom mirror is a familiar example.'),
        p('Place a mirror near the corner so the <strong>incident ray</strong> from the hidden object reflects toward your eye. Draw the normal perpendicular to the mirror where the ray hits. Rotate the mirror until the reflected and incident rays make equal angles with that normal.'),
        p('Object distance is measured from the object to the mirror. Image distance is measured from the mirror to the image. Their magnitudes match for a plane mirror. The image distance is negative in the signed convention because that image is virtual.'),
        p('No light converges at the apparent image behind the plane mirror. The rays reaching your eye only <em>appear</em> to originate there. You cannot catch the virtual image on a screen behind the mirror.'),
        parts('<strong>5</strong> at 60°.', '<strong>7</strong> at 45°.', '<strong>23</strong> at 15°.', '<strong>35</strong> at 10°.', '<strong>359</strong> at 1° in the ideal model.') +
        p('Use 360°/θ − 1 for these symmetric arrangements. Physical size and the field of view limit what you can actually see.'),
        p('The shortest mirror is <strong>90 cm</strong> high. The two points of reflection lie halfway in height between the eye and the head and between the eye and the feet. Their vertical separation is half the person’s height regardless of distance from the mirror.') + plane_mirror_height,
        p('Mirrored lettering on the ambulance reads normally in the driver’s rear-view mirror. To mirror your name, reverse the letter order and flip each letter across a vertical line. Draw the upright stroke of a b to the left of its loop, then place the stroke at the same distance on the right of the loop in the reflected view to obtain d.'),
        p('A ray from the top passes through the hole and reaches the lower screen. The image is <strong>real and inverted</strong>. Its size ratio is screen distance from the hole divided by object distance from the hole.') + pinhole(),
        p('Use two right-angle prisms whose hypotenuse faces are parallel. Light enters the first prism perpendicular to a leg, reflects internally at 45°, and exits down the tube. The second prism turns it toward the eye.') + periscope(),
    ],
    # 7.2 · Warm-up, ray diagrams, sample, and practice
    [p('The concave bowl can give an <strong>inverted</strong> image from farther away and an <strong>upright, enlarged</strong> one when your face is inside its focal length. The convex back gives an upright, reduced virtual image. A spoon’s non-spherical shape can distort the image.')],
    [p('In order, the drawings place the object beyond C, at C, and between C and F. From the arrow tip, draw a ray parallel to the axis and reflect it through F. A second ray through the vertex reflects at equal angles to the axis. Their intersections give the image tips.') +
     converging_cases('mirror', 0, 1, 2)],
    [p('Convert 1.00 m to 100 cm. 1/dᵢ = 1/20.0 − 1/100 = 0.0400 cm⁻¹, so <strong>dᵢ = +25.0 cm</strong>. The image is real and forms in front of the mirror.')],
    [
        p('Real image gives dᵢ = +25.0 cm. 1/dₒ = 1/20.0 − 1/25.0 = 0.0100 cm⁻¹. The object is <strong>100 cm in front</strong>.'),
        p('With dᵢ = dₒ, 2/dₒ = 1/f. Thus <strong>dₒ = dᵢ = 2f</strong>. The object is at C for a spherical concave mirror in the paraxial model.'),
        p('1/f = 1/20.0 + 1/40.0 = 0.0750 cm⁻¹. The focal length is <strong>13.3 cm</strong>.'),
        p('1/dᵢ = 1/15.0 − 1/10.0 = −1/30.0 cm⁻¹. <strong>dᵢ = −30.0 cm</strong> indicates an upright virtual image 30.0 cm behind the mirror.'),
    ],
    # 7-2A · Convex, concave, and focal-length measurements
    [
        p('Parallel incoming rays <strong>spread apart after reflection</strong>. Their backward extensions meet near a virtual focus behind the convex mirror.'),
        p('The curved surface presents different local normals across its width. It can direct rays from a wider range of directions to the eye, at the cost of reduced image size.'),
        p('For a real object, a convex mirror gives a <strong>virtual, upright, reduced</strong> image behind the mirror, between the vertex and F.'),
        p('A vertical cylindrical mirror curves across its width and is straight vertically. With a convex side facing you, your image looks <strong>narrower</strong> while the vertical scale is much less changed. A concave side close enough can stretch the width instead.'),
    ],
    [
        p('Rays parallel to the principal axis <strong>converge after reflecting</strong>. In the paraxial approximation the crossing is at the principal focus.'),
        p('A concave primary mirror collects light from a distant object and forms a real image near the focus. A larger mirror intercepts more light. An eyepiece or sensor views that image.'),
        p('A cylindrical mirror curves in only one direction, so it can focus a parallel sheet of rays to a <strong>line</strong>. The ray-box view shows a cross-section. Rays far from the axis can also show aberration.'),
    ],
    [
        p('If 1.5 m exceeds f, the rays still converge to a real image. Use 1/dᵢ = 1/f − 1/(1.5 m), so <strong>dᵢ > f</strong> for a finite distance. If dₒ = f they leave parallel, and if dₒ < f the image is virtual.'),
        p('A distant source supplies nearly parallel rays. With 1/dₒ ≈ 0, the mirror equation reduces to dᵢ ≈ f. Locate the sharpest image on a screen and measure from the mirror vertex.'),
    ],
    # 7-2B
    [
        p('The first three placements yield real images. At f the reflected rays from an object point are parallel, so there is no real image at a finite distance.') +
        converging_cases('mirror', 0, 1, 2, 3),
        p('A distant star gives nearly parallel incident rays. Its real image forms near the <strong>focal plane</strong>, about f in front of the mirror.'),
        p('Put the filament at the <strong>principal focus</strong> to obtain a nearly parallel outgoing beam. A source of finite size gives some beam spread.'),
        p('At dₒ = f, 1/dᵢ = 0. Rays from each object point leave parallel, so there is no finite screen position that gives a sharp image.'),
        p('A real object must be <strong>farther than the focus</strong>, so dₒ > f. The reflected rays then cross in front of the mirror.'),
        p('For <strong>0 < dₒ < f</strong> the reflected rays diverge. They appear to originate from an upright virtual image behind the mirror.'),
    ],
    # 7.2 Review and Mirage challenge
    [
        p('A simple convex lens is thicker at the centre than at its edges. A simple concave lens is thinner at the centre. In air with ordinary glass, the first converges parallel rays and the second diverges them.'),
        p('A converging lens brings an axial parallel bundle to a real focus. A diverging lens makes it spread as if from a virtual focus on the incoming side.'),
        p('A <strong>convex mirror</strong> always reduces a real object. A concave mirror can also reduce an object placed beyond C, giving a real inverted image in that case.'),
        parts('<strong>Concave</strong>, with your face inside f for a magnified upright image.',
              '<strong>Convex</strong> for a wide field of view.',
              '<strong>Plane</strong> for an upright, undistorted, same-size view.'),
        p('In order, <strong>E, A, F, B, D, C</strong>. The vertex is where the principal axis meets the surface. For a spherical mirror in the small-angle approximation, |f| = R/2.'),
        table(('Object position', 'Image'), [
            ('Far away', 'Near F, real, inverted, strongly reduced'),
            ('Beyond C', 'Between F and C, real, inverted, reduced'),
            ('At C', 'At C, real, inverted, same size'),
            ('Between F and C', 'Beyond C, real, inverted, enlarged'),
            ('At F', 'No finite image'),
            ('Between F and vertex', 'Behind mirror, virtual, upright, enlarged'),
        ]),
        converging_cases('mirror', 0, 2, 3, 4),
        parts('Make it <strong>concave across the width</strong> and stand inside f to appear wider.',
              'Make it <strong>convex across the width</strong> to appear narrower.',
              'Make it <strong>convex in the vertical cross-section</strong> to compress height.',
              'Make it <strong>concave in the vertical cross-section</strong> and stand inside f to stretch height.'),
        p('Draw one incoming ray parallel to the axis. Reflect it so its backward extension passes through F. A second ray striking the vertex reflects at the same angle to the axis. Extend the reflected rays behind the mirror. They meet at a reduced, upright image between F and the vertex.') + convex_mirror,
        parts('For the real object shown in the usual classroom setup, <strong>no</strong>. Reflected rays diverge and only their extensions meet.',
              '<strong>No</strong> for a real object. With f < 0 and dₒ > 0, |dᵢ| = |f|dₒ/(|f| + dₒ) < dₒ, so |m| < 1.') + convex_mirror,
    ],
    [p('The image is <strong>real</strong>. Light from the object at the bottom reflects from the upper concave surface and then from the lower one. The rays really meet near the opening. The mirrors are positioned so the first reflection supplies a bundle the second can focus there.') + mirage],
    # 7.3 · Refraction and critical angles
    [p('The part under water appears displaced, so the pencil seems bent at the surface. Rays from the submerged part speed up and bend away from the normal as they enter air. Your eye traces them back along straight lines to a shallower virtual position.') + apparent_depth()],
    [
        p('Use n₁ sin θ₁ = n₂ sin θ₂ with n(air) ≈ 1.00. n(glass) = sin 18.5°/sin 12.0° ≈ <strong>1.53</strong>.'),
        p('With n(diamond) = 2.42, θ₂ = sin⁻¹(sin 10.0°/2.42) ≈ <strong>4.11°</strong> from the normal.'),
        parts('It slows and bends toward the normal. θ(glass) = sin⁻¹(sin 30°/1.500) ≈ <strong>19.5°</strong>.',
              'It speeds up and bends away from the normal. Snell’s law gives an exit angle of <strong>30°</strong>. For parallel faces and air on both sides, the exiting ray is parallel to the incoming ray and shifted sideways.'),
        p('A <strong>prism</strong> disperses white light because the refractive index depends on wavelength. In ordinary glass, violet is refracted more than red.'),
    ],
    [
        p('Assume a diamond–air interface. sin θc = 1.00/2.42, so <strong>θc = 24.4°</strong>.'),
        p('For glass to air, θc = sin⁻¹(1.000/1.500) = <strong>41.8°</strong>.'),
        p('For the material to air, n = 1.00/sin 52.0° = <strong>1.27</strong>. The index depends on the surrounding medium if it is other than air.'),
    ],
    # 7-3A · Refraction
    [
        p('Light slows down in water or Plexiglas. At oblique incidence it bends toward the normal and its wavelength decreases. Its frequency remains fixed. At normal incidence it continues straight.'),
        p('With θᵢ vertical and θᵣ horizontal as instructed, the small-angle slope Δθᵢ/Δθᵣ is dimensionless and approximately n(material)/n(air). Use measured points near the origin. Plexiglas usually gives a larger slope and a greater bend than water. Plot sin θᵢ vertically against sin θᵣ horizontally for a straight-line fit over all angles. Its slope is n(material)/n(air).'),
        p('Yes. Both light and water waves can change speed at a boundary while their frequency stays fixed. Both bend toward the normal when going into a slower region at oblique incidence.'),
    ],
    # 7-3B · Internal reflection
    [
        p('Compare your observed last grazing refracted ray with θc = sin⁻¹[n(air)/n(material)]. Typical predictions are <strong>48.8° for water</strong> (n ≈ 1.33) and <strong>42.2° for acrylic</strong> (n ≈ 1.49). If the sample is glass, use its measured index. For n = 1.50, θc = 41.8°.'),
        p('Draw successive reflections at the inside wall of the pipe. At each wall, construct the local normal and use equal incident and reflected angles. Total internal reflection continues wherever the incidence angle exceeds the plastic–air critical angle. A very sharp bend can let light escape.') + optical_pipe,
    ],
    # 7-3C · Polarization
    [
        p('A polarizer selects a transverse electric-field direction, and a second crossed polarizer can block that component. This directional behaviour is evidence of the transverse wave nature of light. Photons also carry polarization in the quantum description.'),
        p('Light reflected from a horizontal road or water surface is often strongly <strong>horizontally polarized</strong>. A vertical transmission axis suppresses much of that glare.'),
        p('Rotate the filter to reduce the reflected glare. This can increase contrast and make detail below the surface easier to see. The effect depends on viewing angle.'),
        p('Calcite separates an incident beam into two rays with different polarizations by <strong>birefringence</strong>. An ordinary calcite crystal can transmit both, so the crystal alone differs from a filter that absorbs one component. A device can isolate one of the two rays.'),
    ],
    # 7.3 Review
    [
        p('The shown ray is 20° to the water surface, hence <strong>70° to the normal</strong>. This exceeds the water–air critical angle of about 49°, so the ray is totally internally reflected. Other rays from the fish can leave the water at smaller incidence angles and reach the fisher.'),
        parts('<strong>Choice iii.</strong> Aim below the apparent position, toward the real fish. Rays from the fish bend away from the normal as they leave water, making it appear shallower.',
              'Aim the laser along the line of sight toward the <strong>apparent position</strong>. Refraction is reversible, so the beam will bend toward the normal on entering water and follow the sight ray back to the real fish.') + apparent_depth(),
        p('Some rays reflect directly at the front air–glass surface. Others enter the glass, reflect off the rear coating, and refract out. For a thick sheet and an oblique view, the two reflected bundles are offset. Further internal bounces can give still fainter images.') +
        diagram('Front-surface reflection and reflection from the back coating reach the viewer at offset positions.',
                '<rect x="70" y="65" width="280" height="48" fill="#e8f4f6" stroke="#526b75"/>'
                + path([(100, 20), (154, 65), (208, 20)], '#096a70')
                + path([(100, 20), (154, 65), (186, 113), (218, 65), (272, 20)], '#4863a1')
                + label(74, 135, 'Rear coating') + label(272, 61, 'Front surface')),
        p('For glass to air, θc = sin⁻¹(1/1.58) ≈ <strong>39.3°</strong>.'),
        p('λ = c/f = (3.00 × 10⁸)/(5.00 × 10¹⁴) = 6.00 × 10⁻⁷ m = <strong>600 nm</strong>.'),
        p('v = c/n = (3.00 × 10⁸)/2.42 = <strong>1.24 × 10⁸ m/s</strong>.'),
        p('Matching phase along the boundary gives sin θ₁/λ₁ = sin θ₂/λ₂. Since λ = v/f, f is unchanged, and v = c/n, this becomes <strong>n₁ sin θ₁ = n₂ sin θ₂</strong>. The angles are measured from the normal.'),
        p('1.33 is an approximate value for visible light in ordinary water. Index depends on wavelength and on water conditions such as temperature and composition. It is defined relative to the vacuum speed c.'),
        parts('The three processes are <strong>refraction, dispersion, and internal reflection</strong>.',
              'Look toward rain or spray with the Sun behind you. A primary rainbow is centred on the direction opposite the Sun.',
              'From the outside or top to the inside of a primary bow: <strong>red, orange, yellow, green, blue, indigo, violet</strong>. The colours form a continuum.'),
        p('In a vacuum, red, green, and blue all travel at <strong>c</strong>. In ordinary glass with normal dispersion, red has the lowest index of the three and travels fastest.'),
        p('v = c/n ≈ (3.0 × 10⁸)/1.50 = <strong>2.0 × 10⁸ m/s</strong>.'),
        p('n = c/v = (3.00 × 10⁸)/(1.95 × 10⁸) ≈ <strong>1.54</strong> for the given quartz ray.'),
        parts('The frequency stays fixed, so λ(water) = λ(air)/n ≈ 650/1.33 = <strong>489 nm</strong>.',
              'Light with 489 nm wavelength in air would appear <strong>blue-green</strong>.',
              'The transmitted light has the same frequency as the 650 nm red light in air. Colour perception follows that frequency, so it still looks red.'),
    ],
    # Refraction Brain Stretch
    [
        p('Diamond’s high refractive index gives a small critical angle. Properly cut facets send light through repeated internal reflections and back toward the viewer. Dispersion separates wavelengths into coloured flashes.'),
        p('The signal is encoded as light pulses. The higher-index core guides light within the lower-index cladding. A detector converts the pulses back into an electrical signal.'),
        p('Near the horizon, light bends through layers of changing air density. The Sun appears higher than its geometric position, so it is visible a little before geometric sunrise and a little after geometric sunset.'),
        p('A strong temperature gradient changes the refractive index with height and curves light rays. Above hot pavement, rays from the sky can bend upward toward the eye and appear to come from the ground, making a water-like image.'),
        p('Rays from the bottom bend away from the normal as they leave water. Their straight backward extensions meet at a shallower apparent depth. Viewed close to straight down, apparent depth ≈ actual depth/n(water).'),
        p('A gem tester can compare thermal conductivity, which is much higher for diamond than for ordinary glass. A specialist can corroborate with optical tests or microscopy. Sparkle by itself is an unreliable identifier.'),
        p('One optical effect is that curved, thick glass walls can change the apparent shape or width of the liquid column. Measure the actual volume to test whether apparent size matches capacity. The glass design can also reflect strength or insulation considerations.'),
    ],
    # 7.4 · Lenses warm-up and quick checks
    [p('A converging lens close to the text can give an <strong>upright, enlarged virtual image</strong> when the text is inside f. A diverging lens gives an upright, reduced virtual image. A converging lens held farther away can instead form a real, inverted image. Describe the lens and distance you actually used.')],
    [
        p('A ray parallel to the axis leaves through F₂. A ray through F₁ leaves parallel, and a ray through the centre continues straight. The object position determines the image. For example, if dₒ > 2f, the rays cross on the far side between f and 2f, giving a real, inverted, reduced image. The three ray rules alone do not specify a unique object distance.') + converging_cases('lens', 0),
        p('For a real object, rays leaving a diverging lens spread. Backward extensions meet on the object side, between the lens and near focus. The image is <strong>virtual, upright, and reduced</strong>.') + diverging_lens,
    ],
    [
        p('5.00 m = 5000 mm. 1/dᵢ = 1/50.0 − 1/5000 mm⁻¹, so <strong>dᵢ = +50.5 mm</strong> on the far side.'),
        p('1/dᵢ = 1/50.0 − 1/100.0 mm⁻¹. <strong>dᵢ = +100.0 mm</strong>, a real image on the far side.'),
        p('1/f = 1/30 + 1/60 mm⁻¹ = 1/20 mm⁻¹. The positive focal length is <strong>20 mm</strong>.'),
    ],
    # 7-4A · Four procedure observations
    [
        p('Start with the unaided view in the empty tube. With a nearly flat water surface, the coin appears closer and subtends a larger angle from the same eye position. A convex water surface adds converging power and can magnify the coin when it is inside the effective focus. Compare your circles with the same eye position.'),
        p('A concave cylindrical lens makes the ray sheet spread. A convex one brings it together in the cross-section. In contact, their powers add, so similar opposite powers nearly cancel. Separating the lenses changes how wide and how convergent the bundle is at the second lens.'),
        parts('Hold the text closer than the water-filled flask’s focal length. It acts like a converging lens and gives a magnified upright virtual image.',
              'Place the flame farther away than f. Move the flask or screen until the real, inverted image is sharp on the wall.'),
        p('In the surrounding water, the air-filled round flask tends to act as a <strong>diverging</strong> element because its inside has lower index. It can give a reduced upright view. Filling it with water greatly reduces the index contrast, so there is much less lens effect. Some distortion can remain from the glass wall.'),
    ],
    # 7-4B · Prediction and optical bench
    [
        parts('<strong>a</strong> for a distant landscape, with the object beyond 2f and a small image near F₂.',
              '<strong>c</strong> for an enlarger, with the negative between f and 2f.',
              '<strong>c</strong> for a slide or movie projector.',
              '<strong>c</strong> for an overhead projector’s magnifying stage.',
              '<strong>b</strong> for life size, with object and sensor at 2f.') + converging_cases('lens', 0, 1, 2),
        parts('At F there is no finite real image.', 'Rays from an axial point source at F leave as a nearly parallel bundle.') + converging_cases('lens', 3),
        parts('Inside F the image is upright, enlarged, and virtual, so a screen will not catch it.', 'A magnifying glass uses this arrangement.') + converging_cases('lens', 4),
    ],
    [
        p('Choose <strong>(b) d</strong>. The projected image is rotated 180° relative to the slide as seen from behind the projector. Rotating d by 180° gives p.'),
        p('An overhead projector sends light upward through the transparency and lens. The projection head’s angled mirror turns the beam toward the screen and changes its orientation. With the transparency in the normal writing position, the viewer sees an upright image.'),
        p('Place the target near the <strong>principal focus</strong> on the far side. Sunlight arrives nearly parallel, so it concentrates around the focal plane.'),
        parts('Put the spider <strong>2f from the lens</strong>.', 'Put the film or sensor <strong>2f on the other side</strong>. Then |m| = dᵢ/dₒ = 1 and the image is real and inverted.'),
    ],
    # 7.4 Review
    [
        p('Eyeglasses can use <strong>converging</strong> lenses for farsightedness or <strong>diverging</strong> lenses for nearsightedness. A cylindrical component can correct astigmatism.'),
        parts('For f = +50 cm, 1/dᵢ = 1/50 − 1/25 = −1/50 cm⁻¹. <strong>dᵢ = −50 cm</strong>, on the object side.',
              'It is <strong>virtual</strong>, upright, and twice as tall as the object.'),
        p('At infinity the film is 50 mm from the lens, so f = 50 mm. With dₒ = 3000 mm, dᵢ = 1/(1/50 − 1/3000) ≈ 50.85 mm. Move the lens about <strong>0.85 mm farther from the film</strong>.'),
        p('Use dₒ = 400 mm and dᵢ = 20.0 mm. f = 1/(1/400 + 1/20.0) ≈ <strong>19.0 mm</strong>.'),
        p('dᵢ = 1/(1/20.0 − 1/80.0) = 26.67 cm. m = −26.67/80.0 = −⅓. The projected image is <strong>1.7 cm tall and inverted</strong>.'),
        p('dᵢ = 1/(1/20.0 − 1/30.0) = +60.0 cm. Signed m = −60.0/30.0 = <strong>−2.00</strong>. The image is real, inverted, and twice the object height.'),
        p('Draw the straight ray from the object tip through the optical centre to the image tip. The two triangles with the principal axis are similar, so <strong>|hᵢ|/hₒ = |dᵢ|/dₒ</strong>. For an inverted real image, signed m = −dᵢ/dₒ.'),
        parts('1/dᵢ = 1/(−6.0) − 1/10.0 = −1/3.75 cm⁻¹, giving dᵢ = −3.75 cm, about <strong>3.8 cm</strong> from the lens.',
              'Virtual.', 'Reduced.', 'Upright.',
              'm = −(−3.75)/10.0 = 0.375. The image height is about <strong>1.9 cm</strong>.',
              'On the same side as the object.') + diverging_lens,
        p('Flash light enters a dilated pupil, reflects from the back of the eye, and returns toward a camera close to the flash axis. Move the flash off axis, use more room light, or use a preflash to constrict the pupil.'),
        p('<strong>Hypermetropia</strong> is farsightedness. With insufficient focusing power or an eye that is too short, rays from a nearby object would meet behind the retina. A converging corrective lens increases the incoming convergence.'),
        p('<strong>Myopia</strong> is nearsightedness. With too much focusing power or a long eyeball, rays from a distant object meet in front of the retina. A diverging corrective lens moves the focus back onto the retina.'),
        p('A conventional compound microscope rotates the view by 180°. The bug appears to move from the <strong>upper right to the lower left</strong>. The objective forms the inverted intermediate image, and the eyepiece magnifies it.'),
        p('A <strong>Fresnel lens</strong> uses concentric stepped zones to reproduce the bending action of a much thicker curved lens. The reduced thickness and mass are useful for large apertures such as projector condensers.'),
    ],
    # Chapter review
    [
        p('A pinhole camera needs no lens or focus adjustment. A small hole can give a large depth of field. The trade-off is a dimmer image and possible blur from diffraction if the hole is too small.'),
        p('William Herschel dispersed sunlight with a prism and compared thermometer readings across the spectrum. The thermometer just beyond the visible red end warmed, revealing radiation outside the visible range.'),
        p('A streetlight viewed through fine mesh can show a starburst. The mesh openings and threads diffract the light into different directions.'),
        p('The minimum height is 1.6 m/2 = <strong>0.80 m</strong>, with the mirror mounted to intercept the rays from the head and feet.'),
        p('For 45°, the symmetric ideal count is 360°/45° − 1 = <strong>7 images</strong>.'),
        p('Convex mirrors give a <strong>wide field of view</strong>. Their reduced virtual images let staff see a larger area from one position.'),
        p('Place the filament <strong>between f and 2f</strong> from the vertex. Its image forms beyond 2f and is real, inverted, and enlarged.'),
        p('Place your face <strong>inside the focal length</strong>. The image is then upright, enlarged, and virtual behind the mirror.'),
        p('1/dᵢ = 1/1.0 − 1/2.5 = 0.60 m⁻¹. <strong>dᵢ ≈ +1.7 m</strong>, in front of the mirror. It is real.'),
        p('1/f = 1/6.0 + 1/3.0 = 0.50 m⁻¹, so <strong>f = 2.0 m</strong>.'),
        p('At entry, θ(glass) = sin⁻¹(sin 35°/1.60) ≈ <strong>21.0°</strong>. Parallel faces give that same internal incidence angle at the exit. In air the ray leaves at <strong>35°</strong> to the exit normal.'),
        p('For glass to air, θc = sin⁻¹(1/1.52) ≈ <strong>41.1°</strong>.'),
        p('The rays from the coin bend away from the normal at the water surface. The backward extensions meet above the coin. From the same viewing position, the shallower apparent coin can subtend a larger angle. A flat interface near normal incidence mainly changes apparent depth.') + apparent_depth(),
        p('For the liquid to air, sin 45° = 1/n. Thus <strong>n = √2 ≈ 1.41</strong>.'),
        p('For ordinary glass with normal dispersion, red light has a lower refractive index than violet. At the same oblique incidence from air, red bends less toward the normal.'),
        p('v = c/n = (3.0 × 10⁸)/2.0 = <strong>1.5 × 10⁸ m/s</strong>.'),
        parts('Plot y = sin θᵢ and x = sin θᵣ. By Snell’s law with air as the incident medium, y = n(glass)x.',
              'A fit through the origin gives slope ≈ <strong>1.498</strong>, so n ≈ <strong>1.50</strong>.',
              'For glass to air, θc = sin⁻¹(1/1.498) ≈ <strong>41.9°</strong>.') +
        graph('Snell’s law fit to the textbook measurements',
              [('Measured points and near-linear trend',
                [(sin(radians(r)), sin(radians(i))) for i, r in
                 zip((0, 5, 10, 15, 20, 25), (0, 3.33, 6.65, 9.94, 13.20, 16.40), strict=True)],
                '#096a70')],
              xmax=.30, ymin=0, ymax=.45, xlabel='sin θᵣ', ylabel='sin θᵢ',
              xticks=[0, .1, .2, .3], yticks=[0, .15, .3, .45], dots=True),
        p('Typical glasses for nearsightedness use <strong>diverging lenses</strong>. Parallel sunlight spreads after passing through one, so it cannot produce the focused spot depicted.'),
        parts('Place the object beyond 2f.', 'Place it between f and 2f.', 'Place it at 2f.',
              'Place it between the lens and the near focus.') + converging_cases('lens', 0, 2, 1, 4),
        p('The candle is beyond C. A parallel incident ray reflects through F, and a second ray through the vertex reflects symmetrically. Their intersection is between C and F in front of the mirror. The image is <strong>real, inverted, and smaller</strong>.') +
        ray_diagram('mirror', 4.2, caption='Concave mirror with the candle beyond C.'),
        p('<strong>Position 5</strong> lies between the mirror and F. It gives an upright, magnified virtual image. At F the rays from each point leave parallel. Farther out than F gives an inverted real image.') +
        ray_diagram('mirror', .55, caption='A face inside f gives an upright, magnified virtual image.'),
        p('1/dᵢ = 1/15.0 − 1/45.0 = 1/22.5 cm⁻¹, so the real image is <strong>22.5 cm in front of the mirror</strong>.'),
        p('The candle is between 2f and f. Draw one ray through the lens centre and a second ray parallel to the axis that bends through the far focus. They meet beyond 2f on the far side. The image is <strong>real, inverted, and larger</strong>.') +
        ray_diagram('lens', 1.5, caption='Converging lens with the candle between f and 2f.'),
        p('The real image is on the opposite side, so dᵢ = +20 mm. f = 1/(1/30 + 1/20) = <strong>12 mm</strong>.'),
        p('Use dₒ = 0.8 m = 800 mm. dᵢ = 1/(1/60.0 − 1/800) ≈ <strong>64.9 mm</strong> on the far side. The object height is unnecessary for image position.'),
        p('1/dᵢ = 1/20.5 − 1/15.0 ≈ −0.01789 cm⁻¹. <strong>dᵢ = −55.9 cm</strong>. The virtual image forms on the object side.'),
    ],
    # Extra practice
    [
        p('Light <strong>refracts and disperses</strong> on entering a raindrop, reflects internally, and refracts and disperses again on exit.'),
        p('<strong>Rayleigh scattering</strong> by air molecules preferentially redirects shorter visible wavelengths. Blue light scattered toward your eyes contributes strongly to the daytime sky colour.'),
        p('At sunset, sunlight follows a long path through the atmosphere. Much of the blue light scatters out of the direct beam, leaving a greater proportion of red and orange light.'),
        p('<strong>Refraction</strong> at the curved surfaces changes the direction of the rays and can bring them together or spread them apart.'),
        p('<strong>Violet</strong> bends most in ordinary glass with normal dispersion. Red bends least.'),
        p('<strong>Ultraviolet radiation</strong> causes tanning and sunburn.'),
        p('Every colour travels at the same vacuum speed <strong>c</strong>.'),
        p('<strong>Diffraction</strong> at the closely spaced grooves spreads light into a starburst pattern. Interference controls the bright directions.'),
        p('For 36°, the textbook mirror model gives 360°/36° − 1 = <strong>9 images</strong>.'),
        p('If the camera is beside you, focus at about <strong>4.0 m</strong>. The camera is 2.0 m in front of the mirror and the virtual image lies 2.0 m behind it.'),
        p('Relative to the mirror your image moves toward it at 5.0 m/s while you also move toward it at 5.0 m/s. The closing speed is <strong>10 m/s</strong>.'),
        p('Minimum height = 2.2 m/2 = <strong>1.1 m</strong>, positioned to intercept the head and foot rays.'),
        p('<strong>Frequency</strong> stays the same at the stationary boundary. Speed and wavelength may change.'),
        p('A high index gives a small critical angle. A suitable cut uses <strong>total internal reflection</strong> to return light to the viewer. <strong>Dispersion</strong> separates colours.'),
        p('The expected result is <strong>white</strong> for balanced additive mixing. A yellow beam supplies red and green components and the blue beam supplies blue. Unequal intensities can tint the patch.'),
        p('Aim <strong>below the apparent position C</strong>, along the direct path to the actual fish. The spear does not follow the refracted sight ray through B. Use the fish itself as the target in the sketch because the letters do not mark its exact position.'),
        p('<strong>D.</strong> Both hypotenuse faces are parallel. The top prism admits the horizontal ray through its vertical leg and turns it down. The lower prism admits it through its horizontal leg and turns it left.') + periscope(),
        p('Assuming incidence from air, n = sin 35°/sin 25° ≈ <strong>1.36</strong>. Both angles are from the normal.'),
        p('θ₂ = sin⁻¹(sin 63.0°/2.42) ≈ <strong>21.6°</strong> from the normal.'),
        p('v = c/n = (3.00 × 10⁸)/1.453 ≈ <strong>2.06 × 10⁸ m/s</strong>.'),
    ],
]
