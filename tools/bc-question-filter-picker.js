/* Checkbox menus enhance the existing collection filters for mouse, touch and keyboard. */
(()=>{
  'use strict';
  const pickers=[];
  for(const [id,noun] of [['topic','sections'],['kind','types']]){
    const select=document.getElementById(id),label=document.querySelector(`label[for="${id}"]`);
    const heading=document.createElement('span');heading.id=id+'-label';heading.className='filter-label';heading.textContent=label.textContent;label.replaceWith(heading);
    select.multiple=true;select.value='';select.hidden=true;
    const picker=document.createElement('details'),summary=document.createElement('summary'),menu=document.createElement('div');
    picker.id=id+'-picker';picker.className='filter-picker';summary.id=id+'-summary';summary.setAttribute('aria-labelledby',heading.id+' '+summary.id);
    menu.className='filter-menu';menu.setAttribute('role','group');menu.setAttribute('aria-label',heading.textContent);
    const controls=[...select.options].map(option=>{
      const row=document.createElement('label'),input=document.createElement('input');
      input.type='checkbox';input.value=option.value;input.dataset.filterOption=id;row.append(input,document.createTextNode(option.textContent));menu.append(row);
      input.addEventListener('change',()=>{
        if(!option.value){for(const other of select.options)other.selected=false;}
        else select.options[0].selected=false;
        option.selected=input.checked;select.dispatchEvent(new Event('input',{bubbles:true}));
      });
      return {option,input};
    });
    const sync=()=>{
      const selected=[...select.selectedOptions],all=selected.some(option=>!option.value);
      for(const {option,input} of controls)input.checked=option.selected;
      summary.textContent=all?select.options[0].textContent:!selected.length?'Choose '+noun:selected.length===1?selected[0].textContent:`${selected.length} ${noun} selected`;
      summary.title=selected.map(option=>option.textContent).join('\n');
    };
    select.addEventListener('input',sync);
    picker.append(summary,menu);select.after(picker);sync();pickers.push(picker);
    picker.addEventListener('keydown',event=>{if(event.key==='Escape'){picker.open=false;summary.focus();}});
  }
  document.addEventListener('click',event=>{for(const picker of pickers)if(!picker.contains(event.target))picker.open=false;});
})();
