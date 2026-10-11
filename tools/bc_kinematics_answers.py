"""Worked answers for the 101 extracted BC Science Chapter 2 entries.

These are independently calculated teaching answers, not a publisher answer key.
Question IDs follow content/bc-kinematics-questions.json.
"""
from html import escape


def paragraphs(*items):
    return ''.join(f'<p>{item}</p>' for item in items)


def parts(*items):
    return '<ol class="answer-parts" type="a">' + ''.join(f'<li>{item}</li>' for item in items) + '</ol>'


def table(headers, rows):
    return '<div class="answer-table"><table><thead><tr>' + ''.join(f'<th scope="col">{escape(str(v))}</th>' for v in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{escape(str(v))}</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def graph(title, series, xmax, ymin, ymax, xlabel='Time (s)', ylabel='Position (m)', xticks=None, yticks=None, dots=False):
    """Small inline teaching sketch; data and an accessible description are explicit."""
    xmap = lambda x: 62 + 340*x/xmax
    ymap = lambda y: 226 - 172*(y-ymin)/(ymax-ymin)
    xticks = xticks or [0, xmax/2, xmax]
    yticks = yticks or [ymin, (ymin+ymax)/2, ymax]
    chunks = [f'<figure class="answer-graph"><svg viewBox="0 0 450 285" role="img" aria-label="{escape(title,quote=True)}"><title>{escape(title)}</title>']
    for x in xticks:
        px=xmap(x); chunks.append(f'<path d="M{px:g} 54V226" stroke="#dce4e1"/><text x="{px:g}" y="246" text-anchor="middle">{x:g}</text>')
    for y in yticks:
        py=ymap(y); chunks.append(f'<path d="M62 {py:g}H402" stroke="#dce4e1"/><text x="53" y="{py+4:g}" text-anchor="end">{y:g}</text>')
    chunks.append('<path d="M62 54V226H402" fill="none" stroke="#506770" stroke-width="1.5"/>')
    if ymin<0<ymax: chunks.append(f'<path d="M62 {ymap(0):g}H402" stroke="#506770"/>')
    for label, points, color in series:
        coords=' '.join(f'{xmap(x):.2f},{ymap(y):.2f}' for x,y in points)
        chunks.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        if dots:
            chunks += [f'<circle cx="{xmap(x):g}" cy="{ymap(y):g}" r="3.5" fill="{color}"/>' for x,y in points]
    chunks.append(f'<text x="232" y="273" text-anchor="middle">{escape(xlabel)}</text><text transform="translate(17 140) rotate(-90)" text-anchor="middle">{escape(ylabel)}</text></svg>')
    chunks.append('<figcaption>'+escape(title)+'. '+ '; '.join(f'<span style="color:{c}">{escape(label)}</span>' for label,_,c in series)+'.</figcaption></figure>')
    return ''.join(chunks)


A = {}
def answer(n, body):
    assert f'q-{n}' not in A
    A[f'q-{n}'] = body


answer(1, paragraphs('A round trip to the waterfall and back has <strong>distance 4 km</strong> (2 km out + 2 km back), but <strong>displacement 0 km</strong>, because you finish at the parking lot where you started.'))
answer(2, paragraphs('Take right as positive: x<sub>i</sub> = −2.0 m and x<sub>f</sub> = +4.5 m.', '<strong>Δx = x<sub>f</sub> − x<sub>i</sub> = 4.5 − (−2.0) = 6.5 m right.</strong> The source sample’s printed 2.5 m result is a sign error.'))
answer(3, parts('<strong>1100 m</strong>: distance = 200 + 400 + 500.', 'Net components are 400 m west and 300 m south. Magnitude = √(400² + 300²) = <strong>500 m</strong>.'))
answer(4, parts('Distance = 100 + 100 + 75 + 125 + 75 + 28 = <strong>503 m</strong>.', 'Displacement is the direct arrow from the tee to the hole: <strong>290 m toward the hole</strong> (right in the diagram).'))
answer(5, paragraphs('Distance along the route = 6 + 4 + 8 + 8 + 4 + 8 = <strong>38 m</strong>.', 'The final point is 8 m right and 6 m up from the porch. Displacement magnitude = √(8² + 6²) = <strong>10 m, 53° right of upward</strong> (equivalently 37° above the horizontal).'))
answer(6, parts('Average speed is total distance ÷ total elapsed time. Instantaneous speed is the speed at one particular instant.', 'They are the same throughout the interval when the speed is constant. A particular instantaneous value can also happen to equal the average during a changing-speed trip.'))
answer(7, paragraphs('v̄ = d/t = 320/3.6 = 88.9 km/h ≈ <strong>89 km/h</strong>.'))
answer(8, paragraphs('t = d/v = 65/85 = 0.765 h = 45.9 min ≈ <strong>0.76 h, or 46 min</strong>.'))
answer(9, paragraphs('d = vt = (92)(5.0) = <strong>460 km</strong>.'))
answer(10, paragraphs('v = Δx/Δt = 0.5 m / 1 s = <strong>0.5 m/s right</strong>. Over 10 s the displacement is 5.0 m, which gives the same velocity.'))
answer(11, paragraphs('Plot position increasing from (0 s, 0 m) to (10 s, 5.0 m). Its slope is (5.0 − 0)/(10 − 0) = <strong>+0.5 m/s</strong>, so the velocity is <strong>0.5 m/s right</strong>.'))
answer(12, parts('A horizontal position-time line: <strong>at rest</strong>; position remains constant.', 'A straight line with positive slope: <strong>constant positive velocity</strong>.', 'A straight line with negative slope: <strong>constant negative velocity</strong>. The object moves toward smaller positions.'))
answer(13, parts('Choose east as positive and start at x = 0. A westward ball has <strong>x(t) = −1.5t m</strong>: a straight line with negative slope.', 'For the explicitly stated eastward observation, <strong>x(t) = +1.5t m</strong>: a straight line with positive slope.', 'Treat the cup as fixed to the ground. A person moving west at −1.5 m/s sees the cup move east relative to them: v<sub>cup/person</sub> = 0 − (−1.5) = <strong>+1.5 m/s</strong>. Its relative-position graph rises linearly.') + paragraphs('The wording of (b) and (c) is awkward: a stationary observer at the cup would not reverse the ball’s actual compass direction. The sketches below show the directions stated in (a) and (b), and the relative motion described in (c).') + graph('Position sketches with east positive', [('(a) ball west',[(0,0),(4,-6)],'#bc493e'),('(b) stated eastward motion; (c) apparent cup motion',[(0,0),(4,6)],'#096a70')],4,-6,6))
answer(14, parts('30 km/h = 30/3.6 = <strong>8.333… m/s</strong>. Assuming d = 0 at t = 0, use d = 8.333…t.', 'Plot the table points and join them with a straight line through the origin. Its slope is <strong>8.33 m/s</strong>.') + table(['Time (s)','Distance (m)'],[(t,f'{30/3.6*t:.2f}') for t in range(1,9)]) + graph('Distance-time graph at 30 km/h', [('d = (8.333… m/s)t',[(0,0),(8,200/3)],'#096a70')],8,0,80,yticks=[0,20,40,60,80],dots=True))
answer(15, paragraphs('For a cumulative distance-time graph, slope = Δdistance/Δtime, so it represents <strong>speed</strong>. A secant gives average speed; a tangent gives instantaneous speed.'))
answer(16, paragraphs('<strong>Your measured distances are needed.</strong> For each one-second interval, v̄<sub>k</sub> = [d(k s) − d((k−1) s)] / 1 s, for k = 1, 2, 3, 4, 5. If you measured distance in centimetres, report speed in cm/s.', 'The overall five-second average is [d(5 s) − d(0)]/5 s; it also equals the arithmetic mean of the five equal-duration interval speeds.'))
answer(17, paragraphs('Both calculations measure speed. For nearly uniform motion, the distance-time graph’s slope and the five interval averages should be approximately equal. For changing speed, each interval average can differ; compare a secant slope over the same interval. A best-fit slope across the whole trip may differ slightly because of measurement error.'))
answer(18, paragraphs('The car generally starts from rest and accelerates before reaching its steady running speed, so it covers less distance in the first one-second interval. Startup friction and slack in the tape can also affect the first measurement.'))
answer(19, paragraphs('<strong>Yes.</strong> Speed gives magnitude only; velocity also gives direction. Two cars travelling 50 km/h, one east and one west, have equal speeds but different velocities.'))
answer(20, paragraphs('Use <strong>compass directions</strong> (north, south, east, west) or a <strong>chosen sign convention</strong> (for example, right positive and left negative). State the convention before calculating.'))
answer(21, paragraphs('t = 3.2/60 h. Distance = (12.0)(3.2/60) = <strong>0.64 km = 640 m</strong>.'))
answer(22, paragraphs('t = d/v = (1.8 × 10³)/(8.0 × 10²) = 2.25 h ≈ <strong>2.3 h</strong> (two significant figures).'))
answer(23, parts('3.5 m = 350 cm. t = 350/2.6 = 134.6 s ≈ <strong>1.3 × 10² s</strong>.', 't = 134.6/60 = 2.244 min ≈ <strong>2.2 min</strong>.'))
answer(24, paragraphs('Total distance = 122(20/60) + 108(30/60) = 94.667 km. Total time = 50.0/60 h.', 'v̄ = 94.667/(50.0/60) = <strong>113.6 km/h ≈ 114 km/h</strong>. Weight speeds by time rather than taking their simple mean.'))
answer(25, parts('Distance = 84(45/60) + 96(20/60) = 63 + 32 = <strong>95 km</strong>.', 'Average speed = 95/(65/60) = 87.69 km/h ≈ <strong>88 km/h</strong>.'))
answer(26, parts('For uniform acceleration from rest, average speed during the first second is half the final speed. Thus v(1 s) = 28 m/s and a = 28 m/s². The speed 14 m/s occurs at <strong>t = 0.50 s</strong>.', 'At t = 1.0 s, the instantaneous speed is <strong>28 m/s</strong>.'))
answer(27, parts('Draw a <strong>horizontal line above zero</strong>: v = constant and a = 0.', 'Draw a <strong>straight rising line from the origin</strong>: v = at, with a positive constant slope.') + graph('Illustrative speed-time sketches', [('(a) constant speed',[(0,3),(4,3)],'#bc493e'),('(b) uniform acceleration from rest',[(0,0),(4,4)],'#096a70')],4,0,5,ylabel='Speed (arbitrary units)'))
answer(28, paragraphs('a = (v<sub>f</sub> − v<sub>i</sub>)/t = (9.0 − 0)/4.5 = <strong>2.0 m/s²</strong>.'))
answer(29, parts('60.0 km/h = 16.667 m/s. a = (16.667 − 0)/3.00 = <strong>5.56 m/s²</strong>.', 'a = (9.00 − 0)/3.00 = <strong>3.00 m/s²</strong>.'))
answer(30, paragraphs('Δv = (60.0 − 45.0)/3.6 = 4.1667 m/s. a = 4.1667/7.50 = <strong>0.556 m/s²</strong>.'))
answer(31, paragraphs('Take the initial direction of travel as positive. a = [(60 − 120)/3.6]/4.0 = −4.167 m/s² ≈ <strong>−4.2 m/s²</strong>. The acceleration is negative because velocity is decreasing in that positive direction.'))
answer(32, parts('Initial speed = 60/3.6 = <strong>16.7 m/s</strong>.', 'v<sub>f</sub> = 16.667 + (2.22)(4.00) = <strong>25.5 m/s = 92.0 km/h</strong>.', 'Police speed rises linearly from 16.7 m/s at t = 0 to 25.5 m/s at t = 4.00 s. The speeder’s speed is a horizontal line. Its numerical height is <strong>not determined</strong>, because the initial gap is not supplied.') + graph('Police and speeder speed-time sketch', [('Police: v = 16.667 + 2.22t',[(0,60/3.6),(4,60/3.6+2.22*4)],'#096a70'),('Speeder: illustrative constant speed only',[(0,18),(4,18)],'#bc493e')],4,0,30,ylabel='Speed (m/s)',yticks=[0,10,20,30]) + paragraphs('The speeder line at 18 m/s is an example, not a calculated answer. The police travel 84.43 m in four seconds; a catch-up condition would be initial gap = 84.43 − 4v<sub>s</sub>.'))
answer(33, paragraphs('a = 6.0/1.2 = 5.0 m/s². From rest, t = v/a = 15.0/5.0 = <strong>3.0 s</strong> total.'))
answer(34, parts('Line (a): <strong>v ≈ 20 m/s + (14 m/s²)t</strong>.', 'Line (b): <strong>v ≈ (14 m/s²)t</strong>.', 'The slope of line (a) is approximately <strong>14 m/s²</strong>.', 'The parallel line (b) has the same acceleration, approximately <strong>14 m/s²</strong>.', 'The observers start their clocks at different points in the aircraft’s motion. For (b), t = 0 is at rest; for (a), t = 0 is when the aircraft already has speed 20 m/s.') + paragraphs('Graph readings are approximate. On line (b), (0 s, 0 m/s) and (5 s, 70 m/s) give slope 70/5 = 14 m/s².'))
answer(35, paragraphs('v<sub>i</sub> = v<sub>f</sub> − at = 38 − (6.0)(5.5) = <strong>5.0 m/s</strong>.'))
answer(36, paragraphs('Downhill is positive, so v<sub>i</sub> = +2.0 m/s and v<sub>f</sub> = −5.5 m/s.', 'ā = [−5.5 − (+2.0)]/3.0 = <strong>−2.5 m/s²</strong>, directed uphill.'))
answer(37, parts('From (0 s, 0 m/s) to (3 s, 30 m/s): a = 30/3 = <strong>+10 m/s²</strong>.', 'From 3 s to 6 s, speed stays 30 m/s: <strong>a = 0 m/s²</strong>.', 'From (6 s, 30 m/s) to (10 s, 0 m/s): a = (0 − 30)/(10 − 6) = <strong>−7.5 m/s²</strong>.'))
answer(38, paragraphs('<strong>Initial velocity</strong> is velocity at the start of an interval. <strong>Final velocity</strong> is velocity at its end. <strong>Change in velocity</strong> is Δv = v<sub>f</sub> − v<sub>i</sub>. <strong>Average velocity</strong> is displacement divided by elapsed time; for constant acceleration it also equals (v<sub>i</sub> + v<sub>f</sub>)/2.'))
answer(39, parts('a = (10.0 − 2.0)/(0.80 − 0) = <strong>10 m/s² downward</strong>, taking down as positive.', 'The straight-line equation is <strong>v = 2.0 m/s + (10 m/s²)t</strong>.'))
answer(40, parts('The graph intersects the speed axis at approximately <strong>15 m/s</strong>.', 'Use approximately (0 s, 15 m/s) and (10 s, 55 m/s): slope = (55 − 15)/10 = <strong>4.0 m/s²</strong>.', 'The slope represents <strong>acceleration</strong> for the one-direction motion shown.', '<strong>v = 15 m/s + (4.0 m/s²)t</strong>.'))
answer(41, parts('The constant term gives the initial speed: <strong>5.0 m/s downward</strong>.', 'The coefficient of t is acceleration: <strong>9.8 m/s² downward</strong>.', 'v(1.2 s) = 5.0 + (9.8)(1.2) = 16.76 m/s ≈ <strong>17 m/s downward</strong>.'))
answer(42, paragraphs('Choose east positive. v<sub>i</sub> = v<sub>f</sub> − at = 25.0 − (3.0)(5.0) = <strong>10 m/s east</strong>.'))
answer(43, paragraphs('For uniform acceleration, average speed = (16.0 + 0)/2 = 8.0 m/s. Distance = (8.0)(8.0) = <strong>64 m</strong>; displacement is 64 m west.'))
answer(44, paragraphs('Convert v<sub>i</sub> = 100/3.6 = 27.778 m/s. From v<sub>f</sub>² = v<sub>i</sub>² + 2ad, with v<sub>f</sub> = 0:', 'd = −(27.778)²/[2(−9.29)] = <strong>41.5 m</strong> (about 42 m).'))
answer(45, parts('For your cart, v̄<sub>1</sub> = d<sub>1</sub>/0.10 s. With the <strong>sample</strong> distance 1.1 cm, this is <strong>11 cm/s</strong>.', 'v̄<sub>2</sub> = d<sub>2</sub>/0.10 s. With the <strong>sample</strong> distance 1.8 cm, this is <strong>18 cm/s</strong>.', 'Δv̄ = v̄<sub>2</sub> − v̄<sub>1</sub>; for the sample, <strong>7 cm/s</strong>.', 'a ≈ (v̄<sub>2</sub> − v̄<sub>1</sub>)/0.10 s. For the sample, <strong>70 cm/s² = 0.70 m/s²</strong>.') + paragraphs('Use your measured distances for your own result. The sample values illustrate the method; interval-average speeds correspond to interval midpoints for uniform acceleration.'))
answer(46, paragraphs('Calculate a<sub>23</sub> = (v̄<sub>3</sub> − v̄<sub>2</sub>)/0.10 s, then similarly a<sub>34</sub>, a<sub>45</sub>, and a<sub>56</sub>. <strong>Your measured speeds are needed for numerical answers.</strong>', 'For uniform acceleration these estimates should be approximately equal. Differences can arise from distance measurements, friction, timer variation, or nonuniform motion.'))
answer(47, paragraphs('<strong>Use your own best-fit graph.</strong> Acceleration is its slope: a = (v<sub>2</sub> − v<sub>1</sub>)/(t<sub>2</sub> − t<sub>1</sub>). Choose well-separated points on the best-fit line, not necessarily two raw measurements. Report cm/s² or m/s² consistently.'))
answer(48, paragraphs('Write the fitted speed-time line as <strong>v(t) = v<sub>0</sub> + at</strong>. Here v<sub>0</sub> is your line’s y-intercept and a is its slope. Include their numerical values and units from your experiment; they cannot be determined from the question alone.'))
answer(49, paragraphs('The methods should give similar accelerations within experimental uncertainty. A <strong>best-fit line using all the data</strong> usually averages random measurement errors better than one estimate formed by subtracting two adjacent speeds. Differencing nearby measurements can amplify error.'))
answer(50, parts('From the graph, initial speed is approximately <strong>5.5 m/s</strong>.', 'Using the stop near t = 0.70 s: a ≈ (0 − 5.5)/0.70 = <strong>−7.9 m/s²</strong>.', '<strong>v ≈ 5.5 m/s − (7.9 m/s²)t</strong>, valid until the object stops at about 0.70 s.') + paragraphs('These are approximate readings from the drawn graph, so small differences from graph interpolation are reasonable.'))
answer(51, parts('Initial speed is the constant term: <strong>6.6 m/s</strong>.', 'Acceleration is the coefficient of t: <strong>−2.2 m/s²</strong>.', 'Set v = 0: t = 6.6/2.2 = <strong>3.0 s</strong>.'))
answer(52, paragraphs('a = (8.0 − 12.0)/3.25 = −1.2308 m/s² ≈ <strong>−1.23 m/s²</strong>.'))
answer(53, parts('v = at = (0.80)(5.0) = <strong>4.0 m/s downhill</strong>.', 'd = ½at² = ½(0.80)(5.0)² = <strong>10 m downhill</strong>.'))
answer(54, parts('a = (36.0 − 0)/12.0 = <strong>3.00 m/s²</strong>.', 'v(15.0 s) = (3.00)(15.0) = <strong>45.0 m/s</strong>.', 'd = ½(3.00)(15.0)² = 337.5 m ≈ <strong>338 m</strong>.'))
answer(55, paragraphs('Time = (20.0 − 80.0)/(−5.0) = 12 s. Average speed = (80.0 + 20.0)/2 = 50.0 km/h = 13.889 m/s.', 'Distance = (13.889)(12) = 166.7 m ≈ <strong>1.7 × 10² m</strong>. The mixed unit km/h/s means the speed drops by 5.0 km/h each second.'))
answer(56, paragraphs('For a drop from rest, d = ½gt². t = √(2d/g) = √[2(530)/9.81] = 10.395 s ≈ <strong>10 s</strong> (two significant figures).'))
answer(57, paragraphs('Distance = 5.0 cm = 0.050 m. Final speed = 0.10c = 3.0 × 10⁷ m/s.', 'a = (v<sub>f</sub>² − 0)/(2d) = (3.0 × 10⁷)²/[2(0.050)] = <strong>9.0 × 10¹⁵ m/s²</strong>, under the uniform-acceleration model.'))
answer(58, paragraphs('The <strong>book usually lands first</strong> when the paper is flat. Air resistance is large compared with the paper’s weight, so it falls more slowly. Crumpling reduces its exposed area and drag, so the paper and book should land closer together. In a vacuum they would have the same gravitational acceleration. Record your actual observations rather than inventing experimental results.'))
answer(59, parts('The sample uses g = 9.8 m/s². From rest, v = gt = (9.8)(1.0) = <strong>9.8 m/s downward</strong>.', 'd = ½gt² = ½(9.8)(1.0)² = <strong>4.9 m downward</strong>.'))
answer(60, parts('Using the sample’s g = 9.8 m/s², v = √(2gd) = √[2(9.8)(530)] = 101.9 m/s ≈ <strong>102 m/s downward</strong>.', 'Air resistance acts upward and reduces the net downward acceleration as the speed grows. The ball may approach terminal speed, so the ideal free-fall speed is not reached.'))
answer(61, paragraphs('<strong>Assuming the initial 5.0 m/s is downward</strong>, take down positive: h = v<sub>i</sub>t + ½gt² = (5.0)(3.1) + ½(9.81)(3.1)² = 62.64 m ≈ <strong>63 m</strong>.', 'The prompt does not explicitly state the initial direction. If the rock is initially thrown <strong>upward</strong>, use v<sub>i</sub> = −5.0 m/s, giving h = −15.5 + 47.14 = <strong>31.64 m ≈ 32 m</strong>.'))
answer(62, parts('Assume the rider starts from rest. v = gt = (9.81)(1.9) = 18.64 m/s ≈ <strong>19 m/s downward</strong>.', 'h = ½gt² = ½(9.81)(1.9)² = 17.71 m ≈ <strong>18 m</strong>.'))
answer(63, paragraphs('a = 3g = 3(9.81) = 29.43 m/s². From rest, d = ½at² = ½(29.43)(4.0)² = 235.44 m ≈ <strong>2.4 × 10² m</strong>.'))
answer(64, parts('Thrown from (0 s, 0 m/s) to A(0.2 s, 9.8 m/s): a = 9.8/0.2 = <strong>+49 m/s²</strong>.', 'Free fall from A to C: a = (−9.8 − 9.8)/(2.2 − 0.2) = <strong>−9.8 m/s²</strong>.', 'Caught from C(2.2 s, −9.8 m/s) to E(2.4 s, 0 m/s): a = [0 − (−9.8)]/(2.4 − 2.2) = <strong>+49 m/s²</strong>.') + paragraphs('Positive means upward. The throwing and catching accelerations are net accelerations read from the graph.'))
answer(65, paragraphs('<strong>Point B, at t = 1.2 s.</strong> Here the vertical velocity changes from positive to negative through zero, so upward motion ends and downward motion begins. D and E also have zero velocity, but mark the start and end of handling, not the peak.'))
answer(66, paragraphs('Displacement is the <strong>signed area under the velocity-time graph</strong>. From release at A (0.2 s) to the peak at B (1.2 s), the triangular area is ½(1.0 s)(9.8 m/s) = <strong>4.9 m above the release position</strong>.', 'If altitude is measured from the ball’s position at t = 0, include the throwing segment: ½(0.2)(9.8) = 0.98 m. The total rise is <strong>5.88 m</strong>. The graph gives changes in height; absolute altitude needs a reference height.'))
answer(67, paragraphs('d = ½gt², so g = 2d/t² = 2(0.80)/(2.00)² = <strong>0.40 m/s² downward</strong>.'))
answer(68, parts('Throwing: a = (39.2 − 0)/(0.20 − 0) = <strong>+196 m/s²</strong>.', 'Free flight ABC: a = (0 − 39.2)/(4.20 − 0.20) = <strong>−9.8 m/s²</strong>.', 'Catching CD: a = [0 − (−39.2)]/(8.40 − 8.20) = <strong>+196 m/s²</strong>.', '<strong>B</strong> is the peak: vertical velocity is zero and changes from upward to downward.', 'Gravity acts downward throughout free flight, so the acceleration and graph slope are negative when up is positive.', 'Velocity carries a direction and can be negative. Speed is a magnitude and cannot be negative.', 'In free flight from A to B, rise = ½(4.00)(39.2) = <strong>78.4 m above release</strong>. Including the initial throwing segment, add ½(0.20)(39.2) = 3.92 m: total upward travel from t = 0 is <strong>82.32 m</strong>.', 'From B to C, free-fall distance = <strong>78.4 m</strong>. Including the downward motion while being caught (C to D), add 3.92 m: total downward travel is <strong>82.32 m</strong>.', 'Average velocity for the complete trip = net displacement / total time = <strong>0 m/s</strong>. Equal positive and negative graph areas cancel, and the ball ends at its starting height.') + paragraphs('The distances in (g) and (h) distinguish free flight from the additional motion during throwing and catching. This avoids changing the graph’s stated start and end points.'))
answer(69, parts('Assuming a drop from rest, d(1 s) = ½(9.81)(1)² = <strong>4.905 m ≈ 4.91 m</strong>.', 'During the second second: d(2 s) − d(1 s) = ½(9.81)(4 − 1) = <strong>14.715 m ≈ 14.7 m</strong>. Do not use the total two-second fall distance as the second-second distance.'))
answer(70, paragraphs('<strong>Speed</strong> is a scalar describing how fast an object moves. <strong>Velocity</strong> is a vector specifying both speed and direction. Average speed uses distance/time, while average velocity uses displacement/time.'))
answer(71, paragraphs('v̄ = 568/7.2 = 78.89 km/h ≈ <strong>79 km/h</strong>.'))
answer(72, parts('Unrounded total distance = 4.56 + 3.4 + 12.8 = 20.76 m. Addition is limited by the least precise decimal place: <strong>20.8 m</strong>.', 'Unrounded total time = 12 + 6.89 + 36.235 = 55.125 s. Since 12 s is stated to whole seconds, report <strong>55 s</strong>.', 'Keep unrounded totals for the division: v̄ = 20.76/55.125 = 0.3766 m/s. With the time precision, report <strong>0.38 m/s</strong>.'))
answer(73, paragraphs('The light travels to the Moon and back: d = 2(3.84 × 10⁵) = 7.68 × 10⁵ km.', 't = d/v = (7.68 × 10⁵)/(3.00 × 10⁵) = <strong>2.56 s</strong>.'))
answer(74, paragraphs('This gives the signed acceleration when motion stays along one fixed direction/axis, so a change in speed corresponds to the velocity component’s change. Choose and preserve a sign convention. With changing direction, speed alone is insufficient to determine acceleration. The ratio over an interval is <strong>average</strong> acceleration; it equals the constant acceleration if acceleration is uniform.'))
answer(75, paragraphs('v = v<sub>i</sub> + at = 0 + (7.0)(10.0) = <strong>70 m/s</strong>. Multiply by 3.6: 252 km/h ≈ <strong>2.5 × 10² km/h</strong> to two significant figures.'))
answer(76, parts('a = (60.0 − 20.0)/5.00 = <strong>8.00 m/s²</strong>.', 'Average speed = (20.0 + 60.0)/2 = <strong>40.0 m/s</strong>.', 'Distance = (40.0)(5.00) = <strong>200 m</strong>. This is also the trapezoidal area under the graph.', '<strong>v(t) = 20.0 m/s + (8.00 m/s²)t</strong>, for 0 ≤ t ≤ 5.00 s.'))
answer(77, paragraphs('v<sub>f</sub>² = v<sub>i</sub>² + 2ad = (1.4)² + 2(2.8)(2.5) = 15.96.', 'v<sub>f</sub> = √15.96 = 3.995 m/s ≈ <strong>4.0 m/s downhill</strong>.'))
answer(78, paragraphs('t = (v<sub>f</sub> − v<sub>i</sub>)/a = (1.52 × 10³ − 7.58 × 10³)/(−78.4) = <strong>77.3 s</strong>.'))
answer(79, paragraphs('a = ½g = 4.905 m/s². v<sub>f</sub> = 40.0 + (4.905)(5.2) = 65.506 m/s ≈ <strong>66 m/s</strong> (65.5 m/s before rounding).'))
answer(80, paragraphs('t = (60.0 − 80.0)/(−8.0) = 2.5 s. Average speed = 70.0 km/h = 19.444 m/s.', 'Distance = (19.444)(2.5) = 48.61 m ≈ <strong>49 m</strong>.'))
answer(81, parts('v<sub>f</sub> = √[v<sub>i</sub>² + 2ad] = √[(0.50)² + 2(2.3)(56)] = 16.06 m/s ≈ <strong>16 m/s upward</strong>.', 't = (v<sub>f</sub> − v<sub>i</sub>)/a = (16.0577 − 0.50)/2.3 = 6.764 s ≈ <strong>6.8 s</strong>.', 'Assuming he releases from rest at the 200.00 m height, t = √[2(200.00)/9.81] = <strong>6.39 s</strong>. If he still has an upward velocity when he lets go, that velocity must also be included; the prompt’s “drops” is taken to mean starts from rest.'))
answer(82, paragraphs('Compute the elapsed times from release to the window’s top (20.0 m) and bottom (22.0 m).', 'Δt = √[2(22.0)/9.81] − √[2(20.0)/9.81] = 2.1179 − 2.0193 = <strong>0.0986 s ≈ 0.099 s</strong>. The stone is already moving when it reaches the window.'))
answer(83, parts('a = (20.0 − 0)/5.00 = <strong>4.00 m/s²</strong>.', 'Total time from rest to take-off: t = 36.0/4.00 = <strong>9.00 s</strong>. This is 4.00 s more after the first 5.00 s.'))
answer(84, paragraphs('a = 3(9.81) = 29.43 m/s² and d = 0.25 km = 250 m.', 'v = √(2ad) = √[2(29.43)(250)] = 121.3 m/s ≈ <strong>1.2 × 10² m/s</strong>.'))
answer(85, parts('At the peak, v<sub>f</sub> = 0. Initial speed = √(2gh) = √[2(9.81)(0.50)] = <strong>3.13 m/s upward</strong>.', 'Returning to the same height, total free-flight time = 2v<sub>i</sub>/g = 2(3.1321)/9.81 = <strong>0.639 s</strong>.'))
answer(86, parts('Plot distance against time. The points form an <strong>upward-curving parabola</strong>: d = (2.50 cm/s²)t².', 'Plot distance against t². The points form a <strong>straight line through the origin</strong>, with slope 0.625 cm / 0.250 s² = <strong>2.50 cm/s²</strong>.', 'From rest, d = ½at². On a d-versus-t² graph the slope is a/2, so <strong>a = 2(2.50) = 5.00 cm/s² = 0.0500 m/s²</strong>.') + table(['t (s)','t² (s²)','d (cm)'],[(f'{t:.3f}',f'{t*t:.4f}',f'{2.5*t*t:.3f}') for t in [0,.1,.2,.3,.4,.5]]) + graph('Distance versus time', [('d = 2.50t² (cm)',[(i/100,2.5*(i/100)**2) for i in range(51)],'#096a70')],.5,0,.7,ylabel='Distance (cm)',xticks=[0,.1,.2,.3,.4,.5],yticks=[0,.2,.4,.6]) + graph('Distance versus squared time', [('slope = 2.50 cm/s²',[(0,0),(.25,.625)],'#096a70')],.25,0,.7,xlabel='Time squared (s²)',ylabel='Distance (cm)',xticks=[0,.05,.1,.15,.2,.25],yticks=[0,.2,.4,.6],dots=True))
answer(87, parts('One minute = 60 s: d = (3.00 × 10⁵)(60) = <strong>1.80 × 10⁷ km</strong>.', 'One hour = 3600 s: <strong>1.08 × 10⁹ km</strong>.', 'One day = 86 400 s: <strong>2.592 × 10¹⁰ km</strong>.', 'Using a 365-day year, t = 31 536 000 s: <strong>9.4608 × 10¹² km</strong> (about one light-year).'))
answer(88, paragraphs('v̄ = 1867/3.0 = 622.3 km/h ≈ <strong>6.2 × 10² km/h</strong>.'))
answer(89, paragraphs('v̄ = 2.0 m / (2.0 × 10⁵ s) = 1.0 × 10⁻⁵ m/s. Multiply by 1000 mm/m:', '<strong>v̄ = 1.0 × 10⁻² mm/s = 0.010 mm/s.</strong>'))
answer(90, paragraphs('d = vt = (3.00 × 10⁵)(1.28) = <strong>3.84 × 10⁵ km</strong>.'))
answer(91, paragraphs('d = vt = (82)(6.5) = 533 km ≈ <strong>5.3 × 10² km</strong>.'))
answer(92, parts('The y-intercept is <strong>4.0 m/s</strong>.', 'Use (0 s, 4.0 m/s) and (12 s, 16.0 m/s): slope = (16.0 − 4.0)/12 = <strong>1.0 m/s²</strong>.', '<strong>v = 4.0 m/s + (1.0 m/s²)t</strong>.'))
answer(93, parts('Assuming it starts from rest, v = at = (15.0)(2.5) = 37.5 m/s ≈ <strong>38 m/s</strong>.', 'd = ½at² = ½(15.0)(2.5)² = 46.875 m ≈ <strong>47 m</strong>.', 'Minimum runway under the stated constant-acceleration model: d = v²/(2a) = (60.0)²/[2(15.0)] = <strong>120 m</strong>.'))
answer(94, parts('Using the given rounded speed 22 m/s, reaction distance = (22)(0.40) = 8.8 m. Braking distance = 22²/[2(6.4)] = 37.81 m. Total stopping distance = <strong>46.61 m</strong>, so <strong>yes</strong>, the car stops about 3.4 m before the moose.', 'On the wet road, braking distance = 22²/[2(4.8)] = 50.42 m. Total = 8.8 + 50.42 = <strong>59.22 m</strong>, so <strong>the car hits the moose</strong>. At impact it has braked over 50.0 − 8.8 = 41.2 m: v = √[22² − 2(4.8)(41.2)] = <strong>9.4 m/s</strong>, about 34 km/h.') + paragraphs('Converting 80 km/h without rounding gives a slightly different stopping distance, but the yes/no conclusions are unchanged. These are results of the exercise’s idealized model.'))
answer(95, paragraphs('From rest, t = √(2h/g) = √[2(530)/9.81] = <strong>10.4 s</strong>, neglecting air resistance.'))
answer(96, parts('v<sub>f</sub> = √[v<sub>i</sub>² + 2ad] = √[(2.00)² + 2(3.00)(100.0)] = <strong>24.6 m/s</strong>.', 'Use the unrounded value: (24.5764)(3.6) = <strong>88.5 km/h</strong>.'))
answer(97, paragraphs('Choose forward positive. a = (v<sub>f</sub>² − v<sub>i</sub>²)/(2d) = [0 − (5.00)²]/[2(0.625)] = <strong>−20.0 m/s²</strong>, opposite the motion.'))
answer(98, paragraphs('d = v<sub>i</sub>t + ½at² gives 100.0 = 4.00t + t².', 'Solve t² + 4.00t − 100.0 = 0: t = [−4.00 + √(4.00² + 400.0)]/2 = <strong>8.20 s</strong>. Discard the negative-time root.'))
answer(99, parts('Initial speed is <strong>3.5 m/s</strong>.', 'a = (0 − 3.5)/(14 − 0) = <strong>−0.25 m/s²</strong>.', 'Distance is the triangle’s area: d = ½(14)(3.5) = <strong>24.5 m</strong> (about 25 m at the graph’s precision).', '<strong>v = 3.5 m/s − (0.25 m/s²)t</strong>, for 0 ≤ t ≤ 14 s.'))
answer(100, parts('Returning to the same level means displacement d = 0. Thus v<sub>f</sub>² = v<sub>i</sub>² + 2a(0) = v<sub>i</sub>², so <strong>|v<sub>f</sub>| = |v<sub>i</sub>|</strong>, assuming negligible air resistance.', '<strong>No.</strong> Speed is the same, but the returning velocity points downward. With up positive, v<sub>f</sub> = −v<sub>i</sub>.'))
answer(101, paragraphs('“The third one-second interval” means <strong>t = 2 s to t = 3 s</strong>. From rest, d(t) = ½at².', '7.5 m = d(3) − d(2) = ½a(3² − 2²) = 2.5a. Therefore <strong>a = 3.0 m/s² downhill</strong>.'))

assert set(A) == {f'q-{n}' for n in range(1,102)}
ANSWERS = A
