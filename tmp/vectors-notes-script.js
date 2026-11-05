
(()=>{
const cards=[...document.querySelectorAll('.section-card')],links=[...document.querySelectorAll('nav a')],search=document.querySelector('#search'),nav=document.querySelector('.slide-nav'),empty=document.querySelector('#empty');
let mode='study',slide=0;
function visibleCards(){const q=search.value.trim().toLowerCase();return cards.filter(c=>c.dataset.search.includes(q));}
function render(){const visible=visibleCards();slide=Math.max(0,Math.min(slide,visible.length-1));cards.forEach(c=>{const match=visible.includes(c);c.hidden=!match||(mode==='slides'&&c!==visible[slide]);c.dataset.searchHidden=String(!match);});links.forEach((a,i)=>{a.hidden=!visible.includes(cards[i]);a.classList.toggle('active',mode==='slides'&&cards[i]===visible[slide]);if(mode==='slides'&&cards[i]===visible[slide])a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');});nav.hidden=mode!=='slides'||!visible.length;empty.hidden=!!visible.length;document.querySelector('#slide-position').textContent=`Topic ${visible.length?slide+1:0} of ${visible.length}`;document.querySelector('#previous').disabled=slide===0;document.querySelector('#next').disabled=slide>=visible.length-1;}
document.querySelectorAll('.mode-control button').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;document.body.dataset.mode=mode;document.querySelectorAll('.mode-control button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));if(mode==='simple')search.value='';render();}));
search.addEventListener('input',()=>{slide=0;render();});
function move(delta){slide+=delta;render();document.querySelector('#main').scrollIntoView({behavior:'smooth',block:'start'});}
document.querySelector('#previous').addEventListener('click',()=>move(-1));document.querySelector('#next').addEventListener('click',()=>move(1));
links.forEach(a=>a.addEventListener('click',e=>{if(mode!=='slides')return;e.preventDefault();const target=document.querySelector(a.getAttribute('href'));slide=visibleCards().indexOf(target);render();target.scrollIntoView({behavior:'smooth',block:'start'});}));
document.addEventListener('keydown',e=>{if(mode!=='slides'||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||e.target.closest('input,textarea,select,button,summary,a'))return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();move(e.key==='ArrowRight'?1:-1);}});
document.querySelector('#print').addEventListener('click',()=>window.print());
render();
})();
