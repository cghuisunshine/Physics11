/* Notes mode changes must keep the current topic on screen and support
   navigation immediately after the Slides button receives focus. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..');
for(const [file,count,query,matchTopic] of [
  ['kinematics-notes.html',11,'a ball off a cliff','topic-10'],
  ['vectors-notes.html',7,'relative velocity: boats','topic-7'],
  ['forces-notes.html',10,"Cavendish's measurement",'topic-3'],
  ['newtons-laws-notes.html',12,'a car on a movable road','topic-8']
]){
const html=fs.readFileSync(path.join(root,file),'utf8');
const errors=[],scrolls=[],virtualConsole=new VirtualConsole();virtualConsole.on('jsdomError',error=>errors.push(error));
let scrollY=0;const frames=[];
const dom=new JSDOM(html,{url:`https://physics.test/${file}`,runScripts:'dangerously',virtualConsole,beforeParse(w){
  w.requestAnimationFrame=callback=>{frames.push(callback);return frames.length;};
  w.HTMLElement.prototype.getBoundingClientRect=function(){
    if(this.classList.contains('toolbar-wrap'))return {top:0,bottom:72};
    if(this.classList.contains('sidebar'))return {top:100,bottom:380};
    if(this.matches('.sidebar nav a')){const number=Number(this.getAttribute('href').split('-')[1]);const top=110+(number-1)*70-w.document.querySelector('.sidebar').scrollTop;return {top,bottom:top+50};}
    const cards=[...w.document.querySelectorAll('.section-card')].filter(c=>!c.hidden),index=cards.indexOf(this);
    const top=400+Math.max(0,index)*524-scrollY;return {top,bottom:top+500};
  };
  w.HTMLElement.prototype.scrollIntoView=function(options){scrolls.push({target:this.id||this.className,options});scrollY=300;};
  w.print=()=>{};
}});
try{
  const w=dom.window,d=w.document,$=id=>d.getElementById(id),cards=[...d.querySelectorAll('.section-card')];
  const visible=()=>cards.filter(c=>!c.hidden).map(c=>c.id),button=mode=>d.querySelector(`.mode-control button[data-mode="${mode}"]`);
  const selectMode=mode=>{if($('notes-menu').hidden)$('notes-menu-toggle').click();button(mode).click();};
  const key=(target,value)=>target.dispatchEvent(new w.KeyboardEvent('keydown',{key:value,bubbles:true,cancelable:true}));
  assert.deepEqual(errors,[]);assert.equal(visible().length,count);
  const active=()=>d.querySelector('.sidebar nav a.active')?.getAttribute('href');
  const flush=()=>{for(const callback of frames.splice(0))callback();};
  assert.equal(active(),'#topic-1');
  const priorScrolls=scrolls.length;
  scrollY=400+4*524-72;w.dispatchEvent(new w.Event('scroll'));flush();
  assert.equal(active(),'#topic-5');assert.equal(d.querySelector('.sidebar nav a.active').getAttribute('aria-current'),'location');
  assert.ok(d.querySelector('.sidebar').scrollTop>0,'Current topic stays visible within a scrolling sidebar');
  assert.equal(scrolls.length,priorScrolls,'Following the current topic does not scroll the main page');
  scrollY=400+524-72;w.dispatchEvent(new w.Event('scroll'));flush();assert.equal(active(),'#topic-2');
  assert.equal(d.querySelectorAll('.sidebar nav a.active').length,1);
  const navigationToggle=$('navigation-toggle'),sidebar=$('notes-navigation');
  assert.equal(navigationToggle.getAttribute('aria-controls'),sidebar.id);
  assert.equal(navigationToggle.getAttribute('aria-expanded'),'true');
  const expandedTopics=visible();
  navigationToggle.click();
  assert.ok(sidebar.hidden);assert.equal(navigationToggle.getAttribute('aria-label'),'Show navigation');
  assert.equal(navigationToggle.getAttribute('aria-expanded'),'false');
  assert.equal(d.body.dataset.navigation,'collapsed');assert.deepEqual(visible(),expandedTopics);
  assert.equal(active(),'#topic-2','Collapsing does not reset the reading topic');
  assert.equal(w.localStorage.getItem('physics11-notes-navigation-collapsed'),'true');
  navigationToggle.click();assert.ok(!sidebar.hidden);assert.equal(active(),'#topic-2');
  assert.equal(navigationToggle.getAttribute('aria-label'),'Hide navigation');
  // The reader is at topic 5 when clicking the sticky Slides button.
  scrollY=400+4*524-72;selectMode('slides');assert.equal(d.activeElement,$('notes-menu-toggle'));
  assert.equal(d.body.dataset.mode,'slides');assert.deepEqual(visible(),['topic-5']);assert.equal($('slide-position').textContent,`Topic 5 of ${count}`);
  assert.ok(!d.querySelector('.slide-nav').hidden);assert.deepEqual(JSON.parse(JSON.stringify(scrolls.at(-1))),{target:'slide-nav',options:{behavior:'instant',block:'start'}});
  assert.equal(button('slides').getAttribute('aria-pressed'),'true');assert.equal(d.querySelector('a[href="#topic-5"]').getAttribute('aria-current'),'step');
  // Focus remains on Slides: left/right keys must still change the topic.
  key($('notes-menu-toggle'),'ArrowRight');assert.deepEqual(visible(),['topic-6']);
  key($('notes-menu-toggle'),'ArrowLeft');assert.deepEqual(visible(),['topic-5']);
  $('next').click();assert.deepEqual(visible(),['topic-6']);$('previous').click();assert.deepEqual(visible(),['topic-5']);
  d.querySelector(`a[href="#topic-${count}"]`).click();assert.deepEqual(visible(),[`topic-${count}`]);assert.ok($('next').disabled);
  key($('notes-menu-toggle'),'ArrowRight');assert.deepEqual(visible(),[`topic-${count}`],'Navigation stays within the topic list');
  d.querySelector('a[href="#topic-1"]').click();assert.ok($('previous').disabled);
  // Typing/search and answer disclosures keep their normal keyboard behavior.
  key($('search'),'ArrowRight');assert.deepEqual(visible(),['topic-1']);
  key(d.querySelector('summary'),'ArrowRight');assert.deepEqual(visible(),['topic-1']);
  button('slides').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',ctrlKey:true,bubbles:true}));assert.deepEqual(visible(),['topic-1']);
  navigationToggle.click();assert.ok(sidebar.hidden);
  key($('notes-menu-toggle'),'ArrowRight');assert.deepEqual(visible(),['topic-2'],'Slides still navigate with the sidebar collapsed');
  $('search').value=query;$('search').dispatchEvent(new w.Event('input'));
  assert.deepEqual(visible(),[matchTopic]);assert.equal($('slide-position').textContent,'Topic 1 of 1');
  navigationToggle.click();assert.ok(!sidebar.hidden);assert.equal($('search').value,query);
  assert.deepEqual(visible(),[matchTopic],'Showing navigation retains the search and selected slide');
  $('search').value='nothing matches this phrase';$('search').dispatchEvent(new w.Event('input'));
  assert.equal(visible().length,0);assert.ok(!$('empty').hidden);assert.ok(d.querySelector('.slide-nav').hidden);
  assert.equal(active(),undefined,'Empty searches clear the current section highlight');
  key($('notes-menu-toggle'),'ArrowRight');assert.equal(visible().length,0);
  selectMode('simple');assert.equal($('search').value,'');assert.equal(visible().length,count);
  assert.ok(sidebar.hidden);assert.ok(navigationToggle.hidden,'Simple mode already hides navigation');
  // Leaving Slides also keeps the topic being read in view.
  selectMode('slides');d.querySelector('a[href="#topic-5"]').click();selectMode('study');
  assert.equal(visible().length,count);assert.equal(scrolls.at(-1).target,'topic-5');
  assert.ok(d.querySelector('.slide-nav').hidden);
  assert.ok(!navigationToggle.hidden);assert.ok(!sidebar.hidden,'Study mode restores the navigation preference');
  const source=fs.readFileSync(path.join(root,'tools/vectors-page.html'),'utf8');
  assert.equal(html.match(/<script>([\s\S]*?)<\/script>/)[1],source.match(/<script>([\s\S]*?)<\/script>/)[1],'The rebuild template retains the fix');
  assert.deepEqual(errors,[]);
  console.log(file+': passed collapsible navigation, retained topic/search, scroll-driven highlights, Slides navigation, and Study/Simple modes.');
}finally{dom.window.close();}
}
