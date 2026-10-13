/* The compact menu remains accessible and leaves reading controls functional. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..');
for(const name of ['vectors','kinematics','forces','newtons-laws']){
  const file=name+'-notes.html',errors=[],vc=new VirtualConsole();let printed=0;
  vc.on('jsdomError',e=>errors.push(e));
  const dom=new JSDOM(fs.readFileSync(path.join(root,file),'utf8'),{url:'https://physics.test/'+file,runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
    w.print=()=>printed++;w.scrollBy=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
    w.HTMLElement.prototype.getBoundingClientRect=function(){
      if(this.classList.contains('toolbar-wrap'))return {top:12,bottom:56,height:44};
      const cards=[...w.document.querySelectorAll('.section-card')],index=cards.indexOf(this);
      return {top:100+Math.max(0,index)*500,bottom:550+Math.max(0,index)*500,height:450};
    };
  }});
  try{
    const w=dom.window,d=w.document,$=id=>d.getElementById(id),menu=$('notes-menu'),toggle=$('notes-menu-toggle'),nav=$('navigation-toggle');
    const key=(target,value)=>target.dispatchEvent(new w.KeyboardEvent('keydown',{key:value,bubbles:true,cancelable:true}));
    assert.deepEqual(errors,[]);assert.ok(menu.hidden);assert.equal(toggle.getAttribute('aria-expanded'),'false');
    assert.equal(toggle.getAttribute('aria-controls'),menu.id);assert.ok(toggle.querySelector('svg'));
    assert.equal(menu.querySelectorAll('.mode-control button').length,3);assert.ok(menu.contains($('print')));
    assert.ok(menu.querySelector('a.source-link[href]'),'Original source link is available inside the menu');
    assert.equal(d.querySelector('.top a'),null,'The header no longer duplicates the source control');
    assert.ok(!menu.contains(nav),'The sidebar icon remains independently available');
    assert.ok(nav.querySelector('svg'));assert.equal(nav.getAttribute('aria-label'),'Hide navigation');
    toggle.click();assert.ok(!menu.hidden);assert.equal(toggle.getAttribute('aria-label'),'Close notes menu');
    d.querySelector('.hero h1').click();assert.ok(menu.hidden,'Clicking outside dismisses the menu');
    toggle.click();d.querySelector('.mode-control button').focus();key(d.activeElement,'Escape');
    assert.ok(menu.hidden);assert.equal(d.activeElement,toggle,'Escape returns focus to the menu button');
    toggle.click();$('search').focus();assert.ok(menu.hidden,'Tabbing or focusing outside dismisses the menu');
    toggle.click();$('print').click();assert.equal(printed,1);assert.ok(menu.hidden);assert.equal(d.activeElement,toggle);
    toggle.click();d.querySelector('[data-mode="slides"]').click();
    assert.equal(d.body.dataset.mode,'slides');assert.ok(menu.hidden);assert.equal(d.activeElement,toggle);
    const first=d.querySelector('.section-card:not([hidden])').id;
    toggle.click();key(toggle,'ArrowRight');assert.equal(d.querySelector('.section-card:not([hidden])').id,first,'Menu key presses do not change slides');
    key(toggle,'Escape');key(toggle,'ArrowRight');assert.notEqual(d.querySelector('.section-card:not([hidden])').id,first,'Slide keyboard navigation works after closing the menu');
    nav.click();assert.ok($('notes-navigation').hidden);assert.equal(nav.getAttribute('aria-label'),'Show navigation');
    assert.equal(nav.title,'Show navigation');assert.ok(nav.querySelector('svg'),'Toggling preserves the sidebar icon');
    nav.click();assert.ok(!$('notes-navigation').hidden);assert.equal(nav.getAttribute('aria-expanded'),'true');
    assert.deepEqual(errors,[]);console.log(file+': passed hamburger controls, outside/Escape/focus dismissal, printing, slide keys, and sidebar icon.');
  }finally{dom.window.close();}
}
