/* Verify the complete source collection survives its integration into the notes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'forces-notes.html'),'utf8');
const source=new JSDOM(fs.readFileSync(path.join(root,'bc-forces-questions.html'),'utf8'));
const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
const page=new JSDOM(html,{url:'https://example.test/forces-notes.html',runScripts:'dangerously',virtualConsole:vc,beforeParse(w){w.print=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};}});
try{
  const d=page.window.document,$=id=>d.getElementById(id),original=source.window.document;
  assert.deepEqual(errors,[]);assert.equal(d.querySelectorAll('.section-card').length,10);
  assert.equal(d.querySelectorAll('.practice-set').length,20);assert.equal(d.querySelectorAll('.practice-question').length,79);
  assert.equal(d.querySelectorAll('.answer-disclosure').length,85,'All 79 answers plus six tutorial answers start collapsed');
  assert.equal(d.querySelectorAll('.answer-disclosure[open]').length,0);
  const normalize=s=>s.replace(/([Frgμ])_([A-Za-z]+(?:,[A-Za-z]+)?)/g,'$1$2').replace(/\s+/g,' ').trim();
  for(const q of original.querySelectorAll('.question')){
    const copy=$('forces-'+q.id);assert.ok(copy,q.id);
    assert.deepEqual([...copy.querySelectorAll('.question-image img')].map(i=>i.src),[...q.querySelectorAll('.question-image img')].map(i=>i.src),'Original prompt images preserved: '+q.id);
    const answer=q.querySelector('.answer').cloneNode(true);answer.querySelector('h3').remove();
    const notesAnswer=copy.querySelector('.answer-body').cloneNode(true);notesAnswer.querySelector('h4').remove();
    assert.equal(normalize(notesAnswer.textContent),normalize(answer.textContent),'Full worked answer preserved: '+q.id);
    assert.equal(copy.querySelector('a').getAttribute('href'),'bc-forces-questions.html#'+q.id);
  }
  for(const group of original.querySelectorAll('.question-set')){
    const copy=$('forces-'+group.id);
    assert.deepEqual([...copy.querySelectorAll('.shared img,.context img')].map(i=>i.src),[...group.querySelectorAll('.shared img,.context img')].map(i=>i.src),'Referenced diagrams and procedures preserved: '+group.id);
  }
  const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length,'Every element ID is unique');
  for(const img of d.querySelectorAll('img')){assert.match(img.src,/^data:image\//);assert.ok(img.alt.trim());}
  for(const a of d.querySelectorAll('a[href^="#"]'))assert.ok(d.querySelector(a.getAttribute('href')));
  assert.equal(d.querySelectorAll('script[src],link[rel="stylesheet"]').length,0,'Notes have no runtime asset dependencies');
  assert.match($('topic-4').textContent,/coin-and-feather/);assert.match($('topic-9').textContent,/metre stick clamped horizontally/);
  assert.equal($('forces-example-6-1').querySelector('.answer-body').textContent.includes('135 N'),true,'Friction worked result is hidden inside its disclosure');
  assert.equal($('forces-q-47').querySelector('.answer-body').textContent.includes('N/m'),true,'Source correction about spring-constant units retained');
  const before=$('forces-answer-q-2');before.querySelector('summary').click();assert.ok(before.open);before.querySelector('summary').click();assert.ok(!before.open);
  assert.match(fs.readFileSync(path.join(root,'content.html'),'utf8'),/href="forces-notes.html"/);
  assert.deepEqual(errors,[]);
  console.log('Passed: 10 topics, all 79 original questions/answers and 20 sets, six hidden examples, full shared figures/procedures, unique IDs, offline assets, answer toggles, correct investigations, and notes-index link.');
}finally{page.window.close();source.window.close();}
