const assert = require('node:assert/strict');
const {chromium} = require('/Users/chenguagnghui/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({executablePath:'/Users/chenguagnghui/Library/Caches/ms-playwright/chromium-1228/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing', headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1100,height:1100}});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto('file:///Users/chenguagnghui/tutor/Physics11/newtons-laws-review.html');
    assert.equal(await page.locator('main > section').count(), 9);
    assert.equal(await page.locator('.question').count(), 21);
    assert.equal(await page.locator('.answer-page').count(), 2);
    assert.ok(await page.locator('a[href^="#"]').evaluateAll(links => links.every(a => document.getElementById(a.hash.slice(1)))));
    assert.ok(await page.locator('[id]').evaluateAll(nodes => new Set(nodes.map(n=>n.id)).size === nodes.length));
    assert.equal(await page.locator('script[src], link[rel="stylesheet"]').count(), 0);
    await page.evaluate(() => { window.print = () => { window.printCalled = true; }; });
    await page.locator('#print-review').click();
    assert.ok(await page.evaluate(() => window.printCalled));
    await page.getByRole('link', {name:'Answer key', exact:true}).click();
    assert.equal(new URL(page.url()).hash, '#page-8');
    await page.goto('file:///Users/chenguagnghui/tutor/Physics11/newtons-laws-review.html');
    await page.locator('#page-1').screenshot({path:'tmp/newtons-laws-review-qa/desktop.png'});
    await page.emulateMedia({media:'print'});
    // Match Letter page width inside the 12 mm margins used by @page.
    await page.setViewportSize({width:725,height:1100});
    const layouts = await page.locator('main > section').evaluateAll(sections => sections.map(s => ({page:s.id,height:s.getBoundingClientRect().height,minHeight:parseFloat(getComputedStyle(s).minHeight),lastContent:s.lastElementChild.getBoundingClientRect().bottom-s.getBoundingClientRect().top})));
    console.log('Print layout:', layouts);
    for (const layout of layouts) assert.ok(layout.height <= layout.minHeight + 2, `${layout.page} exceeds one printed page`);
    for (let n=1; n<=9; n++) await page.locator(`#page-${n}`).screenshot({path:`tmp/newtons-laws-review-qa/print-${n}.png`});
    await page.emulateMedia({media:'screen'});
    await page.setViewportSize({width:390,height:844});
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'No mobile horizontal overflow');
    await page.screenshot({path:'tmp/newtons-laws-review-qa/mobile.png'});
    await page.getByRole('link', {name:'Full Newton’s laws notes'}).click();
    assert.match(page.url(), /newtons-laws-notes.html$/);
    await page.locator('#notes-menu-toggle').click();
    await page.getByRole('link', {name:'Quick Review · 21 questions'}).click();
    assert.match(page.url(), /newtons-laws-review.html$/);
    await page.goto('file:///Users/chenguagnghui/tutor/Physics11/content.html');
    await page.getByRole('link', {name:/Newton's Laws: Quick Review/}).click();
    assert.match(page.url(), /newtons-laws-review.html$/);
    assert.deepEqual(errors, []);
    console.log('Passed: 9 print pages, 21 questions, answer anchors, print button, mobile layout, offline assets, notes-menu and index navigation; no browser errors.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
