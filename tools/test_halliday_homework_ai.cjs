/* Custom AI criteria: request contract, matching limits, drafts and cancellation.
   Uses deterministic service/image fixtures; never calls the online AI service. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'halliday-motion-questions.html'),'utf8');
const windows=[],calls=[];let mode='match',lateResponse;
function page(storage={}){
  const errors=[],copied=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
  const dom=new JSDOM(html,{url:'https://example.test/halliday-motion-questions.html',runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
    w.print=()=>{};for(const [k,v] of Object.entries(storage))w.localStorage.setItem(k,v);
    Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async value=>copied.push(value)}});
    w.Image=class{constructor(){this.width=600;this.height=400;}set src(v){if(v)queueMicrotask(()=>this.onload?.());}};
    w.HTMLCanvasElement.prototype.getContext=()=>({fillRect(){},fillText(){},drawImage(){}});
    w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/jpeg;base64,dGVzdA==';
    w.fetch=async(url,options)=>{
      const body=JSON.parse(options.body),questions=JSON.parse(body.message.split('ELIGIBLE QUESTIONS:\n')[1]);
      const amount=Number(body.message.match(/(?:Choose (?:up to|the)|Return at most) (\d+)/)[1]);
      calls.push({url,options,body,questions,amount});
      assert.equal(url,'https://lakesideart.gochatus.org/grade-service/general');
      assert.ok(body.image);assert.equal(body.mime_type,'image/jpeg');
      let selected=questions.slice(0,mode==='default'?amount:Math.min(2,amount)).map(q=>({id:q.id,reason:'Matches the requested skills <tag>.'}));
      if(mode==='none')selected=[];
      if(mode==='invalid')selected=[{id:'q-999',reason:'Invalid ID'}];
      if(mode==='pending')return new Promise(resolve=>{lateResponse=()=>resolve({ok:true,json:async()=>({selected})});});
      if(mode==='network')throw new TypeError('Offline');
      return {ok:true,json:async()=>({response:JSON.stringify({selected})})};
    };
  }});
  windows.push(dom.window);return {w:dom.window,d:dom.window.document,$:id=>dom.window.document.getElementById(id),errors,copied};
}
function edit(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
function select(p,id){const c=p.d.querySelector('[data-homework="'+id+'"]');c.checked=true;c.dispatchEvent(new p.w.Event('change'));}
const selected=p=>[...p.d.querySelectorAll('[data-homework]:checked')].map(c=>c.dataset.homework);
const tick=()=>new Promise(resolve=>setTimeout(resolve,10));
(async()=>{
  const p=page();p.$('create-homework').click();
  assert.equal(p.$('choose-hardest-ai'),null,'Only one section selection action is rendered');
  assert.equal(p.$('apply-section-percentages').textContent,'Choose random questions');
  edit(p,'homework-sampling-order','first');assert.equal(p.$('apply-section-percentages').textContent,'Choose first questions');
  edit(p,'homework-sampling-order','ai');assert.equal(p.$('apply-section-percentages').textContent,'AI: choose questions');
  edit(p,'homework-sampling-order','random');select(p,'q-141');select(p,'q-66');
  edit(p,'topic','2-5');edit(p,'kind','Problem');edit(p,'homework-parity','odd');
  for(const c of p.d.querySelectorAll('[data-section-percent]'))edit(p,c.id,c.dataset.sectionPercent==='2-5'?'100':'0');
  const criteria='Choose free-fall questions with two steps. Avoid calculus.\nPrefer beginner questions.';
  edit(p,'homework-ai-prompt',criteria);assert.equal(p.$('homework-sampling-order').value,'ai');
  assert.match(p.d.querySelector('[data-section-percent="2-5"]').closest('tr').textContent,/Up to 10 of 10/);
  await p.$('apply-section-percentages').onclick();
  assert.equal(calls.length,1,'Custom criteria still call AI at 100%');
  assert.match(calls[0].body.message,/TEACHER SELECTION CRITERIA/);
  assert.ok(calls[0].body.message.includes(JSON.stringify(criteria)));
  assert.match(calls[0].body.message,/do not fill the quota with nonmatching questions/);
  assert.ok(calls[0].questions.every(q=>Number(q.number.replace('Question ',''))%2===1));
  assert.deepEqual(selected(p),['q-67','q-69','q-141'],'Fewer matches replace filtered homework and preserve other sections');
  assert.match(p.$('homework-ai-status').textContent,/matching your criteria/);
  assert.equal(p.$('homework-ai-list').querySelector('tag'),null,'Reasons render as text');
  p.$('copy-homework').click();await tick();
  const link=new URL(p.copied[0]);
  assert.equal(link.searchParams.get('homework'),'q-67,q-69,q-141');
  assert.ok(!link.searchParams.has('aiPrompt')&&!link.searchParams.has('criteria'));
  assert.ok(!link.href.includes(encodeURIComponent(criteria)),'Selection criteria stay out of student links');
  const stored=Object.fromEntries(Object.keys(p.w.localStorage).map(k=>[k,p.w.localStorage.getItem(k)]));
  const restored=page(stored);assert.equal(restored.$('homework-ai-prompt').value,criteria);assert.equal(restored.$('homework-sampling-order').value,'ai');
  restored.w.close();
  for(const failure of ['invalid','network']){
    mode=failure;await p.$('apply-section-percentages').onclick();assert.deepEqual(selected(p),['q-67','q-69','q-141']);assert.match(p.$('homework-ai-status').textContent,/unchanged/);
  }
  const parse=p.w.HomeworkDifficultyAI.parse,candidates=[p.$('q-67'),p.$('q-69')];
  assert.equal(parse({selected:[]},candidates,2,{allowFewer:true}).length,0);
  assert.throws(()=>parse({selected:[]},candidates,2),'Blank criteria still require an exact count');
  assert.throws(()=>parse({selected:[{id:'q-67',reason:'a'},{id:'q-69',reason:'b'}]},candidates,1,{allowFewer:true}));
  assert.throws(()=>parse({selected:[{id:'q-67',reason:'a'},{id:'q-67',reason:'b'}]},candidates,2,{allowFewer:true}));
  mode='pending';const pending=p.$('apply-section-percentages').onclick();await tick();const signal=calls.at(-1).options.signal;
  edit(p,'homework-ai-prompt','Choose only graph interpretation questions.');
  assert.ok(signal.aborted,'Editing criteria cancels pending selection');lateResponse();await pending;
  assert.deepEqual(selected(p),['q-67','q-69','q-141'],'Stale results cannot change homework');
  assert.ok(p.$('homework-ai-results').hidden);
  mode='none';await p.$('apply-section-percentages').onclick();assert.deepEqual(selected(p),['q-141']);assert.match(p.$('homework-ai-status').textContent,/no eligible questions matching your criteria/);
  const beforeZero=calls.length;edit(p,p.d.querySelector('[data-section-percent="2-5"]').id,'0');await p.$('apply-section-percentages').onclick();
  assert.equal(calls.length,beforeZero,'Zero percent makes no AI requests');
  edit(p,p.d.querySelector('[data-section-percent="2-5"]').id,'50');edit(p,'homework-ai-prompt','');mode='default';
  await p.$('apply-section-percentages').onclick();assert.match(calls.at(-1).body.message,/Choose the 5 most difficult/);assert.equal(selected(p).length,6);
  edit(p,p.d.querySelector('[data-section-percent="2-5"]').id,'100');const beforeFull=calls.length;
  Object.defineProperty(p.w.navigator,'onLine',{value:false,configurable:true});await p.$('apply-section-percentages').onclick();
  assert.equal(calls.length,beforeFull,'Blank criteria keep offline 100% selection');
  edit(p,'homework-ai-prompt','Choose graph questions');await p.$('apply-section-percentages').onclick();assert.equal(calls.length,beforeFull);assert.match(p.$('homework-ai-status').textContent,/internet connection/);
  const r=page();r.$('create-homework').click();
  assert.equal(typeof r.$('refine-homework-ai').onclick,'function','Generated page must include the filtering handler');
  for(const id of ['q-67','q-69','q-141'])select(r,id);
  edit(r,'homework-refine-prompt','Remove questions requiring calculus; keep at most two questions across the whole homework.');
  edit(r,'search','no matching search text');for(const input of r.d.querySelectorAll('[data-section-percent]'))edit(r,input.id,'0');
  mode='match';const beforeRefine=calls.length;await r.$('refine-homework-ai').onclick();
  assert.equal(calls.length,beforeRefine+1,'Refinement evaluates the whole selection in one request');
  assert.deepEqual(calls.at(-1).questions.map(q=>q.id),['q-67','q-69','q-141'],'Candidates are only the current selection, independent of browse filters and percentages');
  assert.match(calls.at(-1).body.message,/questions to KEEP/);assert.match(calls.at(-1).body.message,/remove, exclude, drop, or filter out/);assert.match(calls.at(-1).body.message,/across the whole collection/);
  assert.deepEqual(selected(r),['q-67','q-69']);assert.equal(r.$('q-141').hidden,true,'Removed question disappears from homework');
  assert.equal(r.d.querySelectorAll('.question:not([hidden])').length,2,'Only retained questions are displayed');
  assert.match(r.$('homework-refine-status').textContent,/kept 2 of 3.*removed 1/);assert.equal(r.$('homework-refine-list').children.length,2);
  const refineDraft=JSON.parse(r.w.localStorage.getItem('halliday-physics-ch2-homework'));assert.equal(refineDraft.refinePrompt,r.$('homework-refine-prompt').value);
  r.$('copy-homework').click();await tick();assert.ok(!r.copied.at(-1).includes('refinePrompt'));
  for(const failure of ['invalid','network']){mode=failure;await r.$('refine-homework-ai').onclick();assert.deepEqual(selected(r),['q-67','q-69']);assert.match(r.$('homework-refine-status').textContent,/unchanged/);}
  mode='pending';const refining=r.$('refine-homework-ai').onclick();await tick();const refineSignal=calls.at(-1).options.signal;
  assert.equal(r.$('cancel-homework-refine').hidden,false);assert.match(r.$('refine-homework-ai').textContent,/filtering/);
  edit(r,'homework-refine-prompt','Keep graph questions only');assert.ok(refineSignal.aborted);lateResponse();await refining;
  assert.deepEqual(selected(r),['q-67','q-69'],'Changing refinement criteria cancels stale results');
  mode='none';await r.$('refine-homework-ai').onclick();assert.deepEqual(selected(r),[]);assert.equal(r.d.querySelectorAll('.question:not([hidden])').length,0);assert.match(r.$('homework-refine-status').textContent,/selection is now empty/);
  assert.deepEqual(p.errors,[]);assert.deepEqual(r.errors,[]);for(const w of windows)w.close();
  console.log('Passed: custom AI selection and refinement, current-selection scope, global keep/remove instructions, visible filtered results, no matches, persistence, invalid responses, offline behavior, and stale-response cancellation.');
})().catch(e=>{for(const w of windows)w.close();console.error(e);process.exitCode=1;});
