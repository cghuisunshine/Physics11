/* Chapter 4 source coverage, homework isolation, filters, and offline exports. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'bc-newtons-laws-questions.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/bc-newtons-laws-questions.json'),'utf8'));
const windows=[];
function page(source=html,url='https://example.test/bc-newtons-laws-questions.html',storage={}){
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
  const p=page(html,undefined,{'bc-physics11-ch2-completed':JSON.stringify({'q-1':true}),'bc-physics11-ch2-homework':JSON.stringify({ids:['q-1'],title:'Kinematics draft'})});
  assert.deepEqual(p.errors,[]);assert.equal(visible(p).length,121);assert.equal(inventory.chapter,4);assert.equal(inventory.question_count,121);
  assert.equal(p.d.querySelectorAll('.question-set').length,32);assert.equal(p.d.querySelectorAll('.answer').length,121);
  const ids=[...p.d.querySelectorAll('[id]')].map(el=>el.id);assert.equal(new Set(ids).size,ids.length,'All HTML IDs are unique');
  for(const g of inventory.groups){
    const set=p.$(g.id);assert.equal(set.dataset.topic,g.topic);assert.equal(set.querySelectorAll('.question').length,g.questions.length);
    for(const q of g.questions){
      const article=p.$(q.id);assert.ok(article);const expected=p.d.createElement('div');expected.innerHTML=`<h3>Answer</h3>${q.answer_html}`;assert.equal(article.querySelector('.answer').innerHTML,expected.innerHTML);
      assert.equal(article.querySelectorAll('.question-image img').length,q.boxes.length);
      for(const [page,x0,y0,x1,y1] of q.boxes){assert.ok(page>=107&&page<=135);assert.ok(x1>x0&&y1>y0);}
      for(const image of article.querySelectorAll('.question-image img'))assert.ok(image.src.startsWith('data:image/webp;base64,'));
    }
  }
  assert.equal(p.d.querySelectorAll('img:not([src^="data:image/"]),script[src],link[rel=stylesheet]').length,0);
  assert.match(p.$('q-20').dataset.search,/you are carrying a carton of milk/,'The complete concluding-question setup is preserved');
  assert.match(p.$('q-78').dataset.search,/a railway car of mass/,'The sample retains its initial mass and velocity');
  assert.ok(!p.$('q-77').dataset.search.includes('any moving body'),'Impulse question excludes the following explanatory lesson');
  assert.equal(p.$('homework-name').value,'Newton’s Laws of Motion homework');assert.ok(!p.d.querySelector('[data-complete="q-1"]').checked,'Chapter 2 completion does not leak into Chapter 4');
  p.$('toggle-q-38').click();assert.ok(!p.$('answer-q-38').hidden);assert.match(p.$('answer-q-38').textContent,/75 kg/);p.$('toggle-q-38').click();assert.ok(p.$('answer-q-38').hidden);
  change(p,'topic','4.2');assert.equal(visible(p).length,21);change(p,'kind','Practice');assert.equal(visible(p).length,4);
  p.$('reset').click();
  const filterOption=(id,value)=>[...p.d.querySelectorAll(`[data-filter-option="${id}"]`)].find(input=>input.value===value);
  assert.equal(p.$('topic').multiple,true);assert.equal(p.$('kind').multiple,true);
  const selectCombined=()=>{for(const section of ['4.1','4.2'])filterOption('topic',section).click();for(const kind of ['Quick check','Practice'])filterOption('kind',kind).click();};
  selectCombined();
  const matching=inventory.groups.filter(g=>['4.1','4.2'].includes(g.topic)&&['Quick check','Practice'].includes(g.kind)).flatMap(g=>g.questions.map(q=>q.id));
  assert.deepEqual(visible(p),matching,'Multiple sections and multiple types combine as OR within each filter, AND across filters');
  assert.equal(p.$('topic-summary').textContent,'2 sections selected');assert.equal(p.$('kind-summary').textContent,'2 types selected');
  assert.equal(filterOption('topic','').checked,false);
  p.$('create-homework').click();p.$('select-shown').click();
  assert.deepEqual([...p.d.querySelectorAll('[data-homework]:checked')].map(input=>input.dataset.homework),matching,'Select shown uses every selected section and type');
  p.$('clear-selection').click();selectCombined();change(p,'homework-all-percent','100');p.$('set-section-percentages').click();change(p,'homework-sampling-order','first');p.$('apply-section-percentages').click();
  assert.deepEqual([...p.d.querySelectorAll('[data-homework]:checked')].map(input=>input.dataset.homework),matching,'Section sampling uses the same combined filters');
  p.$('clear-selection').click();selectCombined();p.$('create-homework').click();
  for(const section of ['4.1','4.2'])filterOption('topic',section).click();
  assert.deepEqual(visible(p),[]);assert.equal(p.$('topic-summary').textContent,'Choose sections');
  filterOption('topic','').click();filterOption('kind','').click();assert.equal(visible(p).length,121);
  p.$('topic-picker').open=true;p.$('topic-picker').dispatchEvent(new p.w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  assert.equal(p.$('topic-picker').open,false);assert.equal(p.d.activeElement,p.$('topic-summary'));
  p.$('reset').click();change(p,'search','paratrooper');assert.deepEqual(visible(p),['q-38']);p.$('reset').click();
  assert.equal(p.$('topic-summary').textContent,'All sections');assert.equal(p.$('kind-summary').textContent,'All types');
  p.$('create-homework').click();assert.ok(!p.$('homework-panel').hidden);assert.equal(p.d.querySelectorAll('[data-section-percent]').length,6);
  for(const input of p.d.querySelectorAll('[data-section-percent]')){input.value='0';input.dispatchEvent(new p.w.Event('input'));}
  const gravity=p.d.querySelector('[data-section-percent="4.1"]');gravity.value='100';gravity.dispatchEvent(new p.w.Event('input'));
  p.$('apply-section-percentages').click();assert.equal(p.d.querySelectorAll('[data-homework]:checked').length,29);
  p.$('clear-selection').click();
  select(p,'q-7');select(p,'q-52');select(p,'q-87');change(p,'homework-name','Newton’s laws practice');
  p.$('preview-homework').click();assert.deepEqual(visible(p),['q-7','q-52','q-87']);assert.match(p.$('homework-details').textContent,/Chapter 4: Newton’s Laws of Motion/);
  assert.ok(p.$('q-7').closest('.question-set').querySelector('.context').open);assert.ok(p.$('q-52').closest('.question-set').querySelector('.shared img'));
  p.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));const link=new URL(p.copied[0]);assert.equal(link.pathname,'/bc-newtons-laws-questions.html');
  const recipient=page(html,link.href);assert.deepEqual(visible(recipient),['q-7','q-52','q-87']);
  p.$('download-homework').click();const exported=await blobText(p,p.downloads[0]),offline=page(exported);
  assert.equal(offline.d.querySelectorAll('.question').length,3);assert.equal(offline.d.querySelectorAll('.answer,.answer-toggle').length,0);
  assert.ok(offline.d.querySelector('.context img'));assert.ok(offline.d.querySelector('.shared img'));
  assert.match(offline.d.querySelector('footer').textContent,/Chapter 4 Newton’s Laws of Motion/);
  assert.ok(p.w.localStorage.getItem('bc-physics11-ch4-homework'));assert.match(p.w.localStorage.getItem('bc-physics11-ch2-homework'),/Kinematics draft/);
  p.$('homework-answers').checked=true;p.$('homework-answers').dispatchEvent(new p.w.Event('change'));p.$('download-homework').click();
  const withAnswers=page(await blobText(p,p.downloads[1]));assert.equal(withAnswers.d.querySelectorAll('.answer').length,3);assert.ok(withAnswers.$('answer-q-87'));
  const file=page(html,'file:///tmp/bc-newtons-laws-questions.html');file.$('create-homework').click();select(file,'q-1');file.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));
  assert.equal(new URL(file.copied[0]).pathname,'/Physics11/bc-newtons-laws-questions.html','Local-file links point to the Newton’s laws collection');
  assert.deepEqual(p.errors,[]);assert.deepEqual(recipient.errors,[]);assert.deepEqual(offline.errors,[]);assert.deepEqual(withAnswers.errors,[]);
  for(const w of windows)w.close();
  console.log('Passed: 121 questions, 32 sets, source inventory, answers, filters, chapter-isolated storage, sampling, share links, and standalone homework exports.');
})().catch(error=>{for(const w of windows)w.close();console.error(error);process.exitCode=1;});
