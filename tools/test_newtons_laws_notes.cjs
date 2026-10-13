/* Verify the complete source collection survives its integration into the notes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'newtons-laws-notes.html'),'utf8');
const source=new JSDOM(fs.readFileSync(path.join(root,'bc-newtons-laws-questions.html'),'utf8'));
const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
const page=new JSDOM(html,{url:'https://example.test/newtons-laws-notes.html',runScripts:'dangerously',virtualConsole:vc,beforeParse(w){w.print=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};}});
try{
  const d=page.window.document,$=id=>d.getElementById(id),original=source.window.document;
  assert.deepEqual(errors,[]);assert.equal(d.querySelectorAll('.section-card').length,12);
  assert.equal(d.querySelectorAll('.practice-set').length,32);assert.equal(d.querySelectorAll('.practice-question').length,121);
  assert.equal(d.querySelectorAll('.answer-disclosure').length,127,'All 121 answers plus six tutorial answers start collapsed');
  assert.equal(d.querySelectorAll('.answer-disclosure[open]').length,0);
  const normalize=s=>s.replace(/([Fpmvagμ])_([A-Za-z]+(?:,[A-Za-z]+)?)/g,'$1$2').replace(/\s+/g,' ').trim();
  const svgContent=svg=>[svg,...svg.querySelectorAll('*')].map(e=>({tag:e.tagName,
    attributes:[...e.attributes].map(a=>[a.name,a.value]).sort((a,b)=>a[0].localeCompare(b[0])),text:e.textContent}));
  for(const q of original.querySelectorAll('.question')){
    const copy=$('newtons-'+q.id);assert.ok(copy,q.id);
    assert.deepEqual([...copy.querySelectorAll('.question-image img')].map(i=>i.src),[...q.querySelectorAll('.question-image img')].map(i=>i.src),'Original prompt images preserved: '+q.id);
    const answer=q.querySelector('.answer').cloneNode(true);answer.querySelector('h3').remove();
    const notesAnswer=copy.querySelector('.answer-body').cloneNode(true);notesAnswer.querySelector('h4').remove();
    assert.equal(normalize(notesAnswer.textContent),normalize(answer.textContent),'Full worked answer preserved: '+q.id);
    assert.deepEqual([...notesAnswer.querySelectorAll('svg')].map(svgContent),[...answer.querySelectorAll('svg')].map(svgContent),'Answer diagrams preserved: '+q.id);
    assert.equal(copy.querySelector('a').getAttribute('href'),'bc-newtons-laws-questions.html#'+q.id);
  }
  for(const group of original.querySelectorAll('.question-set')){
    const copy=$('newtons-'+group.id);
    assert.deepEqual([...copy.querySelectorAll('.shared img,.context img')].map(i=>i.src),[...group.querySelectorAll('.shared img,.context img')].map(i=>i.src),'Referenced diagrams and procedures preserved: '+group.id);
  }
  const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length,'Every element ID is unique');
  for(const img of d.querySelectorAll('img')){assert.match(img.src,/^data:image\//);assert.ok(img.alt.trim());}
  for(const a of d.querySelectorAll('a[href^="#"]'))assert.ok(d.querySelector(a.getAttribute('href')));
  assert.equal(d.querySelectorAll('script[src],link[rel="stylesheet"]').length,0,'Notes have no runtime asset dependencies');
  assert.match(d.querySelector('.hero p').textContent,/Learn inertia, the three laws, momentum, and impulse/);
  assert.match($('topic-1').textContent,/Inertia is a property of matter/);
  assert.match($('topic-7').textContent,/different objects/);
  assert.match($('topic-11').textContent,/net external impulse/);
  const pairs=[...d.querySelectorAll('.investigation-pair')];assert.equal(pairs.length,13);
  for(const pair of pairs){
    assert.ok(pair.querySelector('.diagram img'));
    assert.ok(pair.querySelector('.investigation-explanation').textContent.length>150);
    assert.equal(pair.closest('details'),null,'Setup diagram remains visible beside its explanation');
  }
  const graphs=[...$('topic-6').querySelectorAll('.law-graph')];assert.equal(graphs.length,3);
  for(const [index,figure] of graphs.entries()){
    const name=['acceleration-force','acceleration-mass','acceleration-reciprocal-mass'][index];
    assert.equal(figure.closest('details'),null);
    assert.equal(Buffer.from(figure.querySelector('img').src.split(',')[1],'base64').toString(),fs.readFileSync(path.join(root,'assets/newtons-laws-notes',name+'.svg'),'utf8'));
  }
  const expectedAnswers={'newtons-example-2-1':'12 N to the left','newtons-example-4-1':'2.00 m/s² right',
    'newtons-example-5-1':'2.04 m/s² right','newtons-example-7-1':'−6.00 m/s²',
    'newtons-example-10-1':'−20.0 N','newtons-example-11-1':'1.00 m/s right'};
  for(const [id,result] of Object.entries(expectedAnswers))assert.ok($(id).querySelector('.answer-body').textContent.includes(result));
  const before=$('newtons-answer-q-2');before.querySelector('summary').click();assert.ok(before.open);before.querySelector('summary').click();assert.ok(!before.open);
  assert.match(fs.readFileSync(path.join(root,'content.html'),'utf8'),/href="newtons-laws-notes.html"/);
  assert.deepEqual(errors,[]);
  console.log('Passed: 12 topics, all 121 original questions/answers and 32 sets, six hidden examples, full shared figures/procedures, unique IDs, offline assets, answer toggles, correct investigations, and notes-index link.');
}finally{page.window.close();source.window.close();}
