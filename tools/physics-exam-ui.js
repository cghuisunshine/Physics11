/* A separate exam workspace keeps practice helpers out of timed sessions. */
(function(){
'use strict';
const E=window.PhysicsExam;
let viewed=null,rendered='',loadingInk=false,flushing=false;
const pad=new window.DrawingPad($('exam-canvas'),()=>{if(!loadingInk&&!pad.active)flush();});
const topics=()=>[...selectedTopics];
function message(text){$('exam-message').textContent=text;}
function currentExam(){return E.active(state);}
function flush(){
  const exam=currentExam();if(!exam||flushing||!rendered.startsWith(student+'|'+exam.id+'|'))return true;
  if(!E.remaining(exam)){finish(true);return false;}
  flushing=true;
  try{E.answer(exam,exam.ids[exam.index],$('exam-response').value,pad.snapshot());const ok=save();$('exam-draft-status').textContent=ok?'Answer saved on this device.':'Could not save on this device. Use Export exam progress before closing.';return ok;}
  catch(error){message(error.message);return false;}finally{flushing=false;}
}
function loadInk(ink){loadingInk=true;pad.reset();if(ink){pad.strokes=JSON.parse(JSON.stringify(ink.strokes));pad.render();}loadingInk=false;}
function finish(expired=false){
  const exam=currentExam();if(!exam)return;
  // On expiry use the last saved draft, never accept input after the deadline.
  if(!expired&&!flush())return;
  pad.enabled=false;E.submit(exam);viewed=exam.id;rendered='';save();refresh();$('exam-review-title').focus();
}
function go(index){const exam=currentExam();if(!exam||!flush())return;exam.index=Math.max(0,Math.min(exam.ids.length-1,index));save();rendered='';refresh();$('exam-question-title').focus();}
function stripLinks(box){for(const a of box.querySelectorAll('a'))a.replaceWith(...a.childNodes);}
function renderRunning(exam){
  const key=student+'|'+exam.id+'|'+exam.index;
  $('exam-position').textContent=`Question ${exam.index+1} of ${exam.ids.length}`;
  const nav=$('exam-nav');nav.replaceChildren();
  for(const [i,id] of exam.ids.entries()){
    const b=document.createElement('button');b.type='button';b.textContent=i+1;const answered=!!(exam.responses[id]?.text.trim()||exam.responses[id]?.ink);b.classList.toggle('answered',answered);b.setAttribute('aria-label',`Question ${i+1}${answered?', answer saved':', unanswered'}`);if(i===exam.index)b.setAttribute('aria-current','true');b.onclick=()=>go(i);nav.append(b);
  }
  if(rendered!==key){const id=exam.ids[exam.index],p=bank.find(p=>p.id===id);$('exam-question-title').textContent=p.title;$('exam-statement').innerHTML=p.html;stripLinks($('exam-statement'));$('exam-response').value=exam.responses[id]?.text||'';loadInk(exam.responses[id]?.ink);pad.enabled=true;rendered=key;$('exam-draft-status').textContent='Answers save as you work.';}
  $('exam-prev').disabled=exam.index===0;$('exam-next').disabled=exam.index===exam.ids.length-1;
}
function resultLabel(exam){const s=E.score(exam,bank);return s?`${s.percent.toFixed(1)}% · ${s.earned}/${s.possible} marks · ${exam.review.by==='teacher'?'teacher-marked':'self-marked'}`:'Awaiting marks';}
function renderReview(exam){
  const key=student+'|review|'+exam.id+'|'+(exam.markedAt||'');
  if(rendered===key)return;
  rendered=key;
  $('exam-review-summary').textContent=`${new Date(exam.submittedAt).toLocaleString()} · ${exam.timedOut?'Time limit reached':'Submitted'} · ${resultLabel(exam)}`;
  $('exam-marker').value=exam.review?.by||'self';$('exam-representative').checked=!!exam.review?.representative;
  const box=$('exam-review-questions');box.replaceChildren();
  for(const [i,id] of exam.ids.entries()){
    const p=bank.find(p=>p.id===id),row=document.createElement('section');row.className='exam-review-question';
    const h=document.createElement('h4');h.textContent=`${i+1}. ${p.title}`;row.append(h);
    const question=document.createElement('details'),summary=document.createElement('summary'),statement=document.createElement('div');summary.textContent='Question';statement.className='statement';statement.innerHTML=p.html;stripLinks(statement);question.append(summary,statement);row.append(question);
    const answer=document.createElement('div');answer.className='exam-saved-answer';answer.textContent=exam.responses[id]?.text||'No typed answer';row.append(answer);const ink=inkPreview(exam.responses[id]?.ink);if(ink)row.append(ink);
    const solution=document.createElement('details'),label=document.createElement('summary'),body=document.createElement('div');label.textContent='Model answer and worked solution';body.className='statement';body.innerHTML=p.solution;solution.append(label,body);row.append(solution);
    const inputs=document.createElement('div');inputs.className='exam-marks';
    for(const field of ['earned','possible']){const l=document.createElement('label'),input=document.createElement('input');l.textContent=field==='earned'?'Marks earned':'Marks possible';input.type='number';input.min=field==='earned'?'0':'0.01';input.max='1000';input.step='0.01';input.required=true;input.dataset.question=id;input.dataset.field=field;input.setAttribute('aria-label',`Question ${i+1}: ${l.textContent}`);input.value=exam.marks[id]?.[field]??(field==='possible'?10:(!exam.responses[id]?.text.trim()&&!exam.responses[id]?.ink?0:''));l.append(input);inputs.append(l);}row.append(inputs);box.append(row);
  }
}
function renderReadiness(){
  const selection=topics(),r=E.readiness(state,bank,selection);
  $('readiness-status').textContent=r.status;
  $('readiness-scope').textContent=selection.length?`Evidence for the ${selection.length} topics currently selected above. Changing topics changes this assessment.`:'Select topics above to assess readiness.';
  $('readiness-evidence').textContent=r.latest?`Latest marked exam: ${resultLabel(r.latest)}. ${r.qualified.length} teacher-marked, representative exam(s) meet the size and coverage requirements.`:'No marked exam for this exact selection yet. Submit an exam, then save its marks.';
  if(r.status==='Nearly ready')$('readiness-evidence').textContent+=' Complete two qualifying exams at 90% or higher, at least seven days apart, to demonstrate consistency.';
  const scope=bank.filter(p=>selection.includes(p.topic)),attempted=new Set(state.attempts.map(a=>a.id)),first=state.attempts.filter(a=>!a.review&&scope.some(p=>p.id===a.id));
  $('readiness-coverage').textContent=`Practice coverage: ${scope.length?Math.round(scope.filter(p=>attempted.has(p.id)).length/scope.length*100):0}% (${scope.filter(p=>attempted.has(p.id)).length}/${scope.length} textbook questions). First-attempt practice accuracy: ${first.length?Math.round(first.filter(a=>a.correct).length/first.length*100)+'%':'not assessed'}. Exams do not change practice accuracy.`;
  const tableBox=$('readiness-topics');tableBox.replaceChildren();const actions=$('readiness-actions');actions.replaceChildren();
  if(r.latest){
    const table=document.createElement('table'),caption=document.createElement('caption');caption.textContent='Latest marked exam: chapter and topic marks';table.append(caption);const head=table.createTHead().insertRow();for(const title of ['Chapter / topic','Marks','Score']){const th=document.createElement('th');th.scope='col';th.textContent=title;head.append(th);}const tbody=table.createTBody();
    function add(label,s){const row=tbody.insertRow();for(const value of [label,s?`${s.earned}/${s.possible}`:'Not tested',s?s.percent.toFixed(1)+'%':'—'])row.insertCell().textContent=value;}
    for(const chapter of chapters){const selected=r.latest.ids.filter(id=>bank.find(p=>p.id===id)?.chapter===chapter.chapter);if(!selected.length)continue;const s=E.score({...r.latest,ids:selected},bank);add('Chapter '+chapter.number+': '+chapter.title,s);for(const t of r.topics.filter(t=>bank.some(p=>p.chapter===chapter.chapter&&p.topic===t.topic)))add(topicName(t.topic),t.score);}
    tableBox.append(table);
    for(const t of r.topics.filter(t=>t.score&&t.score.percent<90)){
      const button=document.createElement('button');button.type='button';button.className='secondary';button.textContent='Practise '+topicName(t.topic);button.onclick=()=>{$('mode').value='adaptive';$('practice-chapter').value=bank.find(p=>p.topic===t.topic).chapter;refreshTopicOptions();selectedTopics=new Set([t.topic]);syncTopicSelection();next(true);};actions.append(button);
    }
  }
  const list=$('exam-history-list');list.replaceChildren();$('exam-history-count').textContent=(state.exams||[]).length;
  for(const exam of [...(state.exams||[])].reverse()){
    const b=document.createElement('button');b.type='button';b.className='secondary exam-history-item';b.textContent=`${new Date(exam.startedAt).toLocaleString()} · ${exam.ids.length} questions · ${exam.topics.length} topics · ${resultLabel(exam)}`;b.onclick=()=>{viewed=exam.id;rendered='';refresh();$('exam-review-title').focus();};list.append(b);
  }
  if(!list.children.length)list.textContent='No exams saved yet.';
}
function refresh(){
  let exam=currentExam();
  if(exam&&!E.remaining(exam)){E.submit(exam);viewed=exam.id;rendered='';save();exam=null;}
  if(exam)$('mode').value='exam';
  const enabled=$('mode').value==='exam';document.body.classList.toggle('exam-mode',enabled);$('exam-panel').hidden=!enabled;
  $('practice-chapter').disabled=!!exam;$('topic-control').inert=!!exam;$('topic-control').setAttribute('aria-disabled',String(!!exam));$('topic-picker').open=false;
  if(!enabled){viewed=null;rendered='';return;}
  // Practice callbacks also refuse question navigation while an exam is running.
  const review=(state.exams||[]).find(e=>e.id===viewed&&e.status==='submitted');
  $('exam-running').hidden=!exam;$('exam-setup').hidden=!!exam||!!review;$('exam-review').hidden=!!exam||!review;$('exam-evidence').hidden=!!exam;
  if(exam){renderRunning(exam);tick();return;}
  if(review)renderReview(review);else rendered='';
  if(!review&&Number($('exam-count').value)<topics().length)$('exam-count').value=topics().length;
  const available=E.pool(bank,state,topics());$('exam-available').textContent=`${available.length} unseen exam questions available across ${topics().length} selected topics. Every selected topic needs at least one question.`;$('exam-start').disabled=!student||!topics().length||live.role!=='idle';
  renderReadiness();
}
function tick(){const exam=currentExam();if(!exam)return;const seconds=E.remaining(exam);$('exam-timer').textContent=`${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`;$('exam-timer').classList.toggle('urgent',seconds<=60);if(!seconds)finish(true);}
$('exam-start-form').onsubmit=e=>{
  e.preventDefault();if(!$('exam-start-form').reportValidity())return;
  try{if(!student)throw Error('Choose a student profile first.');if(live.role!=='idle')throw Error('Leave live sharing before starting an exam.');cancelGeneration();resetFollowUp();resetPhotoReview();
    const exam=E.start(bank,state,topics(),Number($('exam-count').value),Number($('exam-minutes').value));
    viewed=null;rendered='';message('');if(!save()){state.exams.pop();throw Error('Browser storage is unavailable or full. Free some space or export progress before starting an exam.');}refresh();$('exam-question-title').focus();
  }catch(error){message(error.message);}
};
$('exam-response').oninput=()=>{flush();const exam=currentExam();if(exam){const b=$('exam-nav').children[exam.index];b?.classList.toggle('answered',!!($('exam-response').value.trim()||exam.responses[exam.ids[exam.index]]?.ink));}};
$('exam-prev').onclick=()=>{const e=currentExam();if(e)go(e.index-1);};$('exam-next').onclick=()=>{const e=currentExam();if(e)go(e.index+1);};
$('exam-submit').onclick=()=>{if(currentExam()&&window.confirm('Submit this exam? Answers will be locked and unanswered questions will receive zero marks.'))finish();};
$('exam-new').onclick=()=>{viewed=null;rendered='';message('');refresh();};
$('exam-mark-form').onsubmit=e=>{
  e.preventDefault();if(!$('exam-mark-form').reportValidity())return;
  try{const exam=(state.exams||[]).find(e=>e.id===viewed);if(!exam)throw Error('Select a submitted exam.');const marks={};for(const input of $('exam-review-questions').querySelectorAll('input[data-question]')){marks[input.dataset.question]=marks[input.dataset.question]||{};marks[input.dataset.question][input.dataset.field]=Number(input.value);}
    E.grade(exam,marks,{by:$('exam-marker').value,representative:$('exam-marker').value==='teacher'&&$('exam-representative').checked});const ok=save();rendered='';refresh();message(ok?'Exam marks saved. Readiness updated for the selected topics.':'Marks could not be saved on this device. Export progress before closing.');
  }catch(error){message(error.message);}
};
$('exam-backup').onclick=()=>{$('export').click();};
$('exam-pen').onclick=()=>{pad.tool='pen';$('exam-pen').setAttribute('aria-pressed','true');$('exam-eraser').setAttribute('aria-pressed','false');};
$('exam-eraser').onclick=()=>{pad.tool='eraser';$('exam-pen').setAttribute('aria-pressed','false');$('exam-eraser').setAttribute('aria-pressed','true');};
$('exam-undo').onclick=()=>pad.undo();$('exam-clear').onclick=()=>{if(window.confirm('Clear this question’s handwritten working?'))pad.clear();};
document.addEventListener('visibilitychange',tick);window.addEventListener('pagehide',()=>{flush();});
setInterval(tick,1000);
window.ExamUI={refresh,tick,invalidate:()=>{rendered='';viewed=null;}};refresh();
})();
