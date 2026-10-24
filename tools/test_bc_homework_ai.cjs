/* Exercise the actual AI request handlers on each BC collection.
   Deterministic network/image fixtures avoid calls to the online service. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),windows=[];
const configs=[['kinematics',2],['forces',3],['newtons-laws',4]];
const tick=()=>new Promise(resolve=>setTimeout(resolve,10));
function edit(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('input'));}
const selected=p=>[...p.d.querySelectorAll('[data-homework]:checked')].map(c=>c.dataset.homework);
function page(file,storage={}){
  const errors=[],calls=[],copied=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
  const p={errors,calls,copied,mode:'match',late:null};
  const dom=new JSDOM(fs.readFileSync(path.join(root,file),'utf8'),{url:'https://physics.test/'+file,runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
    w.print=()=>{};for(const [k,v] of Object.entries(storage))w.localStorage.setItem(k,v);
    Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async value=>copied.push(value)}});
    w.Image=class{constructor(){this.width=600;this.height=400;}set src(value){if(value)queueMicrotask(()=>this.onload?.());}};
    w.HTMLCanvasElement.prototype.getContext=()=>({fillRect(){},fillText(){},drawImage(){}});
    w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/jpeg;base64,dGVzdA==';
    w.fetch=async(url,options)=>{
      const body=JSON.parse(options.body),questions=JSON.parse(body.message.split('ELIGIBLE QUESTIONS:\n')[1]);
      const amount=Number(body.message.match(/(?:Choose (?:up to|the)|Return at most) (\d+)/)[1]);
      calls.push({url,options,body,questions,amount});
      assert.equal(url,'https://lakesideart.gochatus.org/grade-service/general');
      assert.ok(body.image);assert.equal(body.mime_type,'image/jpeg');
      assert.ok(questions.every(q=>q.question_text&&q.worked_solution&&q.set&&q.number));
      let chosen=questions.slice(0,Math.min(2,amount)).map(q=>({id:q.id,reason:'Matches the requested skills <tag>.'}));
      if(p.mode==='none')chosen=[];
      if(p.mode==='invalid')chosen=[{id:'q-999',reason:'Not an eligible ID'}];
      if(p.mode==='network')throw new TypeError('Network unavailable');
      if(p.mode==='pending')return new Promise(resolve=>{p.late=()=>resolve({ok:true,json:async()=>({selected:chosen})});});
      return {ok:true,json:async()=>({response:JSON.stringify({selected:chosen})})};
    };
  }});
  windows.push(dom.window);Object.assign(p,{w:dom.window,d:dom.window.document,$:id=>dom.window.document.getElementById(id)});return p;
}
(async()=>{
  for(const [name,chapter] of configs){
    if(name==='newtons-laws'){
      const multi=page('bc-newtons-laws-questions.html');multi.$('create-homework').click();
      for(const [id,values] of [['topic',['4.1','4.2']],['kind',['Quick check','Practice']]])for(const value of values){
        [...multi.d.querySelectorAll(`[data-filter-option="${id}"]`)].find(input=>input.value===value).click();
      }
      edit(multi,'homework-all-percent','100');multi.$('set-section-percentages').click();edit(multi,'homework-ai-prompt','Find beginner questions.');
      const candidates=[...multi.d.querySelectorAll('.question:not([hidden])')].map(q=>q.id);
      await multi.$('apply-section-percentages').onclick();
      assert.deepEqual(multi.calls.flatMap(call=>call.questions.map(q=>q.id)),candidates,'AI receives all matching sections and types, with no outside questions');
      assert.equal(multi.calls.length,2,'AI applies each selected section percentage');assert.deepEqual(multi.errors,[]);multi.w.close();
    }
    const file='bc-'+name+'-questions.html',p=page(file);p.$('create-homework').click();
    assert.deepEqual(p.errors,[]);assert.equal(p.$('choose-hardest-ai'),null);
    assert.equal(p.$('apply-section-percentages').textContent,'Choose random questions');
    edit(p,'homework-sampling-order','first');assert.equal(p.$('apply-section-percentages').textContent,'Choose first questions');
    const topic=p.$('topic').options[1].value;
    edit(p,'topic',topic);edit(p,'kind','Quick check');edit(p,'homework-parity','odd');
    for(const input of p.d.querySelectorAll('[data-section-percent]'))edit(p,input.id,input.dataset.sectionPercent===topic?'100':'0');
    const candidates=[...p.d.querySelectorAll('.question')].filter(q=>q.closest('.question-set').dataset.topic===topic&&q.closest('.question-set').dataset.kind==='Quick check'&&Number(q.querySelector('.question-top a').textContent.replace('Question ',''))%2===1).map(q=>q.id);
    assert.ok(candidates.length>=2);
    const outside=[...p.d.querySelectorAll('.question')].findLast(q=>q.closest('.question-set').dataset.topic!==topic).id;
    const box=p.d.querySelector('[data-homework="'+outside+'"]');box.checked=true;box.dispatchEvent(new p.w.Event('change'));
    const criteria='Choose beginner questions with two steps.\nAvoid questions with more than two parts.';
    edit(p,'homework-ai-prompt',criteria);assert.equal(p.$('homework-sampling-order').value,'ai');
    assert.equal(p.$('apply-section-percentages').textContent,'AI: choose questions');
    await p.$('apply-section-percentages').onclick();
    assert.equal(p.calls.length,1,'Criteria at 100% still call AI');
    assert.deepEqual(p.calls[0].questions.map(q=>q.id),candidates,'Section, type and textbook parity constrain AI candidates');
    assert.ok(p.calls[0].body.message.includes(JSON.stringify(criteria)));
    assert.match(p.calls[0].body.message,/do not fill the quota with nonmatching questions/);
    const initial=[...candidates.slice(0,2),outside];assert.deepEqual(selected(p),initial);
    assert.equal(p.$('homework-ai-list').querySelector('tag'),null,'AI explanations are plain text');
    assert.equal(typeof p.$('refine-homework-ai').onclick,'function');
    edit(p,'homework-refine-prompt','Remove multi-part questions; keep at most two questions across the whole homework.');
    edit(p,'search','no questions match this phrase');
    for(const input of p.d.querySelectorAll('[data-section-percent]'))edit(p,input.id,'0');
    await p.$('refine-homework-ai').onclick();
    assert.equal(p.calls.length,2,'Refinement makes one request for the whole selection');
    assert.deepEqual(p.calls[1].questions.map(q=>q.id),initial,'Browse filters and percentages do not narrow the current-selection filter');
    assert.match(p.calls[1].body.message,/questions to KEEP/);assert.match(p.calls[1].body.message,/remove, exclude, drop, or filter out/);
    assert.match(p.calls[1].body.message,/across the whole collection/);
    assert.deepEqual(selected(p),candidates.slice(0,2));assert.ok(p.$(outside).hidden);
    assert.equal(p.d.querySelectorAll('.question:not([hidden])').length,2);
    assert.match(p.$('homework-refine-status').textContent,/kept 2 of 3.*removed 1/);
    const storage=Object.fromEntries(Object.keys(p.w.localStorage).map(k=>[k,p.w.localStorage.getItem(k)]));
    const restored=page(file,storage);
    assert.equal(restored.$('homework-ai-prompt').value,criteria);
    assert.equal(restored.$('homework-refine-prompt').value,p.$('homework-refine-prompt').value);
    assert.ok(storage['bc-physics11-ch'+chapter+'-homework']);restored.w.close();
    p.$('copy-homework').click();await tick();const link=new URL(p.copied[0]);
    assert.equal(link.searchParams.get('homework'),candidates.slice(0,2).join(','));assert.equal(link.pathname,'/'+file);
    assert.ok(!link.href.includes('aiPrompt')&&!link.href.includes('refinePrompt'));
    for(const failure of ['invalid','network']){
      p.mode=failure;await p.$('refine-homework-ai').onclick();assert.deepEqual(selected(p),candidates.slice(0,2));
      assert.match(p.$('homework-refine-status').textContent,/unchanged/);
    }
    p.mode='pending';const pending=p.$('refine-homework-ai').onclick();await tick();const signal=p.calls.at(-1).options.signal;
    assert.ok(!p.$('cancel-homework-refine').hidden);p.$('cancel-homework-refine').click();assert.ok(signal.aborted);
    p.late();await pending;assert.deepEqual(selected(p),candidates.slice(0,2),'A canceled result cannot replace the selection');
    p.mode='none';await p.$('refine-homework-ai').onclick();assert.deepEqual(selected(p),[]);
    assert.equal(p.d.querySelectorAll('.question:not([hidden])').length,0);assert.match(p.$('homework-refine-status').textContent,/selection is now empty/);
    assert.deepEqual(p.errors,[]);p.w.close();console.log(file+': passed prompt selection, global current-selection filtering, persistence, share links, failures, cancellation, and empty results.');
  }
  for(const w of windows)w.close();
})().catch(e=>{for(const w of windows)w.close();console.error(e);process.exitCode=1;});
