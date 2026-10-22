/* Called by the studio DOM suite; all service responses are mocked. */
const assert=require('node:assert/strict');
module.exports=async function({page,html,bank,login,change,response,history,storageOf,until,pause}){
  const c=page();login(c,'Coach');
  const A=c.w.AdaptivePractice,P=c.w.Practice,scope=bank.filter(p=>p.topic===bank[0].topic);
  let seq=0;
  const content={title:'A new motion question',question:'A car travels 12 m east in 3 s. Find its average velocity.',answer:'4 m/s east',steps:['Average velocity = displacement ÷ time.','12 ÷ 3 = 4 m/s east.'],check:'4 m/s × 3 s = 12 m east.'};
  const make=(skill='concepts',level=1)=>A.problem({...content,id:'gen-00000000-0000-4000-8000-'+String(++seq).padStart(12,'0'),anchorId:scope[0].id,skill,level},bank);
  const fresh=()=>({version:1,attempts:[],items:{}});
  let s=fresh(),plan=A.plan(s,bank,scope);
  assert.equal(plan.level,1);assert.equal(plan.skill,'concepts');assert.equal(A.plan(s,bank,[]),null);
  const match=A.chooseTextbook(plan,scope,s);assert.ok(match);assert.equal(match.level,plan.level);
  assert.equal(A.chooseTextbook(plan,scope,s,scope.map(q=>q.id)),null,'AI is needed only after appropriate textbook questions run out');
  P.record(s,match,'My reasoning',10,true,{practiceSkill:'reasoning'});
  assert.equal(P.hydrate(P.compact(s),bank).attempts[0].practiceSkill,'reasoning','Textbook skill targets survive reloads');
  s=fresh();
  assert.equal(A.coverage(s,bank,scope).length,5);
  for(const skill of Object.keys(A.skills))for(let n=0;n<2;n++)P.record(s,make(skill),'My answer',12,true);
  plan=A.plan(s,bank,scope);assert.equal(plan.skill,'concepts');assert.equal(plan.level,2,'Two successes at the same level raise the challenge');
  const retryOnly=fresh();for(const skill of Object.keys(A.skills)){const same=make(skill);P.record(retryOnly,same,'My answer',12,true);P.record(retryOnly,same,'My answer',12,true);}
  assert.equal(A.plan(retryOnly,bank,scope).level,1,'Repeating the same correct answer does not raise the challenge');
  P.record(s,make('calculations',3),'Wrong calculation',12,false);
  plan=A.plan(s,bank,scope);assert.equal(plan.skill,'calculations');assert.equal(plan.level,2,'A miss lowers the next difficulty');assert.ok(plan.last);
  s=fresh();for(let n=0;n<3;n++)P.record(s,make('units'),'Wrong units',12,false);
  plan=A.plan(s,bank,scope);assert.notEqual(plan.skill,'units','Repeated misses do not trap the student in one skill');
  assert.equal(plan.topic,scope[0].topic);
  s=fresh();P.record(s,scope[0],'5',5,false,{assessment:'ai',answerVerification:{verdict:'partly_correct',confidence:'high',feedback:'Missing direction.',weak_points:[{skill:'Direction',evidence:'No east/west direction.'}]}});
  plan=A.plan(s,bank,scope);assert.equal(plan.skill,'units');assert.equal(plan.anchor.id,scope[0].id);
  assert.match(A.prompt(plan,s,'Question text','Worked solution'),/Missing|Direction/);
  s=fresh();P.record(s,scope[0],'',5,false);assert.equal(A.plan(s,bank,scope).last,null,'Empty self-ratings are not skill evidence');
  const generated=make(),saved=fresh();P.record(saved,generated,'4 m/s',30,false);
  const compact=JSON.parse(JSON.stringify(P.compact(saved)));
  assert.equal(P.validState(compact,bank),true);assert.equal(P.hydrate(compact,bank).items[generated.id].problem.html,generated.html);
  compact.generated[generated.id].html='<script>bad()</script>';compact.generated[generated.id].question='<img src=x onerror=bad()>';
  const safe=P.hydrate(compact,bank).items[generated.id].problem;
  assert.ok(!safe.html.includes('<img'));assert.match(safe.html,/&lt;img/,'Generated and imported text is escaped');
  delete compact.generated[generated.id].answer;assert.equal(P.validState(compact,bank),false);
  const packed=c.w.LivePractice.pack(generated);assert.equal(c.w.LivePractice.unpack(packed,bank).id,generated.id);assert.ok(!JSON.stringify(packed).includes('studentAnswer'));
  assert.throws(()=>A.parse({response:'not json'},plan,bank,generated.id),/incomplete/);
  assert.throws(()=>A.parse({response:{...content,check:''}},plan,bank,generated.id),/complete/);

  change(c,'practice-chapter',bank[0].chapter);change(c,'topic',bank[0].topic);change(c,'mode','coach');
  assert.equal(c.$('adaptive-panel').hidden,false);c.$('adaptive-create').click();assert.match(c.$('adaptive-status').textContent,/Selected a suitable unused textbook/,'Suitable textbook questions are available offline');
  for(let n=0;n<=scope.length&&!/offline/.test(c.$('adaptive-status').textContent);n++)c.$('adaptive-create').click();
  assert.match(c.$('adaptive-status').textContent,/offline/);assert.equal(history(c,'Coach').attempts.length,0,'Skipping textbook questions does not record scores');
  c.w.navigator.onLine=true;
  let requests=[];
  c.w.fetch=async(url,options)=>{requests.push(JSON.parse(options.body));return {ok:true,json:async()=>({response:{title:'Incomplete'}})};};
  c.$('adaptive-create').click();await until(()=>!c.$('adaptive-create').disabled);
  assert.match(c.$('adaptive-status').textContent,/complete/);assert.equal(history(c,'Coach').attempts.length,0);
  c.w.fetch=async(url,options)=>{requests.push(JSON.parse(options.body));return {ok:true,json:async()=>({response:content})};};
  c.$('adaptive-create').click();await until(()=>c.$('question-title').textContent===content.title);
  assert.equal(c.$('solution').hidden,true);assert.equal(history(c,'Coach').attempts.length,0,'Generating and skipping do not award scores');
  assert.ok(requests.at(-1).image,'The source question image grounds generation');
  c.w.navigator.onLine=false;response(c,'12 m/s');c.$('check').click();c.$('rate-practice').click();
  const savedCoach=history(c,'Coach'),id=savedCoach.attempts[0].id;
  assert.equal(savedCoach.generated[id].question,content.question);assert.equal(P.validState(savedCoach,bank),true);
  assert.match(c.$('adaptive-coverage').textContent,/Concepts: Needs practice/);
  assert.equal(c.$('attempt-count').textContent,'1');
  const reload=page(html,{storage:storageOf(c)});await pause();
  change(reload,'mode','review');assert.equal(reload.$('question-title').textContent,content.title,'Saved generated questions remain in offline review');
  assert.match(reload.$('statement').textContent,/12 m east/);
  change(reload,'mode','day');assert.equal(reload.$('day-question').options.length,2,'Generated attempts also appear in day history');
  const link=new URL('https://physics.test/physics-practice.html');link.searchParams.set('q',id);link.hash=new URLSearchParams({practice:JSON.stringify(savedCoach.generated[id])});
  const shared=page(html,{url:link.href});login(shared,'Shared coach');assert.equal(shared.$('question-title').textContent,content.title);assert.equal(shared.$('solution').hidden,true);
  assert.equal(history(shared,'Shared coach').attempts.length,0);

  // Old responses cannot cross changes of mode, scope, current question or student.
  for(const action of ['cancel','mode','topic','student']){
    change(c,'mode','coach');c.w.navigator.onLine=true;
    let finish,pending=false;
    c.w.fetch=async()=>{pending=true;return new Promise(resolve=>{finish=()=>resolve({ok:true,json:async()=>({response:{...content,title:'Late question',question:'Late '+action}})});});};
    c.$('adaptive-create').click();await until(()=>pending);
    if(action==='cancel')c.$('adaptive-cancel').click();
    if(action==='mode')change(c,'mode','random');
    if(action==='topic')change(c,'topic',scope[0].topic);
    if(action==='student'){c.$('student-button').click();login(c,'Second coach');}
    finish();await pause();assert.notEqual(c.$('question-title').textContent,'Late question');assert.equal(history(c,'Coach').attempts.length,1);
  }
  const timeout=page(html,{online:true});login(timeout,'Timeout coach');change(timeout,'mode','coach');
  change(timeout,'practice-chapter',bank[0].chapter);change(timeout,'topic',bank[0].topic);timeout.w.navigator.onLine=false;
  for(let n=0;n<=scope.length&&!/offline/.test(timeout.$('adaptive-status').textContent);n++)timeout.$('adaptive-create').click();
  timeout.w.navigator.onLine=true;
  const setTimeout=timeout.w.setTimeout.bind(timeout.w);timeout.w.setTimeout=(fn,delay,...args)=>setTimeout(fn,delay===60000?25:delay,...args);
  timeout.w.fetch=async(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new timeout.w.DOMException('Aborted','AbortError'))));
  timeout.$('adaptive-create').click();await until(()=>/timed out/.test(timeout.$('adaptive-status').textContent));assert.equal(timeout.$('adaptive-create').disabled,false);
  // Always AI bypasses unused textbook matches and includes the selected textbook context.
  const forced=page();login(forced,'Always AI');change(forced,'practice-chapter',bank[0].chapter);change(forced,'topic',bank[0].topic);change(forced,'mode','coach');change(forced,'adaptive-source','ai');
  assert.ok(forced.w.AdaptivePractice.chooseTextbook(forced.w.AdaptivePractice.plan(fresh(),bank,scope),scope,fresh()),'Suitable unused textbook questions still exist');
  const readyTitle=forced.$('question-title').textContent;
  forced.$('adaptive-create').click();assert.match(forced.$('adaptive-status').textContent,/offline.*Always AI/);assert.equal(forced.$('question-title').textContent,readyTitle,'Offline Always AI never substitutes a textbook question');
  forced.w.navigator.onLine=true;let forcedRequest;
  forced.w.fetch=async(url,options)=>{forcedRequest=JSON.parse(options.body);return {ok:true,json:async()=>({response:{...content,title:'Always AI question'}})};};
  forced.$('adaptive-create').click();await until(()=>forced.$('question-title').textContent==='Always AI question');
  assert.ok(forced.$('badge').querySelector('.ai-marker'),'Mandatory generation keeps the circled AI marker');
  assert.ok(forcedRequest.image);assert.match(forcedRequest.message,/Stay within the selected textbook chapter\/section/);
  const context=JSON.parse(forcedRequest.message.split('\n').at(-1));
  assert.equal(context.textbookContext.topic,scope[0].topic);assert.equal(context.textbookContext.chapterTitle,scope[0].chapterTitle);assert.ok(context.sourceQuestion);assert.ok(context.sourceSolution);
  assert.equal(history(forced,'Always AI').attempts.length,0);
  const forcedReload=page(html,{storage:storageOf(forced)});await pause();change(forcedReload,'mode','coach');assert.equal(forcedReload.$('adaptive-source').value,'ai');assert.match(forcedReload.$('adaptive-status').textContent,/Always AI/);
  forced.w.fetch=async()=>{throw new forced.w.TypeError('Service unavailable');};forced.$('adaptive-create').click();await until(()=>/Could not reach/.test(forced.$('adaptive-status').textContent));assert.equal(forced.$('question-title').textContent,'Always AI question','A failed AI request keeps the current question');
  let finishSource,pendingSource=false;forced.w.fetch=async()=>{pendingSource=true;return new Promise(resolve=>{finishSource=()=>resolve({ok:true,json:async()=>({response:{...content,title:'Wrong source response'}})});});};
  forced.$('adaptive-create').click();await until(()=>pendingSource);change(forced,'adaptive-source','textbook-first');finishSource();await pause();assert.equal(forced.$('question-title').textContent,'Always AI question','Changing source cancels late AI responses');
  forced.$('adaptive-create').click();assert.match(forced.$('adaptive-status').textContent,/Selected a suitable unused textbook/,'The textbook-first option remains available');
  for(const p of [c,reload,shared,timeout,forced,forcedReload]){assert.deepEqual(p.errors,[]);p.w.close();}
};
