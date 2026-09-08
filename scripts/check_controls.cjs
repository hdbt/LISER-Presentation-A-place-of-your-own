// Offline DOM stub: exercises calculations and control handlers, not visual rendering.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2] || 'A_Place_of_Your_Own.html','utf8');
class Element{
 constructor(){this.children=[];this.dataset={};this.style={};this.value='';this.textContent='';this.attrs={};this.events={};this.classList={toggle:()=>{}}}
 setAttribute(k,v){this.attrs[k]=v}append(...v){this.children.push(...v)}replaceChildren(...v){this.children=v}add(o){this.children.push(o)}addEventListener(k,v){this.events[k]=v}
}
const elements={};for(const m of html.matchAll(/id="([^"]+)"/g))elements[m[1]]=new Element();
for(const [id,v]of Object.entries({budget:'1200',size:'45',basis:'real'}))elements[id].value=v;
const slideCount=[...html.matchAll(/class="slide(?:\s[^"]*)?"/g)].length;
const slides=Array.from({length:slideCount},()=>{const e=new Element();e.querySelector=()=>({textContent:'Speaker notes'});return e});
const ctx={document:{getElementById:id=>{assert(elements[id],id);return elements[id]},querySelectorAll:()=>slides,createElementNS:()=>new Element(),createElement:()=>new Element(),addEventListener:()=>{}},Option:function(t,v){this.text=t;this.value=v},Intl,location:{hash:''},setInterval:()=>1,clearInterval:()=>{},innerWidth:1440,innerHeight:900,console};
ctx.window=ctx;
vm.createContext(ctx);for(const m of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],ctx);
assert.equal(elements.within.textContent,14);assert.equal(elements.available.textContent,34);
elements.budget.value=3000;vm.runInContext('update()',ctx);assert.equal(elements.within.textContent,34);
elements.budget.value=1200;elements.year.value=2010;vm.runInContext('update()',ctx);
const data=JSON.parse(fs.readFileSync('data/clean/rental_scenario.json','utf8'));
const historicalBudget=1200*91.575/(1504.93/12);
assert(Math.abs(vm.runInContext("nominalBudget('2010',1200)",ctx)-historicalBudget)<1e-10);
assert.equal(elements.within.textContent,Object.values(data.panel['2010']).filter(r=>r.rate!==null&&r.rate*45<=historicalBudget).length);
assert(elements.formula.textContent.includes('876'));
const adjusted2010=elements.within.textContent;
elements.basis.value='nominal';vm.runInContext('update()',ctx);assert.equal(elements.within.textContent,51);
assert.equal(vm.runInContext("nominalBudget('2010',1200)",ctx),1200);
elements.basis.value='real';vm.runInContext('update()',ctx);
assert.equal(vm.runInContext("nominalBudget('2025',1200)",ctx),1200);
elements.size.value=70;vm.runInContext('update()',ctx);
assert.equal(elements.hero.dataset.size,'45');
assert.equal(elements.mainMap.dataset.size,'70');
const heroPath=elements.hero.children.find(e=>e.dataset.name==='Luxembourg');
heroPath.events.pointermove({clientX:100,clientY:100});
const expectedHero=new Intl.NumberFormat('en-IE',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(data.panel['2025'].Luxembourg.rate*45);
assert(elements.tip.textContent.includes(expectedHero));
elements.reset.onclick();assert.equal(elements.within.textContent,14);
vm.runInContext("selected='Esch-sur-Alzette';detail()",ctx);elements.zoom.onclick();assert.notEqual(elements.mainMap.attrs.viewBox,vm.runInContext('view',ctx));elements.unzoom.onclick();
for(let i=0;i<slideCount;i++)vm.runInContext(`go(${i})`,ctx);assert.equal(elements.pageCount.textContent,`${slideCount} / ${slideCount}`);
assert(!/<(?:script|link|img)[^>]+(?:src|href)="https?:/i.test(html));
assert(!html.includes('__PAYLOAD__'));
const D=JSON.parse(fs.readFileSync('data/clean/rental_scenario.json','utf8'));
for(const y of D.years)assert.equal(Object.keys(D.panel[y]).length,100);
const both=Object.keys(D.shapes).filter(n=>D.panel[2010][n].rate!==null&&D.panel[2025][n].rate!==null);
console.log(`PASS: ${slideCount} slide states, baseline counts, high budget, year change, reset, commune selection, zoom, offline assets, 100 areas/year.`);
console.log('Purchasing-power matched endpoints:',both.length,'communes;',both.filter(n=>D.panel[2010][n].rate*45<=historicalBudget).length,'→',both.filter(n=>D.panel[2025][n].rate*45<=1200).length);
console.log('All observed 2010: nominal 51; CPI-adjusted',adjusted2010,'; historical budget',historicalBudget);
console.log('This is a calculation/control test, not a browser or layout test.');
