(()=>{
  'use strict';
  const $=id=>document.getElementById(id),sets=[...document.querySelectorAll('.question-set')],qs=[...document.querySelectorAll('.question')];
  const known=new Set(qs.map(q=>q.id)),search=$('search'),topic=$('topic'),kind=$('kind');
  const DRAFT='bc-physics11-ch2-homework',DONE='bc-physics11-ch2-completed';
  function read(key,fallback){try{return JSON.parse(localStorage.getItem(key))||fallback;}catch{return fallback;}}
  const params=new URLSearchParams(location.search),incoming=params.has('homework');
  const draft=read(DRAFT,{}),ids=incoming?(params.get('homework')||'').split(','):(Array.isArray(draft.ids)?draft.ids:[]);
  const selected=new Set(ids.filter(id=>known.has(id)));
  let completed=read(DONE,{}),composing=false,homeworkView=incoming,aiRequest=null;
  if(typeof completed!=='object'||Array.isArray(completed))completed={};
  $('homework-name').value=String(incoming?params.get('title')||'Kinematics homework':draft.title||'Kinematics homework').slice(0,160);
  $('homework-instructions').value=String(incoming?params.get('instructions')||'':draft.instructions||'').slice(0,2000);
  $('homework-answers').checked=incoming?params.get('answers')==='1':draft.answers===true;
  const aiPrompt=$('homework-ai-prompt'),criteria=()=>aiPrompt?.value.trim().slice(0,4000)||'';
  const refinePrompt=$('homework-refine-prompt'),refineCriteria=()=>refinePrompt?.value.trim().slice(0,4000)||'';
  if(aiPrompt)aiPrompt.value=String(draft.aiPrompt||'').slice(0,4000);
  if(refinePrompt)refinePrompt.value=String(draft.refinePrompt||'').slice(0,4000);
  const sectionRules=[...topic.options].filter(option=>option.value).map((option,index)=>{
    const row=document.createElement('tr'),heading=document.createElement('th'),cell=document.createElement('td'),count=document.createElement('td'),input=document.createElement('input'),label=document.createElement('label');
    heading.scope='row';label.textContent=option.textContent;input.id=`homework-percent-${index}`;label.htmlFor=input.id;heading.append(label);
    input.type='number';input.min='0';input.max='100';input.step='1';input.value=String(Number.isInteger(draft.percentages?.[option.value])&&draft.percentages[option.value]>=0&&draft.percentages[option.value]<=100?draft.percentages[option.value]:50);
    input.dataset.sectionPercent=option.value;input.setAttribute('aria-describedby','sampling-help');count.setAttribute('aria-live','polite');
    cell.append(input);row.append(heading,cell,count);$('homework-sections').append(row);
    return {topic:option.value,input,count};
  });
  $('homework-parity').value=['all','odd','even'].includes(draft.parity)?draft.parity:'all';
  $('homework-sampling-order').value=['first','ai'].includes(draft.samplingOrder)?draft.samplingOrder:'random';
  function cancelAI(message='AI selection canceled. Your selection is unchanged.'){
    if(!aiRequest)return;const status=aiRequest.kind==='refine'?$('homework-refine-status'):$('homework-ai-status');aiRequest.controller.abort();clearTimeout(aiRequest.timer);aiRequest=null;status.textContent=message;renderSampling();
  }
  function selectionChanged(){const pending=!!aiRequest;cancelAI('Settings or selection changed. Run AI selection again when ready.');if(!pending){$('homework-ai-status').textContent='';if($('homework-refine-status'))$('homework-refine-status').textContent='';}$('homework-ai-results').hidden=true;$('homework-ai-list').replaceChildren();if($('homework-refine-results')){$('homework-refine-results').hidden=true;$('homework-refine-list').replaceChildren();}}
  function matchesChoice(select,value){return select.multiple?[...select.selectedOptions].some(option=>!option.value||option.value===value):!select.value||select.value===value;}
  function matchesFilters(q){const set=q.closest('.question-set');return matchesChoice(topic,set.dataset.topic)&&matchesChoice(kind,set.dataset.kind)&&q.dataset.search.includes(search.value.trim().toLowerCase());}
  function matchesNumber(q){
    if($('homework-parity').value==='all')return true;
    const label=q.querySelector('.question-top a').textContent.replace(/^Question\s+/,'').trim();
    return /^\d+$/.test(label)&&Number(label)%2===($('homework-parity').value==='odd'?1:0);
  }
  function samplingPlan(){return sectionRules.map(rule=>{const candidates=qs.filter(q=>matchesFilters(q)&&q.closest('.question-set').dataset.topic===rule.topic&&matchesNumber(q));return {...rule,candidates,amount:Math.ceil(candidates.length*Number(rule.input.value)/100)};});}
  function validPercentages(){return sectionRules.every(rule=>rule.input.checkValidity());}
  function renderSampling(){
    const valid=validPercentages(),plan=samplingPlan();
    for(const rule of plan)rule.count.textContent=rule.input.checkValidity()?`${$('homework-sampling-order').value==='ai'&&criteria()?'Up to ':''}${rule.amount} of ${rule.candidates.length} eligible`:'Enter 0–100';
    $('apply-section-percentages').disabled=!!aiRequest||!valid||!qs.some(matchesFilters);
    if($('choose-hardest-ai'))$('choose-hardest-ai').disabled=$('apply-section-percentages').disabled;
    const action=$('apply-section-percentages'),mode=$('homework-sampling-order').value;
    action.dataset.selectionMode=mode;
    action.textContent=action.hasAttribute('data-single-selection-action')?(aiRequest&&aiRequest.kind!=='refine'?'AI: choosing…':({random:'Choose random questions',first:'Choose first questions',ai:'AI: choose questions'})[mode]):mode==='ai'?'Apply AI percentages':'Apply section percentages';
    $('cancel-homework-ai').hidden=!aiRequest;
    $('select-matching-numbers').disabled=!plan.some(rule=>rule.candidates.length);
    if($('refine-homework-ai')){$('refine-homework-ai').disabled=!!aiRequest||!selected.size||!refineCriteria();$('refine-homework-ai').textContent=aiRequest?.kind==='refine'?'AI: filtering…':'AI: filter selected questions';}
    if($('cancel-homework-refine'))$('cancel-homework-refine').hidden=aiRequest?.kind!=='refine';
  }
  const orderedIds=()=>qs.filter(q=>selected.has(q.id)).map(q=>q.id);
  const title=()=>$('homework-name').value.trim()||'Kinematics homework';
  function saveDraft(){try{localStorage.setItem(DRAFT,JSON.stringify({ids:orderedIds(),title:title(),instructions:$('homework-instructions').value,answers:$('homework-answers').checked,percentages:Object.fromEntries(sectionRules.filter(rule=>rule.input.checkValidity()).map(rule=>[rule.topic,Number(rule.input.value)])),parity:$('homework-parity').value,samplingOrder:$('homework-sampling-order').value,...(aiPrompt?{aiPrompt:aiPrompt.value.slice(0,4000)}:{}),...(refinePrompt?{refinePrompt:refinePrompt.value.slice(0,4000)}:{})}));}catch{}}
  function resetFilters(){search.value='';for(const select of [topic,kind]){select.value='';select.dispatchEvent(new Event('input'));}}
  function homeworkURL(){
    const base=location.protocol==='file:'?'https://cghuisunshine.github.io/Physics11/bc-kinematics-questions.html':location.href;
    const url=new URL(base);url.search='';url.hash='';
    url.searchParams.set('homework',orderedIds().join(','));url.searchParams.set('title',title());
    if($('homework-instructions').value.trim())url.searchParams.set('instructions',$('homework-instructions').value.trim());
    if($('homework-answers').checked)url.searchParams.set('answers','1');
    return url.toString();
  }
  function updateLocation(){
    try{
      const url=new URL(location.href);
      for(const key of ['homework','title','instructions','answers'])url.searchParams.delete(key);
      if(homeworkView){const assignment=new URL(homeworkURL());for(const [key,value] of assignment.searchParams)url.searchParams.set(key,value);url.hash='';}
      history.replaceState(null,'',url);
    }catch{/* File browsers may not allow replacing their URL. */}
  }
  function changed(){
    selectionChanged();
    saveDraft();$('homework-message').textContent='';$('homework-link-row').hidden=true;
    if(homeworkView)updateLocation();render();
  }
  function setView(value){cancelAI();homeworkView=value;resetFilters();updateLocation();render();}
  function render(){
    renderSampling();
    let shown=0;
    for(const set of sets){
      let count=0;
      for(const q of set.querySelectorAll('.question')){
        q.hidden=!(matchesFilters(q)&&(!homeworkView||selected.has(q.id)));
        q.dataset.homework=String(composing&&selected.has(q.id));
        const input=q.querySelector('[data-homework]');input.checked=selected.has(q.id);input.closest('label').hidden=!composing;
        if(!q.hidden)count++;
      }
      set.hidden=!count;shown+=count;
      const entries=set.querySelector('.set-heading p');
      entries.textContent=homeworkView?`${count} assigned question${count===1?'':'s'}`:`${set.querySelectorAll('.question').length} entries`;
      document.querySelector(`nav a[href="#${set.id}"]`).hidden=set.hidden;
      if(homeworkView&&count)for(const context of set.querySelectorAll('.context'))context.open=true;
    }
    document.body.classList.toggle('homework-view',homeworkView);
    document.body.dataset.homeworkAnswers=String($('homework-answers').checked);
    $('homework-panel').hidden=!composing;$('homework-banner').hidden=!homeworkView;$('all-questions').hidden=!homeworkView;
    $('create-homework').setAttribute('aria-expanded',String(composing));$('create-homework').textContent=composing?'Close homework editor':homeworkView?'Edit homework':'Create homework';
    $('homework-title').textContent=title();$('homework-directions').textContent=$('homework-instructions').value;
    $('homework-directions').hidden=!$('homework-instructions').value.trim();
    $('homework-details').textContent=`${selected.size} question${selected.size===1?'':'s'} · Chapter 2: Kinematics`;
    $('homework-count').textContent=`${selected.size} question${selected.size===1?'':'s'} selected for homework.`;
    for(const id of ['clear-selection','preview-homework','copy-homework','download-homework','print-homework'])$(id).disabled=!selected.size;
    $('select-shown').disabled=!shown;
    $('empty').hidden=shown>0;$('empty').textContent=homeworkView?'No homework questions match. Clear the filters or edit the selection.':'No questions match. Try a different word or clear the filters.';
    $('status').textContent=`${shown} of ${homeworkView?selected.size:qs.length} question entries shown · ${qs.filter(q=>q.dataset.done==='true'&&(!homeworkView||selected.has(q.id))).length} marked done`;
    $('print').disabled=homeworkView&&!selected.size;
  }
  document.querySelectorAll('[data-complete]').forEach(input=>{
    input.checked=!!completed[input.dataset.complete];input.closest('.question').dataset.done=String(input.checked);
    input.addEventListener('change',()=>{completed[input.dataset.complete]=input.checked;input.closest('.question').dataset.done=String(input.checked);try{localStorage.setItem(DONE,JSON.stringify(completed));}catch{}render();});
  });
  document.querySelectorAll('[data-answer-toggle]').forEach(button=>button.addEventListener('click',()=>{
    const panel=$(button.getAttribute('aria-controls'));panel.hidden=!panel.hidden;button.setAttribute('aria-expanded',String(!panel.hidden));button.textContent=panel.hidden?'Show answer':'Hide answer';
  }));
  document.querySelectorAll('[data-homework]').forEach(input=>input.addEventListener('change',()=>{
    if(input.checked)selected.add(input.dataset.homework);else selected.delete(input.dataset.homework);changed();
  }));
  [search,topic,kind].forEach(input=>input.addEventListener('input',()=>{cancelAI('Filters changed. Run AI selection again when ready.');render();}));
  $('reset').onclick=()=>{cancelAI();resetFilters();render();};
  $('create-homework').onclick=()=>{composing=!composing;render();};
  $('all-questions').onclick=()=>setView(false);
  document.querySelectorAll('[data-edit-selection]').forEach(button=>button.addEventListener('click',()=>{
    composing=true;setView(false);
    $('homework-message').textContent='Check Homework to add a question, or uncheck it to remove one. Your current selection is highlighted. Preview again when ready.';
    const first=qs.find(q=>selected.has(q.id))||qs[0];first?.querySelector('[data-homework]').focus();
  }));
  $('select-shown').onclick=()=>{for(const q of qs)if(!q.hidden)selected.add(q.id);changed();};
  $('set-section-percentages').onclick=()=>{
    const input=$('homework-all-percent');if(!input.reportValidity()||input.value==='')return;
    selectionChanged();
    for(const rule of sectionRules)rule.input.value=input.value;saveDraft();renderSampling();
  };
  for(const rule of sectionRules){rule.input.required=true;rule.input.addEventListener('input',()=>{selectionChanged();saveDraft();renderSampling();});}
  for(const id of ['homework-parity','homework-sampling-order'])$(id).addEventListener('input',()=>{selectionChanged();saveDraft();renderSampling();});
  aiPrompt?.addEventListener('input',()=>{$('homework-sampling-order').value='ai';selectionChanged();saveDraft();renderSampling();});
  refinePrompt?.addEventListener('input',()=>{if(aiRequest?.kind==='refine')cancelAI('Criteria changed. Run AI filtering again when ready.');saveDraft();renderSampling();});
  $('select-matching-numbers').onclick=()=>{for(const q of qs)if(matchesFilters(q)&&matchesNumber(q))selected.add(q.id);changed();};
  $('cancel-homework-ai').onclick=()=>cancelAI();
  if($('cancel-homework-refine'))$('cancel-homework-refine').onclick=()=>cancelAI('AI filtering canceled. Your selection is unchanged.');
  if($('refine-homework-ai'))$('refine-homework-ai').onclick=async()=>{
    const selectionCriteria=refineCriteria();if(!selectionCriteria||!selected.size||aiRequest)return;
    const candidates=qs.filter(q=>selected.has(q.id)),plan=[{topic:'current homework selection',candidates,amount:candidates.length}],status=$('homework-refine-status');
    selectionChanged();
    const request={controller:new AbortController(),timer:null,kind:'refine'};aiRequest=request;renderSampling();status.textContent='Preparing AI to review the selected questions…';
    request.timer=setTimeout(()=>cancelAI('AI filtering timed out. Your selection is unchanged; try again.'),360000);
    try{
      const result=await window.HomeworkDifficultyAI.choose(plan,{signal:request.controller.signal,criteria:selectionCriteria,filterMode:true,onProgress:message=>{if(aiRequest===request)status.textContent=message;}});
      if(aiRequest!==request||request.controller.signal.aborted)return;
      clearTimeout(request.timer);aiRequest=null;selected.clear();for(const item of result.selected)selected.add(item.id);homeworkView=true;resetFilters();changed();
      for(const item of result.selected){const q=$(item.id),entry=document.createElement('li'),link=document.createElement('a');link.href='#'+item.id;link.textContent=q.closest('.question-set').querySelector('h2').textContent+' — '+q.querySelector('.question-top a').textContent;entry.append(link,document.createTextNode(': '+item.reason));$('homework-refine-list').append(entry);}
      $('homework-refine-results').hidden=!result.selected.length;
      status.textContent=`AI kept ${result.selected.length} of ${candidates.length} selected questions and removed ${candidates.length-result.selected.length}. ${result.selected.length?'Only the remaining homework questions are shown below.':'Your selection is now empty.'}`;
    }catch(error){if(aiRequest===request)status.textContent=error.name==='AbortError'?'AI filtering canceled. Your selection is unchanged.':(error instanceof TypeError?'Could not reach the AI service. Check your connection and try again.':error.message)+' Your selection is unchanged.';}
    finally{clearTimeout(request.timer);if(aiRequest===request){aiRequest=null;renderSampling();}}
  };
  if($('choose-hardest-ai'))$('choose-hardest-ai').onclick=()=>{
    if(!validPercentages()||aiRequest||!qs.some(matchesFilters))return;
    $('homework-sampling-order').value='ai';selectionChanged();saveDraft();renderSampling();
    return $('apply-section-percentages').onclick();
  };
  $('apply-section-percentages').onclick=async()=>{
    if(!validPercentages()||aiRequest)return;
    const plan=samplingPlan();
    if($('homework-sampling-order').value==='ai'){
      const selectionCriteria=criteria();
      const request={controller:new AbortController(),timer:null};aiRequest=request;renderSampling();
      $('homework-ai-status').textContent='Preparing AI selection…';
      request.timer=setTimeout(()=>cancelAI('AI selection timed out. Your selection is unchanged; try again.'),360000);
      try{
        const result=await window.HomeworkDifficultyAI.choose(plan,{signal:request.controller.signal,criteria:selectionCriteria,onProgress:message=>{if(aiRequest===request)$('homework-ai-status').textContent=message;}});
        if(aiRequest!==request||request.controller.signal.aborted)return;
        clearTimeout(request.timer);aiRequest=null;
        for(const q of qs)if(matchesFilters(q))selected.delete(q.id);
        for(const item of result.selected)selected.add(item.id);
        changed();
        for(const item of result.selected){const q=$(item.id),entry=document.createElement('li'),link=document.createElement('a');link.href='#'+item.id;link.textContent=q.closest('.question-set').querySelector('h2').textContent+' — '+q.querySelector('.question-top a').textContent;entry.append(link,document.createTextNode(': '+item.reason));$('homework-ai-list').append(entry);}
        $('homework-ai-results').hidden=!result.selected.length;
        $('homework-ai-results').querySelector('summary').textContent=result.requests?'Why AI selected these questions':'Selected questions';
        $('homework-ai-status').textContent=result.requests?(selectionCriteria?(result.selected.length?'AI selected '+result.selected.length+' question'+(result.selected.length===1?'':'s')+' matching your criteria within the section limits. Use Adjust questions to add or remove any.':'AI found no eligible questions matching your criteria. Try broader criteria or adjust your filters.'):'AI selected the hardest questions for each section percentage. Use Adjust questions to add or remove any.'):'Section percentages applied. All eligible questions or none were requested, so AI ranking was not needed.';
      }catch(error){
        if(aiRequest===request)$('homework-ai-status').textContent=error.name==='AbortError'?'AI selection canceled. Your selection is unchanged.':(error instanceof TypeError?'Could not reach the AI service. Check your connection and try again.':error.message)+' Your selection is unchanged.';
      }finally{clearTimeout(request.timer);if(aiRequest===request){aiRequest=null;renderSampling();}}
      return;
    }
    for(const q of qs)if(matchesFilters(q))selected.delete(q.id);
    for(const {candidates,amount} of plan){
      if($('homework-sampling-order').value==='random')for(let i=candidates.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[candidates[i],candidates[j]]=[candidates[j],candidates[i]];}
      for(const q of candidates.slice(0,amount))selected.add(q.id);
    }
    changed();$('homework-message').textContent='Section percentages applied. You can adjust individual Homework checkboxes before sharing.';
  };
  $('clear-selection').onclick=()=>{selected.clear();homeworkView=false;resetFilters();updateLocation();changed();};
  $('preview-homework').onclick=()=>{if(selected.size)setView(true);};
  for(const id of ['homework-name','homework-instructions','homework-answers'])$(id).addEventListener('input',changed);
  $('copy-homework').onclick=async()=>{
    if(!selected.size)return;
    const link=homeworkURL();$('homework-link').value=link;$('homework-link-row').hidden=false;
    try{await navigator.clipboard.writeText(link);$('homework-message').textContent='Homework link copied. Send it to your student.';}
    catch{$('homework-link').focus();$('homework-link').select();$('homework-message').textContent='Select and copy the homework link below.';}
  };
  async function printQuestions(){
    const images=qs.filter(q=>!q.hidden).flatMap(q=>[...q.querySelectorAll('img')]);
    for(const set of sets)if(!set.hidden)images.push(...set.querySelectorAll('.shared img,.context img'));
    await Promise.all(images.map(image=>{image.setAttribute('loading','eager');return image.decode?image.decode().catch(()=>{}):Promise.resolve();}));
    window.print();
  }
  $('print').onclick=printQuestions;
  $('print-homework').onclick=()=>{if(selected.size){setView(true);return printQuestions();}};
  $('download-homework').onclick=()=>{
    if(!selected.size)return;
    const output=document.implementation.createHTMLDocument(title()),body=output.body;
    output.documentElement.lang='en';
    const charset=output.createElement('meta');charset.setAttribute('charset','utf-8');output.head.prepend(charset);
    const viewport=output.createElement('meta');viewport.name='viewport';viewport.content='width=device-width,initial-scale=1';output.head.append(viewport);
    const style=output.createElement('style');style.textContent=[...document.querySelectorAll('style')].map(s=>s.textContent).join('\n')+'\n.homework-export main{max-width:1000px;margin:24px auto;padding:0 20px}.homework-export>header{display:block;padding:0}.homework-export .homework-banner{border:0;margin:20px auto}.homework-export .context{display:block}@media print{.homework-export main{margin:0;padding:0}.homework-export .context{display:block}.homework-export .context>summary{display:none}}';output.head.append(style);
    body.className='homework-view homework-export';body.dataset.homeworkAnswers=String($('homework-answers').checked);
    const header=output.createElement('header'),banner=$('homework-banner').cloneNode(true);banner.hidden=false;
    banner.querySelector('[data-edit-selection]').remove();
    banner.querySelector('h1').textContent=title();banner.querySelector('#homework-details').textContent=`${selected.size} question${selected.size===1?'':'s'} · Chapter 2: Kinematics`;
    banner.querySelector('#homework-directions').textContent=$('homework-instructions').value;
    header.append(banner);body.append(header);
    const main=output.createElement('main');
    for(const set of sets){
      if(![...set.querySelectorAll('.question')].some(q=>selected.has(q.id)))continue;
      const clone=set.cloneNode(true);clone.hidden=false;
      for(const q of clone.querySelectorAll('.question')){
        if(!selected.has(q.id)){q.remove();continue;}
        q.hidden=false;delete q.dataset.done;delete q.dataset.homework;
        for(const label of q.querySelectorAll('.question-top label'))label.remove();
        if(!$('homework-answers').checked){q.querySelector('.answer').remove();q.querySelector('.answer-toggle').remove();}
        else{q.querySelector('.answer').hidden=true;q.querySelector('.answer-toggle').setAttribute('aria-expanded','false');q.querySelector('.answer-toggle').textContent='Show answer';}
      }
      for(const context of clone.querySelectorAll('.context'))context.open=true;
      for(const image of clone.querySelectorAll('img'))image.setAttribute('loading','eager');
      clone.querySelector('.set-heading p').textContent=`${clone.querySelectorAll('.question').length} assigned question${clone.querySelectorAll('.question').length===1?'':'s'}`;
      main.append(clone);
    }
    body.append(main);
    const footer=output.createElement('footer');footer.textContent='Source: BC Science Physics 11, Chapter 2 Kinematics, Edvantage Interactive (2012).';body.append(footer);
    if($('homework-answers').checked){
      const script=output.createElement('script');script.textContent="document.querySelectorAll('[data-answer-toggle]').forEach(button=>button.addEventListener('click',()=>{const panel=document.getElementById(button.getAttribute('aria-controls'));panel.hidden=!panel.hidden;button.setAttribute('aria-expanded',String(!panel.hidden));button.textContent=panel.hidden?'Show answer':'Hide answer';}));";body.append(script);
    }
    const blob=new Blob(['<!doctype html>\n'+output.documentElement.outerHTML],{type:'text/html;charset=utf-8'}),url=URL.createObjectURL(blob),anchor=document.createElement('a');
    anchor.href=url;anchor.download=(title().replace(/[^a-z0-9]+/gi,'-').replace(/^-|-$/g,'').slice(0,80)||'kinematics-homework')+'.html';
    document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
    $('homework-message').textContent='Homework HTML downloaded. Send the file to your student; it works offline.';
  };
  render();
})();
