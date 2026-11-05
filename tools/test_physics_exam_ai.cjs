/* Submitted exam marking uses mocked network responses, never real student data. */
const assert=require('node:assert/strict');
module.exports=async function({page,html,login,change,history,storageOf,pause,until}){
  const instances=[],review=(earned=7.5,confidence='high')=>({earned,possible:10,confidence,feedback:'Method: 5/5. Calculation and units: '+(earned-5)+'/5.'});
  function setup(name,online=true){
    const p=page(html,{online});instances.push(p);login(p,name);change(p,'practice-chapter','bc-ch2');change(p,'topic','Ch 2 · 2.1');change(p,'mode','exam');p.$('exam-count').value=3;
    p.$('exam-start-form').dispatchEvent(new p.w.Event('submit',{cancelable:true}));assert.equal(p.$('exam-running').hidden,false);return p;
  }
  function answer(p,text){p.$('exam-response').value=text;p.$('exam-response').dispatchEvent(new p.w.Event('input'));}
  function ink(p){
    p.$('exam-drawing-open').click();
    for(const [type,x,y] of [['pointerdown',10,10],['pointermove',30,30],['pointerup',30,30]]){const event=new p.w.MouseEvent(type,{clientX:x,clientY:y,button:0,bubbles:true,cancelable:true});Object.defineProperties(event,{pointerId:{value:1},isPrimary:{value:true},pointerType:{value:'pen'}});p.$('exam-canvas').dispatchEvent(event);}
  }
  function result(body){return {ok:true,json:async()=>({response:JSON.stringify(body)})};}
  const p=setup('AI Exam'),requests=[];
  p.w.fetch=async(url,options)=>{requests.push({url,options,body:JSON.parse(options.body)});return result(review(requests.length===1?7.5:10));};
  answer(p,'My original typed answer');p.$('exam-next').click();ink(p);p.$('exam-close').click();
  const original=history(p,'AI Exam').exams[0].responses;
  assert.equal(requests.length,0,'AI never marks before exam submission');p.$('exam-submit').click();
  await until(()=>history(p,'AI Exam').exams[0].review?.by==='ai');
  let exam=history(p,'AI Exam').exams[0];assert.equal(requests.length,2,'Only answered questions call AI, including handwriting-only answers');
  assert.equal(exam.status,'submitted');assert.equal(exam.aiPending,false);assert.deepEqual(exam.responses,original,'AI marks the locked submission');
  assert.equal(exam.marks[exam.ids[0]].earned,7.5);assert.equal(exam.marks[exam.ids[1]].earned,10);assert.equal(exam.marks[exam.ids[2]].earned,0);
  assert.equal(exam.review.representative,false);assert.equal(history(p,'AI Exam').attempts.length,0);assert.match(p.$('exam-review-summary').textContent,/17.5\/30 marks · AI-marked/);
  assert.equal(p.$('exam-review-questions').querySelectorAll('.exam-ai-feedback').length,3);assert.match(p.$('exam-ai-status').textContent,/complete/);assert.equal(p.$('exam-ai-retry').hidden,true);
  assert.match(requests[0].body.message,/STUDENT ANSWER:\nMy original typed answer/);assert.match(requests[0].body.message,/partial|credit/i);assert.match(requests[0].body.message,/reference worked solution/);assert.equal(requests[0].body.mime_type,'image/jpeg');
  assert.ok(p.w.__lastEncodedLabels.some(label=>label.includes('handwritten answer and steps')),'Saved handwriting is sent as labelled student work');
  const after=page(html,{storage:storageOf(p)});instances.push(after);await pause();change(after,'mode','exam');after.$('exam-history-list').lastElementChild.click();
  assert.match(after.$('exam-review-summary').textContent,/17.5\/30 marks · AI-marked/);assert.equal(after.$('exam-review-questions').querySelectorAll('.exam-ai-feedback').length,3,'Marks and feedback survive reload');
  // Manual corrections retain the AI feedback but change the marking label.
  const earned=after.$('exam-review-questions').querySelector('input[data-field="earned"]');earned.value=8;earned.dispatchEvent(new after.w.Event('input',{bubbles:true}));assert.equal(after.$('exam-marker').value,'self');
  after.$('exam-mark-form').dispatchEvent(new after.w.Event('submit',{cancelable:true}));assert.equal(history(after,'AI Exam').exams[0].review.by,'self');
  // Offline submission preserves drafts and blank zeros; reconnecting retries only missing marks.
  const offline=setup('Offline Exam',false);answer(offline,'Saved offline answer');offline.$('exam-submit').click();await until(()=>/Offline/.test(offline.$('exam-ai-status').textContent)&&!offline.$('exam-ai-retry').hidden);
  exam=history(offline,'Offline Exam').exams[0];assert.equal(exam.markedAt,undefined);assert.equal(Object.keys(exam.aiResults).length,2);assert.match(offline.$('exam-ai-status').textContent,/Offline/);
  Object.defineProperty(offline.w.navigator,'onLine',{value:true,configurable:true});let retried=0;offline.w.fetch=async()=>{retried++;return result(review(10));};offline.$('exam-ai-retry').click();await until(()=>history(offline,'Offline Exam').exams[0].markedAt);
  assert.equal(retried,1);assert.match(offline.$('exam-review-summary').textContent,/10\/30 marks/);
  // A low-confidence answer receives feedback, but no guessed score or total.
  const uncertain=setup('Uncertain Exam');answer(uncertain,'Ambiguous work');uncertain.$('exam-next').click();answer(uncertain,'Readable working');let count=0;
  uncertain.w.fetch=async()=>{count++;return result(review(8,count===1?'low':'high'));};uncertain.$('exam-submit').click();await until(()=>count===2&&!uncertain.$('exam-ai-retry').hidden);
  exam=history(uncertain,'Uncertain Exam').exams[0];assert.equal(exam.aiResults[exam.ids[0]].earned,null);assert.equal(exam.markedAt,undefined);assert.equal(uncertain.$('exam-review-questions').querySelector('input[data-field="earned"]').value,'');assert.match(uncertain.$('exam-review-questions').textContent,/needs review/);
  // Pending marking resumes after reload without requesting successful answers again.
  const resumed=page(html,{storage:storageOf(uncertain),online:true});instances.push(resumed);let resumedCalls=0;resumed.w.fetch=async()=>{resumedCalls++;return result(review(9));};await until(()=>history(resumed,'Uncertain Exam').exams[0].markedAt);assert.equal(resumedCalls,1);
  // Errors leave questions ungraded and allow a later retry.
  const failed=setup('Failed Exam');answer(failed,'A valid submission');failed.w.fetch=async()=>({ok:false,status:503});failed.$('exam-submit').click();await until(()=>/HTTP 503/.test(failed.$('exam-ai-status').textContent));assert.equal(history(failed,'Failed Exam').exams[0].markedAt,undefined);
  failed.w.fetch=async()=>result(review(6));failed.$('exam-ai-retry').click();await until(()=>history(failed,'Failed Exam').exams[0].markedAt);
  // Canceling and changing profiles discard even successful late responses.
  for(const action of ['cancel','student','navigate']){
    const late=setup('Late '+action);answer(late,'Locked late answer');let release,signal;
    late.w.fetch=async(url,options)=>{signal=options.signal;return new Promise(resolve=>{release=()=>resolve(result(review(10)));});};late.$('exam-submit').click();await until(()=>!!release);
    assert.equal(late.$('exam-mark-fields').disabled,true);
    if(action==='cancel')late.$('exam-ai-cancel').click();
    if(action==='student')login(late,'Other '+action);
    if(action==='navigate')late.$('exam-new').click();
    assert.equal(signal.aborted,true);release();await pause();exam=history(late,'Late '+action).exams[0];assert.equal(exam.markedAt,undefined);assert.equal(exam.aiResults?.[exam.ids[0]],undefined,'Late '+action+' marks are discarded');
    if(action==='cancel'){assert.equal(late.$('exam-mark-fields').disabled,false);assert.equal(late.$('exam-ai-retry').hidden,false);}
  }
  // A per-question timeout does not fabricate zero marks.
  const timed=setup('Timed Exam');answer(timed,'Timeout work');const timer=timed.w.setTimeout.bind(timed.w);timed.w.setTimeout=(fn,delay,...args)=>timer(fn,delay===120000?30:delay,...args);
  timed.w.fetch=async(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new timed.w.DOMException('Aborted','AbortError')),{once:true}));timed.$('exam-submit').click();await until(()=>/timed out/.test(timed.$('exam-ai-status').textContent));assert.equal(history(timed,'Timed Exam').exams[0].markedAt,undefined);
  // All-blank exams need no network and still have a complete denominator.
  const blank=setup('Blank Exam',false);blank.$('exam-submit').click();await until(()=>history(blank,'Blank Exam').exams[0].markedAt);assert.match(blank.$('exam-review-summary').textContent,/0\/30 marks/);
  // An exam whose deadline passed while closed is submitted and marked on return.
  const expiring=setup('Expired AI Exam');answer(expiring,'Work saved before the deadline');const expiredStorage=storageOf(expiring),key='physics11Practice.v1:'+encodeURIComponent('expired ai exam');
  const payload=JSON.parse(expiredStorage[key]),saved=JSON.parse(payload.state);saved.exams[0].startedAt=new Date(Date.now()-31*60000).toISOString();saved.exams[0].deadlineAt=new Date(Date.now()-60000).toISOString();payload.state=JSON.stringify(saved);expiredStorage[key]=JSON.stringify(payload);
  const expired=page(html,{storage:expiredStorage,online:true});instances.push(expired);expired.w.fetch=async()=>result(review(8));await until(()=>history(expired,'Expired AI Exam').exams[0].markedAt);assert.equal(history(expired,'Expired AI Exam').exams[0].timedOut,true);assert.match(expired.$('exam-review-summary').textContent,/8\/30 marks · AI-marked/);
  for(const instance of instances){assert.deepEqual(instance.errors,[]);instance.w.close();}
  console.log('Exam AI checks passed: automatic partial-credit marks, handwriting, blank zeros, persistence, corrections, offline retries, uncertainty, resume, errors, cancellation, profile isolation and timeouts.');
};
