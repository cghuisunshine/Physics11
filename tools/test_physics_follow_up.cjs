/* Run by the practice DOM suite. AI responses are mocked. */
const assert=require('node:assert/strict');
module.exports=async function({page,html,bank,login,change,response,history,storageOf,until,pause,fakeFirebase}){
  const question={text:'A cyclist travels 24 m east in 6 s. Find the average velocity.',choices:['2 m/s east','4 m/s east','6 m/s east','8 m/s east','24 m/s east'],answer:'B',explanation:'Average velocity = displacement ÷ time = 24 m ÷ 6 s = 4 m/s east. Check: 4 × 6 = 24 m east, using the same method as the textbook.'};
  const p=page();login(p,'Follow-up');change(p,'practice-chapter',bank[0].chapter);change(p,'mode','chapter');
  const F=p.w.PhysicsFollowUp,P=p.w.Practice;
  const choose=(instance,index)=>instance.$('followup-choices').children[index].click();
  const enable=(instance,value)=>{instance.$('followup-enabled').checked=value;instance.$('followup-enabled').dispatchEvent(new instance.w.Event('change'));};
  const miss=(instance)=>{response(instance,'My attempt');instance.$('check').click();instance.$('rate-practice').click();};
  assert.equal(p.$('followup-enabled').checked,true);
  assert.equal(F.normalize({...question,choices:['same','same','x','y','z']}),null);
  assert.throws(()=>F.parseResponse({response:{...question,answer:'Z'}}),/incomplete/);
  assert.throws(()=>F.parseResponse({response:question},question.text),/repeated/);
  assert.throws(()=>F.parseResponse({ok:false}),/could not/);
  assert.equal(F.parseResponse({response:'```json\n'+JSON.stringify(question)+'\n```'}).answer,'B');
  miss(p);assert.equal(p.$('followup').hidden,false);assert.match(p.$('followup-status').textContent,/offline/);
  assert.equal(history(p,'Follow-up').attempts.length,1,'An offline miss remains saved');
  const requests=[];
  p.w.navigator.onLine=true;p.w.fetch=async(url,options)=>{requests.push(JSON.parse(options.body));return {ok:true,json:async()=>({response:question})};};
  p.$('followup-retry').click();await until(()=>!p.$('followup-content').hidden);
  assert.equal(requests.length,1);assert.ok(requests[0].image,'Question diagrams ground the follow-up');
  assert.match(requests[0].message,/Grade 11/);assert.match(requests[0].message,/workedSolution/);assert.match(requests[0].message,/My attempt/);assert.match(requests[0].message,/do not use calculus/);
  assert.equal(p.$('solution').open,true,'The original worked solution stays available');
  assert.equal(p.$('followup-solution').textContent,'','No answer leaks before checking');
  choose(p,0);p.$('followup-check').click();assert.match(p.$('followup-feedback').textContent,/Not quite/);
  assert.equal(p.$('followup-solution').hidden,true);assert.equal(p.$('followup-reveal').hidden,false);
  p.$('followup-check').click();assert.equal(history(p,'Follow-up').attempts[0].followUp.answers.length,1,'Repeated checks do not duplicate answers');
  p.$('followup-retry').click();assert.equal(p.$('followup-check').disabled,true);choose(p,1);p.$('followup-check').click();
  assert.match(p.$('followup-feedback').textContent,/Correct!/);assert.equal(p.$('followup-solution').hidden,false);
  let saved=history(p,'Follow-up');assert.equal(saved.attempts.length,1);assert.equal(saved.attempts[0].correct,false);assert.equal(saved.items[bank[0].id].missed,true);assert.equal(p.$('attempt-count').textContent,'1');assert.match(p.$('accuracy').textContent,/0%/);
  assert.equal(saved.attempts[0].followUp.answers.length,2);assert.equal(P.validState(saved,bank),true);
  const hydrated=P.hydrate(P.compact(saved),bank);assert.equal(hydrated.attempts[0].followUp.answers[1].correct,true,'Backups retain follow-up results');
  saved.attempts[0].followUp.answers[0].correct=true;assert.equal(P.hydrate(saved,bank).attempts[0].followUp.answers[0].correct,false,'Imported correctness is recomputed');
  saved.attempts[0].followUp.question.answer='Z';assert.equal(P.hydrate(saved,bank).attempts[0].followUp,undefined,'Invalid optional follow-up data does not lose textbook history');
  const reload=page(html,{storage:storageOf(p)});change(reload,'chapter-question',bank[0].id);
  assert.equal(reload.$('followup').hidden,false);assert.match(reload.$('followup-feedback').textContent,/Correct!/);assert.equal(reload.$('followup-solution').hidden,false,'Follow-up works offline after reload');
  enable(reload,false);assert.equal(reload.$('followup').hidden,true);assert.equal(reload.w.localStorage.getItem('physics11PracticeFollowUp'),'false');
  const disabled=page(html,{storage:storageOf(reload)});assert.equal(disabled.$('followup-enabled').checked,false);
  enable(reload,true);assert.equal(reload.$('followup').hidden,false,'Enabling restores the saved follow-up');
  change(p,'chapter-question',bank[1].id);p.w.navigator.onLine=false;miss(p);p.w.navigator.onLine=true;p.$('followup-retry').click();await until(()=>!p.$('followup-content').hidden);
  choose(p,0);p.$('followup-check').click();p.$('followup-reveal').click();assert.equal(p.$('followup-solution').hidden,false);assert.equal(p.$('followup-check').hidden,true);
  p.w.fetch=async()=>({ok:true,json:async()=>({response:question})});p.$('followup-retry').click();await until(()=>/repeated/.test(p.$('followup-status').textContent));
  const another={...question,text:'A cyclist travels 30 m east in 5 s. Find the average velocity.',answer:'C'};
  p.w.fetch=async()=>({ok:true,json:async()=>({response:another})});p.$('followup-retry').click();await until(()=>p.$('followup-statement').textContent===another.text);
  assert.equal(p.$('followup-solution').hidden,true);assert.equal(history(p,'Follow-up').attempts[1].followUp.answers.length,0);
  // Wrong AI verdicts also trigger follow-ups; uncertain verdicts do not.
  const auto=page(html,{online:true});login(auto,'Auto follow-up');change(auto,'practice-chapter',bank[0].chapter);change(auto,'mode','chapter');
  let verdict='partly_correct',calls=0;
  auto.w.fetch=async(url,options)=>{calls++;return {ok:true,json:async()=>({response:JSON.parse(options.body).message.startsWith('Create ONE')?question:{verdict,confidence:verdict==='unassessed'?'low':'high',feedback:'Check your direction.',answer_check:'Direction missing.',steps:[],weak_points:[]}})};};
  response(auto,'24 m');auto.$('check').click();await until(()=>!auto.$('followup-content').hidden);assert.equal(calls,2);assert.equal(history(auto,'Auto follow-up').attempts[0].answerVerification.verdict,'partly_correct');
  change(auto,'chapter-question',bank[1].id);verdict='correct';response(auto,'Correct');auto.$('check').click();await until(()=>history(auto,'Auto follow-up').attempts.length===2);await pause();assert.equal(calls,3);assert.equal(auto.$('followup').hidden,true);
  change(auto,'chapter-question',bank[2].id);verdict='unassessed';response(auto,'Uncertain');auto.$('check').click();await until(()=>!auto.$('self-rating').hidden);assert.equal(calls,4);assert.equal(auto.$('followup').hidden,true);
  // Cancel, setting, navigation and student changes must discard late responses.
  for(const action of ['cancel','setting','question','mode','topic','student']){
    p.w.navigator.onLine=false;change(p,'chapter-question',bank[3].id);miss(p);p.w.navigator.onLine=true;
    let finish,signal;p.w.fetch=async(url,options)=>{signal=options.signal;return new Promise(resolve=>{finish=()=>resolve({ok:true,json:async()=>({response:question})});});};
    p.$('followup-retry').click();await until(()=>!!finish);
    if(action==='cancel')p.$('followup-cancel').click();
    if(action==='setting')enable(p,false);
    if(action==='question')change(p,'chapter-question',bank[4].id);
    if(action==='mode')change(p,'mode','random');
    if(action==='topic')change(p,'topic',bank[0].topic);
    if(action==='student'){p.$('student-button').click();login(p,'Other follow-up');}
    assert.equal(signal.aborted,true,'The '+action+' action aborts generation');finish();await pause();
    if(['cancel','setting','question','student'].includes(action))assert.equal(p.$('followup-content').hidden,true,'No stale question after '+action);
    assert.equal(history(p,'Follow-up').attempts.at(-1).followUp,undefined,'Late '+action+' response was ignored');
    if(action==='setting')enable(p,true);
    change(p,'mode','chapter');
  }
  // HTTP, invalid output, network failure and timeouts are recoverable.
  const failure=page();login(failure,'Failure follow-up');change(failure,'practice-chapter',bank[0].chapter);change(failure,'mode','chapter');miss(failure);failure.w.navigator.onLine=true;
  for(const [fetch,expected] of [
    [async()=>({ok:false,status:503}),/HTTP 503/],
    [async()=>({ok:true,json:async()=>({response:{}})}),/incomplete/],
    [async()=>{throw new failure.w.TypeError('Offline');},/Could not reach/]
  ]){failure.w.fetch=fetch;failure.$('followup-retry').click();await until(()=>failure.$('followup').getAttribute('aria-busy')==='false');assert.match(failure.$('followup-status').textContent,expected);assert.equal(failure.$('followup-retry').hidden,false);}
  const timer=failure.w.setTimeout.bind(failure.w);failure.w.setTimeout=(fn,delay,...args)=>timer(fn,delay===120000?30:delay,...args);
  failure.w.fetch=async(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new failure.w.DOMException('Aborted','AbortError'))));
  failure.$('followup-retry').click();await until(()=>/timed out/.test(failure.$('followup-status').textContent));assert.equal(history(failure,'Failure follow-up').attempts.length,1);
  const generated=failure.w.AdaptivePractice.problem({id:'gen-00000000-0000-4000-8000-000000000099',anchorId:bank[0].id,skill:'concepts',level:1,title:'Generated question',question:'Find 2 m / 2 s.',answer:'1 m/s',steps:['Divide distance by time.'],check:'1 m/s × 2 s = 2 m.'},bank);
  failure.w.show(generated,'AI practice');failure.w.navigator.onLine=false;miss(failure);assert.equal(failure.$('followup').hidden,true,'Generated questions do not trigger textbook follow-ups');
  const key='AIza'+'f'.repeat(35),id='f'.repeat(48),firebase=fakeFirebase({['live-'+id]:{kind:'physics11-live',version:1,active:true,revision:1,expiresAt:Date.now()+3600000,question:{q:bank[0].id}}});
  const follower=page(html,{url:'https://physics.test/physics-practice.html?follow='+id+'#liveKey='+key,firebase});await until(()=>follower.$('live-status').textContent.startsWith('Following live.'));login(follower,'Follow-up follower');miss(follower);assert.equal(follower.$('followup').hidden,true,'Followers stay on the host question');
  for(const instance of [p,reload,disabled,auto,failure,follower]){assert.deepEqual(instance.errors,[]);instance.w.close();}
  console.log('Passed: follow-up generation, grading, retries, solution reveal, separate scores, persistence, settings, offline recovery, validation, late responses, failures, timeout and live follower isolation.');
};
