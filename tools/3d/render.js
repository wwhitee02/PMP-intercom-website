const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage();// three.js из node_modules через локальный сервер (см. README)
p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')console.log('console:',m.text().slice(0,300))});p.on('pageerror',e=>console.log('pageerror',e.message));
await p.goto('http://127.0.0.1:8765/render.html');await p.waitForFunction(()=>window.ready,{timeout:60000});
const t0=Date.now();const out=await p.evaluate(()=>window.renderAll());
for(const [k,v] of Object.entries(out)){if(k==='anchors'){fs.writeFileSync('out/anchors.json',v);continue}fs.writeFileSync('out/'+k+'.png',Buffer.from(v.split(',')[1],'base64'))}
console.log('rendered',Object.keys(out).join(','),(Date.now()-t0)/1000+'s');await b.close();})();
