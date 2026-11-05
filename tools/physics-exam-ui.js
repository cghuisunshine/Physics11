/* A separate exam workspace keeps practice helpers out of timed sessions. */
(function(){
'use strict';
const E=window.PhysicsExam;
let viewed=null,rendered='',loadingInk=false,flushing=false,drawingShift=false;
let markingRequest=null,markingNotice=null;
let examStudent=student;
const markingAttempted=new Set(),markingKey=exam=>student+'|'+exam.id;
const pad=new window.DrawingPad($('exam-canvas'),()=>{syncDrawingTools();if(!loadingInk&&!pad.active)flush();});
const topics=()=>[...selectedTopics];
function syncDrawingTools(){
  const erasing=drawingShift||pad.tool==='eraser';
  $('exam-pen').setAttribute('aria-pressed',String(!erasing));$('exam-eraser').setAttribute('aria-pressed',String(erasing));$('exam-canvas').classList.toggle('erasing',erasing);
  document.querySelectorAll('[data-exam-color]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.examColor===pad.color)));
  $('exam-undo').disabled=!pad.history.length||!!pad.active;$('exam-clear').disabled=!pad.hasInk||!!pad.active;
  $('exam-drawing-status').textContent=pad.hasInk?'Your handwritten working is saved with this exam question.':'Write your working here. It saves as you draw.';
}
function showDrawing(open){
  if(!open)pad.finish();
  $('exam-drawing-panel').hidden=!open;$('exam-drawing-tools').hidden=!open;$('exam-drawing-open').hidden=open;$('exam-drawing-open').setAttribute('aria-expanded',String(open));
  drawingShift=false;syncDrawingTools();
  (open?$('exam-canvas'):$('exam-drawing-open')).focus({preventScroll:true});
}
function message(text){$('exam-message').textContent=text;}
function currentExam(){return E.active(state);}
function cancelMarking(text='AI marking canceled. Saved marks are kept; retry to continue.'){
  if(!markingRequest)return;
  const request=markingRequest;markingRequest=null;clearTimeout(request.timer);request.controller?.abort();markingNotice={key:request.key,text};
}
function markingCurrent(request){return markingRequest===request&&student===request.student&&state===request.state&&state.exams?.includes(request.exam)&&!request.exam.markedAt&&viewed===request.exam.id&&$('mode').value==='exam';}
function inkForMarking(ink){
  if(!ink)return [];
  const canvas=document.createElement('canvas');canvas.width=ink.width;canvas.height=ink.height;
  const drawing=new window.DrawingPad(canvas,()=>{});drawing.strokes=ink.strokes;drawing.render();
  return [{dataURL:canvas.toDataURL('image/jpeg',.9),filename:'drawn-answer-and-steps.jpg'}];
}
function markingStatus(exam){
  const key=markingKey(exam),busy=markingRequest?.key===key,done=exam.ids.filter(id=>typeof exam.aiResults?.[id]?.earned==='number').length;
  $('exam-mark-fields').disabled=busy;$('exam-ai-cancel').hidden=!busy;$('exam-ai-retry').hidden=busy||!!exam.markedAt;
  $('exam-ai-retry').textContent=Object.keys(exam.aiResults||{}).length?'Retry AI marking':'Mark with AI';
  $('exam-ai-status').textContent=busy?`AI marking: ${done} of ${exam.ids.length} questions marked. You can review saved answers while marking continues.`:markingNotice?.key===key?markingNotice.text:exam.review?.by==='ai'?'AI marking complete. Scores and feedback are saved.':exam.markedAt?'Saved marks are shown below.':`${done} of ${exam.ids.length} questions marked. Retry AI marking or complete the remaining marks manually.`;
}
async function markExam(exam){
  if(markingRequest||exam.status!=='submitted'||exam.markedAt||viewed!==exam.id||$('mode').value!=='exam')return;
  const request={exam,key:markingKey(exam),student,state,controller:null,timer:null};markingRequest=request;markingAttempted.add(request.key);markingNotice=null;
  exam.aiPending=true;rendered='';refresh();let failure='',storageFailed=false;
  try{
    for(const id of exam.ids){
      if(!markingCurrent(request))return;
      if(typeof exam.aiResults?.[id]?.earned==='number')continue;
      const response=exam.responses[id];
      if(!response?.text.trim()&&!response?.ink){E.recordAIMark(exam,id,{earned:0,possible:10,confidence:'high',feedback:'No answer submitted. 0/10 marks.'});}
      else if(navigator.onLine===false){failure='Offline: AI marking needs an internet connection.';continue;}
      else{
        const controller=new AbortController();request.controller=controller;let timedOut=false;
        request.timer=setTimeout(()=>{timedOut=true;controller.abort();},120000);
        try{
          const problem=bank.find(p=>p.id===id),work=inkForMarking(response.ink);
          const image=await questionAndWorkingImage(problem,work,controller.signal,problem.solution);
          if(!markingCurrent(request)||controller.signal.aborted){if(timedOut)throw Error('AI marking timed out.');return;}
          const result=await fetch(AI.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({message:E.markingPrompt(problem,response.text,readableHTML(problem.html),readableHTML(problem.solution)),image:image.image,mime_type:image.mime_type,filename:image.filename})});
          if(!result.ok)throw Error('AI marking returned HTTP '+result.status+'.');
          const review=E.parseAIMark(await result.json());
          if(!markingCurrent(request))return;
          if(controller.signal.aborted)throw Error('AI marking timed out.');
          E.recordAIMark(exam,id,review);
          if(review.earned===null)failure='Some answers could not be assessed confidently.';
        }catch(error){if(!markingCurrent(request))return;failure=timedOut?'AI marking timed out.':error.message||'Could not reach the AI marking service.';}
        finally{clearTimeout(request.timer);request.timer=null;}
      }
      if(!markingCurrent(request))return;
      if(!save()){storageFailed=true;break;}rendered='';refresh();
    }
    if(!markingCurrent(request))return;
    if(!storageFailed&&E.applyAIMarks(exam)){
      storageFailed=!save();
      markingNotice={key:request.key,text:'AI marking complete. Scores and feedback are saved.'};
    }else markingNotice={key:request.key,text:(failure||'Some questions still need marking.')+' Saved marks are kept. Retry AI marking or enter the remaining marks manually.'};
    if(storageFailed)markingNotice={key:request.key,text:'Could not save marks on this device. Export exam progress before closing.'};
  }catch(error){
    if(markingRequest===request)markingNotice={key:request.key,text:(error.message||'AI marking could not finish.')+' Saved marks are kept. Retry or mark the remaining questions manually.'};
  }finally{
    if(markingRequest===request){clearTimeout(request.timer);markingRequest=null;rendered='';refresh();}
  }
}
function flush(){
  const exam=currentExam();if(!exam||flushing||!rendered.startsWith(student+'|'+exam.id+'|'))return true;
  if(!E.remaining(exam)){finish(true);return false;}
  flushing=true;
  try{E.answer(exam,exam.ids[exam.index],$('exam-response').value,pad.snapshot());const ok=save();$('exam-draft-status').textContent=ok?'Answer saved on this device.':'Could not save on this device. Use Export exam progress before closing.';return ok;}
  catch(error){message(error.message);return false;}finally{flushing=false;}
}
function loadInk(ink){loadingInk=true;drawingShift=false;pad.reset();if(ink){pad.strokes=JSON.parse(JSON.stringify(ink.strokes));pad.render();}loadingInk=false;syncDrawingTools();}
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
  if(rendered!==key){const id=exam.ids[exam.index],p=bank.find(p=>p.id===id);$('exam-question-title').textContent=p.title;$('exam-statement').innerHTML=p.html;stripLinks($('exam-statement'));$('exam-response').value=exam.responses[id]?.text||'';loadInk(exam.responses[id]?.ink);pad.enabled=true;rendered=key;$('exam-draft-status').textContent='Answers save as you work.';$('exam-answer').hidden=true;$('exam-answer-body').replaceChildren();$('exam-check').textContent='Check answer';$('exam-check').setAttribute('aria-expanded','false');}
  $('exam-prev').disabled=exam.index===0;$('exam-next').disabled=exam.index===exam.ids.length-1;
}
function resultLabel(exam){const s=E.score(exam,bank);return s?`${s.percent.toFixed(1)}% · ${s.earned}/${s.possible} marks · ${{teacher:'teacher-marked',self:'self-marked',ai:'AI-marked'}[exam.review.by]}`:'Awaiting marks';}
function renderReview(exam){
  markingStatus(exam);
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
    const ai=exam.aiResults?.[id];if(ai){const feedback=document.createElement('div');feedback.className='exam-ai-feedback';const title=document.createElement('strong'),body=document.createElement('p');title.textContent=ai.earned===null?'AI: needs review':`AI: ${ai.earned}/${ai.possible} marks`;body.textContent=ai.feedback;feedback.append(title,body);row.append(feedback);}
    const solution=document.createElement('details'),label=document.createElement('summary'),body=document.createElement('div');label.textContent='Model answer and worked solution';body.className='statement';body.innerHTML=p.solution;solution.append(label,body);row.append(solution);
    const inputs=document.createElement('div');inputs.className='exam-marks';
    for(const field of ['earned','possible']){const l=document.createElement('label'),input=document.createElement('input');l.textContent=field==='earned'?'Marks earned':'Marks possible';input.type='number';input.min=field==='earned'?'0':'0.01';input.max='1000';input.step='0.01';input.required=true;input.dataset.question=id;input.dataset.field=field;input.setAttribute('aria-label',`Question ${i+1}: ${l.textContent}`);input.value=exam.marks[id]?.[field]??ai?.[field]??(field==='possible'?10:(!exam.responses[id]?.text.trim()&&!exam.responses[id]?.ink?0:''));l.append(input);inputs.append(l);}row.append(inputs);box.append(row);
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
  if(examStudent!==student){cancelMarking();examStudent=student;viewed=null;rendered='';}
  let exam=currentExam();
  if(exam&&!E.remaining(exam)){E.submit(exam);viewed=exam.id;rendered='';save();exam=null;}
  if(exam)$('mode').value='exam';
  const enabled=$('mode').value==='exam';document.body.classList.toggle('exam-mode',enabled);$('exam-panel').hidden=!enabled;
  if(markingRequest&&!markingCurrent(markingRequest))cancelMarking();
  $('practice-chapter').disabled=!!exam;$('topic-control').inert=!!exam;$('topic-control').setAttribute('aria-disabled',String(!!exam));$('topic-picker').open=false;
  if(!enabled){viewed=null;rendered='';return;}
  if(!exam&&viewed===null)viewed=[...(state.exams||[])].reverse().find(e=>e.status==='submitted'&&e.aiPending&&!e.markedAt)?.id||null;
  // Practice callbacks also refuse question navigation while an exam is running.
  const review=(state.exams||[]).find(e=>e.id===viewed&&e.status==='submitted');
  $('exam-running').hidden=!exam;$('exam-setup').hidden=!!exam||!!review;$('exam-review').hidden=!!exam||!review;$('exam-evidence').hidden=!!exam;
  if(exam){renderRunning(exam);tick();return;}
  if(review){renderReview(review);if(review.aiPending&&!review.markedAt&&!markingRequest&&!markingAttempted.has(markingKey(review))){markingAttempted.add(markingKey(review));queueMicrotask(()=>{if(student&&viewed===review.id&&state.exams?.includes(review))markExam(review);});}}else rendered='';
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
$('exam-check').onclick=()=>{
  const exam=currentExam();if(!exam||!flush())return;
  const show=$('exam-answer').hidden;
  $('exam-answer-body').innerHTML=show?bank.find(p=>p.id===exam.ids[exam.index]).solution:'';
  $('exam-answer').hidden=!show;$('exam-check').textContent=show?'Hide answer':'Check answer';$('exam-check').setAttribute('aria-expanded',String(show));
};
$('exam-submit').onclick=()=>{if(currentExam()&&window.confirm('Submit this exam? Answers will be locked and unanswered questions will receive zero marks.'))finish();};
$('exam-new').onclick=()=>{viewed='setup';rendered='';message('');refresh();};
$('exam-ai-retry').onclick=()=>{const exam=(state.exams||[]).find(e=>e.id===viewed);if(exam)markExam(exam);};
$('exam-ai-cancel').onclick=()=>{cancelMarking();rendered='';refresh();};
$('exam-mark-form').addEventListener('input',event=>{if(event.target.matches('input[data-question]')&&$('exam-marker').value==='ai'){$('exam-marker').value='self';$('exam-representative').checked=false;}});
$('exam-mark-form').onsubmit=e=>{
  e.preventDefault();if(!$('exam-mark-form').reportValidity())return;
  try{const exam=(state.exams||[]).find(e=>e.id===viewed);if(!exam)throw Error('Select a submitted exam.');if(markingRequest)throw Error('Wait for AI marking or cancel it before saving manual marks.');if($('exam-marker').value==='ai')throw Error('Choose student or teacher marking to save manual changes.');const marks={};for(const input of $('exam-review-questions').querySelectorAll('input[data-question]')){marks[input.dataset.question]=marks[input.dataset.question]||{};marks[input.dataset.question][input.dataset.field]=Number(input.value);}
    E.grade(exam,marks,{by:$('exam-marker').value,representative:$('exam-marker').value==='teacher'&&$('exam-representative').checked});const ok=save();markingNotice=null;rendered='';refresh();message(ok?'Exam marks saved. Readiness updated for the selected topics.':'Marks could not be saved on this device. Export progress before closing.');
  }catch(error){message(error.message);}
};
$('exam-backup').onclick=()=>{$('export').click();};
$('exam-drawing-open').onclick=()=>showDrawing(true);$('exam-close').onclick=()=>showDrawing(false);
$('exam-pen').onclick=()=>{pad.tool='pen';syncDrawingTools();};
$('exam-eraser').onclick=()=>{pad.tool='eraser';syncDrawingTools();};
document.querySelectorAll('[data-exam-color]').forEach(button=>{button.onclick=()=>{pad.color=button.dataset.examColor;pad.tool='pen';syncDrawingTools();};});
document.addEventListener('keydown',event=>{if(event.key==='Shift'&&currentExam()&&!$('exam-drawing-panel').hidden){drawingShift=true;syncDrawingTools();}});
document.addEventListener('keyup',event=>{if(event.key==='Shift'){drawingShift=false;syncDrawingTools();}});
window.addEventListener('blur',()=>{drawingShift=false;syncDrawingTools();});
for(const type of ['pointerdown','pointermove'])$('exam-canvas').addEventListener(type,event=>{drawingShift=!!event.shiftKey;syncDrawingTools();});
$('exam-undo').onclick=()=>pad.undo();$('exam-clear').onclick=()=>{if(window.confirm('Clear this question’s handwritten working?'))pad.clear();};
// Match the practice pad's touch preference while keeping exam ink separate.
(()=>{if(!(navigator.maxTouchPoints>0))return;const button=$('exam-finger'),canvas=$('exam-canvas');button.hidden=false;
  const iPad=/iPad/.test(navigator.userAgent)||(/Macintosh/.test(navigator.userAgent)&&navigator.maxTouchPoints>1);
  const apply=()=>{let finger=!iPad;try{const saved=localStorage.getItem('physics11-finger-drawing');if(saved!==null)finger=saved==='1';}catch(error){}
    pad.pencilOnly=!finger;button.setAttribute('aria-pressed',String(finger));button.title=finger?'Finger drawing on (tap for Apple Pencil only)':'Apple Pencil only (tap to draw with finger)';canvas.classList.toggle('pencil-only',!finger);
  };
  button.onclick=()=>{const finger=pad.pencilOnly;try{localStorage.setItem('physics11-finger-drawing',finger?'1':'0');}catch(error){}pad.pencilOnly=!finger;button.setAttribute('aria-pressed',String(finger));canvas.classList.toggle('pencil-only',!finger);button.title=finger?'Finger drawing on (tap for Apple Pencil only)':'Apple Pencil only (tap to draw with finger)';};
  $('exam-drawing-open').addEventListener('click',apply);window.addEventListener('storage',event=>{if(event.key==='physics11-finger-drawing')apply();});apply();
})();
document.addEventListener('visibilitychange',tick);window.addEventListener('pagehide',()=>{flush();cancelMarking();});
setInterval(tick,1000);
window.ExamUI={refresh,tick,invalidate:()=>{cancelMarking();rendered='';viewed=null;}};refresh();
})();
