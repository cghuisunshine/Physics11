/* Homework selection, share links, offline exports, and source fidelity.
   Requires jsdom >= 26; PHYSICS_JSDOM_PATH can point to an installation. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const {createHash}=require('node:crypto');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'bc-kinematics-questions.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/bc-kinematics-questions.json'),'utf8'));
const windows=[];
function page(source=html,{url='https://cghuisunshine.github.io/Physics11/bc-kinematics-questions.html',storage={},blockedStorage=false,fetch=null}={}){
  const errors=[],virtualConsole=new VirtualConsole(),downloads=[],copied=[],printed=[];
  virtualConsole.on('jsdomError',error=>errors.push(error));
  const dom=new JSDOM(source,{url,runScripts:'dangerously',virtualConsole,beforeParse(w){
    w.print=()=>printed.push(true);
    Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async text=>copied.push(text)}});
    w.URL.createObjectURL=blob=>{downloads.push(blob);return 'blob:homework';};w.URL.revokeObjectURL=()=>{};
    w.HTMLAnchorElement.prototype.click=function(){w.__downloadName=this.download;};
    for(const [key,value] of Object.entries(storage))w.localStorage.setItem(key,value);
    if(blockedStorage)Object.defineProperty(w,'localStorage',{get(){throw Error('storage blocked');}});
    if(fetch){
      w.fetch=fetch;
      w.Image=class{constructor(){this.width=600;this.height=400;}set src(value){this.source=value;if(value)queueMicrotask(()=>this.onload?.());}};
      w.HTMLCanvasElement.prototype.getContext=()=>({fillRect(){},fillText(){},drawImage(){}});
      w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/jpeg;base64,dGVzdA==';
    }
  }});
  windows.push(dom.window);
  return {dom,w:dom.window,d:dom.window.document,errors,downloads,copied,printed,$:id=>dom.window.document.getElementById(id)};
}
const pause=()=>new Promise(resolve=>setTimeout(resolve,10));
function select(p,id,value=true){const input=p.d.querySelector(`input[data-homework="${id}"]`);input.checked=value;input.dispatchEvent(new p.w.Event('change'));}
function edit(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
function filter(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
const visible=p=>[...p.d.querySelectorAll('.question')].filter(q=>!q.hidden).map(q=>q.id);
function blobText(p,blob){return new Promise((resolve,reject)=>{const reader=new p.w.FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsText(blob);});}

(async()=>{
  const p=page();assert.deepEqual(p.errors,[]);assert.equal(visible(p).length,101);
  assert.ok(p.$('homework-panel').hidden);p.$('create-homework').click();assert.ok(!p.$('homework-panel').hidden);
  assert.ok(p.$('download-homework').disabled,'Empty selections cannot be exported');
  // Include a shared graph, investigation procedure, and the recently cropped graph.
  select(p,'q-40');select(p,'q-15');select(p,'q-99');
  assert.match(p.$('homework-count').textContent,/3 questions/);
  edit(p,'homework-name','October homework <practice>');edit(p,'homework-instructions','Show all steps.\nInclude units & directions.');
  p.$('preview-homework').click();assert.deepEqual(visible(p),['q-15','q-40','q-99']);
  assert.equal(p.$('homework-title').textContent,'October homework <practice>');
  const procedure=p.$('q-15').closest('.question-set').querySelector('.context');assert.ok(procedure.open,'Investigation context opens in homework view');
  assert.ok(p.$('q-40').closest('.question-set').querySelector('.shared'),'Shared graphs remain available');
  assert.equal(p.d.body.dataset.homeworkAnswers,'false');
  p.$('copy-homework').click();await pause();assert.equal(p.copied.length,1);
  const link=new URL(p.copied[0]);assert.equal(link.searchParams.get('homework'),'q-15,q-40,q-99');
  assert.equal(link.searchParams.get('title'),'October homework <practice>');assert.equal(link.searchParams.get('answers'),null);
  const recipient=page(html,{url:link.href});assert.deepEqual(visible(recipient),['q-15','q-40','q-99']);
  assert.ok(recipient.$('homework-panel').hidden);assert.equal(recipient.$('homework-title').textContent,p.$('homework-name').value);
  assert.equal(recipient.$('homework-directions').textContent,p.$('homework-instructions').value);
  assert.equal(recipient.d.querySelectorAll('practice').length,0,'Homework title is plain text, never HTML');
  recipient.$('reset').click();assert.deepEqual(visible(recipient),['q-15','q-40','q-99'],'Clear filters preserves the assignment');
  // A download contains exactly the assigned questions, needed context, and no model answers.
  p.$('download-homework').click();assert.equal(p.downloads.length,1);
  const exportHTML=await blobText(p,p.downloads[0]),offline=page(exportHTML);
  assert.deepEqual([...offline.d.querySelectorAll('.question')].map(q=>q.id),['q-15','q-40','q-99']);
  assert.equal(offline.d.querySelectorAll('.answer,.answer-toggle').length,0);
  assert.equal(offline.d.querySelectorAll('script[src],img:not([src^="data:image/"])').length,0,'Homework downloads are standalone');
  assert.ok(offline.d.querySelector('.shared img'));assert.ok(offline.d.querySelector('.context[open] img'));
  assert.equal(offline.d.querySelectorAll('[data-homework],[data-complete]').length,0,'Teacher and collection progress controls are omitted');
  assert.equal(offline.d.querySelectorAll('[data-edit-selection]').length,0,'Offline homework omits the teacher selection button');
  assert.equal(offline.d.querySelector('h1').textContent,'October homework <practice>');
  assert.equal(offline.d.querySelector('#homework-directions').textContent,p.$('homework-instructions').value);
  const digest=text=>createHash('sha256').update(text).digest('hex');
  for(const id of ['q-15','q-40','q-99'])assert.equal(digest(offline.$(id).querySelector('.question-image').innerHTML),digest(p.$(id).querySelector('.question-image').innerHTML.replaceAll('loading="lazy"','loading="eager"')),'Question images are preserved');
  const css=[...offline.d.querySelectorAll('style')].map(s=>s.textContent).join('\n');assert.match(css,/\.homework-export \.context\{display:block\}/,'Procedures are included in print styles');
  assert.equal(p.w.__downloadName,'October-homework-practice.html');
  // Teachers can choose to include worked answers; they remain individually revealable.
  p.$('homework-answers').checked=true;p.$('homework-answers').dispatchEvent(new p.w.Event('input'));
  p.$('download-homework').click();const withAnswers=page(await blobText(p,p.downloads[1]));
  assert.equal(withAnswers.d.querySelectorAll('.answer').length,3);
  const toggle=withAnswers.d.querySelector('.answer-toggle'),answer=withAnswers.$(toggle.getAttribute('aria-controls'));
  assert.ok(answer.hidden);toggle.click();assert.ok(!answer.hidden);
  p.$('copy-homework').click();await pause();assert.equal(new URL(p.copied[1]).searchParams.get('answers'),'1');
  p.$('print-homework').click();await pause();assert.equal(p.printed.length,1);assert.deepEqual(visible(p),['q-15','q-40','q-99']);
  // Selection survives filtering/reload and stays independent of completion marks.
  p.$('all-questions').click();filter(p,'kind','Extra practice');
  const extra=visible(p);assert.equal(extra.length,15);p.$('select-shown').click();assert.match(p.$('homework-count').textContent,/17 questions/);
  const done=p.d.querySelector('[data-complete="q-99"]');done.checked=true;done.dispatchEvent(new p.w.Event('change'));
  const storage=Object.fromEntries(Object.keys(p.w.localStorage).map(k=>[k,p.w.localStorage.getItem(k)]));
  const restored=page(html,{storage});restored.$('create-homework').click();assert.match(restored.$('homework-count').textContent,/17 questions/);
  assert.equal(restored.$('homework-name').value,'October homework <practice>');assert.ok(restored.d.querySelector('[data-complete="q-99"]').checked);
  restored.$('clear-selection').click();assert.match(restored.$('homework-count').textContent,/0 questions/);assert.equal(visible(restored).length,101);
  assert.ok(restored.d.querySelector('[data-complete="q-99"]').checked,'Clearing homework does not clear completed work');
  // Percentages apply separately to each section, using original textbook numbers.
  const sampling=page();sampling.$('create-homework').click();
  const selectedIds=()=>[...sampling.d.querySelectorAll('[data-homework]')].filter(input=>input.checked).map(input=>input.dataset.homework);
  const ratio=section=>sampling.d.querySelector(`[data-section-percent="${section}"]`);
  const setRatio=(section,value)=>{ratio(section).value=String(value);ratio(section).dispatchEvent(new sampling.w.Event('input'));};
  const topics=[...new Set(inventory.groups.map(group=>group.topic))];
  assert.equal(sampling.d.querySelectorAll('[data-section-percent]').length,topics.length);
  sampling.w.Math.random=()=>0.37;
  sampling.$('apply-section-percentages').click();
  for(const section of topics){
    const candidates=inventory.groups.filter(g=>g.topic===section).flatMap(g=>g.questions);
    assert.equal(candidates.filter(q=>selectedIds().includes(q.id)).length,Math.ceil(candidates.length/2),'Random sampling honors each section percentage');
  }
  assert.equal(new Set(selectedIds()).size,selectedIds().length);
  for(const value of ['-1','101','25.5','']){setRatio('2.1',value);assert.ok(sampling.$('apply-section-percentages').disabled);}
  edit(sampling,'homework-all-percent','100');sampling.$('set-section-percentages').click();
  edit(sampling,'homework-parity','odd');sampling.$('apply-section-percentages').click();
  const numbered=inventory.groups.flatMap(g=>g.questions).filter(q=>/^\d+$/.test(q.label));
  assert.deepEqual(selectedIds(),numbered.filter(q=>Number(q.label)%2===1).map(q=>q.id),'Odd uses textbook labels, not collection IDs or sample suffixes');
  edit(sampling,'homework-parity','even');sampling.$('apply-section-percentages').click();
  assert.deepEqual(selectedIds(),numbered.filter(q=>Number(q.label)%2===0).map(q=>q.id));
  // Zero and partial ratios; a preview never shrinks the sampling population.
  sampling.$('clear-selection').click();select(sampling,'q-99');select(sampling,'q-3');sampling.$('preview-homework').click();
  filter(sampling,'topic','2.1');edit(sampling,'homework-parity','all');edit(sampling,'homework-sampling-order','first');
  setRatio('2.1',25);sampling.$('apply-section-percentages').click();
  assert.deepEqual(selectedIds(),['q-1','q-2','q-3','q-4','q-5','q-6','q-7','q-99'],'Quarter of 26 rounds up to 7, preserving selections outside filters');
  assert.deepEqual(visible(sampling),['q-1','q-2','q-3','q-4','q-5','q-6','q-7']);
  assert.equal(new URL(sampling.w.location.href).searchParams.get('homework'),selectedIds().join(','),'Preview URL updates after sampling');
  setRatio('2.1',0);sampling.$('apply-section-percentages').click();assert.deepEqual(selectedIds(),['q-99']);
  // Type/search filters and additive parity selection retain prior questions.
  sampling.$('all-questions').click();filter(sampling,'topic','2.1');filter(sampling,'kind','Practice');
  edit(sampling,'homework-parity','even');sampling.$('select-matching-numbers').click();assert.deepEqual(selectedIds(),['q-4','q-13','q-99']);
  filter(sampling,'search','graphically');setRatio('2.1',100);sampling.$('apply-section-percentages').click();assert.deepEqual(selectedIds(),['q-4','q-13','q-99']);
  assert.match(ratio('2.1').closest('tr').textContent,/1 of 1 eligible/);
  filter(sampling,'search','this search cannot match');assert.ok(sampling.$('apply-section-percentages').disabled);assert.ok(sampling.$('select-matching-numbers').disabled);
  const samplingStorage=Object.fromEntries(Object.keys(sampling.w.localStorage).map(k=>[k,sampling.w.localStorage.getItem(k)]));
  const samplingRestored=page(html,{storage:samplingStorage});
  assert.equal(samplingRestored.$('homework-parity').value,'even');assert.equal(samplingRestored.$('homework-sampling-order').value,'first');
  assert.equal(samplingRestored.d.querySelector('[data-section-percent="2.1"]').value,'100');
  assert.ok(samplingRestored.d.querySelector('[data-homework="q-99"]').checked);
  sampling.$('copy-homework').click();await pause();
  assert.equal(new URL(sampling.copied[0]).searchParams.get('homework'),'q-4,q-13,q-99','Sharing stores selected IDs, not a changing sampling rule');
  sampling.$('preview-homework').click();sampling.$('create-homework').click();
  assert.ok(sampling.$('homework-panel').hidden);
  sampling.$('homework-banner').querySelector('[data-edit-selection]').click();
  assert.ok(!sampling.$('homework-panel').hidden);assert.equal(visible(sampling).length,101);
  assert.equal(sampling.$('search').value,'');assert.equal(sampling.$('topic').value,'');assert.equal(sampling.$('kind').value,'');
  assert.deepEqual(selectedIds(),['q-4','q-13','q-99'],'Adjusting preserves automatic selection');
  assert.equal(sampling.d.activeElement.dataset.homework,'q-4');
  select(sampling,'q-13',false);select(sampling,'q-1');
  assert.deepEqual(selectedIds(),['q-1','q-4','q-99'],'Manual additions and removals override the automatic selection');
  assert.equal(sampling.$('q-4').dataset.homework,'true');assert.equal(sampling.$('q-13').dataset.homework,'false');
  sampling.$('preview-homework').click();assert.deepEqual(visible(sampling),['q-1','q-4','q-99']);
  sampling.$('copy-homework').click();await pause();assert.equal(new URL(sampling.copied[1]).searchParams.get('homework'),'q-1,q-4,q-99');
  // Real AI request/response protocol with deterministic network and canvas fixtures.
  const aiCalls=[];let aiFailure=false,aiPending=false,lateResponse;
  const ai=page(html,{fetch:async(url,options)=>{
    const body=JSON.parse(options.body),questions=JSON.parse(body.message.split('ELIGIBLE QUESTIONS:\n')[1]);
    const amount=Number(body.message.match(/Choose the (\d+)/)[1]);
    aiCalls.push({url,options,body,questions,amount});
    assert.ok(body.image);assert.equal(body.mime_type,'image/jpeg');
    assert.ok(questions.every(q=>q.question_text&&q.worked_solution&&q.set&&q.number));
    const selected=questions.slice(-amount).reverse().map(q=>({id:q.id,reason:'Multiple connected steps <test>.'}));
    if(aiPending)return new Promise(resolve=>{lateResponse=()=>resolve({ok:true,json:async()=>({response:JSON.stringify({selected})})});});
    if(aiFailure==='http')return {ok:false,status:503};
    if(aiFailure==='network')throw new TypeError('Network unavailable');
    if(aiFailure&&aiCalls.length%2===0)return {ok:true,json:async()=>({selected:[{id:'q-999',reason:'Invalid'}]})};
    return {ok:true,json:async()=>({response:'```json\n'+JSON.stringify({selected})+'\n```'})};
  }});
  ai.$('create-homework').click();select(ai,'q-99');select(ai,'q-4');filter(ai,'kind','Practice');
  for(const input of ai.d.querySelectorAll('[data-section-percent]')){input.value=['2.1','2.3'].includes(input.dataset.sectionPercent)?'50':'0';input.dispatchEvent(new ai.w.Event('input'));}
  edit(ai,'homework-sampling-order','ai');assert.ok(!ai.$('homework-ai-help').hidden);
  const aiSelected=()=>[...ai.d.querySelectorAll('[data-homework]')].filter(input=>input.checked).map(input=>input.dataset.homework);
  await ai.$('apply-section-percentages').onclick();
  assert.equal(aiCalls.length,2);assert.equal(aiCalls[0].url,'https://lakesideart.gochatus.org/grade-service/general');
  assert.deepEqual(aiCalls.map(call=>call.amount),[3,1]);
  assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-41','q-99'],'AI selects exact section counts, keeping questions outside filters');
  assert.equal(ai.$('homework-ai-list').children.length,4);assert.equal(ai.$('homework-ai-list').querySelector('test'),null,'AI reasons are plain text');
  assert.match(ai.$('homework-ai-status').textContent,/AI selected the hardest/);
  ai.$('copy-homework').click();await pause();assert.equal(new URL(ai.copied[0]).searchParams.get('homework'),'q-12,q-13,q-14,q-41,q-99');
  select(ai,'q-41',false);select(ai,'q-40');assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-40','q-99']);
  assert.ok(ai.$('homework-ai-results').hidden,'Manual changes clear stale AI explanations');assert.equal(ai.$('homework-ai-status').textContent,'');
  select(ai,'q-40',false);select(ai,'q-41');
  aiFailure=true;await ai.$('apply-section-percentages').onclick();
  assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-41','q-99'],'A later section failure cannot partially replace homework');
  assert.match(ai.$('homework-ai-status').textContent,/invalid selection/);
  for(const failure of ['http','network']){
    aiFailure=failure;await ai.$('apply-section-percentages').onclick();
    assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-41','q-99']);assert.match(ai.$('homework-ai-status').textContent,/unchanged/);assert.ok(!ai.$('apply-section-percentages').disabled);
  }
  const parse=ai.w.HomeworkDifficultyAI.parse,candidates=[ai.$('q-40'),ai.$('q-41')];
  for(const bad of [{selected:[]},{selected:[{id:'q-999',reason:'wrong'}]},{selected:[{id:'q-40',reason:''}]},{selected:[{id:'q-40',reason:'a'},{id:'q-40',reason:'b'}]}])assert.throws(()=>parse(bad,candidates,bad.selected.length===2?2:1));
  assert.throws(()=>parse({ok:false},candidates,1));assert.throws(()=>parse({response:'not JSON'},candidates,1));
  aiFailure=false;aiPending=true;const pending=ai.$('apply-section-percentages').onclick();await pause();
  assert.ok(ai.$('apply-section-percentages').disabled);assert.ok(!ai.$('cancel-homework-ai').hidden);
  ai.$('cancel-homework-ai').click();assert.ok(ai.$('cancel-homework-ai').hidden);lateResponse();await pending;
  assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-41','q-99'],'Canceled responses cannot alter selection');
  const changedRequest=ai.$('apply-section-percentages').onclick();await pause();edit(ai,'homework-parity','even');lateResponse();await changedRequest;
  assert.deepEqual(aiSelected(),['q-12','q-13','q-14','q-41','q-99'],'Changing number choice cancels stale AI results');
  aiPending=false;Object.defineProperty(ai.w.navigator,'onLine',{value:false,configurable:true});
  edit(ai,'homework-parity','all');await ai.$('apply-section-percentages').onclick();assert.match(ai.$('homework-ai-status').textContent,/internet connection/);
  edit(ai,'homework-all-percent','100');ai.$('set-section-percentages').click();const beforeAll=aiCalls.length;
  await ai.$('apply-section-percentages').onclick();assert.equal(aiCalls.length,beforeAll,'100% works offline without AI requests');
  assert.ok(ai.$('homework-ai-help').hidden===false);assert.match(ai.$('homework-ai-status').textContent,/ranking was not needed/);
  assert.deepEqual(aiSelected(),inventory.groups.filter(g=>g.kind==='Practice').flatMap(g=>g.questions.map(q=>q.id)).concat('q-99'));
  edit(ai,'homework-all-percent','0');ai.$('set-section-percentages').click();await ai.$('apply-section-percentages').onclick();assert.equal(aiCalls.length,beforeAll);assert.deepEqual(aiSelected(),['q-99'],'Zero percent also works offline and keeps selections outside filters');
  const aiStorage=Object.fromEntries(Object.keys(ai.w.localStorage).map(k=>[k,ai.w.localStorage.getItem(k)])),aiRestored=page(html,{storage:aiStorage});
  assert.equal(aiRestored.$('homework-sampling-order').value,'ai');
  // Local files generate hosted links; offline students can instead use the downloaded HTML.
  const local=page(html,{url:'file:///tmp/bc-kinematics-questions.html',blockedStorage:true});local.$('create-homework').click();select(local,'q-99');local.$('copy-homework').click();await pause();
  assert.equal(new URL(local.copied[0]).origin,'https://cghuisunshine.github.io');
  const invalid=page(html,{url:'https://physics.test/bc-kinematics-questions.html?homework=bad,q-999',storage});
  assert.equal(visible(invalid).length,0,'Invalid assignment IDs cannot expose a saved teacher selection');assert.ok(!invalid.$('empty').hidden);
  const duplicate=page(html,{url:'https://physics.test/bc-kinematics-questions.html?homework=q-99,q-99,q-999'});assert.deepEqual(visible(duplicate),['q-99']);
  p.w.navigator.clipboard.writeText=async()=>{throw Error('Clipboard unavailable');};p.$('copy-homework').click();await pause();assert.ok(!p.$('homework-link-row').hidden);assert.match(p.$('homework-message').textContent,/Select and copy/);
  // Existing collections retain all answers and stable IDs for the practice studio.
  for(const group of inventory.groups)for(const question of group.questions){
    assert.ok(p.$(question.id));
    const reference=new p.w.DOMParser().parseFromString('<div><h3>Answer</h3>'+question.answer_html+'</div>','text/html').body.firstChild.innerHTML;
    assert.equal(digest(p.$('answer-'+question.id).innerHTML),digest(reference),'Source answer preserved for '+question.id);
  }
  for(const w of windows)w.close();
  for(const instance of [p,recipient,offline,withAnswers,restored,sampling,samplingRestored,ai,aiRestored,local,invalid,duplicate])assert.deepEqual(instance.errors,[]);
  console.log('Passed: AI difficulty selection/counts/reasons, response validation, atomic failures, cancellation/stale responses, offline 0/100%, section percentages/random sampling, textbook odd/even numbers, filtered and preview sampling, validation/rounding, saved settings, homework selection/filtering, draft persistence, shared links, standalone downloads, optional answers, required graphs/procedures, print flow, invalid IDs, offline/storage/clipboard fallback, and all 101 source questions.');
})().catch(error=>{for(const w of windows)w.close();console.error(error);process.exit(1);});
