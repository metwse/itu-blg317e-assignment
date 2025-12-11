const $=i=>document.getElementById(i);
const REGIONS=['Europe & Central Asia','Middle East & North Africa','South Asia','Latin America & Caribbean','Sub-Saharan Africa','East Asia & Pacific','North America'];
const KEY_FIELDS=['id','code','provider_id','economy_code'];
const NUM_FIELDS=['lat','lng'];

// Load saved token on page load
window.addEventListener('DOMContentLoaded',()=>{
  const saved=localStorage.getItem('token');
  if(saved)$('token').value=saved;
  $('token').addEventListener('input',()=>localStorage.setItem('token',$('token').value));
});

function getHeaders(){
  const h={'Content-Type':'application/json'};
  const t=$('token').value;
  if(t)h['token']=t;
  return h;
}

function getId(row){
  return row.id||row.code||(row.provider_id&&row.economy_code?`${row.provider_id}/${row.economy_code}`:'');
}

function isKeyField(k){
  return KEY_FIELDS.includes(k);
}

function formatValue(val){
  return val===null?`<span style="color:#888">null</span>`:val;
}

function toTable(d,endpoint){
  if(!d||typeof d!=='object')return`<pre class="border p-3 mt-3">${JSON.stringify(d,null,2)}</pre>`;
  const arr=Array.isArray(d)?d:[d];
  if(!arr.length)return'<pre class="border p-3 mt-3">No results</pre>';
  const keys=Object.keys(arr[0]);
  let t='<table class="table table-dark table-striped table-bordered mt-3"><thead><tr>';
  keys.forEach(k=>t+=`<th>${k}</th>`);
  t+='<th>Actions</th></tr></thead><tbody>';
  arr.forEach(row=>{
    t+='<tr>';
    keys.forEach(k=>{
      const val=row[k];
      const displayVal=formatValue(val);
      if(isKeyField(k)){
        t+=`<td>${displayVal}</td>`;
      }else{
        const rowJson=JSON.stringify(row).replace(/"/g,'&quot;');
        const style=k==='region'?' style="max-width:200px"':'';
        t+=`<td class="editable-cell"${style} onclick="edit(this,'${endpoint}',${rowJson},'${k}')"><span class="cell-val">${displayVal}</span><span class="edit-icon">✏️</span></td>`;
      }
    });
    const id=getId(row);
    t+=`<td><button class="btn-trash" onclick="del('${endpoint}${id}','${endpoint}')">🗑️</button></td>`;
    t+='</tr>';
  });
  if(endpoint==='/economies/'){
    t+=`<tr class="add-row" id="add-economy-row"><td colspan="${keys.length+1}" style="text-align:center;cursor:pointer;" onclick="showAddEconomyForm()"><span style="color:#0088ff;font-weight:bold;font-size:20px;">+</span> Add New Economy</td></tr>`;
    t+=`<tr class="add-economy-form" id="add-economy-form" style="display:none;">`;
    keys.forEach(k=>{
      if(k==='code'){
        t+=`<td><input type="text" class="form-control form-control-sm" id="new-code" placeholder="Code" maxlength="3" style="text-transform:uppercase;"></td>`;
      }else if(k==='name'){
        t+=`<td><input type="text" class="form-control form-control-sm" id="new-name" placeholder="Name"></td>`;
      }else if(k==='region'){
        t+=`<td><select class="form-select form-select-sm" id="new-region"><option value="">Choose...</option>${REGIONS.map(c=>`<option value="${c}">${c}</option>`).join('')}</select></td>`;
      }else{
        t+=`<td></td>`;
      }
    });
    t+=`<td><button class="btn btn-sm btn-success" onclick="submitNewCountry()">✓</button> <button class="btn btn-sm btn-secondary" onclick="cancelAddEconomy()">✗</button></td>`;
    t+=`</tr>`;
  }
  t+='</tbody></table>';
  return t;
}

function createInput(field,val){
  if(field==='region'){
    const wrapper=document.createElement('div');
    wrapper.className='continent-dropdown-wrapper';
    wrapper.style.position='relative';
    const sel=document.createElement('div');
    sel.className='edit-input continent-display';
    sel.textContent=val||'Choose...';
    sel.style.cursor='pointer';
    const menu=document.createElement('div');
    menu.className='continent-menu';
    menu.innerHTML=REGIONS.map(c=>`<div class="continent-option" data-value="${c}">${c}</div>`).join('');
    menu.style.display='block';
    wrapper.appendChild(sel);
    wrapper.appendChild(menu);
    wrapper._getValue=()=>sel.dataset.value||val;
    wrapper._setValue=(v)=>{sel.textContent=v;sel.dataset.value=v};
    menu.querySelectorAll('.continent-option').forEach(opt=>{
      opt.onclick=()=>{
        sel.textContent=opt.dataset.value;
        sel.dataset.value=opt.dataset.value;
        wrapper.dispatchEvent(new Event('change'));
      };
    });
    return wrapper;
  }
  const inp=document.createElement('input');
  inp.className='edit-input';
  inp.value=val;
  return inp;
}

function edit(cell,endpoint,row,field){
  const span=cell.querySelector('.cell-val');
  const val=span.textContent;
  const input=createInput(field,val);
  cell.replaceChild(input,span);
  
  const handleSave=async()=>{
    const newVal=input._getValue?input._getValue():input.value;
    if(newVal!==val){
      const id=getId(row);
      const body={[field]:NUM_FIELDS.includes(field)?+newVal:newVal};
      try{
        await fetch(`/internal${endpoint}${id}`,{method:'PATCH',headers:getHeaders(),body:JSON.stringify(body)});
        api(endpoint,'GET');
      }catch(e){
        alert(`Update failed: ${e.message}`);
      }
    }else{
      api(endpoint,'GET');
    }
  };
  
  if(field==='region'){
    input.onchange=handleSave;
    const closeOnClickOutside=(e)=>{
      if(!input.contains(e.target)){
        document.removeEventListener('click',closeOnClickOutside);
        api(endpoint,'GET');
      }
    };
    setTimeout(()=>{
      cell.querySelector('.continent-menu').scrollIntoView({block:'nearest'});
      document.addEventListener('click',closeOnClickOutside);
    },50);
  }else{
    input.focus();
    input.onblur=handleSave;
    input.onkeydown=e=>{if(e.key==='Enter')input.blur()};
  }
}

async function del(path,endpoint){
  try{
    await fetch(`/internal${path}`,{method:'DELETE',headers:getHeaders()});
    api(endpoint,'GET');
  }catch(e){
    $('o').innerHTML=`<pre class="border p-3 mt-3">${e.message}</pre>`;
  }
}

function showAddEconomyForm(){
  document.getElementById('add-economy-row').style.display='none';
  document.getElementById('add-economy-form').style.display='';
  setTimeout(()=>document.getElementById('new-code').focus(),50);
}

function cancelAddEconomy(){
  document.getElementById('add-economy-row').style.display='';
  document.getElementById('add-economy-form').style.display='none';
}

async function submitNewCountry(){
  const code=$('new-code').value.trim();
  const name=$('new-name').value.trim();
  const region=$('new-region').value||null;
  
  if(!code||code.length!==3)return alert('Economy code must be 3 letters');
  if(!name)return alert('Economy name is required');
  
  const body={code,name,region};
  
  try{
    await fetch('/internal/economies/',{method:'POST',headers:getHeaders(),body:JSON.stringify(body)});
    api('/economies/','GET');
  }catch(e){
    alert(`Failed to add economy: ${e.message}`);
  }
}

async function api(e,m='GET',b){
  try{
    const r=await fetch(`/internal${e}`,{method:m,headers:getHeaders(),body:b?JSON.stringify(b):null});
    const data=await r.json();
    $('o').innerHTML=m==='GET'&&Array.isArray(data)?toTable(data,e):`<pre class="border p-3 mt-3">${JSON.stringify(data,null,2)}</pre>`;
  }catch(e){
    $('o').innerHTML=`<pre class="border p-3 mt-3">${e.message}</pre>`;
  }
}

window.api=api;
window.del=del;
window.edit=edit;
window.showAddEconomyForm=showAddEconomyForm;
window.cancelAddEconomy=cancelAddEconomy;
window.submitNewCountry=submitNewCountry;
window.$=$;
