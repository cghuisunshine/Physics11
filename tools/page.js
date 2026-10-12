(()=>{
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  let saved={};try{saved=JSON.parse(localStorage.getItem('physics11-progress')||'{}')}catch{}
  const lessons=$$('.lesson'), search=$('#lesson-search'), mode=$('#mode');
  let current=0;
  function progress(){const n=$$('.complete input:checked').length; const el=$('#progress-count');if(el)el.textContent=`${n} of ${lessons.length} lessons marked complete`;if($('#progress'))$('#progress').value=n;
    $$('.unit-card').forEach(c=>{const ids=c.dataset.lessons.split(',');const n=ids.filter(id=>saved[id]).length;c.querySelector('.completion').textContent=`${n}/${ids.length} complete`})}
  $$('.complete input').forEach(c=>{c.checked=!!saved[c.dataset.key];c.addEventListener('change',()=>{saved[c.dataset.key]=c.checked;try{localStorage.setItem('physics11-progress',JSON.stringify(saved))}catch{}progress()})});progress();
  function applyFilter(){const q=(search?.value||'').trim().toLowerCase();let visible=0;lessons.forEach((l,i)=>{const match=l.textContent.toLowerCase().includes(q);const show=document.body.classList.contains('mode-slides')?i===current:match;l.hidden=!show;if(show)visible++});if($('#search-status'))$('#search-status').textContent=q?`${visible} lesson${visible===1?'':'s'} match your search`:'Search explanations, equations, and examples.';if($('#empty'))$('#empty').hidden=visible>0;if($('#slide-count'))$('#slide-count').textContent=`Lesson ${current+1} of ${lessons.length}`;$$('.sidebar nav a').forEach(a=>{const target=$(a.getAttribute('href'));if(target)a.hidden=!!target.hidden});if($('#prev-slide'))$('#prev-slide').disabled=current===0;if($('#next-slide'))$('#next-slide').disabled=current===lessons.length-1}
  search?.addEventListener('input',applyFilter);
  mode?.addEventListener('change',()=>{document.body.className=mode.value==='study'?'':`mode-${mode.value}`;if(mode.value!=='study')$$('details.solution').forEach(d=>d.open=true);if(mode.value==='study')$$('details.solution').forEach(d=>d.open=false);if(mode.value==='slides'&&search)search.value='';applyFilter()});
  function slide(d){if(!document.body.classList.contains('mode-slides'))return;current=Math.max(0,Math.min(lessons.length-1,current+d));applyFilter();lessons[current]?.scrollIntoView({block:'start'})}
  $('#prev-slide')?.addEventListener('click',()=>slide(-1));$('#next-slide')?.addEventListener('click',()=>slide(1));
  document.addEventListener('keydown',e=>{if(/INPUT|SELECT|TEXTAREA/.test(e.target.tagName))return;if(e.key==='ArrowRight')slide(1);if(e.key==='ArrowLeft')slide(-1)});
  $('#show-answers')?.addEventListener('click',()=>$$('details.solution').forEach(d=>d.open=true));
  $('#hide-answers')?.addEventListener('click',()=>$$('details.solution').forEach(d=>d.open=false));
  $('#print')?.addEventListener('click',()=>window.print());
  let printState=[];window.addEventListener('beforeprint',()=>{printState=$$('details.solution').map(d=>d.open);$$('details.solution').forEach(d=>d.open=true)});window.addEventListener('afterprint',()=>$$('details.solution').forEach((d,i)=>d.open=printState[i]));
  $$('.copy').forEach(b=>b.addEventListener('click',async()=>{const t=b.parentElement.querySelector('pre').textContent;try{await navigator.clipboard.writeText(t);b.textContent='Copied'}catch{const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(b.parentElement.querySelector('pre'));selection.removeAllRanges();selection.addRange(range);b.textContent='Selected: copy with Ctrl/Cmd+C'}setTimeout(()=>b.textContent='Copy equations',2500)}));
  $$('.quiz').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();let score=0;let answered=0;form.querySelectorAll('fieldset').forEach(f=>{const input=f.querySelector('input:checked'),out=f.querySelector('.feedback');if(input)answered++;const ok=input&&input.value===f.dataset.answer;if(ok)score++;out.textContent=!input?'Choose an answer.':ok?'Correct. '+f.dataset.explanation:'Try again. '+f.dataset.explanation;out.style.color=ok?'#216348':'#8a381b'});form.querySelector('.score').textContent=`${score}/${form.querySelectorAll('fieldset').length} correct; ${answered} answered. You can revise and check again.`}));
  applyFilter();
  const bank=$('#textbook-problems');
  if(bank){
    const unit=$('#problem-unit'),query=$('#problem-search'),chapters=$$('.problem-chapter');
    function filterProblems(){
      const searchText=query.value.trim().toLowerCase(),words=searchText.split(/\s+/).filter(Boolean),exactNumber=/^\d+[.-]\d+$/.test(searchText)?searchText.replace('-','.'):null;let count=0,sets=0;
      chapters.forEach(ch=>{
        const eligible=unit.value==='all'||ch.dataset.units.split(',').includes(unit.value);let matches=0;
        ch.querySelectorAll('.problem-module').forEach(module=>{
          let moduleCount=0;
          module.querySelectorAll('.problem-number').forEach(link=>{const show=eligible&&(exactNumber?link.dataset.number===exactNumber:words.every(word=>link.dataset.search.includes(word)));link.hidden=!show;if(show){moduleCount++;matches++}});
          module.hidden=moduleCount===0;
          const tag=module.querySelector('.topic-tag');if(tag.textContent!=='Mixed review'){
            const focus=unit.value==='all'?!!module.dataset.units:module.dataset.units.split(',').includes(unit.value);
            tag.textContent=focus?'Lesson focus':'Extension';tag.classList.toggle('focus',focus);
          }
        });
        ch.hidden=!eligible||matches===0;if(!ch.hidden){sets++;count+=matches;if(words.length)ch.open=true}
      });
      $('#problem-status').textContent=`${count.toLocaleString()} problem${count===1?'':'s'} in ${sets} chapter${sets===1?'':'s'}${words.length?count===1?' matches your search':' match your search':''}.`;
      $('#problem-empty').hidden=count>0;
    }
    function loadPage(page){const img=page.querySelector('img');if(!img.getAttribute('src'))img.src=img.dataset.src}
    function revealPage(id){const page=document.getElementById(id);if(!page)return null;const chapter=page.closest('.problem-chapter');chapter.hidden=false;chapter.open=true;page.open=true;loadPage(page);return page}
    unit.addEventListener('change',filterProblems);query.addEventListener('input',filterProblems);
    $('#problem-reset').addEventListener('click',()=>{unit.value='all';query.value='';filterProblems()});
    $$('.problem-page').forEach(page=>{
      page.addEventListener('toggle',()=>{if(page.open)loadPage(page)});
      page.querySelector('.close-problem-page').addEventListener('click',()=>{page.open=false;page.querySelector('summary').focus()});
    });
    $$('.problem-number').forEach(link=>link.addEventListener('click',event=>{
      if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
      event.preventDefault();$$('.problem-number.selected').forEach(old=>old.classList.remove('selected'));link.classList.add('selected');
      $$('.problem-marker').forEach(marker=>marker.hidden=true);$$('.page-selection').forEach(label=>label.textContent='');
      const pages=link.dataset.pages.split(',');pages.forEach((number,i)=>{const page=revealPage(`problem-page-${number}`);page.querySelector('.page-selection').textContent=i===0?`Problem ${link.dataset.number} starts here`:`Possible continuation of problem ${link.dataset.number}`});
      const page=document.getElementById(link.dataset.target),marker=page.querySelector('.problem-marker');marker.hidden=false;marker.style.top=`${Number(link.dataset.y)/796.68*100}%`;marker.style.left=`${Number(link.dataset.x)/667.3*100-0.5}%`;
      page.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
      page.querySelector('summary').focus({preventScroll:true});
    }));
    function fromHash(){if(/^#problem-page-\d+$/.test(location.hash))revealPage(location.hash.slice(1));if(/^#problems-ch-\d+$/.test(location.hash)){const chapter=document.getElementById(location.hash.slice(1));if(chapter)chapter.open=true}}
    window.addEventListener('hashchange',fromHash);filterProblems();fromHash();
  }
  // Each diagram is generated from the same equations explained in its readout.
  const box=$('.explorer');if(!box)return;const svg=box.querySelector('svg'),out=box.querySelector('output');
  const read=id=>Number(box.querySelector('#'+id)?.value||0), esc=t=>String(t).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const text=(x,y,t,c='#52677b')=>`<text x="${x}" y="${y}" fill="${c}" font-size="15" font-family="system-ui">${esc(t)}</text>`;
  const line=(x1,y1,x2,y2,c='#126b83',w=3)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"/>`;
  const arrow=(x1,y1,x2,y2,c='#126b83')=>{const a=Math.atan2(y2-y1,x2-x1),bx=x2-12*Math.cos(a),by=y2-12*Math.sin(a),dx=5*Math.sin(a),dy=5*Math.cos(a);return line(x1,y1,x2,y2,c)+`<polygon points="${x2},${y2} ${bx+dx},${by-dy} ${bx-dx},${by+dy}" fill="${c}"/>`};
  const circle=(x,y,r,c)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
  function axes(xLabel,yLabel){return line(60,260,600,260,'#a7b8c5',1)+line(60,260,60,35,'#a7b8c5',1)+text(320,310,xLabel)+text(15,22,yLabel)}
  function draw(){const kind=box.dataset.kind;let h='',r='';
    if(kind==='vector'){const a=read('magnitude'),deg=read('angle'),rad=deg*Math.PI/180,x=a*Math.cos(rad),y=a*Math.sin(rad);const ox=300,oy=150,s=5;h=line(70,oy,590,oy,'#b9c8d2',1)+line(ox,35,ox,260,'#b9c8d2',1)+arrow(ox,oy,ox+x*s,oy-y*s)+line(ox,oy,ox+x*s,oy,'#b96720')+line(ox+x*s,oy,ox+x*s,oy-y*s,'#b96720')+circle(ox+x*s,oy-y*s,6,'#126b83')+text(490,175,'+x')+text(310,45,'+y')+text(30,290,'Blue: vector   Orange: component projections');r=`Magnitude = ${a.toFixed(1)} N; angle = ${deg}° from +x\nFₓ = ${x.toFixed(2)} N; Fᵧ = ${y.toFixed(2)} N`}
    if(kind==='motion'){const v0=read('initial-speed'),a=read('acceleration'),t=read('duration'),vf=v0+a*t,dx=v0*t+.5*a*t*t,min=Math.min(0,v0,vf),max=Math.max(1,v0,vf),span=max-min;const yy=v=>245-(v-min)*195/span;h=axes('Time (s)','Velocity (m/s)')+line(60,yy(0),600,yy(0),'#b9c8d2',1)+`<polygon points="60,${yy(0)} 60,${yy(v0)} 580,${yy(vf)} 580,${yy(0)}" fill="#d9efef"/>`+line(60,yy(v0),580,yy(vf))+text(65,yy(v0)-8,`${v0.toFixed(1)} m/s`)+text(435,yy(vf)-8,`${vf.toFixed(1)} m/s`)+text(60,280,'0')+text(580,280,String(t));r=`Final velocity = ${vf.toFixed(2)} m/s\nDisplacement (signed graph area) = ${dx.toFixed(2)} m\nAcceleration (slope) = ${a.toFixed(1)} m/s²; elapsed time = ${t.toFixed(1)} s`}
    if(kind==='projectile'){const v=read('launch-speed'),deg=read('launch-angle'),height=read('height'),rad=deg*Math.PI/180,vx=v*Math.cos(rad),vy=v*Math.sin(rad),t=(vy+Math.sqrt(vy*vy+2*9.81*height))/9.81,R=vx*t,H=height+vy*vy/(2*9.81),xScale=520/Math.max(1,R),yScale=205/Math.max(1,H);let pts=[];for(let i=0;i<=80;i++){const ti=t*i/80;pts.push(`${60+vx*ti*xScale},${260-(height+vy*ti-.5*9.81*ti*ti)*yScale}`)}h=axes('Horizontal distance (m)','Height above ground (m)')+`<polyline points="${pts.join(' ')}" fill="none" stroke="#126b83" stroke-width="3"/>`+text(64,280,'0')+text(480,280,`${R.toFixed(1)} m`)+text(80,45,`Peak: ${H.toFixed(1)} m`);r=`v₀ₓ = ${vx.toFixed(2)} m/s; v₀ᵧ = ${vy.toFixed(2)} m/s\nFlight time = ${t.toFixed(2)} s; range = ${R.toFixed(2)} m\nMaximum height above ground = ${H.toFixed(2)} m. No drag; axes scale independently.`}
    if(kind==='forces'){const m=read('mass'),p=read('push'),mu=read('friction'),N=m*9.81,f=mu*N,a=(p-f)/m;h=line(70,235,600,235,'#a7b8c5',2)+`<rect x="265" y="130" width="100" height="100" fill="#e8f3f4" stroke="#126b83"/>`+arrow(315,180,315,55)+text(325,65,`N = ${N.toFixed(1)} N`)+arrow(315,180,315,280,'#b96720')+text(325,280,`mg = ${N.toFixed(1)} N`)+arrow(315,180,520,180)+text(420,155,`Pull: ${p.toFixed(1)} N`)+arrow(315,180,110,180,'#b96720')+text(60,155,`Friction: ${f.toFixed(1)} N`)+text(65,25,'Forces on a block already sliding right; arrows show directions only');r=`Normal force = ${N.toFixed(2)} N; kinetic friction = ${f.toFixed(2)} N\nHorizontal net force = ${(p-f).toFixed(2)} N; acceleration = ${a.toFixed(2)} m/s²\nThe block is assumed to be sliding right at this instant; negative a means it slows.`}
    if(kind==='ramp'){const m=read('mass'),deg=read('incline'),mu=read('friction'),rad=deg*Math.PI/180,N=m*9.81*Math.cos(rad),par=m*9.81*Math.sin(rad),a=9.81*(Math.sin(rad)-mu*Math.cos(rad));const x1=120,y1=255,x2=480,y2=255-190*Math.tan(rad)/Math.tan(60*Math.PI/180);h=line(x1,y1,x2,y2,'#126b83',4)+line(x1,y1,x2,y1,'#a7b8c5',1)+`<rect x="280" y="${(y1+y2)/2-30}" width="50" height="30" fill="#d9efef" stroke="#126b83" transform="rotate(${-Math.atan2(y1-y2,x2-x1)*180/Math.PI} 300 ${(y1+y2)/2})"/>`+text(70,45,`Ramp angle: ${deg}° (illustration not to scale)`)+text(400,280,'Downhill is positive')+text(80,90,`Normal: ${N.toFixed(1)} N`)+text(80,115,`Downslope gravity: ${par.toFixed(1)} N`)+text(80,140,`Uphill friction: ${(mu*N).toFixed(1)} N`);r=`N = mg cos θ = ${N.toFixed(2)} N\na = g(sin θ - μₖ cos θ) = ${a.toFixed(2)} m/s² downhill\nModel: already sliding downhill; this is not a static-friction release test.`}
    if(kind==='energy'){const m=read('mass'),h0=read('start-height'),hNow=read('current-height')/100*h0,U=m*9.81*hNow,K=m*9.81*(h0-hNow),E=U+K,v=Math.sqrt(2*9.81*(h0-hNow)),scale=190/Math.max(1,E);h=line(60,260,600,260,'#a7b8c5',1)+`<rect x="110" y="${260-U*scale}" width="95" height="${U*scale}" fill="#126b83"/><rect x="280" y="${260-K*scale}" width="95" height="${K*scale}" fill="#dba34f"/><rect x="450" y="${260-E*scale}" width="95" height="${E*scale}" fill="#52677b"/>`+text(110,285,'Potential U')+text(280,285,'Kinetic K')+text(450,285,'Total E')+text(80,35,'Energy (J): frictionless fall from rest');r=`Current height = ${hNow.toFixed(2)} m above the chosen zero\nU = ${U.toFixed(2)} J; K = ${K.toFixed(2)} J; total = ${E.toFixed(2)} J\nSpeed = ${v.toFixed(2)} m/s (mass cancels from speed).`}
    if(kind==='circuit'){const V=read('voltage'),r1=read('resistance1'),r2=read('resistance2'),parallel=box.querySelector('#connection').value==='parallel',R=parallel?r1*r2/(r1+r2):r1+r2,I=V/R,i1=parallel?V/r1:I,i2=parallel?V/r2:I,v1=i1*r1,v2=i2*r2;h=line(90,80,550,80)+line(90,80,90,140)+line(90,180,90,235)+line(90,235,550,235)+line(65,140,115,140,'#b96720',4)+line(75,180,105,180,'#b96720',4)+text(20,167,`${V} V`);if(parallel){h+=line(250,80,250,125)+line(250,175,250,235)+line(550,80,550,125)+line(550,175,550,235)+`<rect x="225" y="125" width="50" height="50" fill="#e8f3f4" stroke="#126b83"/><rect x="525" y="125" width="50" height="50" fill="#e8f3f4" stroke="#126b83"/>`+text(280,155,`${r1} Ω`)+text(460,155,`${r2} Ω`)}else{h+=line(550,80,550,235)+`<rect x="210" y="60" width="80" height="40" fill="#e8f3f4" stroke="#126b83"/><rect x="390" y="60" width="80" height="40" fill="#e8f3f4" stroke="#126b83"/>`+text(220,50,`${r1} Ω`)+text(400,50,`${r2} Ω`)}h+=text(120,280,`Ideal battery, ideal wires, two ${parallel?'parallel':'series'} resistors`);r=`Equivalent resistance = ${R.toFixed(2)} Ω; source current = ${I.toFixed(2)} A\nR₁: ${v1.toFixed(2)} V, ${i1.toFixed(2)} A; R₂: ${v2.toFixed(2)} V, ${i2.toFixed(2)} A\nTotal power = ${(V*I).toFixed(2)} W.`}
    if(kind==='wave'){const f=read('frequency'),v=read('wave-speed'),A=read('amplitude'),lambda=v/f,L=4;let pts=[];for(let i=0;i<=200;i++){const x=L*i/200;pts.push(`${60+520*x/L},${150-65*A*Math.sin(2*Math.PI*x/lambda)}`)}h=line(60,150,600,150,'#a7b8c5',1)+line(60,250,600,250,'#a7b8c5',1)+`<polyline points="${pts.join(' ')}" fill="none" stroke="#126b83" stroke-width="3"/>`+text(15,25,'Displacement (cm) at one instant')+text(60,275,'0 m')+text(545,275,'4.0 m')+text(75,305,'Position along medium; this is a spatial snapshot, not a time graph');r=`Frequency = ${f.toFixed(1)} Hz; speed = ${v.toFixed(1)} m/s\nWavelength = v/f = ${lambda.toFixed(2)} m; period = ${(1/f).toFixed(3)} s\nAmplitude = ${A.toFixed(1)} cm. Changing amplitude leaves λ unchanged in this model.`}
    svg.innerHTML=`<title>${esc(box.querySelector('h2').textContent)}</title>`+h;out.textContent=r;
  }
  box.querySelectorAll('input,select').forEach(i=>i.addEventListener('input',draw));draw();
})();
