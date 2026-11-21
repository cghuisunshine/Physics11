/* Verify observable wave motion, matching projection, and accessible controls. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require(process.env.PHYSICS_JSDOM_PATH || 'jsdom');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'ripple-tank-animation.html'), 'utf8');

function setup(reducedMotion) {
  const callbacks = new Map(), errors = [];
  let id = 0, prints = 0;
  const vc = new VirtualConsole();
  vc.on('jsdomError', error => errors.push(error));
  const dom = new JSDOM(html, {
    url: 'https://physics.test/ripple-tank-animation.html', runScripts: 'dangerously', virtualConsole: vc,
    beforeParse(w) {
      w.matchMedia = () => ({ matches: reducedMotion });
      Object.defineProperty(w.document, 'hidden', { configurable: true, get: () => false });
      w.requestAnimationFrame = fn => { callbacks.set(++id, fn); return id; };
      w.cancelAnimationFrame = key => callbacks.delete(key);
      w.print = () => { prints++; };
    },
  });
  return {
    dom, callbacks, errors, prints: () => prints,
    frame(time) {
      assert.equal(callbacks.size, 1, 'Only one animation frame is scheduled');
      const [key, callback] = callbacks.entries().next().value;
      callbacks.delete(key); callback(time);
    },
  };
}

const test = setup(false);
try {
  const w = test.dom.window, d = w.document, $ = id => d.getElementById(id);
  const radius = () => Number($('water-fronts').querySelector('circle').getAttribute('r'));
  const phase = () => Number($('water-view').getAttribute('data-phase'));
  assert.deepEqual(test.errors, []);
  assert.equal($('play').textContent, 'Pause');
  const initial = radius();
  test.frame(0); test.frame(50);
  assert.ok(Math.abs(radius() - initial - 6) < 0.001, 'Circular crests travel 6 units in 0.05 s at speed 120');
  assert.equal($('water-fronts').innerHTML, $('screen-fronts').innerHTML, 'Projected lines match the water crests');
  $('play').click();
  assert.equal(test.callbacks.size, 0, 'Pausing cancels animation');
  assert.equal($('play').getAttribute('aria-pressed'), 'false');
  const paused = phase(); $('step').click();
  assert.ok(Math.abs(phase() - paused - 1 / 12) < 0.000002, 'Step advances one twelfth of a cycle');
  $('reset').click(); assert.equal(phase(), 0.25);
  assert.equal(test.callbacks.size, 0, 'Reset respects paused state');

  $('frequency').value = '2'; $('frequency').dispatchEvent(new w.Event('input', { bubbles: true }));
  assert.equal($('wavelength').textContent, '6.0 cm', 'Wavelength follows v/f');
  assert.equal($('frequency').getAttribute('aria-valuetext'), '2.0 hertz');
  const circles = [...$('water-fronts').querySelectorAll('circle')];
  assert.ok(Math.abs(Number(circles[1].getAttribute('r')) - Number(circles[0].getAttribute('r')) - 60) < 0.001);

  const bar = d.querySelector('[value="bar"]'); bar.checked = true;
  bar.dispatchEvent(new w.Event('change', { bubbles: true }));
  assert.equal($('water-fronts').querySelectorAll('circle').length, 0);
  assert.ok($('water-fronts').querySelectorAll('path').length > 2, 'Bar emits straight fronts');
  const position = () => Number($('water-fronts').querySelector('path').getAttribute('data-x'));
  const x = position(); $('play').click(); test.frame(0); test.frame(50);
  assert.ok(Math.abs(position() - x - 6) < 0.001, 'Bar crests have the same fixed speed');

  $('lamp').checked = false; $('lamp').dispatchEvent(new w.Event('change', { bubbles: true }));
  assert.equal($('screen-light').getAttribute('visibility'), 'hidden');
  assert.equal($('light-rays').getAttribute('visibility'), 'hidden');
  assert.equal($('side-bright-lines').getAttribute('visibility'), 'hidden');
  const darkPosition = position(); test.frame(100);
  assert.ok(position() > darkPosition, 'Turning off the lamp does not stop the water');
  $('lamp').checked = true; $('lamp').dispatchEvent(new w.Event('change', { bubbles: true }));
  assert.equal($('screen-light').getAttribute('visibility'), 'visible');
  assert.equal($('side-bright-lines').getAttribute('visibility'), 'visible');
  w.dispatchEvent(new w.Event('beforeprint')); assert.equal(test.callbacks.size, 0);
  w.dispatchEvent(new w.Event('afterprint')); assert.equal(test.callbacks.size, 1);
  $('print').click(); assert.equal(test.prints(), 1);
  assert.deepEqual(test.errors, []);
  assert.ok(!/<(?:script|link)\b[^>]*(?:src|href)=/.test(html), 'No external script or stylesheet is required');
  const notes = new JSDOM(fs.readFileSync(path.join(root, 'wave-motion-notes.html'), 'utf8'));
  assert.ok(notes.window.document.querySelector('#topic-6 a[href="ripple-tank-animation.html"]'));
  notes.window.close();
} finally { test.dom.window.close(); }

const reduced = setup(true);
try {
  assert.deepEqual(reduced.errors, []);
  assert.equal(reduced.dom.window.document.getElementById('play').textContent, 'Play');
  assert.equal(reduced.callbacks.size, 0, 'Reduced motion starts paused with a fully drawn snapshot');
  assert.ok(reduced.dom.window.document.querySelector('#water-fronts circle'));
} finally { reduced.dom.window.close(); }
console.log('Passed: circular/straight crest motion, projection alignment, v=fλ, lamp independence, pause/step/reset, print, reduced motion, offline assets, and Section 6 link.');
