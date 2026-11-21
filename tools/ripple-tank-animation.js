/* Kinematic crest model and a deliberately schematic optical projection. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const state = { source: 'point', frequency: 1.2, phase: 0.25, playing: !reducedMotion, lamp: true };
  const speed = 120; // Logical units/s; 10 logical units represent 1 cm.
  let lastTime = null, frameId = null;
  const tau = 2 * Math.PI;
  const wavelength = () => speed / state.frequency;
  const distance = x => state.source === 'point' ? Math.abs(x - 240) : x - 40;
  const elevation = x => state.source === 'bar' && x < 40 ? 0 : Math.cos(tau * (distance(x) / wavelength() - state.phase));

  function fronts() {
    const lambda = wavelength(), parts = [];
    if (state.source === 'point') {
      for (let r = state.phase * lambda; r < 290; r += lambda) {
        parts.push(`<circle cx="240" cy="150" r="${r.toFixed(3)}"/>`);
      }
    } else {
      for (let x = 40 + state.phase * lambda; x < 480; x += lambda) {
        parts.push(`<path d="M${x.toFixed(3)} 0V300" data-x="${x.toFixed(3)}"/>`);
      }
    }
    return parts.join('');
  }

  function drawSideView() {
    const scale = 1.75, left = 60, baseline = 135, amplitude = 16;
    const lambda = wavelength(), waveNumber = tau / lambda;
    const points = [];
    for (let x = 0; x <= 480; x += 2) points.push(`${(left + x * scale).toFixed(2)},${(baseline - amplitude * elevation(x)).toFixed(2)}`);
    $('water-profile').setAttribute('d', 'M' + points.join('L'));
    $('water-fill').setAttribute('d', 'M' + points.join('L') + 'L900,230H60Z');
    const rays = [];
    for (let x = 4; x < 480; x += 10) {
      const sx = left + x * scale, sy = baseline - amplitude * elevation(x);
      const sign = state.source === 'point' && x < 240 ? -1 : 1;
      // Mapping compresses neighbouring rays near crests and spreads them near troughs.
      // It conveys focusing qualitatively; it is not a Snell-law ray trace.
      const shift = state.source === 'bar' && x < 40 ? 0 : sign * 0.85 / waveNumber * Math.sin(waveNumber * distance(x) - tau * state.phase) * scale;
      rays.push(`<path d="M${sx.toFixed(2)},57V${sy.toFixed(2)}L${(sx - shift * 0.45).toFixed(2)},230L${(sx - shift * 0.46).toFixed(2)},242L${(sx - shift).toFixed(2)},349"/>`);
    }
    $('light-rays').innerHTML = rays.join('');
    const bands = [];
    for (let x = 0; x <= 480; x += 1) {
      if (state.source === 'bar' && x < 40) continue;
      const bright = Math.pow(Math.max(0, elevation(x)), 18);
      if (bright > 0.015) bands.push(`<rect x="${left + x * scale}" y="339" width="1.8" height="21" fill="#fff0bf" opacity="${bright.toFixed(3)}"/>`);
    }
    $('side-bright-lines').innerHTML = bands.join('');
    const sourceX = state.source === 'point' ? 240 : 40;
    $('side-generator').innerHTML = `<rect x="${left + sourceX * scale - 5}" y="${baseline - amplitude * elevation(sourceX) - 17}" width="10" height="20" rx="3"/>`;
    $('light-rays').setAttribute('visibility', state.lamp ? 'visible' : 'hidden');
    $('side-bright-lines').setAttribute('visibility', state.lamp ? 'visible' : 'hidden');
    $('overhead-lamp').setAttribute('fill', state.lamp ? '#ffd481' : '#b6cdd1');
  }

  function draw() {
    const geometry = fronts();
    $('water-fronts').innerHTML = geometry;
    $('screen-fronts').innerHTML = geometry;
    $('screen-halos').innerHTML = geometry;
    $('water-view').setAttribute('data-phase', state.phase.toFixed(6));
    $('generator').innerHTML = state.source === 'point'
      ? '<circle cx="240" cy="150" r="8" fill="#182e3c" stroke="white" stroke-width="2"/>'
      : '<path d="M40 12V288" stroke="#182e3c" stroke-width="9" stroke-linecap="round"/>';
    $('travel-direction').innerHTML = state.source === 'point'
      ? '<path d="M270 175H325"/><path d="M210 125H155"/>' : '<path d="M70 150H135"/>';
    $('screen-light').setAttribute('visibility', state.lamp ? 'visible' : 'hidden');
    $('lamp-off-label').setAttribute('visibility', state.lamp ? 'hidden' : 'visible');
    drawSideView();
  }

  function updateControls() {
    $('play').textContent = state.playing ? 'Pause' : 'Play';
    $('play').setAttribute('aria-pressed', String(state.playing));
    $('frequency-value').textContent = state.frequency.toFixed(1) + ' Hz';
    $('frequency').setAttribute('aria-valuetext', state.frequency.toFixed(1) + ' hertz');
    $('wavelength').textContent = (wavelength() / 10).toFixed(1) + ' cm';
    $('water-caption').textContent = state.source === 'point'
      ? 'Each teal circle joins points at a crest. The pattern travels outwards in every horizontal direction.'
      : 'Each teal line is a crest parallel to the bar. This view shows waves on one side; waves can travel on both sides of a real bar.';
    $('status').textContent = `${state.playing ? 'Running' : 'Paused'} · ${state.source === 'point' ? 'point source' : 'straight bar'} · lamp ${state.lamp ? 'on' : 'off'}.`;
  }

  function tick(now) {
    frameId = null;
    if (!state.playing || document.hidden) return;
    if (lastTime !== null) state.phase = (state.phase + Math.min((now - lastTime) / 1000, 0.1) * state.frequency) % 1;
    lastTime = now;
    draw();
    frameId = requestAnimationFrame(tick);
  }

  function schedule() {
    if (frameId !== null) cancelAnimationFrame(frameId);
    frameId = null;
    lastTime = null;
    if (state.playing && !document.hidden) frameId = requestAnimationFrame(tick);
  }

  $('play').addEventListener('click', () => { state.playing = !state.playing; updateControls(); schedule(); });
  $('step').addEventListener('click', () => {
    state.playing = false;
    state.phase = (state.phase + 1 / 12) % 1;
    updateControls(); draw(); schedule();
  });
  $('reset').addEventListener('click', () => { state.phase = 0.25; updateControls(); draw(); schedule(); });
  $('frequency').addEventListener('input', event => {
    state.frequency = Number(event.target.value);
    updateControls(); draw(); schedule();
  });
  document.querySelectorAll('input[name="source"]').forEach(input => input.addEventListener('change', () => {
    if (!input.checked) return;
    state.source = input.value;
    updateControls(); draw();
  }));
  $('lamp').addEventListener('change', event => { state.lamp = event.target.checked; updateControls(); draw(); });
  document.addEventListener('visibilitychange', schedule);
  let resumeAfterPrint = false;
  window.addEventListener('beforeprint', () => {
    resumeAfterPrint = state.playing;
    state.playing = false; updateControls(); schedule();
  });
  window.addEventListener('afterprint', () => {
    state.playing = resumeAfterPrint; updateControls(); schedule();
  });
  $('print').addEventListener('click', () => window.print());
  updateControls(); draw(); schedule();
})();
