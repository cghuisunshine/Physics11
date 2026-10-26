/* Chapter 5 source coverage, hidden answers, filters, and portable homework. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'bc-energy-questions.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/bc-energy-questions.json'),'utf8'));
const windows=[];
function page(source=html,url='https://example.test/bc-energy-questions.html',storage={}){
  const errors=[],downloads=[],copied=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
  const dom=new JSDOM(source,{url,runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
    w.print=()=>{};w.URL.createObjectURL=blob=>{downloads.push(blob);return 'blob:test';};w.URL.revokeObjectURL=()=>{};
    w.HTMLAnchorElement.prototype.click=function(){};
    Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async text=>copied.push(text)}});
    for(const [k,v] of Object.entries(storage))w.localStorage.setItem(k,v);
  }});windows.push(dom.window);
  return {w:dom.window,d:dom.window.document,$:id=>dom.window.document.getElementById(id),errors,downloads,copied};
}
function change(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
function select(p,id){const input=p.d.querySelector(`[data-homework="${id}"]`);input.checked=true;input.dispatchEvent(new p.w.Event('change'));}
const visible=p=>[...p.d.querySelectorAll('.question')].filter(q=>!q.hidden).map(q=>q.id);
const blobText=(p,b)=>new Promise(resolve=>{const r=new p.w.FileReader();r.onload=()=>resolve(r.result);r.readAsText(b);});
(async()=>{
  const p=page(html,undefined,{'bc-physics11-ch2-completed':'{"q-1":true}',
    'bc-physics11-ch2-homework':'{"ids":["q-1"],"title":"Kinematics draft"}',
    'bc-physics11-ch4-homework':'{"ids":["q-2"],"title":"Newton draft"}'});
  assert.deepEqual(p.errors,[]);assert.equal(visible(p).length,144);
  assert.equal(inventory.chapter,5);assert.equal(inventory.question_count,144);
  assert.equal(p.d.querySelectorAll('.question-set').length,34);
  assert.equal(p.$('set-33').dataset.kind,'Chapter review');
  assert.equal(p.d.querySelectorAll('.answer[hidden]').length,144);
  const ids=[...p.d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);
  for(const g of inventory.groups){
    const set=p.$(g.id);assert.equal(set.dataset.topic,g.topic);
    assert.equal(set.querySelectorAll('.question').length,g.questions.length);
    for(const q of g.questions){
      const article=p.$(q.id);assert.ok(article);const expected=p.d.createElement('div');
      expected.innerHTML=`<h3>Answer</h3>${q.answer_html}`;
      assert.equal(article.querySelector('.answer').innerHTML,expected.innerHTML);
      assert.equal(article.querySelectorAll('.question-image img').length,q.boxes.length);
      for(const [page,x0,y0,x1,y1] of q.boxes){assert.ok(page>=137&&page<=177);assert.ok(x1>x0&&y1>y0);}
    }
  }
  assert.equal(p.d.querySelectorAll('img:not([src^="data:image/"]),script[src],link[rel=stylesheet]').length,0);
  assert.deepEqual([...p.$('set-19').querySelectorAll('.question-top a')].map(a=>a.textContent),['Question 1','Question 2','Question 4','Question 5'],'Source numbering gap is preserved');
  for(const number of [2,6,10,39,77,83])assert.ok(!p.$(`q-${number}`).dataset.search.includes('what to think about'),'Sample answers are excluded from question images');
  assert.match(p.$('answer-q-97').textContent,/0.040°C\/s/);
  assert.match(p.$('answer-q-108').textContent,/6Ek/);
  assert.match(p.$('answer-q-110').textContent,/25 cm/);
  assert.match(p.$('answer-q-127').textContent,/0.70 m/);
  assert.match(p.$('answer-q-128').textContent,/4800 N/);
  assert.equal(p.$('homework-name').value,'Energy homework');
  assert.ok(!p.d.querySelector('[data-complete="q-1"]').checked,'Other chapters do not supply completion marks');
  p.$('toggle-q-110').click();assert.ok(!p.$('answer-q-110').hidden);
  p.$('toggle-q-110').click();assert.ok(p.$('answer-q-110').hidden);
  change(p,'topic','5.4');assert.equal(visible(p).length,25);
  change(p,'kind','Practice');assert.equal(visible(p).length,9);p.$('reset').click();
  const option=(id,value)=>[...p.d.querySelectorAll(`[data-filter-option="${id}"]`)].find(i=>i.value===value);
  for(const section of ['5.1','5.2'])option('topic',section).click();
  for(const kind of ['Practice','Quick check'])option('kind',kind).click();
  const matching=inventory.groups.filter(g=>['5.1','5.2'].includes(g.topic)&&['Practice','Quick check'].includes(g.kind)).flatMap(g=>g.questions.map(q=>q.id));
  assert.deepEqual(visible(p),matching);assert.equal(matching.length,16);
  assert.equal(p.$('topic-summary').textContent,'2 sections selected');
  p.$('create-homework').click();p.$('select-shown').click();
  assert.deepEqual([...p.d.querySelectorAll('[data-homework]:checked')].map(i=>i.dataset.homework),matching);
  p.$('clear-selection').click();p.$('reset').click();
  change(p,'search','radiometer');assert.ok(visible(p).includes('q-135'));p.$('reset').click();
  assert.equal(p.d.querySelectorAll('[data-section-percent]').length,6);
  for(const i of p.d.querySelectorAll('[data-section-percent]')){i.value=i.dataset.sectionPercent==='5.1'?'100':'0';i.dispatchEvent(new p.w.Event('input'));}
  change(p,'homework-sampling-order','first');p.$('apply-section-percentages').click();
  assert.equal(p.d.querySelectorAll('[data-homework]:checked').length,30);
  p.$('clear-selection').click();
  select(p,'q-11');select(p,'q-110');select(p,'q-127');change(p,'homework-name','Energy practice');
  p.$('preview-homework').click();assert.deepEqual(visible(p),['q-11','q-110','q-127']);
  assert.match(p.$('homework-details').textContent,/Chapter 5: Energy/);
  assert.ok(p.$('q-11').closest('.question-set').querySelector('.context').open);
  assert.ok(p.$('q-127').closest('.question-set').querySelector('.shared img'));
  p.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));const link=new URL(p.copied[0]);
  assert.equal(link.pathname,'/bc-energy-questions.html');
  const recipient=page(html,link.href);assert.deepEqual(visible(recipient),['q-11','q-110','q-127']);
  p.$('download-homework').click();const exported=await blobText(p,p.downloads[0]),offline=page(exported);
  assert.equal(offline.d.querySelectorAll('.question').length,3);
  assert.equal(offline.d.querySelectorAll('.answer,.answer-toggle').length,0);
  assert.ok(offline.d.querySelector('.context img'));assert.ok(offline.d.querySelector('.shared img'));
  assert.match(offline.d.querySelector('footer').textContent,/Chapter 5 Energy/);
  assert.ok(p.w.localStorage.getItem('bc-physics11-ch5-homework'));
  assert.match(p.w.localStorage.getItem('bc-physics11-ch2-homework'),/Kinematics draft/);
  assert.match(p.w.localStorage.getItem('bc-physics11-ch4-homework'),/Newton draft/);
  p.$('homework-answers').checked=true;p.$('homework-answers').dispatchEvent(new p.w.Event('change'));p.$('download-homework').click();
  const solved=page(await blobText(p,p.downloads[1]));assert.equal(solved.d.querySelectorAll('.answer').length,3);
  assert.match(solved.$('answer-q-110').textContent,/25 cm/);
  const local=page(html,'file:///tmp/bc-energy-questions.html');local.$('create-homework').click();select(local,'q-1');
  local.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));
  assert.equal(new URL(local.copied[0]).pathname,'/Physics11/bc-energy-questions.html');
  assert.match(fs.readFileSync(path.join(root,'content.html'),'utf8'),/href="bc-energy-questions.html"/);
  for(const result of [p,recipient,offline,solved,local])assert.deepEqual(result.errors,[]);
  console.log('Passed: all 144 entries and 34 sets, original numbering, hidden worked answers, filters, independent chapter storage, sampling, sharing, and homework exports with required figures.');
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(()=>windows.forEach(w=>w.close()));
