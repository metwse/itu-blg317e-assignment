const $=i=>document.getElementById(i);
const REGIONS=['Europe & Central Asia','Middle East & North Africa','South Asia','Latin America & Caribbean','Sub-Saharan Africa','East Asia & Pacific','North America'];
const KEY_FIELDS=['id','code','provider_id','economy_code','year'];
const NUM_FIELDS=['year_start','year_end','year'];

window.addEventListener('DOMContentLoaded',()=>{
  const saved=localStorage.getItem('token');
  if(saved)$('token').value=saved;
  $('token').addEventListener('input',()=>localStorage.setItem('token',$('token').value));
});

const getHeaders=()=>({
  'Content-Type':'application/json',
  ...(($('token').value)&&{token:$('token').value})
});

const getId=row=>row.id||row.code||
  (row.provider_id&&row.economy_code&&row.year?`${row.provider_id}/${row.economy_code}/${row.year}`:
  (row.provider_id&&row.economy_code?`${row.provider_id}/${row.economy_code}`:''));

const isKeyField=k=>KEY_FIELDS.includes(k);
const formatValue=val=>val===null?`<span style="color:#888">null</span>`:val;

const toTable=(d,endpoint)=>{
  if(!d||typeof d!=='object')return`<pre class="border p-3 mt-3">${JSON.stringify(d,null,2)}</pre>`;
  const arr=Array.isArray(d)?d:[d];
  if(!arr.length)return'<pre class="border p-3 mt-3">No results</pre>';
  
  const keys=Object.keys(arr[0]);
  const headers=keys.map(k=>`<th>${k}</th>`).join('')+'<th>Actions</th>';
  
  const rows=arr.map(row=>{
    const cells=keys.map(k=>{
      const val=formatValue(row[k]);
      if(isKeyField(k))return`<td>${val}</td>`;
      const rowJson=JSON.stringify(row).replace(/"/g,'&quot;');
      const style=k==='region'?' style="max-width:200px"':'';
      return`<td class="editable-cell"${style} onclick="edit(this,'${endpoint}',${rowJson},'${k}')"><span class="cell-val">${val}</span><span class="edit-icon">✏️</span></td>`;
    }).join('');
    const id=getId(row);
    return`<tr>${cells}<td><button class="btn-trash" onclick="del('${endpoint}${id}','${endpoint}')">🗑️</button></td></tr>`;
  }).join('');
  
  const addRow=endpoint==='/economies/'?
    `<tr class="add-row" id="add-economy-row"><td colspan="${keys.length+1}" style="text-align:center;cursor:pointer;" onclick="showAddEconomyForm()"><span style="color:#0088ff;font-weight:bold;font-size:20px;">+</span> Add New Economy</td></tr>
    <tr class="add-economy-form" id="add-economy-form" style="display:none;">
      <td><input type="text" class="form-control form-control-sm" id="new-code" placeholder="Code" maxlength="3" style="text-transform:uppercase;"></td>
      <td><input type="text" class="form-control form-control-sm" id="new-name" placeholder="Name"></td>
      <td><select class="form-select form-select-sm" id="new-region"><option value="">Choose...</option>${REGIONS.map(r=>`<option value="${r}">${r}</option>`).join('')}</select></td>
      <td><button class="btn btn-sm btn-success" onclick="submitNewCountry()">✓</button> <button class="btn btn-sm btn-secondary" onclick="cancelAddEconomy()">✗</button></td>
    </tr>`:'';
  
  return`<table class="table table-dark table-striped table-bordered mt-3"><thead><tr>${headers}</tr></thead><tbody>${rows}${addRow}</tbody></table>`;
};

const createRegionDropdown=(val,onSave)=>{
  const wrapper=document.createElement('div');
  wrapper.className='continent-dropdown-wrapper';
  const menu=document.createElement('div');
  menu.className='continent-menu';
  menu.style.display='block';
  menu.innerHTML=REGIONS.map(r=>
    `<div class="continent-option" data-value="${r}">${r}</div>`
  ).join('');
  wrapper.appendChild(menu);
  menu.querySelectorAll('.continent-option').forEach(opt=>
    opt.onclick=()=>onSave(opt.dataset.value)
  );
  setTimeout(()=>menu.scrollIntoView({block:'nearest'}),50);
  return wrapper;
};

const edit=(cell,endpoint,row,field)=>{
  const span=cell.querySelector('.cell-val');
  const oldVal=span.textContent;
  
  const save=async(newVal)=>{
    if(newVal===oldVal){
      cell.replaceChild(span,cell.firstChild);
      return;
    }
    try{
      const id=getId(row);
      const body={[field]:NUM_FIELDS.includes(field)?+newVal:newVal};
      await fetch(`/internal${endpoint}${id}`,{method:'PATCH',headers:getHeaders(),body:JSON.stringify(body)});
      api(endpoint,'GET');
    }catch(e){
      alert(`Update failed: ${e.message}`);
      cell.replaceChild(span,cell.firstChild);
    }
  };
  
  if(field==='region'){
    const dropdown=createRegionDropdown(oldVal,save);
    cell.replaceChild(dropdown,span);
    const clickOut=e=>{
      if(!dropdown.contains(e.target)){
        document.removeEventListener('click',clickOut);
        save(oldVal);
      }
    };
    setTimeout(()=>document.addEventListener('click',clickOut),100);
  }else{
    const inp=document.createElement('input');
    inp.className='edit-input';
    inp.value=oldVal;
    cell.replaceChild(inp,span);
    inp.focus();
    inp.onblur=()=>save(inp.value);
    inp.onkeydown=e=>e.key==='Enter'&&inp.blur();
  }
};

const del=async(path,endpoint)=>{
  try{
    await fetch(`/internal${path}`,{method:'DELETE',headers:getHeaders()});
    api(endpoint,'GET');
  }catch(e){
    $('o').innerHTML=`<pre class="border p-3 mt-3">${e.message}</pre>`;
  }
};

const showAddEconomyForm=()=>{
  $('add-economy-row').style.display='none';
  $('add-economy-form').style.display='';
  setTimeout(()=>$('new-code').focus(),50);
};

const cancelAddEconomy=()=>{
  $('add-economy-row').style.display='';
  $('add-economy-form').style.display='none';
};

const submitNewCountry=async()=>{
  const code=$('new-code').value.trim();
  const name=$('new-name').value.trim();
  const region=$('new-region').value||null;
  
  if(!code||code.length!==3)return alert('Economy code must be 3 letters');
  if(!name)return alert('Economy name is required');
  
  try{
    await fetch('/internal/economies/',{method:'POST',headers:getHeaders(),body:JSON.stringify({code,name,region})});
    api('/economies/','GET');
  }catch(e){
    alert(`Failed to add economy: ${e.message}`);
  }
};

const api=async(e,m='GET',b)=>{
  try{
    const r=await fetch(`/internal${e}`,{method:m,headers:getHeaders(),body:b?JSON.stringify(b):null});
    const data=await r.json();
    $('o').innerHTML=m==='GET'&&Array.isArray(data)?toTable(data,e):`<pre class="border p-3 mt-3">${JSON.stringify(data,null,2)}</pre>`;
  }catch(e){
    $('o').innerHTML=`<pre class="border p-3 mt-3">${e.message}</pre>`;
  }
};

window.api=api;
window.del=del;
window.edit=edit;
window.showAddEconomyForm=showAddEconomyForm;
window.cancelAddEconomy=cancelAddEconomy;
window.submitNewCountry=submitNewCountry;
window.$=$;
