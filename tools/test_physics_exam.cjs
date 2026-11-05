/* Exam lifecycle, persistence, marking and readiness, plus integration in the DOM suite. */
const assert=require('node:assert/strict');
function pure(){
  const E=require('./physics-exam.js'),P=require('./physics-practice-core.js');
  const bank=Array.from({length:90},(_,i)=>({id:'q'+i,topic:'t'+i%3,chapter:'c'+i%3,level:1+Math.floor(i/3)%3,questionType:i===89?'Investigation':'Practice'}));
  const fresh=()=>({version:1,attempts:[],items:{}}),state=fresh(),now=Date.parse('2026-01-01T12:00:00Z');
  state.exposures={q0:new Date(now).toISOString()};state.items.q1={problem:{id:'q1'},manual:true,missed:false};
  assert.ok(!E.pool(bank,state,['t0','t1','t2']).some(p=>['q0','q1','q89'].includes(p.id)));
  assert.throws(()=>E.start(bank,state,['t0','t1','t2'],2,30,now),/at least 3/);
  const exam=E.start(bank,state,['t0','t1','t2'],12,30,now,()=>0.4);
  assert.equal(new Set(exam.ids).size,12);assert.equal(new Set(exam.ids.map(id=>bank.find(p=>p.id===id).topic)).size,3);assert.equal(new Set(exam.ids.map(id=>bank.find(p=>p.id===id).level)).size,3);
  assert.throws(()=>E.start(bank,state,['t0'],10,30,now),/Finish/);assert.throws(()=>E.grade(exam,{},{}),/Submit/);
  E.answer(exam,exam.ids[0],'A response',null,now+1000);assert.throws(()=>E.answer(exam,exam.ids[1],'Too late',null,now+1800000),/ended/);
  assert.ok(E.valid(state,bank));assert.ok(P.validState(state,bank));const hydrated=P.hydrate(JSON.parse(JSON.stringify(P.compact(state))),bank);assert.deepEqual(hydrated.exams,state.exams);assert.deepEqual(hydrated.exposures,state.exposures);
  E.submit(exam,now+1800001);assert.equal(exam.timedOut,true);assert.equal(exam.submittedAt,exam.deadlineAt);assert.equal(E.submit(exam),false);assert.throws(()=>E.answer(exam,exam.ids[0],'Edit'),/ended/);
  const marks=Object.fromEntries(exam.ids.map(id=>[id,{earned:id===exam.ids[0]?8:0,possible:10}]));E.grade(exam,marks,{by:'self',representative:false},now+1900000);assert.equal(E.score(exam,bank).earned,8);assert.equal(E.score(exam,bank).possible,120);assert.ok(E.valid(state,bank));
  marks[exam.ids[1]].earned=1;assert.throws(()=>E.grade(exam,marks,{by:'teacher',representative:true}),/Unanswered/);
  assert.equal(state.attempts.length,0,'Exams never produce practice attempts');
  const invalid=JSON.parse(JSON.stringify(state));invalid.exams[0].ids.push('unknown');assert.equal(P.validState(invalid,bank),false);
  const invalidInk=JSON.parse(JSON.stringify(state));invalidInk.exams[0].responses[exam.ids[0]].ink={width:1};assert.equal(P.validState(invalidInk,bank),false);
  assert.ok(P.validState(fresh(),bank),'Legacy profiles remain valid');
  const evidence=fresh();
  function completed(day,percent,by='teacher',count=12){const e=E.start(bank,evidence,['t0','t1','t2'],count,30,now+day*86400000,()=>0.5);for(const id of e.ids)E.answer(e,id,'Working',null,now+day*86400000+1000);E.submit(e,now+day*86400000+60000);E.grade(e,Object.fromEntries(e.ids.map(id=>[id,{earned:percent/10,possible:10}])),{by,representative:true},now+day*86400000+120000);return e;}
  completed(0,95);assert.equal(E.readiness(evidence,bank,['t0','t1','t2']).status,'Nearly ready');completed(8,95);assert.equal(E.readiness(evidence,bank,['t0','t1','t2']).status,'Ready');assert.equal(E.readiness(evidence,bank,['t0']).status,'Not assessed');completed(16,80);assert.equal(E.readiness(evidence,bank,['t0','t1','t2']).status,'Needs practice');
  const selfState={...fresh(),exams:evidence.exams.slice(0,2).map(e=>({...e,review:{by:'self',representative:true}}))};assert.notEqual(E.readiness(selfState,bank,['t0','t1','t2']).status,'Ready');
  const tooSoon={...fresh(),exams:JSON.parse(JSON.stringify(evidence.exams.slice(0,2)))};tooSoon.exams[1].startedAt=new Date(now+86400000).toISOString();assert.notEqual(E.readiness(tooSoon,bank,['t0','t1','t2']).status,'Ready');
  assert.ok(E.valid(evidence,bank));console.log('Exam logic checks passed.');
  const aiState=fresh(),ai=E.start(bank,aiState,['t0'],2,30,now,()=>0.5);
  E.answer(ai,ai.ids[0],'Partial answer',null,now+1000);E.submit(ai,now+60000);
  assert.equal(ai.aiPending,true);
  const review={earned:7.5,possible:10,confidence:'high',feedback:'Method: 5/5. Calculation and units: 2.5/5.'};
  assert.deepEqual(E.parseAIMark({response:JSON.stringify(review)}),review);
  assert.equal(E.parseAIMark({response:{...review,confidence:'low'}}).earned,null,'Uncertain work cannot get an automatic score');
  for(const bad of [{...review,earned:11},{...review,earned:'7.5'},{...review,possible:100},{...review,feedback:''},{...review,confidence:'unknown'}])assert.throws(()=>E.parseAIMark({response:bad}),/invalid/);
  assert.throws(()=>E.parseAIMark({response:'not json'}),/unreadable/);assert.throws(()=>E.parseAIMark({error:'Unavailable'}),/error/);
  E.recordAIMark(ai,ai.ids[0],review);assert.equal(E.applyAIMarks(ai,now+120000),false,'Incomplete marking cannot produce a total');
  assert.throws(()=>E.recordAIMark(ai,ai.ids[1],review),/Unanswered/);
  E.recordAIMark(ai,ai.ids[1],{...review,earned:0,feedback:'Blank answer.'});assert.ok(P.validState(aiState,bank));
  const restoredAI=P.hydrate(JSON.parse(JSON.stringify(P.compact(aiState))),bank);assert.deepEqual(restoredAI.exams[0].aiResults,ai.aiResults,'Partial marks and feedback survive backups');
  assert.equal(E.applyAIMarks(ai,now+120000),true);assert.equal(E.score(ai,bank).earned,7.5);assert.equal(ai.review.by,'ai');assert.equal(ai.review.representative,false);assert.equal(ai.aiPending,false);assert.ok(P.validState(aiState,bank));
  assert.throws(()=>E.recordAIMark(ai,ai.ids[0],review),/cannot accept/);
  const invalidAI=JSON.parse(JSON.stringify(aiState));invalidAI.exams[0].aiResults[ai.ids[0]].earned=100;assert.equal(P.validState(invalidAI,bank),false);
  const aiEvidence={...fresh(),exams:evidence.exams.slice(0,2).map(e=>({...e,review:{by:'ai',representative:false}}))};assert.notEqual(E.readiness(aiEvidence,bank,['t0','t1','t2']).status,'Ready');
  console.log('Exam AI mark validation checks passed.');
}
module.exports=async function({page,html,bank,login,change,history,storageOf,pause,fakeFirebase,until}){
  const p=page();login(p,'Exam Ada');const firstId=Object.keys(history(p,'Exam Ada').exposures)[0];assert.ok(firstId,'Displayed practice questions are tracked');
  change(p,'practice-chapter','bc-ch2');change(p,'mode','exam');p.$('exam-count').value=10;p.$('exam-minutes').value=30;
  p.$('exam-start-form').dispatchEvent(new p.w.Event('submit',{cancelable:true}));assert.equal(p.$('exam-running').hidden,false);let exam=history(p,'Exam Ada').exams[0];assert.equal(exam.status,'active');assert.ok(!exam.ids.includes(firstId));assert.equal(p.$('exam-statement').querySelectorAll('a').length,0);assert.equal(p.$('exam-review').hidden,true);
  p.$('exam-response').value='My independent working';p.$('exam-response').dispatchEvent(new p.w.Event('input'));
  const deadline=exam.deadlineAt;
  assert.equal(p.$('exam-answer').hidden,true);assert.equal(p.$('exam-answer-body').childElementCount,0);
  p.$('exam-check').click();assert.equal(p.$('exam-answer').hidden,false);assert.equal(p.$('exam-check').getAttribute('aria-expanded'),'true');assert.equal(p.$('exam-check').textContent,'Hide answer');
  const expected=p.w.document.createElement('div');expected.innerHTML=bank.find(q=>q.id===exam.ids[0]).solution;
  assert.equal(p.$('exam-answer-body').innerHTML,expected.innerHTML,'Checking immediately reveals this question’s worked solution offline');
  assert.equal(history(p,'Exam Ada').exams[0].status,'active');assert.equal(history(p,'Exam Ada').exams[0].deadlineAt,deadline);assert.equal(p.$('exam-response').value,'My independent working');
  p.$('exam-check').click();assert.equal(p.$('exam-answer').hidden,true);assert.equal(p.$('exam-check').getAttribute('aria-expanded'),'false');assert.equal(p.$('exam-answer-body').childElementCount,0);
  p.$('exam-check').click();p.$('exam-next').click();assert.equal(p.$('exam-answer').hidden,true);assert.equal(p.$('exam-answer-body').childElementCount,0);assert.equal(p.$('exam-check').textContent,'Check answer');
  p.$('exam-check').click();expected.innerHTML=bank.find(q=>q.id===exam.ids[1]).solution;assert.equal(p.$('exam-answer-body').innerHTML,expected.innerHTML,'The next problem reveals its own solution');
  p.$('exam-prev').click();assert.equal(p.$('exam-answer').hidden,true);assert.equal(p.$('exam-response').value,'My independent working');
  for(const [type,x,y] of [['pointerdown',10,10],['pointermove',30,30],['pointerup',30,30]]){const event=new p.w.MouseEvent(type,{clientX:x,clientY:y,button:0,bubbles:true,cancelable:true});Object.defineProperties(event,{pointerId:{value:1},isPrimary:{value:true},pointerType:{value:'pen'}});p.$('exam-canvas').dispatchEvent(event);}
  assert.ok(history(p,'Exam Ada').exams[0].responses[exam.ids[0]].ink,'Handwritten exam work is saved');p.$('exam-next').click();p.$('exam-prev').click();assert.equal(p.$('exam-response').value,'My independent working');
  change(p,'mode','random');assert.equal(p.$('mode').value,'exam','An active exam prevents practice navigation');assert.equal(history(p,'Exam Ada').attempts.length,0);
  const reloaded=page(html,{storage:storageOf(p)});await pause();assert.equal(reloaded.$('exam-running').hidden,false);assert.equal(reloaded.$('exam-response').value,'My independent working');assert.equal(history(reloaded,'Exam Ada').exams.length,1);
  login(reloaded,'Exam Ben');assert.equal(reloaded.$('exam-panel').hidden,true);assert.equal(history(reloaded,'Exam Ben').exams,undefined);login(reloaded,'Exam Ada');assert.equal(reloaded.$('exam-running').hidden,false);
  reloaded.$('exam-submit').click();exam=history(reloaded,'Exam Ada').exams[0];assert.equal(exam.status,'submitted');assert.equal(reloaded.$('exam-review').hidden,false);assert.equal(reloaded.$('exam-running').hidden,true);assert.equal(exam.responses[exam.ids[0]].text,'My independent working');
  for(const input of reloaded.$('exam-review-questions').querySelectorAll('input[data-field="earned"]'))input.value=input.dataset.question===exam.ids[0]?8:0;
  reloaded.$('exam-mark-form').dispatchEvent(new reloaded.w.Event('submit',{cancelable:true}));assert.equal(history(reloaded,'Exam Ada').exams[0].marks[exam.ids[0]].earned,8);assert.equal(history(reloaded,'Exam Ada').attempts.length,0);assert.match(reloaded.$('exam-review-summary').textContent,/8\/100 marks/);assert.equal(reloaded.$('readiness-status').textContent,'Needs practice');
  const expiredStorage=storageOf(p),key='physics11Practice.v1:'+encodeURIComponent('exam ada'),payload=JSON.parse(expiredStorage[key]),saved=JSON.parse(payload.state),e=saved.exams[0];e.startedAt=new Date(Date.now()-3600000).toISOString();e.deadlineAt=new Date(Date.now()-1800000).toISOString();payload.state=JSON.stringify(saved);expiredStorage[key]=JSON.stringify(payload);
  const expired=page(html,{storage:expiredStorage});await pause();assert.equal(history(expired,'Exam Ada').exams[0].status,'submitted');assert.equal(history(expired,'Exam Ada').exams[0].timedOut,true);assert.equal(expired.$('exam-review').hidden,false,'Overdue reload submits immediately');
  // Optional sync uses the same validated state; startup must not overwrite remote results.
  const apiKey='AIza'+'x'.repeat(35),remote=history(reloaded,'Exam Ada'),firebase=fakeFirebase({[encodeURIComponent('exam sync')]:{version:1,student:'Exam Sync',updatedAt:'2026-01-01T00:00:00.000Z',state:JSON.stringify(remote)}});
  const synced=page(html,{storage:{physics11FirebaseApiKey:apiKey},firebase});login(synced,'Exam Sync');await until(()=>history(synced,'Exam Sync').exams?.length===1);assert.equal(history(synced,'Exam Sync').exams[0].marks[exam.ids[0]].earned,8);assert.equal(history(synced,'Exam Sync').attempts.length,0);
  for(const instance of [p,reloaded,expired,synced]){assert.deepEqual(instance.errors,[]);instance.w.close();}
  console.log('Exam DOM checks passed.');
};
if(require.main===module)pure();
