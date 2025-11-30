const $=i=>document.getElementById(i);
const CONTINENTS=['Asia','Europe','North America','South America','Africa','Oceania'];
const KEY_FIELDS=['id','code','provider_id','country_code'];
const NUM_FIELDS=['lat','lng'];

function getHeaders(){
  const h={'Content-Type':'application/json'};
  const t=$('token').value;
  if(t)h['token']=t;
  return h;
}

function getId(row){
  return row.id||row.code||(row.provider_id&&row.country_code?`${row.provider_id}/${row.country_code}`:'');
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
        t+=`<td class="editable-cell" onclick="edit(this,'${endpoint}',${rowJson},'${k}')"><span class="cell-val">${displayVal}</span><span class="edit-icon">✏️</span></td>`;
      }
    });
    const id=getId(row);
    t+=`<td><button class="btn-trash" onclick="del('${endpoint}${id}','${endpoint}')">🗑️</button></td>`;
    t+='</tr>';
  });
  t+='</tbody></table>';
  return t;
}

function createInput(field,val){
  if(field==='continent'){
    const sel=document.createElement('select');
    sel.className='edit-input';
    sel.innerHTML='<option value="">Select</option>'+CONTINENTS.map(c=>`<option>${c}</option>`).join('');
    sel.value=val;
    return sel;
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
  input.focus();
  input.onblur=async()=>{
    const newVal=input.value;
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
  input.onkeydown=e=>{if(e.key==='Enter')input.blur()};
}

async function del(path,endpoint){
  try{
    await fetch(`/internal${path}`,{method:'DELETE',headers:getHeaders()});
    api(endpoint,'GET');
  }catch(e){
    $('o').innerHTML=`<pre class="border p-3 mt-3">${e.message}</pre>`;
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
window.$=$;
