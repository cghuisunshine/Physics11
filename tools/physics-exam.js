/* Saved mock exams are independent of practice attempts. No network or automatic grading. */
(function(root){
'use strict';
const types=['Practice','Quick check','Section review','Chapter review','Extra practice','Challenge'];
const iso=n=>new Date(n).toISOString(),date=s=>typeof s==='string'&&s.length<=50&&Number.isFinite(Date.parse(s));
const scopeKey=topics=>[...topics].sort().join('|');
function active(state){return (state.exams||[]).find(e=>e.status==='active')||null;}
function exposed(state){return new Set([...Object.keys(state.exposures||{}),...state.attempts.map(a=>a.id),...Object.keys(state.items),...(state.exams||[]).flatMap(e=>e.ids)]);}
function pool(bank,state,topics){const seen=exposed(state);return bank.filter(p=>types.includes(p.questionType)&&topics.includes(p.topic)&&!seen.has(p.id));}
function shuffle(values,rng){const out=values.slice();for(let i=out.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;}
function start(bank,state,topics,count,minutes,now=Date.now(),rng=Math.random){
  if(active(state))throw Error('Finish the current exam first.');
  if((state.exams||[]).length>=200)throw Error('This profile has reached its 200-exam limit. Export a backup before starting a new profile.');
  const known=[...new Set(bank.map(p=>p.topic))];
  if(!Array.isArray(topics)||!topics.length||new Set(topics).size!==topics.length||topics.some(t=>!known.includes(t)))throw Error('Choose one or more topics.');
  if(!Number.isInteger(count)||count<1||count>40||!Number.isInteger(minutes)||minutes<1||minutes>180)throw Error('Use 1–40 questions and 1–180 minutes.');
  if(count<topics.length)throw Error(`Choose at least ${topics.length} questions to include every selected topic.`);
  const available=pool(bank,state,topics);
  const missing=topics.filter(t=>!available.some(p=>p.topic===t));
  if(missing.length)throw Error('Some selected topics have no unseen exam questions. Narrow the topic selection; previously seen questions will not be reused.');
  if(available.length<count)throw Error(`Only ${available.length} unseen exam questions remain in this selection. Reduce the question count.`);
  // Spread questions over topics and estimated levels; no mastery-based selection in exams.
  const groups=new Map(shuffle(topics,rng).map(t=>{const levels=shuffle([1,2,3],rng).map(level=>shuffle(available.filter(p=>p.topic===t&&p.level===level),rng)),questions=[];while(levels.some(list=>list.length))for(const list of levels)if(list.length)questions.push(list.shift());return [t,questions];}));
  const chosen=[];while(chosen.length<count)for(const list of groups.values()){if(list.length&&chosen.length<count)chosen.push(list.shift());}
  const ids=shuffle(chosen,rng).map(p=>p.id);
  const exam={id:'exam-'+now+'-'+Math.floor(rng()*1e9),status:'active',topics:topics.slice(),ids,startedAt:iso(now),deadlineAt:iso(now+minutes*60000),responses:{},marks:{},index:0};
  state.exams=state.exams||[];state.exams.push(exam);return exam;
}
function remaining(exam,now=Date.now()){return Math.max(0,Math.ceil((Date.parse(exam.deadlineAt)-now)/1000));}
function answer(exam,id,text,ink=null,now=Date.now()){
  if(exam.status!=='active'||!remaining(exam,now))throw Error('The exam has ended.');
  if(!exam.ids.includes(id)||typeof text!=='string'||text.length>12000)throw Error('Invalid exam answer.');
  if(ink&&!root.Practice.normalizeInk(ink))throw Error('The drawing is too large to save. Shorten it before continuing.');
  exam.responses[id]={text,...(ink?{ink:root.Practice.normalizeInk(ink)}:{})};
}
function submit(exam,now=Date.now()){
  if(exam.status!=='active')return false;
  exam.status='submitted';exam.submittedAt=iso(Math.min(now,Date.parse(exam.deadlineAt)));exam.timedOut=now>=Date.parse(exam.deadlineAt);return true;
}
function validMark(m){return !!m&&Number.isFinite(m.earned)&&Number.isFinite(m.possible)&&m.possible>0&&m.possible<=1000&&m.earned>=0&&m.earned<=m.possible;}
function grade(exam,marks,review,now=Date.now()){
  if(exam.status!=='submitted')throw Error('Submit the exam before marking.');
  if(!marks||Object.keys(marks).length!==exam.ids.length||!exam.ids.every(id=>validMark(marks[id])))throw Error('Enter earned and possible marks for every question, including zero for unanswered questions.');
  // Blank answers cannot receive credit; all planned marks stay in the denominator.
  if(exam.ids.some(id=>!exam.responses[id]?.text.trim()&&!exam.responses[id]?.ink&&marks[id].earned>0))throw Error('Unanswered questions must receive zero marks.');
  if(!review||!['self','teacher'].includes(review.by)||typeof review.representative!=='boolean')throw Error('Choose who marked this exam.');
  exam.marks=JSON.parse(JSON.stringify(marks));exam.review={by:review.by,representative:review.representative};exam.markedAt=iso(now);
}
function score(exam,bank,topic){
  const ids=topic?exam.ids.filter(id=>bank.find(p=>p.id===id)?.topic===topic):exam.ids;
  if(!exam.markedAt||!ids.length||!ids.every(id=>validMark(exam.marks[id])))return null;
  const earned=ids.reduce((s,id)=>s+exam.marks[id].earned,0),possible=ids.reduce((s,id)=>s+exam.marks[id].possible,0);
  return {earned,possible,percent:100*earned/possible};
}
function readiness(state,bank,topics){
  const exams=(state.exams||[]).filter(e=>e.status==='submitted'&&scopeKey(e.topics)===scopeKey(topics)).sort((a,b)=>Date.parse(b.submittedAt)-Date.parse(a.submittedAt));
  const marked=exams.filter(e=>score(e,bank)),latest=marked[0];
  const qualified=marked.filter(e=>e.review?.by==='teacher'&&e.review.representative&&e.ids.length>=Math.max(10,topics.length)&&topics.every(t=>e.ids.some(id=>bank.find(p=>p.id===id)?.topic===t)));
  // The latest two qualifying exams must both pass; older successes cannot mask a recent miss.
  const pair=qualified.slice(0,2),consistent=pair.length===2&&pair.every(e=>score(e,bank).percent>=90)&&Date.parse(pair[0].startedAt)-Date.parse(pair[1].submittedAt)>=7*86400000&&!pair[0].ids.some(id=>pair[1].ids.includes(id));
  let status='Not assessed';
  if(latest)status=consistent&&score(latest,bank).percent>=90?'Ready':score(latest,bank).percent>=85?'Nearly ready':'Needs practice';
  return {status,exams,latest,qualified,pair,topics:topics.map(topic=>({topic,score:latest?score(latest,bank,topic):null})),ready:status==='Ready'};
}
function valid(state,bank){
  const ids=new Set(bank.map(p=>p.id)),topics=new Set(bank.map(p=>p.topic));
  if(state.exposures!==undefined&&(!state.exposures||typeof state.exposures!=='object'||Array.isArray(state.exposures)||!Object.entries(state.exposures).every(([id,at])=>ids.has(id)&&date(at))))return false;
  if(state.exams===undefined)return true;
  if(!Array.isArray(state.exams)||state.exams.length>200||state.exams.filter(e=>e?.status==='active').length>1||new Set(state.exams.map(e=>e?.id)).size!==state.exams.length)return false;
  return state.exams.every(e=>{
    if(!e||typeof e.id!=='string'||e.id.length>100||!['active','submitted'].includes(e.status)||!Array.isArray(e.ids)||!e.ids.length||e.ids.length>40||new Set(e.ids).size!==e.ids.length||!e.ids.every(id=>ids.has(id))||!Array.isArray(e.topics)||!e.topics.length||new Set(e.topics).size!==e.topics.length||!e.topics.every(t=>topics.has(t))||!e.ids.every(id=>e.topics.includes(bank.find(p=>p.id===id).topic))||!date(e.startedAt)||!date(e.deadlineAt)||Date.parse(e.deadlineAt)-Date.parse(e.startedAt)<60000||Date.parse(e.deadlineAt)-Date.parse(e.startedAt)>180*60000||!Number.isInteger(e.index)||e.index<0||e.index>=e.ids.length)return false;
    if(!e.responses||typeof e.responses!=='object'||Array.isArray(e.responses)||!Object.entries(e.responses).every(([id,r])=>e.ids.includes(id)&&r&&typeof r.text==='string'&&r.text.length<=12000&&(!r.ink||!!root.Practice.normalizeInk(r.ink))))return false;
    if(!e.marks||typeof e.marks!=='object'||Array.isArray(e.marks)||!Object.entries(e.marks).every(([id,m])=>e.ids.includes(id)&&validMark(m)))return false;
    if(e.status==='active')return !e.submittedAt&&!e.markedAt&&Object.keys(e.marks).length===0;
    if(!date(e.submittedAt)||Date.parse(e.submittedAt)<Date.parse(e.startedAt)||Date.parse(e.submittedAt)>Date.parse(e.deadlineAt)||typeof e.timedOut!=='boolean')return false;
    if(!e.markedAt)return Object.keys(e.marks).length===0&&!e.review;
    return date(e.markedAt)&&Date.parse(e.markedAt)>=Date.parse(e.submittedAt)&&Object.keys(e.marks).length===e.ids.length&&e.ids.every(id=>validMark(e.marks[id])&&((e.responses[id]?.text.trim()||e.responses[id]?.ink)||e.marks[id].earned===0))&&['self','teacher'].includes(e.review?.by)&&typeof e.review.representative==='boolean';
  });
}
const api={types,active,exposed,pool,start,remaining,answer,submit,grade,score,readiness,valid};
root.PhysicsExam=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
