const fs = require('fs'), vm = require('vm'), assert = require('assert');
const content=fs.readFileSync('bc-kinematics-questions.html','utf8');
const inventory=JSON.parse(fs.readFileSync('content/bc-kinematics-questions.json','utf8'));
const script=content.match(/<script>([\s\S]*?)<\/script>/)[1];
const make=(extra={})=>Object.assign({hidden:false,value:'',handlers:{},addEventListener(e,f){this.handlers[e]=f}},extra);
const controls=Object.fromEntries(['search','topic','kind','reset','print','empty','status'].map(k=>['#'+k,make()]));
const all=[]; const checks=[]; const nav={}; const panels={}; const toggles=[];
for(const g of inventory.groups)for(const q of g.questions){
 const panelId='answer-'+q.id;
 assert(content.includes(`id="${panelId}" role="region" aria-labelledby="toggle-${q.id}" hidden`));
 assert(q.answer_html&&q.answer_html.replace(/<[^>]*>/g,'').trim().length>0);
 panels[panelId]=make({hidden:true});
 toggles.push(make({textContent:'Show answer',attrs:{'aria-controls':panelId,'aria-expanded':'false'},getAttribute(k){return this.attrs[k]},setAttribute(k,v){this.attrs[k]=v}}));
}
const sets=inventory.groups.map(g=>{const qs=g.questions.map(q=>{const x=make({dataset:{search:(g.title+' '+q.label+' '+q.text).toLowerCase()}});all.push(x);const c=make({dataset:{complete:q.id},checked:false,closest:()=>x});checks.push(c);return x});nav[`nav a[href="#${g.id}"]`]=make();return make({id:g.id,dataset:{topic:g.topic,kind:g.kind},querySelectorAll:()=>qs})});
const context={document:{getElementById(id){return panels[id]},querySelector(s){return controls[s]||nav[s]},querySelectorAll(s){if(s==='.question-set')return sets;if(s==='.question')return all;if(s==='[data-complete]')return checks;if(s==='[data-answer-toggle]')return toggles;throw Error(s)}},localStorage:{getItem:()=>null,setItem(){}},window:{print(){}}};
vm.runInNewContext(script,context);
const visible=()=>all.filter(q=>!q.hidden).length;
assert.equal(visible(),101);
assert.equal(toggles.length,101);
for(const button of toggles){
 const panel=panels[button.attrs['aria-controls']];
 assert.equal(panel.hidden,true);
 button.handlers.click();assert.equal(panel.hidden,false);assert.equal(button.attrs['aria-expanded'],'true');assert.equal(button.textContent,'Hide answer');
 button.handlers.click();assert.equal(panel.hidden,true);assert.equal(button.attrs['aria-expanded'],'false');assert.equal(button.textContent,'Show answer');
}
// Opening one answer must leave the next answer collapsed.
toggles[0].handlers.click();assert.equal(panels['answer-q-1'].hidden,false);assert.equal(panels['answer-q-2'].hidden,true);
controls['#topic'].value='2.3';controls['#topic'].handlers.input();assert.equal(visible(),20);
controls['#kind'].value='Investigation';controls['#kind'].handlers.input();assert.equal(visible(),5);
controls['#reset'].handlers.click();assert.equal(visible(),101);
controls['#kind'].value='Sample prompt';controls['#kind'].handlers.input();assert.equal(visible(),6);
controls['#reset'].handlers.click();controls['#search'].value='golf';controls['#search'].handlers.input();assert(visible()>0&&visible()<101);
controls['#search'].value='unmatchedxyz';controls['#search'].handlers.input();assert.equal(visible(),0);assert.equal(controls['#empty'].hidden,false);
controls['#reset'].handlers.click();checks[0].checked=true;checks[0].handlers.change();assert.equal(all[0].dataset.done,'true');assert(controls['#status'].textContent.includes('1 marked done'));
const images=[...content.matchAll(/<img[^>]+src="([^"]+)"/g)];assert.equal(images.length,109);assert(images.every(m=>m[1].startsWith('data:image/webp;base64,')));
assert.equal((content.match(/data-answer-toggle aria-expanded="false"/g)||[]).length,101);
assert.equal((content.match(/<svg /g)||[]).length,6);
assert(!/<(?:script|link|img)[^>]+(?:src|href)="https?:/i.test(content));
console.log('Passed: 101 complete answers and independent Show/Hide controls; section/type/search filters; empty state; reset; completion controls; 109 embedded images; six inline graphs; no network assets.');
