/* Chapter 3 source coverage, homework isolation, filters, and offline exports. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'bc-forces-questions.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/bc-forces-questions.json'),'utf8'));
const windows=[];
function page(source=html,url='https://example.test/bc-forces-questions.html',storage={}){
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
  assert.deepEqual(p.errors,[]);assert.equal(visible(p).length,79);assert.equal(inventory.chapter,3);assert.equal(inventory.question_count,79);
  assert.equal(p.d.querySelectorAll('.question-set').length,20);assert.equal(p.d.querySelectorAll('.answer').length,79);
  const ids=[...p.d.querySelectorAll('[id]')].map(el=>el.id);assert.equal(new Set(ids).size,ids.length,'All HTML IDs are unique');
  for(const g of inventory.groups){
    const set=p.$(g.id);assert.equal(set.dataset.topic,g.topic);assert.equal(set.querySelectorAll('.question').length,g.questions.length);
    for(const q of g.questions){
      const article=p.$(q.id);assert.ok(article);const expected=p.d.createElement('div');expected.innerHTML=`<h3>Answer</h3>${q.answer_html}`;assert.equal(article.querySelector('.answer').innerHTML,expected.innerHTML);
      assert.equal(article.querySelectorAll('.question-image img').length,q.boxes.length);
      for(const [page,x0,y0,x1,y1] of q.boxes){assert.ok(page>=81&&page<=105);assert.ok(x1>x0&&y1>y0);}
      for(const image of article.querySelectorAll('.question-image img'))assert.ok(image.src.startsWith('data:image/webp;base64,'));
    }
  }
  assert.equal(p.d.querySelectorAll('img:not([src^="data:image/"]),script[src],link[rel=stylesheet]').length,0);
  assert.equal(p.$('homework-name').value,'Forces homework');assert.ok(!p.d.querySelector('[data-complete="q-1"]').checked,'Chapter 2 completion does not leak into Chapter 3');
  p.$('toggle-q-47').click();assert.ok(!p.$('answer-q-47').hidden);assert.match(p.$('answer-q-47').textContent,/does have units/);p.$('toggle-q-47').click();assert.ok(p.$('answer-q-47').hidden);
  change(p,'topic','3.2');assert.equal(visible(p).length,18);change(p,'kind','Practice');assert.equal(visible(p).length,3);
  p.$('reset').click();change(p,'search','bowling');assert.deepEqual(visible(p),['q-67']);p.$('reset').click();
  p.$('create-homework').click();assert.ok(!p.$('homework-panel').hidden);assert.equal(p.d.querySelectorAll('[data-section-percent]').length,5);
  for(const input of p.d.querySelectorAll('[data-section-percent]')){input.value='0';input.dispatchEvent(new p.w.Event('input'));}
  const gravity=p.d.querySelector('[data-section-percent="3.1"]');gravity.value='100';gravity.dispatchEvent(new p.w.Event('input'));
  p.$('apply-section-percentages').click();assert.equal(p.d.querySelectorAll('[data-homework]:checked').length,21);
  p.$('clear-selection').click();
  select(p,'q-27');select(p,'q-42');select(p,'q-55');change(p,'homework-name','Forces practice');
  p.$('preview-homework').click();assert.deepEqual(visible(p),['q-27','q-42','q-55']);assert.match(p.$('homework-details').textContent,/Chapter 3: Forces/);
  assert.ok(p.$('q-27').closest('.question-set').querySelector('.context').open);assert.ok(p.$('q-42').closest('.question-set').querySelector('.shared img'));
  p.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));const link=new URL(p.copied[0]);assert.equal(link.pathname,'/bc-forces-questions.html');
  const recipient=page(html,link.href);assert.deepEqual(visible(recipient),['q-27','q-42','q-55']);
  p.$('download-homework').click();const exported=await blobText(p,p.downloads[0]),offline=page(exported);
  assert.equal(offline.d.querySelectorAll('.question').length,3);assert.equal(offline.d.querySelectorAll('.answer,.answer-toggle').length,0);
  assert.ok(offline.d.querySelector('.context img'));assert.ok(offline.d.querySelector('.shared img'));
  assert.match(offline.d.querySelector('footer').textContent,/Chapter 3 Forces/);
  assert.ok(p.w.localStorage.getItem('bc-physics11-ch3-homework'));assert.match(p.w.localStorage.getItem('bc-physics11-ch2-homework'),/Kinematics draft/);
  p.$('homework-answers').checked=true;p.$('homework-answers').dispatchEvent(new p.w.Event('change'));p.$('download-homework').click();
  const withAnswers=page(await blobText(p,p.downloads[1]));assert.equal(withAnswers.d.querySelectorAll('.answer').length,3);assert.ok(withAnswers.$('answer-q-55'));
  const file=page(html,'file:///tmp/bc-forces-questions.html');file.$('create-homework').click();select(file,'q-1');file.$('copy-homework').click();await new Promise(r=>setTimeout(r,10));
  assert.equal(new URL(file.copied[0]).pathname,'/Physics11/bc-forces-questions.html','Local-file links point to the Forces collection');
  assert.deepEqual(p.errors,[]);assert.deepEqual(recipient.errors,[]);assert.deepEqual(offline.errors,[]);assert.deepEqual(withAnswers.errors,[]);
  for(const w of windows)w.close();
  console.log('Passed: 79 questions, 20 sets, source inventory, answers, filters, chapter-isolated storage, sampling, share links, and standalone homework exports.');
})().catch(error=>{for(const w of windows)w.close();console.error(error);process.exitCode=1;});
