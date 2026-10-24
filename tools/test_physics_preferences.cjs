/* Per-student settings use the same local, backup and sync path as progress. */
const assert=require('node:assert/strict');
module.exports=async function({page,html,bank,login,change,chooseTopics,checkedTopics,history,storageOf,until,pause,fakeFirebase}){
  const p=page();login(p,'Preferences Ada');
  const topics=[...new Set(bank.filter(q=>q.chapter==='bc-ch3').map(q=>q.topic))].slice(0,2);
  change(p,'practice-chapter','bc-ch3');chooseTopics(p,topics);change(p,'mode','coach');
  const expected={mode:'coach',chapter:'bc-ch3',topics};
  assert.deepEqual(history(p,'Preferences Ada').preferences,expected,'Choices save before answering a question');
  assert.equal(history(p,'Preferences Ada').attempts.length,0);
  login(p,'Preferences Ben');
  assert.equal(p.$('mode').value,'adaptive');assert.equal(p.$('practice-chapter').value,'');
  assert.equal(checkedTopics(p).length,new Set(bank.map(q=>q.topic)).size,'New students start with their own defaults');
  change(p,'mode','random');p.$('topic-clear').click();
  login(p,'preferences ada');
  assert.equal(p.$('mode').value,'coach');assert.equal(p.$('practice-chapter').value,'bc-ch3');
  assert.deepEqual(checkedTopics(p),topics);assert.equal(p.$('adaptive-panel').hidden,false);
  const reload=page(html,{storage:storageOf(p)});await pause();
  assert.equal(reload.$('mode').value,'coach');assert.equal(reload.$('practice-chapter').value,'bc-ch3');assert.deepEqual(checkedTopics(reload),topics);
  login(reload,'Preferences Ben');
  assert.equal(reload.$('mode').value,'random');assert.deepEqual(checkedTopics(reload),[],'An intentionally empty selection survives switching and reload');
  assert.equal(reload.$('source').hidden,true);
  login(reload,'Preferences Ada');change(reload,'practice-chapter','');
  const mixed=[bank[0].topic,topics[0]];chooseTopics(reload,mixed);change(reload,'mode','chapter');
  const crossChapter=page(html,{storage:storageOf(reload)});await pause();
  assert.equal(crossChapter.$('practice-chapter').value,'');assert.equal(crossChapter.$('mode').value,'chapter');assert.deepEqual(checkedTopics(crossChapter),mixed);
  const packed=JSON.parse(JSON.stringify(crossChapter.w.Practice.compact(crossChapter.w.Practice.hydrate(history(reload,'Preferences Ada'),bank))));
  assert.deepEqual(packed.preferences,{mode:'chapter',chapter:'',topics:mixed},'Backup hydration retains preferences');
  const stale=crossChapter.w.Practice.normalizePreferences({mode:'removed',chapter:'removed',topics:[bank[0].topic,'removed']},bank);
  assert.equal(stale.mode,'adaptive');assert.equal(stale.chapter,'');assert.deepEqual(Array.from(stale.topics),[bank[0].topic]);
  const key='AIza'+'p'.repeat(35),remoteState={version:1,attempts:[],items:{},preferences:expected};
  // Store IDs encode spaces; use the same canonical id as StudentStore.
  const remoteFirebase=fakeFirebase({[encodeURIComponent('preferences sync')]:{version:1,student:'Preferences sync',updatedAt:'2026-01-01T00:00:00.000Z',state:JSON.stringify(remoteState)}});
  const synced=page(html,{storage:{physics11FirebaseApiKey:key},firebase:remoteFirebase});login(synced,'Preferences sync');
  await until(()=>synced.$('mode').value==='coach');
  assert.equal(synced.$('practice-chapter').value,'bc-ch3');assert.deepEqual(checkedTopics(synced),topics);
  assert.equal(remoteFirebase.writes.length,0,'Signing in cannot overwrite older synced progress with new defaults');
  change(synced,'mode','random');await pause();
  assert.equal(JSON.parse(remoteFirebase.writes.at(-1).data.state).preferences.mode,'random','Preference changes use optional sync');
  for(const instance of [p,reload,crossChapter,synced]){assert.deepEqual(instance.errors,[]);instance.w.close();}
};
