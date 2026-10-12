/* Functional DOM tests without a browser, network, Firebase, or an AI request.
   Requires jsdom >= 26; PHYSICS_JSDOM_PATH may point to an installation. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {createHash}=require('node:crypto');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'physics-practice.html'),'utf8');
const pause=()=>new Promise(resolve=>setTimeout(resolve,25));
let networkCalls=0;
function page(source=html,{url='https://physics.test/physics-practice.html',storage={},online=false,firebase=null}={}){
  const errors=[],console=new VirtualConsole();console.on('jsdomError',e=>errors.push(e));
  const dom=new JSDOM(source,{url,runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:console,beforeParse(w){
    Object.defineProperty(w.navigator,'onLine',{value:online,writable:true,configurable:true});
    if(firebase)w.firebase=firebase;
    const contexts=new WeakMap();
    w.HTMLCanvasElement.prototype.getContext=function(){
      if(!contexts.has(this)){const data={ink:false,labels:[],getImageData(){return {data:new Uint8ClampedArray(this.ink?[0,0,0,255]:[255,255,255,255])};},fillRect(){this.ink=this.fillStyle!=='#fff';},fill(){this.ink=true;},stroke(){this.ink=true;},drawImage(){this.ink=true;},fillText(label){this.labels.push(label);}};
        contexts.set(this,new Proxy(data,{get:(obj,k)=>k in obj?obj[k]:()=>{},set:(obj,k,v)=>{obj[k]=v;return true;}}));}
      return contexts.get(this);
    };
    w.HTMLCanvasElement.prototype.toDataURL=function(){w.__lastEncodedLabels=this.getContext('2d').labels.slice();return 'data:image/jpeg;base64,YQ==';};
    w.HTMLCanvasElement.prototype.getBoundingClientRect=function(){return {left:0,top:0,width:this.width/2,height:this.height/2,bottom:this.height/2,right:this.width/2};};
    w.HTMLCanvasElement.prototype.setPointerCapture=function(id){this._pointer=id;};
    w.HTMLCanvasElement.prototype.hasPointerCapture=function(id){return this._pointer===id;};
    w.HTMLCanvasElement.prototype.releasePointerCapture=function(){this._pointer=null;};
    w.Image=class{constructor(){this.width=this.naturalWidth=1200;this.height=this.naturalHeight=480;}set src(value){this._src=value;setTimeout(()=>this.onload?.(),0);}get src(){return this._src;}};
    w.HTMLMediaElement.prototype.pause=()=>{};
    w.HTMLElement.prototype.scrollIntoView=()=>{};
    w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};
    w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
    w.fetch=async()=>{networkCalls++;throw Error('Unexpected network request during offline practice');};
    w.prompt=()=>null;w.confirm=()=>true;
    for(const [k,v] of Object.entries(storage))w.localStorage.setItem(k,v);
  }});
  return {dom,w:dom.window,d:dom.window.document,errors,$:id=>dom.window.document.getElementById(id)};
}
function login(p,name){p.$('login-name').value=name;p.$('login-form').dispatchEvent(new p.w.Event('submit',{cancelable:true}));}
function change(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('change'));}
function response(p,value){p.$('response-input').value=value;p.$('response-input').dispatchEvent(new p.w.Event('input'));}
function history(p,name){const saved=JSON.parse(p.w.localStorage.getItem('physics11Practice.v1:'+encodeURIComponent(name.toLowerCase())));return saved?JSON.parse(saved.state):{version:1,attempts:[],items:{}};}
function sameHTML(p,actual,expected,message){
  const normalized=new p.w.DOMParser().parseFromString(expected,'text/html').body.innerHTML;
  const digest=s=>createHash('sha256').update(s).digest('hex');
  assert.equal(digest(actual),digest(normalized),message);
}
function pointer(p,type,x,y,pointerType='pen'){
  const event=new p.w.MouseEvent(type,{clientX:x,clientY:y,button:0,bubbles:true,cancelable:true});
  Object.defineProperties(event,{pointerId:{value:1},isPrimary:{value:true},pointerType:{value:pointerType}});
  p.$('drawing-canvas').dispatchEvent(event);
}
async function until(predicate){for(let i=0;i<80;i++){if(predicate())return;await pause();}throw Error('Timed out waiting for verification');}
function storageOf(p){return Object.fromEntries(Array.from({length:p.w.localStorage.length},(_,i)=>{const k=p.w.localStorage.key(i);return [k,p.w.localStorage.getItem(k)];}));}
function review(verdict='correct',confidence='high'){return {verdict,confidence,feedback:'Comparison completed.',answer_check:'Checked every requested part against the model answer.',steps:[],weak_points:[]};}

(async()=>{
  const p=page();await pause();assert.deepEqual(p.errors,[]);assert.equal(p.$('login-overlay').hidden,false);
  const bank=JSON.parse(p.$('question-bank').textContent),P=p.w.Practice;
  assert.equal(bank.length,301);assert.equal(new Set(bank.map(q=>q.id)).size,301);
  const kinematics=bank.filter(q=>q.chapter==='bc-ch2'),forces=bank.filter(q=>q.chapter==='bc-ch3'),newtons=bank.filter(q=>q.chapter==='bc-ch4');
  assert.equal(kinematics.length,101);assert.equal(forces.length,79);assert.equal(newtons.length,121);
  assert.equal(p.d.querySelectorAll('script[src]').length,0,'No external assets on startup');
  assert.ok(bank.every(q=>q.solution&&q.html.includes('data:image/')));
  assert.ok(bank.some(q=>q.solution.includes('<svg')),'Worked-answer graphs retained');
  login(p,'Ada');change(p,'mode','chapter');await pause();
  assert.equal(p.$('chapter-grid').children.length,101);assert.equal(p.$('chapter-question').options.length,102);
  assert.ok(p.$('solution').hidden);assert.equal(p.$('solution').open,false);assert.equal(p.$('solution-body').childElementCount,0);
  assert.ok(p.$('self-rating').hidden);assert.equal(p.$('rate-correct').onclick() ,undefined);assert.equal(p.$('attempt-count').textContent,'0');
  response(p,'Distance 4 km; displacement 0 km.');await pause();assert.equal(p.$('dock-response').value,p.$('response-input').value);
  p.$('dock-check').click();await pause();assert.equal(p.$('solution').hidden,false);assert.equal(p.$('solution').open,true);assert.equal(p.$('self-rating').hidden,false);
  assert.equal(p.$('attempt-count').textContent,'0','Revealing alone is not a scored attempt');
  p.$('dock-rate-practice').click();await pause();assert.equal(p.$('attempt-count').textContent,'1');assert.equal(p.$('review-count').textContent,'1');
  assert.equal(history(p,'Ada').attempts[0].assessment,'self');assert.equal(history(p,'Ada').attempts[0].choice,'Distance 4 km; displacement 0 km.');
  assert.deepEqual(Object.keys(history(p,'Ada').items[bank[0].id].problem),['id'],'Storage never duplicates images/HTML');
  p.$('chapter-grid').children[0].click();assert.ok(p.$('solution').hidden);assert.equal(p.$('solution-body').childElementCount,0);
  response(p,'4 km travelled, 0 km displacement');p.$('check').click();p.$('rate-correct').click();
  assert.equal(p.$('review-count').textContent,'0','Correct retry clears missed status');
  assert.equal(history(p,'Ada').attempts[1].review,true);assert.match(p.$('accuracy').textContent,/0%/,'Retry does not inflate first-attempt accuracy');
  p.$('flag').click();assert.equal(p.$('review-count').textContent,'1');
  p.$('check').click();assert.equal(history(p,'Ada').attempts.length,2,'Repeated clicks do not record duplicate ratings');
  for(const q of bank){
    if(p.$('practice-chapter').value!==q.chapter)change(p,'practice-chapter',q.chapter);
    change(p,'chapter-question',q.id);assert.equal(p.$('question-title').textContent,q.title);
    sameHTML(p,p.$('statement').innerHTML,q.html,'Exact question and shared context retained for '+q.id);
    assert.ok(p.$('solution').hidden);p.$('check').click();sameHTML(p,p.$('solution-body').innerHTML,q.solution,'Worked solution retained for '+q.id);
  }
  assert.equal(p.$('chapter-grid').children.length,121);assert.equal(p.$('chapter-question').options.length,122);
  assert.ok([...p.$('topic').options].some(o=>o.value==='Ch 4 · 4.4'));
  change(p,'chapter-question',newtons.at(-1).id);p.$('skip').click();assert.equal(p.$('chapter-question').value,newtons[0].id,'Chapter 4 navigation wraps within its 121 questions');
  change(p,'practice-chapter','bc-ch3');
  assert.equal(p.$('chapter-grid').children.length,79);assert.equal(p.$('chapter-question').options.length,80);
  assert.ok([...p.$('topic').options].some(o=>o.value==='Ch 3 · 3.3'));
  change(p,'chapter-question',forces.at(-1).id);p.$('skip').click();assert.equal(p.$('chapter-question').value,forces[0].id,'Forces navigation wraps within its 79 questions');
  change(p,'practice-chapter','bc-ch2');change(p,'chapter-question',bank[0].id);assert.equal(p.$('chapter-previous').disabled,true);
  change(p,'chapter-question',kinematics.at(-1).id);p.$('skip').click();assert.equal(p.$('chapter-question').value,bank[0].id,'Chapter navigation wraps by actual count');
  change(p,'mode','review');assert.equal(p.$('question-title').textContent,bank[0].title);
  change(p,'mode','day');assert.equal(p.$('day-question').options.length,2);p.$('day-exclude-correct').checked=true;p.$('day-exclude-correct').dispatchEvent(new p.w.Event('change'));assert.equal(p.$('day-question').options.length,1);
  p.$('sidebar-toggle').click();assert.equal(p.$('sidebar-body').hidden,false);p.$('question-toggle').click();assert.equal(p.$('question-toggle').getAttribute('aria-expanded'),'false');
  p.$('student-button').click();login(p,'Ben');assert.equal(p.$('attempt-count').textContent,'0');p.$('student-button').click();login(p,'ADA');assert.equal(p.$('student-name-label').textContent,'Ada');assert.equal(p.$('attempt-count').textContent,'2');
  const saved=Object.fromEntries(Array.from({length:p.w.localStorage.length},(_,i)=>{const k=p.w.localStorage.key(i);return [k,p.w.localStorage.getItem(k)];}));
  const restored=page(html,{storage:saved});await pause();assert.deepEqual(restored.errors,[]);assert.equal(restored.$('attempt-count').textContent,'2');assert.ok(restored.$('solution').hidden);
  const shared=page(html,{url:'https://physics.test/physics-practice.html?q='+bank[65].id});login(shared,'Shared');assert.equal(shared.$('question-title').textContent,bank[65].title);assert.ok(shared.$('solution').hidden);
  // A new chapter, different count and new topics, with the same source q-number.
  const forcesShared=page(html,{url:'https://physics.test/physics-practice.html?q='+forces[54].id});login(forcesShared,'Forces link');assert.equal(forcesShared.$('question-title').textContent,forces[54].title);assert.ok(forcesShared.$('solution').hidden);change(forcesShared,'mode','chapter');change(forcesShared,'practice-chapter','bc-ch3');assert.equal(forcesShared.$('chapter-grid').children.length,79);
  const newtonsShared=page(html,{url:'https://physics.test/physics-practice.html?q='+newtons[76].id});login(newtonsShared,'Newton link');assert.equal(newtonsShared.$('question-title').textContent,newtons[76].title);assert.ok(newtonsShared.$('solution').hidden);
  newtonsShared.$('check').click();sameHTML(newtonsShared,newtonsShared.$('solution-body').innerHTML,newtons[76].solution,'Shared Chapter 4 question reveals its own solution');newtonsShared.$('rate-correct').click();assert.equal(history(newtonsShared,'Newton link').attempts[0].id,'bc-ch4-q-77');
  const future=[...bank,...[1,2,3].map(n=>({...bank[0],id:'test-chapter-q-'+n,chapter:'test-chapter',chapterNumber:99,chapterTitle:'Test chapter',number:n,topic:'Ch 99 · Future',title:'Test question '+n}))];
  const futureHTML=html.replace(/(<script id="question-bank"[^>]*>)[\s\S]*?(<\/script>)/,(_,a,b)=>a+JSON.stringify(future).replace(/</g,'\\u003c')+b);
  const f=page(futureHTML);login(f,'Future');change(f,'mode','chapter');change(f,'practice-chapter','test-chapter');assert.equal(f.$('chapter-grid').children.length,3);assert.equal(f.$('chapter-question').options.length,4);assert.match(f.$('reason').textContent,/of 3/);assert.ok([...f.$('topic').options].some(o=>o.value==='Ch 99 · Future'));
  change(f,'chapter-question','test-chapter-q-3');f.$('skip').click();assert.equal(f.$('chapter-question').value,'test-chapter-q-1');
  const empty={version:1,attempts:[],items:{}};
  assert.throws(()=>P.record(empty,bank[0],'answer',1),/Rate your work/);
  P.record(empty,bank[0],'zero metres',40,false);P.record(empty,bank[0],'0 m',20,true);
  assert.equal(P.stats(empty,bank[0].topic).total,1);assert.equal(P.reviewQueue(empty,'').length,0);assert.equal(P.chapterProgress(empty,[bank[0]]).correct,1);
  const compact=JSON.parse(JSON.stringify(P.compact(empty)));compact.items[bank[0].id].problem.html='<script>malicious</script>';
  assert.equal(P.validState(compact,bank),true);assert.equal(P.hydrate(compact,bank).items[bank[0].id].problem.html,bank[0].html,'Imported HTML is discarded');
  compact.attempts[0].id='missing-chapter';assert.equal(P.validState(compact,bank),false);
  assert.ok(P.chooseExam(bank,empty,bank[0].topic,bank[0].id).id!==bank[0].id);assert.ok(P.randomQuestion(bank,empty,'',bank[0].id).id!==bank[0].id);
  assert.deepEqual(JSON.parse(JSON.stringify(p.w.LivePractice.pack(bank[0]))),{q:bank[0].id});assert.equal(p.w.LivePractice.unpack({q:'unknown'},bank),null);
  const AI=p.w.PhotoReview;assert.equal(AI.normalize({verdict:'incorrect',confidence:'low',feedback:'Unreadable',weak_points:[{skill:'Signs',evidence:'Unknown'}]}).weak_points.length,0);
  assert.match(AI.hintPrompt(bank[0],'', 'text','solution',false),/Never state, confirm, or reject a final answer/);
  assert.equal(networkCalls,0,'All core practice works offline without network requests');
  // A pasted sharing URL must never be saved or shared as the Firebase key.
  const key='AIza'+'x'.repeat(35),liveId='a'.repeat(48),keyStorage='physics11FirebaseApiKey';
  const amcLink='https://physics.test/amc8_practice.html?follow='+'b'.repeat(48)+'#liveKey='+key;
  const brokenLink='https://physics.test/physics-practice.html?follow='+liveId+'#'+new URLSearchParams({liveKey:amcLink});
  const nestedLink='https://physics.test/physics-practice.html?follow='+liveId+'#'+new URLSearchParams({liveKey:brokenLink});
  function fakeFirebase(initial={}){
    const initialized=[],writes=[],documents=new Map(Object.entries(initial)),apps=[];
    const db={collection:()=>({doc:id=>({
      async set(data){writes.push({id,data});documents.set(id,data);},
      onSnapshot(...args){const callback=typeof args[0]==='function'?args[0]:args[1];callback({exists:documents.has(id),metadata:{fromCache:false},data:()=>documents.get(id)});return ()=>{};}
    })})};
    return {initialized,writes,apps,initializeApp(config){initialized.push(config.apiKey);const app={name:'[DEFAULT]',delete:async()=>{apps.length=0;}};apps.push(app);return app;},firestore:()=>db};
  }
  const hostFirebase=fakeFirebase(),host=page(html,{storage:{[keyStorage]:amcLink},firebase:hostFirebase});
  const store=host.w.StudentStore;
  assert.equal(store.getApiKey(),key);assert.equal(host.w.localStorage.getItem(keyStorage),key,'Previously saved sharing links are repaired');
  for(const input of [key,' '+key+' ',amcLink,brokenLink,nestedLink,'https://physics.test/?apiKey='+encodeURIComponent(amcLink),'https://physics.test/physics-monitor.html#apiKey='+key])assert.equal(store.normalizeApiKey(input),key);
  for(const input of ['not-a-key','https://physics.test/no-key','https://physics.test/'+key,'javascript:alert(1)','AIza'+'x'.repeat(36)])assert.equal(store.normalizeApiKey(input),'');
  assert.equal(store.setApiKey('not-a-key'),false);assert.equal(store.getApiKey(),key,'Invalid input preserves the saved key');
  host.dom.reconfigure({url:'https://physics.test/physics-practice.html?apiKey='+encodeURIComponent(amcLink)});assert.equal(store.getApiKey(),key);
  host.dom.reconfigure({url:'https://physics.test/physics-practice.html?apiKey=bad'});assert.equal(store.getApiKey(),key,'Invalid URL configuration cannot replace a valid saved key');
  host.dom.reconfigure({url:'https://physics.test/physics-practice.html'});
  host.$('firebase-key').value=amcLink;host.$('sync-enable').click();assert.equal(store.getApiKey(),key);assert.equal(host.$('firebase-key').value,'••••••••');
  host.$('firebase-key').value='bad';host.$('sync-enable').click();assert.match(host.$('sync-status').textContent,/valid Firebase API key/);assert.equal(store.getApiKey(),key);
  login(host,'Host');await until(()=>hostFirebase.initialized.length===1);
  host.$('share-live').click();await until(()=>!!host.$('live-link').value);
  const generated=new URL(host.$('live-link').value);assert.equal(new URLSearchParams(generated.hash.slice(1)).get('liveKey'),key);
  assert.ok(host.w.LivePractice.validId(generated.searchParams.get('follow')));assert.deepEqual(hostFirebase.initialized,[key]);
  assert.throws(()=>host.w.LivePractice.shareURL(generated.href,liveId,amcLink),/invalid-firebase-api-key/);
  assert.equal(new URL(store.shareLink()).searchParams.get('apiKey'),key);
  assert.ok(hostFirebase.writes.some(write=>write.id.startsWith('live-')),'Host publishes a live question');
  const followerFirebase=fakeFirebase({['live-'+liveId]:{kind:'physics11-live',version:1,active:true,revision:1,expiresAt:Date.now()+3600000,question:{q:bank[27].id}}});
  const follower=page(html,{url:brokenLink,firebase:followerFirebase});
  await until(()=>follower.$('live-status').textContent.startsWith('Following live.'));
  assert.equal(follower.$('question-title').textContent,bank[27].title);assert.deepEqual(followerFirebase.initialized,[key]);
  assert.equal(followerFirebase.writes.length,0,'Opening an old malformed link reads the session without writing progress');
  const invalidFollower=page(html,{url:'https://physics.test/physics-practice.html?follow='+liveId+'#liveKey=bad'});
  await until(()=>invalidFollower.$('live-status').textContent.includes('invalid Firebase key'));
  assert.equal(networkCalls,0,'Invalid keys are rejected before loading Firebase');
  assert.equal(store.setApiKey(''),true);assert.equal(store.getApiKey(),'','This device only still clears the key');
  // One shared steps pad supplies handwritten answers alongside typed text.
  const ink=page();login(ink,'Ink');change(ink,'mode','chapter');
  assert.equal(ink.$('answer-tab-handwritten'),null);assert.equal(ink.$('answer-canvas'),null);assert.equal(ink.d.querySelectorAll('canvas').length,1,'Only the shared steps canvas remains');
  pointer(ink,'pointerdown',25,25);pointer(ink,'pointermove',60,40);pointer(ink,'pointerup',60,40);await pause();
  assert.equal(ink.$('drawing-undo').disabled,false);assert.equal(ink.$('drawing-clear').disabled,false);
  ink.$('drawing-undo').click();assert.equal(ink.$('drawing-clear').disabled,true,'Undo removes the handwritten stroke');
  pointer(ink,'pointerdown',40,40,'mouse');pointer(ink,'pointermove',60,40,'mouse');pointer(ink,'pointerup',60,40,'mouse');
  ink.$('drawing-eraser').click();pointer(ink,'pointerdown',40,40);pointer(ink,'pointerup',40,40);assert.equal(ink.$('drawing-clear').disabled,true,'Eraser removes a hit stroke');
  ink.$('drawing-undo').click();assert.equal(ink.$('drawing-clear').disabled,false,'Undo restores an erased answer');
  ink.$('drawing-clear').click();assert.equal(ink.$('drawing-clear').disabled,true);ink.$('drawing-pen').click();
  pointer(ink,'pointerdown',90,40);pointer(ink,'pointermove',110,40);pointer(ink,'pointerup',110,40);
  response(ink,'Optional typed units: m/s');ink.$('drawing-close').click();
  assert.equal(ink.$('drawing-panel').hidden,true);assert.ok(ink.$('solution').hidden);ink.$('check').click();ink.$('rate-correct').click();
  const handAttempt=history(ink,'Ink').attempts[0];assert.equal(handAttempt.answerInputMode,'typed');assert.equal(handAttempt.choice,'Optional typed units: m/s');assert.equal(handAttempt.answerInk.strokes.length,1,'Closed steps pad is included in the submission');
  assert.deepEqual(handAttempt.answerInk.strokes[0].points,[{x:180,y:80},{x:220,y:80}]);assert.equal(ink.$('response-input').readOnly,true);
  ink.$('drawing-open').click();const handSnapshot=JSON.stringify(handAttempt.answerInk);pointer(ink,'pointerdown',200,50);pointer(ink,'pointerup',200,50);assert.equal(JSON.stringify(history(ink,'Ink').attempts[0].answerInk),handSnapshot,'Later steps edits do not change saved submissions');
  const handState=history(ink,'Ink');assert.equal(ink.w.Practice.validState(handState,bank),true);assert.equal(JSON.stringify(ink.w.Practice.hydrate(handState,bank).attempts[0].answerInk),handSnapshot);
  handState.attempts[0].answerInputMode='handwritten';assert.equal(ink.w.Practice.validState(handState,bank),true,'Legacy handwritten backups remain valid');
  handState.attempts[0].answerInk.strokes[0].color='url(malicious)';assert.equal(ink.w.Practice.validState(handState,bank),false,'Invalid imported ink is rejected');
  const requests=[];ink.w.fetch=async(url,options)=>{requests.push({url,body:JSON.parse(options.body)});return {ok:true,json:async()=>({verdict:'correct',confidence:'high',feedback:'Your handwritten answer has the correct units.',steps:[],weak_points:[]})};};
  ink.$('ai-check').click();await pause();await pause();assert.equal(requests.length,1);assert.match(requests[0].body.message,/Show your steps work attached/);assert.match(requests[0].body.message,/Optional typed units: m\/s/);assert.ok(ink.w.__lastEncodedLabels.some(label=>label.includes('STUDENT WORK')),'AI receives labelled steps alongside typed text');assert.equal(history(ink,'Ink').attempts[0].aiReview.verdict,'correct');
  const inkStorage=storageOf(ink);
  const inkReload=page(html,{storage:inkStorage});change(inkReload,'mode','chapter');change(inkReload,'chapter-question',bank[0].id);await pause();
  assert.ok(inkReload.$('solution').hidden);assert.equal(inkReload.$('previous-response').open,false);assert.ok(inkReload.$('previous-response').querySelector('polyline'),'Saved handwriting is reviewable after reload');assert.equal(inkReload.$('drawing-clear').disabled,true,'Retry starts with a fresh shared steps pad');
  // Online Show answer verifies automatically using the pre-reveal submission.
  const auto=page(html,{online:true}),autoRequests=[];login(auto,'Auto');change(auto,'mode','chapter');
  let nextReview=review('incorrect');
  auto.w.fetch=async(url,options)=>{autoRequests.push({url,body:JSON.parse(options.body)});return {ok:true,json:async()=>({response:JSON.stringify(nextReview)})};};
  response(auto,'My original answer');await pause();auto.$('dock-check').click();
  assert.equal(auto.$('solution').open,true);assert.equal(auto.$('self-rating').hidden,true);assert.equal(auto.$('response-input').readOnly,true);
  response(auto,'Edited after seeing solution');await until(()=>history(auto,'Auto').attempts.length===1);
  let a=history(auto,'Auto').attempts[0];assert.equal(a.assessment,'ai');assert.equal(a.choice,'My original answer');assert.equal(a.correct,false);assert.equal(a.answerVerification.verdict,'incorrect');
  assert.match(autoRequests[0].body.message,/MODEL ANSWER/);assert.match(autoRequests[0].body.message,/Reference worked solution/);assert.match(autoRequests[0].body.message,/Student written answer: My original answer/);assert.ok(autoRequests[0].body.image);
  assert.equal(auto.$('review-count').textContent,'1');assert.equal(auto.$('next').hidden,false);auto.$('check').click();auto.$('rate-correct').click();assert.equal(autoRequests.length,1);assert.equal(history(auto,'Auto').attempts.length,1,'Automatic results cannot also be self-rated');
  nextReview=review();change(auto,'chapter-question',bank[0].id);response(auto,'Correct retry');auto.$('check').click();await until(()=>history(auto,'Auto').attempts.length===2);
  assert.equal(auto.$('review-count').textContent,'0');assert.equal(history(auto,'Auto').attempts[1].review,true);assert.match(auto.$('accuracy').textContent,/0%/,'AI retries do not inflate first-attempt accuracy');
  nextReview=review('partly_correct','medium');change(auto,'chapter-question',bank[1].id);response(auto,'Only part a');pointer(auto,'pointerdown',20,25);pointer(auto,'pointerup',20,25);
  auto.w.URL.createObjectURL=()=> 'blob:test-photo';auto.w.URL.revokeObjectURL=()=>{};
  Object.defineProperty(auto.$('photo-file'),'files',{configurable:true,value:[new auto.w.File(['test-photo'],'steps.jpg',{type:'image/jpeg'})]});
  await auto.$('photo-file').onchange({target:auto.$('photo-file')});assert.equal(auto.$('drawing-panel').hidden,true);
  auto.$('check').click();await until(()=>history(auto,'Auto').attempts.length===3);
  a=history(auto,'Auto').attempts[2];assert.equal(a.correct,false);assert.equal(a.answerVerification.verdict,'partly_correct');assert.match(auto.$('feedback').textContent,/Partly correct/);assert.ok(a.answerInk.strokes.length);assert.match(autoRequests.at(-1).body.message,/Student written answer: Only part a/);assert.match(autoRequests.at(-1).body.message,/Combine the student's typed answer/);assert.ok(auto.w.__lastEncodedLabels.some(label=>label.includes('handwritten answer and steps')));assert.ok(auto.w.__lastEncodedLabels.some(label=>label.includes('uploaded photograph')),'Typed text, closed-pad drawing and uploaded photo are combined');
  // A handwritten-only answer is sent under a distinct label and saved with its verdict.
  nextReview=review();change(auto,'chapter-question',bank[2].id);pointer(auto,'pointerdown',20,25);pointer(auto,'pointermove',60,25);pointer(auto,'pointerup',60,25);auto.$('check').click();await until(()=>history(auto,'Auto').attempts.length===4);
  a=history(auto,'Auto').attempts[3];assert.equal(a.choice,'');assert.equal(a.assessment,'ai');assert.ok(a.answerInk.strokes.length);assert.match(autoRequests.at(-1).body.message,/Show your steps work attached/);assert.ok(auto.w.__lastEncodedLabels.some(label=>label.includes('STUDENT WORK')));
  const autoState=history(auto,'Auto');assert.equal(P.validState(autoState,bank),true);autoState.attempts[0].aiReview=review();assert.equal(P.validState(autoState,bank),true,'Later step feedback is separate from the recorded verdict');autoState.attempts[0].answerVerification.verdict='correct';assert.equal(P.validState(autoState,bank),false,'Imported verdict must agree with the recorded score');
  const autoReload=page(html,{storage:storageOf(auto)});await pause();assert.equal(autoReload.$('attempt-count').textContent,'4');assert.equal(history(autoReload,'Auto').attempts[3].answerVerification.verdict,'correct');
  // Uncertain results allow a retry or manual fallback without awarding a score.
  nextReview=review('unreadable','low');change(auto,'chapter-question',bank[3].id);response(auto,'Uncertain original');pointer(auto,'pointerdown',30,20);pointer(auto,'pointerup',30,20);auto.$('check').click();await until(()=>!auto.$('self-rating').hidden&&!auto.$('verify-retry').disabled);
  assert.equal(history(auto,'Auto').attempts.length,4);assert.equal(auto.$('verify-retry').hidden,false);assert.equal(auto.$('solution').open,true);
  response(auto,'Model answer copied after reveal');auto.$('drawing-clear').click();pointer(auto,'pointerdown',90,60);pointer(auto,'pointerup',90,60);nextReview=review();auto.$('dock-verify-retry').click();await until(()=>history(auto,'Auto').attempts.length===5);assert.equal(history(auto,'Auto').attempts[4].choice,'Uncertain original');assert.deepEqual(history(auto,'Auto').attempts[4].answerInk.strokes[0].points,[{x:60,y:40}],'Verification retries preserve the original steps too');assert.match(autoRequests.at(-1).body.message,/Student written answer: Uncertain original/);
  nextReview=review('correct','low');change(auto,'chapter-question',bank[4].id);response(auto,'Low confidence');auto.$('check').click();await until(()=>!auto.$('rate-practice').disabled&&!auto.$('self-rating').hidden);assert.equal(history(auto,'Auto').attempts.length,5);auto.$('rate-practice').click();assert.equal(history(auto,'Auto').attempts[5].assessment,'self');
  // Service failure, empty response and offline conditions preserve the model solution.
  auto.w.fetch=async()=>{throw new auto.w.TypeError('Network unavailable');};change(auto,'chapter-question',bank[5].id);response(auto,'Failed request');auto.$('check').click();await until(()=>!auto.$('self-rating').hidden&&!auto.$('verify-retry').disabled);assert.equal(history(auto,'Auto').attempts.length,6);assert.match(auto.$('feedback').textContent,/Could not reach/);assert.equal(auto.$('solution').open,true);
  auto.w.fetch=async()=>({ok:true,json:async()=>({response:{}})});auto.$('verify-retry').click();await until(()=>!auto.$('verify-retry').disabled);assert.match(auto.$('feedback').textContent,/incomplete review/);assert.equal(history(auto,'Auto').attempts.length,6);
  let unexpected=0;auto.w.fetch=async()=>{unexpected++;throw Error('Must not send');};change(auto,'chapter-question',bank[6].id);auto.$('check').click();await pause();assert.equal(unexpected,0,'Empty submissions do not contact AI');assert.equal(history(auto,'Auto').attempts.length,6);
  auto.w.navigator.onLine=false;change(auto,'chapter-question',bank[7].id);response(auto,'Offline response');auto.$('check').click();assert.equal(unexpected,0);assert.match(auto.$('feedback').textContent,/Offline/);assert.equal(auto.$('self-rating').hidden,false);auto.w.navigator.onLine=true;
  // Cancellation, navigation and student changes ignore even late service responses.
  for(const action of ['cancel','navigate','student']){
    let finish,pending=false;auto.w.fetch=async()=>{pending=true;return new Promise(resolve=>{finish=()=>resolve({ok:true,json:async()=>review()});});};
    change(auto,'chapter-question',bank[8].id);response(auto,'Pending answer');auto.$('check').click();await until(()=>pending);
    assert.equal(auto.$('solution').hidden,false);assert.equal(auto.$('solution').open,true);
    sameHTML(auto,auto.$('solution-body').innerHTML,bank[8].solution,'Full model answer is available while the service is still pending');
    assert.ok(auto.$('solution').compareDocumentPosition(auto.$('feedback'))&auto.w.Node.DOCUMENT_POSITION_FOLLOWING,'Model answer comes before the waiting status');
    assert.equal(auto.$('dock-solution').open,true,'Pinned model answer also opens before the verdict arrives');
    assert.match(auto.$('feedback').textContent,/running in the background/);
    assert.equal(auto.$('rate-correct').disabled,true);
    if(action==='cancel'){auto.$('ai-cancel').click();assert.equal(auto.$('self-rating').hidden,false);assert.equal(auto.$('verify-retry').disabled,false);}
    if(action==='navigate')change(auto,'chapter-question',bank[9].id);
    if(action==='student'){auto.$('student-button').click();login(auto,'Other');}
    finish();await pause();assert.equal(history(auto,'Auto').attempts.length,6,'Late '+action+' result is not recorded');
  }
  // Timeout aborts the request and leaves manual fallback available.
  const timed=page(html,{online:true});login(timed,'Timed');change(timed,'mode','chapter');response(timed,'Timeout answer');
  const originalTimeout=timed.w.setTimeout.bind(timed.w);timed.w.setTimeout=(fn,delay,...args)=>originalTimeout(fn,delay===120000?20:delay,...args);
  timed.w.fetch=async(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new timed.w.DOMException('Aborted','AbortError')),{once:true}));
  timed.$('check').click();await until(()=>!timed.$('self-rating').hidden&&!timed.$('verify-retry').disabled);assert.match(timed.$('feedback').textContent,/timed out/);assert.equal(history(timed,'Timed').attempts.length,0);
  const monitorSource=fs.readFileSync(path.join(root,'physics-monitor.html'),'utf8');
  const m=page(monitorSource,{url:'https://physics.test/physics-monitor.html?student=Ada&period=week&exclude=',storage:saved});await pause();assert.deepEqual(m.errors,[]);assert.equal(m.$('activity-days').children.length,7);assert.match(m.$('activity-status').textContent,/saved on this device/);assert.ok(!m.w.StudentStore,'Monitor has no history-writing store');
  for(const instance of [p,restored,shared,forcesShared,newtonsShared,f,host,follower,invalidFollower,ink,inkReload,auto,autoReload,timed,m]){assert.deepEqual(instance.errors,[]);instance.w.close();}
  console.log('Passed: 301 question/answer pairs, graphs, navigation, student storage, future chapters, handwriting tools/backups, automatic model-answer verification, typed/handwritten submissions, correct/incorrect/partial verdicts, immutable submissions, uncertain/offline/error fallback, retries, cancellation/navigation/student isolation, timeout, read-only monitor, and offline startup.');
})().catch(error=>{console.error(error);process.exit(1);});
