/* Pure practice logic, shared by the browser and Node tests. */
(function (root) {
  'use strict';
  const topics = ['Algebra', 'Geometry', 'Number Theory', 'Combinatorics', 'Probability'];
  const levels = ['Foundation', 'Intermediate', 'Challenge'];
  const gcd = (a,b) => b ? gcd(b,a%b) : a;
  const fraction = (a,b) => `${a/gcd(a,b)}/${b/gcd(a,b)}`;
  function stats(state, topic) {
    const attempts = state.attempts.filter(a => (!topic || a.topic === topic) && !a.review);
    const recent = attempts.slice(-12);
    return {total: attempts.length, correct: attempts.filter(a=>a.correct).length,
      mastery: (recent.filter(a=>a.correct).length+2)/(recent.length+4)};
  }
  function targetLevel(state, topic) {
    const recent = state.attempts.filter(a=>a.topic===topic && !a.review).slice(-5);
    if (!recent.length) return 1;
    let level = recent[recent.length-1].level;
    const last = recent.slice(-2);
    if (last.length === 2 && last.every(a=>a.correct && a.level===level)) level++;
    else if (!recent[recent.length-1].correct) level--;
    return Math.max(1,Math.min(3,level));
  }
  function chooseTopic(state, filter, rng=Math.random) {
    if (topics.includes(filter)) return filter;
    const weights = topics.map(t=>1-stats(state,t).mastery + (stats(state,t).total ? 0 : .2));
    let draw = rng()*weights.reduce((a,b)=>a+b,0);
    return topics.find((t,i)=>(draw-=weights[i])<=0) || topics[4];
  }
  function chooseExam(bank, state, filter, currentId, rng=Math.random) {
    const topic = chooseTopic(state,filter,rng);
    const eligible = bank.filter(p=>!filter || p.topic===filter);
    let unseen = eligible.filter(p=>!state.attempts.some(a=>a.id===p.id));
    const other = unseen.filter(p=>p.id!==currentId);
    if (other.length) unseen = other;
    if (!unseen.length) return null;
    const pool = unseen.filter(p=>p.topic===topic);
    const candidates = pool.length ? pool : unseen;
    const score = p => Math.abs(p.level-targetLevel(state,p.topic));
    const best = Math.min(...candidates.map(score));
    const near = candidates.filter(p=>score(p)===best);
    return near[Math.floor(rng()*near.length)];
  }
  function dayKey(value) {
    const d=new Date(value);
    if(!Number.isFinite(d.getTime()))return '';
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  }
  function pastDays(now=new Date()) {
    return Array.from({length:7},(_,i)=>{const d=new Date(now);d.setHours(0,0,0,0);d.setDate(d.getDate()-i);return {key:dayKey(d),date:d};});
  }
  function dayQuestions(state, day, filter='', excludeCorrect=false) {
    const latest=new Map(), onDay=new Map();
    for(const a of state.attempts){
      const at=Date.parse(a.at);if(!Number.isFinite(at))continue;
      const previous=latest.get(a.id);
      if(!previous||at>=Date.parse(previous.at))latest.set(a.id,a);
      if(dayKey(a.at)===day){const previousDay=onDay.get(a.id);if(!previousDay||at>=Date.parse(previousDay.at))onDay.set(a.id,a);}
    }
    return [...onDay.values()].sort((a,b)=>Date.parse(b.at)-Date.parse(a.at)).filter(a=>!excludeCorrect||!latest.get(a.id).correct)
      .map(a=>state.items[a.id]?.problem).filter(p=>p&&(!filter||p.topic===filter));
  }
  function problemNumber(problem) {
    return Number(problem.id.match(/^exam-\d{4}-(\d+)$/)?.[1]) || 0;
  }
  function yearQuestions(bank, year) {
    return bank.filter(p=>p.kind==='exam' && p.year===Number(year))
      .sort((a,b)=>problemNumber(a)-problemNumber(b));
  }
  function examYears(bank) {
    return [...new Set(bank.filter(p=>p.kind==='exam').map(p=>p.year))].sort((a,b)=>b-a).map(year=>{
      const numbers=new Set(yearQuestions(bank,year).map(problemNumber));
      const missing=Array.from({length:25},(_,i)=>i+1).filter(n=>!numbers.has(n));
      return {year,count:numbers.size,missing};
    });
  }
  function yearProgress(state, questions) {
    const ids=new Set(questions.map(p=>p.id)), latest=new Map();
    for(const a of state.attempts){
      if(!ids.has(a.id) || !Number.isFinite(Date.parse(a.at)))continue;
      const previous=latest.get(a.id);
      if(!previous || Date.parse(a.at)>=Date.parse(previous.at))latest.set(a.id,a);
    }
    return {answered:latest.size,correct:[...latest.values()].filter(a=>a.correct).length,latest};
  }
  function record(state, problem, choice, elapsed) {
    if (!'ABCDE'.includes(choice) || choice.length !== 1) throw Error('Choose A–E.');
    const review = state.attempts.some(a=>a.id===problem.id);
    const correct = choice===problem.answer;
    state.attempts.push({id:problem.id, topic:problem.topic, level:problem.level, kind:problem.kind,
      title:problem.title, choice, answer:problem.answer, correct, review, seconds:elapsed, at:new Date().toISOString()});
    const old = state.items[problem.id] || {};
    state.items[problem.id] = {problem, manual:!!old.manual, missed:!correct, aiConcern:!!old.aiConcern};
    return correct;
  }
  function reviewQueue(state, filter) {
    return Object.values(state.items).filter(x=>(x.manual || x.missed || x.aiConcern) && (!filter || x.problem.topic===filter));
  }
  function generate(topic, level, rng=Math.random) {
    const n=(lo,hi)=>lo+Math.floor(rng()*(hi-lo+1));
    let question, answer, explanation, distractors;
    const a=n(3,9), b=n(2,7), c=n(2,6);
    if (topic==='Algebra') {
      if (level===1) {answer=a*b; question=`A notebook costs $${a}. How much do ${b} notebooks cost?`; explanation=`Multiply the number of notebooks by the price: ${b} × ${a} = ${answer}.`;}
      else if (level===2) {answer=c; question=`What value of x satisfies ${a}x + ${b} = ${a*c+b}?`; explanation=`Subtract ${b}, then divide by ${a}: x = ${a*c} ÷ ${a} = ${c}.`;}
      else {answer=10*c; const total=answer*(100-b*5)/100; question=`After a ${b*5}% discount, a game costs $${total.toFixed(2)}. What was its original price?`; explanation=`The sale price is ${(100-b*5)}% of the original, so divide $${total.toFixed(2)} by ${(100-b*5)/100} to get $${answer}.`;}
    } else if (topic==='Geometry') {
      if (level===1) {answer=2*(a+b); question=`A rectangle is ${a} cm long and ${b} cm wide. What is its perimeter in centimeters?`; explanation=`Add all four sides: 2 × (${a} + ${b}) = ${answer} cm.`;}
      else if (level===2) {answer=a*b; question=`A triangle has base ${2*a} cm and perpendicular height ${b} cm. What is its area in square centimeters?`; explanation=`Triangle area = base × height ÷ 2 = ${2*a} × ${b} ÷ 2 = ${answer}.`;}
      else {answer=a*b+2*c*(a+b)+4*c*c; question=`A ${a} m by ${b} m rectangle is surrounded on every side by a path ${c} m wide. What is the total area of the rectangle and path, in square meters?`; explanation=`The outside dimensions are ${a+2*c} m and ${b+2*c} m. Their product is ${answer} square meters.`;}
    } else if (topic==='Number Theory') {
      if (level===1) {answer=(a*b+c)%a; question=`What is the remainder when ${a*b+c} is divided by ${a}?`; explanation=`${a*b+c} = ${Math.floor((a*b+c)/a)} × ${a} + ${answer}.`;}
      else if (level===2) {answer=a*b/gcd(a,b); question=`Two bells ring every ${a} minutes and every ${b} minutes. They ring together now. In how many minutes will they next ring together?`; explanation=`Find the least common multiple: ${a} × ${b} ÷ gcd(${a}, ${b}) = ${a*b} ÷ ${gcd(a,b)} = ${answer}.`;}
      else {answer=(b+1)*(c+1); question=`How many positive divisors does 2^${b} × 3^${c} have?`; explanation=`A divisor chooses an exponent from 0 to ${b} for 2 and 0 to ${c} for 3: (${b}+1)(${c}+1) = ${answer}.`;}
    } else if (topic==='Combinatorics') {
      if (level===1) {answer=a*b; question=`A café offers ${a} sandwiches and ${b} drinks. How many meals can be made by choosing one sandwich and one drink?`; explanation=`Each sandwich pairs with ${b} drinks, giving ${a} × ${b} = ${answer} meals.`;}
      else if (level===2) {answer=a*(a-1)/2; question=`A club has ${a} members. How many different pairs of members can be chosen?`; explanation=`There are ${a} × ${a-1} ordered choices. Divide by 2 because order does not matter: ${answer}.`;}
      else {answer=(a+1)*(a+2)/2; question=`How many triples of nonnegative integers (x, y, z) satisfy x + y + z = ${a}?`; explanation=`For x = 0 through ${a}, the numbers of choices for y are ${a+1}, ${a}, …, 1. Their sum is (${a+1} × ${a+2}) ÷ 2 = ${answer}.`;}
    } else {
      topic='Probability';
      if (level===1) {answer=fraction(a,a+b); question=`A bag contains ${a} red and ${b} blue marbles. One marble is picked at random. What is the probability it is red?`; explanation=`There are ${a} favorable outcomes out of ${a+b}, so the probability is ${answer}.`;}
      else if (level===2) {answer=fraction(a*(a-1),(a+b)*(a+b-1)); question=`A bag contains ${a} red and ${b} blue marbles. Two marbles are picked without replacement. What is the probability both are red?`; explanation=`Multiply the probabilities: ${a}/${a+b} × ${a-1}/${a+b-1} = ${answer}.`;}
      else {answer=fraction(2*a*b,(a+b)*(a+b-1)); question=`A bag contains ${a} red and ${b} blue marbles. Two marbles are picked without replacement. What is the probability they are different colors?`; explanation=`Count red–blue and blue–red: 2 × ${a}/${a+b} × ${b}/${a+b-1} = ${answer}.`;}
      const value = s=>{const [x,y]=s.split('/').map(Number);return x/y;};
      distractors=[];
      // Canonical reduced fractions prevent equivalent choices.
      for(let d=2;d<=30 && distractors.length<4;d++) for(let k=1;k<d && distractors.length<4;k++) {
        const f=fraction(k,d);
        if(Math.abs(value(f)-value(answer))>1e-9 && !distractors.includes(f)) distractors.push(f);
      }
    }
    if (!distractors) {
      distractors=[];
      for (const offset of [1,-1,2,-2,3,4,5]) if(answer+offset>=0 && distractors.length<4) distractors.push(String(answer+offset));
    }
    const values=[String(answer),...distractors];
    for(let i=4;i>0;i--){const j=n(0,i);[values[i],values[j]]=[values[j],values[i]];}
    // Ignore parameters that do not appear in the question when identifying repeats.
    const keyA=(topic==='Algebra' || topic==='Number Theory') && level===3 ? 0 : a;
    const keyB=topic==='Combinatorics' && level>1 ? 0 : b;
    const usesC=(topic==='Algebra' && level>1)||(topic==='Geometry' && level===3)||(topic==='Number Theory' && level!==2);
    return {id:`new-${topic}-${level}-${keyA}-${keyB}-${usesC?c:0}`, kind:'generated', title:'Original practice question', topic, level,
      text:question, choices:values, answer:'ABCDE'[values.indexOf(String(answer))], explanation};
  }

  // Readable plain text for a LaTeX formula, used when a formula image cannot be loaded.
  const SUP={'0':'\u2070','1':'\u00b9','2':'\u00b2','3':'\u00b3','4':'\u2074','5':'\u2075','6':'\u2076','7':'\u2077','8':'\u2078','9':'\u2079','+':'\u207a','-':'\u207b','n':'\u207f','x':'\u02e3','a':'\u1d43','b':'\u1d47','c':'\u1d9c','k':'\u1d4f'};
  const SUB={'0':'\u2080','1':'\u2081','2':'\u2082','3':'\u2083','4':'\u2084','5':'\u2085','6':'\u2086','7':'\u2087','8':'\u2088','9':'\u2089','n':'\u2099','x':'\u2093','a':'\u2090','i':'\u1d62','k':'\u2096'};
  const SYMBOLS=[[/\\(?:dfrac|tfrac|frac)\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g,'($1/$2)'],[/\\sqrt\s*\{([^{}]*)\}/g,'\u221a($1)'],
    [/\\(?:times)\b/g,'\u00d7'],[/\\(?:cdot)\b/g,'\u00b7'],[/\\(?:div)\b/g,'\u00f7'],[/\\(?:pm)\b/g,'\u00b1'],[/\\(?:leq|le)\b/g,'\u2264'],[/\\(?:geq|ge)\b/g,'\u2265'],
    [/\\(?:neq|ne)\b/g,'\u2260'],[/\\approx\b/g,'\u2248'],[/\\(?:pi)\b/g,'\u03c0'],[/\\(?:theta)\b/g,'\u03b8'],[/\\(?:degree|circ)\b/g,'\u00b0'],[/\\(?:angle)\b/g,'\u2220'],
    [/\\(?:triangle)\b/g,'\u25b3'],[/\\(?:cdots|dots|ldots)\b/g,'\u2026'],[/\\(?:infty)\b/g,'\u221e'],[/\\(?:overline|underline|mathrm|mathbf|operatorname)\s*\{([^{}]*)\}/g,'$1'],
    [/\\(?:qquad|quad|,|;|:|!|\s)/g,' '],[/\\(?:left|right|displaystyle|limits)\b/g,''],[/\\%/g,'%'],[/\\\$/g,'$'],[/\\&/g,'&'],[/\\#/g,'#'],[/\\_/g,'_'],[/\\\\/g,' ']];
  function latexText(input){
    let t=String(input||'');
    t=t.replace(/\\\$/g,'\u0001').replace(/\$+/g,' ');
    for(let i=0;i<4;i++)t=t.replace(/\\(?:boxed|fbox|text|textbf|textit|mbox|mathbf|mathrm)\s*\{([^{}]*)\}/g,'$1');
    t=t.replace(/\^\s*\{?\s*\\(?:circ|degree)\s*\}?/g,'\u00b0');
    for(let i=0;i<3;i++)for(const [re,to] of SYMBOLS)t=t.replace(re,to);
    t=t.replace(/[\^_]\s*\{\s*\}/g,'');
    t=t.replace(/\^\s*\{?([A-Za-z0-9+-]+)\}?/g,(m,g)=>[...g].every(c=>SUP[c])?[...g].map(c=>SUP[c]).join(''):'^'+g);
    t=t.replace(/_\s*\{?([A-Za-z0-9]+)\}?/g,(m,g)=>[...g].every(c=>SUB[c])?[...g].map(c=>SUB[c]).join(''):'_'+g);
    t=t.replace(/\\[A-Za-z]+/g,'').replace(/[{}]/g,'').replace(/\u0001/g,'$');
    return t.replace(/\s+/g,' ').replace(/\s+([,.;?!])/g,'$1').trim();
  }
  const activityDays=root.ActivityMonitor.days;
  const api={activityDays,topics,levels,stats,targetLevel,chooseTopic,chooseExam,record,reviewQueue,generate,latexText,dayKey,pastDays,dayQuestions,problemNumber,yearQuestions,examYears,yearProgress};
  if(typeof module!=='undefined') module.exports=api;
  root.Practice=api;
})(typeof window!=='undefined'?window:globalThis);
