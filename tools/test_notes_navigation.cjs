/* Navigation preferences survive page changes; restricted storage stays optional. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.PHYSICS_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),key='physics11-notes-navigation-collapsed',saved=new Map();
for(const file of ['vectors-notes.html','kinematics-notes.html','forces-notes.html','newtons-laws-notes.html']){
  const html=fs.readFileSync(path.join(root,file),'utf8');
  for(const blocked of [false,true]){
    const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
    const dom=new JSDOM(html,{url:`https://physics.test/${file}`,runScripts:'dangerously',virtualConsole:vc,beforeParse(w){
      w.print=()=>{};w.scrollBy=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
      Object.defineProperty(w,'localStorage',{get(){
        if(blocked)throw new Error('Storage unavailable');
        return {getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v)};
      }});
    }});
    try{
      const d=dom.window.document,button=d.getElementById('navigation-toggle'),sidebar=d.getElementById('notes-navigation');
      assert.deepEqual(errors,[]);
      if(blocked){
        assert.ok(!sidebar.hidden);button.click();assert.ok(sidebar.hidden);button.click();assert.ok(!sidebar.hidden);
      }else{
        if(file!=='vectors-notes.html')assert.ok(sidebar.hidden,'Previous page’s collapsed preference carries to '+file);
        if(!sidebar.hidden)button.click();assert.ok(sidebar.hidden);assert.equal(saved.get(key),'true');
        // Reload the same page through a second instance of the next loop iteration/page.
      }
      assert.deepEqual(errors,[]);
    }finally{dom.window.close();}
  }
}
console.log('Passed: navigation preference carries across all four notes pages and toggles work when storage is unavailable.');
