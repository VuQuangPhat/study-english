"""Kiểm tra tự động Cẩm Nang Tiếng Anh: chạy  python3 tools/audit.py [390,1366,1905,2560]
Quét mọi chủ đề: chữ SVG tràn ô, nút/nhãn bị cắt chữ, trang tràn ngang. Mong đợi: issues: 0."""
import asyncio,json,sys,subprocess,time,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PORT=8791
srv=subprocess.Popen([sys.executable,'-m','http.server',str(PORT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
from playwright.async_api import async_playwright
d=json.load(open('data.json'))
H=d['CHU_DE']['h']
cds=[(r[H.index('tab')],r[H.index('id')]) for r in d['CHU_DE']['r']]
WIDTHS=[int(x) for x in sys.argv[1].split(',')] if len(sys.argv)>1 else [390,1366,1905,2560]
JS="""()=>{
const out=[];
const tol=1.5;
document.querySelectorAll('details').forEach(x=>x.open=true);
document.querySelectorAll('.fig svg').forEach(svg=>{
  const id=(svg.closest('[data-fig]')||{}).dataset?.fig||'?';
  const rects=[...svg.querySelectorAll('rect')].map(r=>({r,b:r.getBoundingClientRect()})).filter(o=>o.b.width>20&&o.b.height>12);
  svg.querySelectorAll('text').forEach(t=>{
    const b=t.getBoundingClientRect(); if(!b.width)return;
    const cx=b.left+b.width/2,cy=b.top+b.height/2;
    const cont=rects.filter(o=>o.b.left<=cx&&o.b.right>=cx&&o.b.top<=cy&&o.b.bottom>=cy&&!(o.b.left>=b.left-1&&o.b.right<=b.right+1&&o.b.height<b.height)).sort((a,c)=>a.b.width*a.b.height-c.b.width*c.b.height)[0];
    const s=svg.getBoundingClientRect();
    const box=cont?cont.b:s;
    const over=Math.max(box.left-b.left,b.right-box.right,box.top-b.top,b.bottom-box.bottom);
    if(over>tol)out.push({k:'svg-text',fig:id,txt:(t.textContent||'').slice(0,40),over:Math.round(over)});
  });
});
const sel='button,.pill,.chip,.tk,.tab,summary,th,td,.fc,.opt,.tools *,.chips a,.rail a,.toc a,.tabs a';
document.querySelectorAll(sel).forEach(e=>{
  const cs=getComputedStyle(e);if(cs.display==='none'||e.offsetWidth===0)return;
  if(e.scrollWidth>e.clientWidth+2&&cs.overflowX!=='auto'&&cs.overflowX!=='scroll'&&cs.display!=='table-cell'&&cs.display!=='inline')out.push({k:'html-clip',el:e.tagName+'.'+e.className,txt:(e.innerText||'').slice(0,40),over:e.scrollWidth-e.clientWidth});
});
const de=document.documentElement;
if(de.scrollWidth>innerWidth+1)out.push({k:'page-hscroll',over:de.scrollWidth-innerWidth});
return out}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();tot={}
        for w in WIDTHS:
            pg=await b.new_page(viewport={'width':w,'height':900})
            for tab,cid in cds:
                await pg.goto(f'http://localhost:{PORT}/index.html#/{tab}/{cid}');await pg.wait_for_timeout(700)
                try: await pg.wait_for_function("[...document.querySelectorAll('[data-fig]')].every(e=>e.querySelector('svg'))",timeout=3000)
                except Exception: pass
                res=await pg.evaluate(JS)
                for r in res:
                    key=(r['k'],r.get('fig') or r.get('el') or '',r.get('txt',''))
                    tot.setdefault(key,{'w':set(),'cds':set(),'over':0});tot[key]['w'].add(w);tot[key]['cds'].add(cid);tot[key]['over']=max(tot[key]['over'],r['over'])
            await pg.close()
        await b.close()
        print('issues:',len(tot))
        for k,v in sorted(tot.items(),key=lambda x:-x[1]['over'])[:60]:
            print(k[0],'|',k[1],'|',k[2],'| over',v['over'],'| w',sorted(v['w']),'|',sorted(v['cds'])[:3])
try: asyncio.run(main())
finally: srv.terminate()
