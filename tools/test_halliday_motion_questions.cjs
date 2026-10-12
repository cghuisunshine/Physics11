/* Source coverage and offline homework behavior for Halliday Chapter 2. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),source=fs.readFileSync(path.join(root,'halliday-motion-questions.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/halliday-motion-questions.json'),'utf8'));
const windows=[];
function page(html=source,url='https://example.test/halliday-motion-questions.html'){
  const errors=[],downloads=[],copied=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
  const dom=new JSDOM(html,{url,runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
    w.print=()=>{};w.URL.createObjectURL=b=>{downloads.push(b);return 'blob:test';};w.URL.revokeObjectURL=()=>{};
    w.HTMLAnchorElement.prototype.click=function(){};
    Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async s=>copied.push(s)}});
    try{w.localStorage.setItem('bc-physics11-ch2-completed','{"q-1":true}');}catch{}
  }});windows.push(dom.window);return {w:dom.window,d:dom.window.document,$:id=>dom.window.document.getElementById(id),errors,downloads,copied};
}
function input(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
function select(p,id){const c=p.d.querySelector('[data-homework="'+id+'"]');c.checked=true;c.dispatchEvent(new p.w.Event('change'));}
const visible=p=>[...p.d.querySelectorAll('.question')].filter(q=>!q.hidden).map(q=>q.id);
const blobText=(p,b)=>new Promise(resolve=>{const r=new p.w.FileReader();r.onload=()=>resolve(r.result);r.readAsText(b);});
(async()=>{
  const p=page();assert.deepEqual(p.errors,[]);assert.equal(inventory.question_count,141);
  assert.equal(visible(p).length,141);assert.equal(p.d.querySelectorAll('.question-set').length,19);
  const ids=[...p.d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);
  const problems=inventory.groups.filter(g=>['Problem','Additional problem'].includes(g.kind)).flatMap(g=>g.questions);
  assert.deepEqual(problems.map(q=>+q.label),Array.from({length:119},(_,i)=>i+1));
  assert.equal(inventory.groups.find(g=>g.kind==='Conceptual question').questions.length,11);
  for(const g of inventory.groups)for(const q of g.questions){
    const article=p.$(q.id);assert.ok(article);assert.equal(article.closest('.question-set').id,g.id);
    assert.equal(article.querySelectorAll('.question-image img').length,q.boxes.length+q.figures.length);
    for(const [page,x0,y0,x1,y1] of q.boxes){assert.ok(page>=49&&page<=75);assert.ok(x1>x0&&y1>y0);}
    if(q.solution_boxes.length){
      assert.equal(article.querySelectorAll('.answer-image img').length,q.solution_boxes.length);
      for(const [page] of q.solution_boxes)assert.ok(q.sample?page>=49&&page<=75:page>=31&&page<=89);
    }else assert.ok(article.querySelector('.answer').textContent.length>40);
    assert.ok(article.querySelector('.answer').hidden);
    if(g.kind==='Sample prompt')assert.doesNotMatch(q.text,/Calculation|\(Answer\)|KEY IDEA/,'Solutions stay hidden in sample prompts');
  }
  for(const f of Object.keys(inventory.figures))assert.ok(problems.some(q=>q.figures.includes(+f)),'Figure 2-'+f+' is attached');
  assert.ok(problems[33].figures.includes(27));assert.ok(problems[34].figures.includes(27));
  assert.deepEqual(problems[23].figures,[],'Neighboring figure 2-26 does not belong to problem 24');
  assert.deepEqual(problems[56].figures,[],'Neighboring figure 2-35 does not belong to problem 57');
  assert.ok(problems[5].boxes.every(b=>b[1]<330||b[2]>=439),'First-page column continuation excludes the conceptual questions and page legend');
  assert.equal(p.d.querySelectorAll('img:not([src^="data:image/"]),script[src],link[rel=stylesheet]').length,0);
  assert.ok(!p.d.querySelector('[data-complete="q-1"]').checked,'BC storage does not leak into Halliday');
  assert.equal(p.$('homework-name').value,'Motion Along a Straight Line homework');
  const sample=inventory.groups.find(g=>g.title.startsWith('Sample 2.01')).questions[0];
  assert.match(sample.text,/\(d\) Suppose/);
  const acceleration=inventory.groups.find(g=>g.title.startsWith('Sample 2.03')).questions[0];
  assert.match(acceleration.text,/\(b\) Is there ever/);assert.match(acceleration.text,/\(c\) Describe/);
  p.$('toggle-q-23').click();assert.ok(!p.$('answer-q-23').hidden);p.$('toggle-q-23').click();assert.ok(p.$('answer-q-23').hidden);
  input(p,'topic','2-4');assert.equal(visible(p).length,23);input(p,'kind','Problem');assert.equal(visible(p).length,21);
  p.$('reset').click();input(p,'search','hard sneeze');assert.deepEqual(visible(p),[problems[0].id]);p.$('reset').click();
  p.$('create-homework').click();assert.equal(p.d.querySelectorAll('[data-section-percent]').length,8);
  select(p,problems[33].id);select(p,problems[118].id);input(p,'homework-name','Straight-line motion practice');
  p.$('preview-homework').click();assert.deepEqual(visible(p),[problems[33].id,problems[118].id]);
  p.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));
  const link=new URL(p.copied[0]);assert.equal(link.pathname,'/halliday-motion-questions.html');
  const recipient=page(source,link.href);assert.deepEqual(visible(recipient),visible(p));
  p.$('download-homework').click();const offline=page(await blobText(p,p.downloads[0]));
  assert.equal(offline.d.querySelectorAll('.question').length,2);assert.equal(offline.d.querySelectorAll('.answer,.answer-toggle').length,0);
  assert.equal(offline.$(problems[33].id).querySelectorAll('.question-image img').length,problems[33].boxes.length+1);
  assert.match(offline.d.querySelector('footer').textContent,/Halliday & Resnick/);
  p.$('homework-answers').checked=true;p.$('homework-answers').dispatchEvent(new p.w.Event('change'));p.$('download-homework').click();
  const withAnswers=page(await blobText(p,p.downloads[1]));assert.equal(withAnswers.d.querySelectorAll('.answer').length,2);
  assert.equal(withAnswers.$(problems[118].id).querySelectorAll('.answer-image img').length,2,'Last solution includes its continuation page');
  assert.ok(p.w.localStorage.getItem('halliday-physics-ch2-homework'));
  const local=page(source,'file:///tmp/halliday-motion-questions.html');local.$('create-homework').click();select(local,'q-1');local.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));
  assert.equal(new URL(local.copied[0]).pathname,'/Physics11/halliday-motion-questions.html');
  for(const check of [p,recipient,offline,withAnswers,local])assert.deepEqual(check.errors,[]);
  for(const w of windows)w.close();console.log('Passed: 141 entries, complete numbering, figures, filters, isolated storage, answers, links, and offline homework exports.');
})().catch(e=>{for(const w of windows)w.close();console.error(e);process.exitCode=1;});
