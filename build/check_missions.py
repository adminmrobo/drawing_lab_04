# 실전 연습장 미션 판정 점검 (로컬 서버 8765번 필요). 직접 조작하기 전에는 미션이 판정되지 않아야 하고, 조작하면 판정돼야 한다.
import asyncio
from playwright.async_api import async_playwright
async def setr(page,sc,name,v):
    await page.evaluate("([sc,n,v])=>{const e=document.querySelector('#'+sc+' [name='+n+']');if(e.type==='checkbox'){e.checked=v;}else e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",[sc,name,v])
async def done(page,sc): return await page.evaluate("sc=>[...document.querySelectorAll('#'+sc+' .missions li')].map(l=>l.classList.contains('done'))",sc)
async def main():
    ok=True
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        page=await b.new_page();await page.route('**/fonts.g*/**',lambda r: r.abort())
        errs=[];page.on("pageerror",lambda e: errs.append(str(e)))
        await page.goto("http://localhost:8765/practice/index.html#bench");await page.wait_for_timeout(800)
        r0=await done(page,'bench');print('bench before',r0);ok&=not any(r0)
        # 올라간 눈·정면 / 처진 눈·비스듬히 / 기본 눈·정면
        for vals in [dict(target='up',turn='0',inY=-3,outY=15,far=100,pupil=0),dict(target='down',turn='1',inY=0,outY=-8,far=58,pupil=0),dict(target='mid',turn='0',inY=0,outY=5,far=100,pupil=0)]:
            for n,v in vals.items(): await setr(page,'bench',n,v)
        r=await done(page,'bench');print('bench after',r);ok&=all(r)
        await page.click('.tabs button[data-t=expr]')
        r0=await done(page,'expr');print('expr before',r0);ok&=not any(r0)
        T=[(0,0,50,'smile'),(1,0,120,'wide'),(2,14,50,'closed'),(3,14,120,'wide'),(4,-14,110,'closed'),(5,-14,50,'wide')]
        for t,br,op,m in T:
            await setr(page,'expr','target',str(t))
            for n,v in [('brow',br),('open',op),('mouth',m)]: await setr(page,'expr',n,v)
        r=await done(page,'expr');print('expr after',r);ok&=all(r)
        await page.click('.tabs button[data-t=workshop]')
        r0=await done(page,'workshop');print('workshop before',r0);ok&=not any(r0)
        await setr(page,'workshop','job','close')
        for n,v in [('eye','mid'),('paint','layer'),('nose','dot'),('mouth','smile'),('hair','vol'),('level','even'),('age','adult')]: await setr(page,'workshop',n,v)
        for n,v in [('mouth','wide')]: await setr(page,'workshop',n,v)
        r=await done(page,'workshop');print('workshop after',r);ok&=all(r)
        await page.click('.tabs button[data-t=desk]')
        SYM=['동공이 눈 표면보다','똑같이 크다','턱선 가까이','이쪽을 보고 서','얼굴이 유난히 커','코에만 콧구멍','납작한 스티커','화가 난 듯']
        CA=['동공이 각막 밖','안쪽 눈 너비 그대로','귀가 낮음','어금니가 정면','머리 부피 없음','코만 진함','순백 흰자·한 색 눈동자','눈썹 방향 어긋남']
        r0=await done(page,'desk');print('desk before',r0);ok&=not any(r0)
        for _ in range(60):
            sym=await page.text_content('#desk .sym');k=[i for i,s in enumerate(SYM) if s in sym][0]
            await page.click(f"#desk .deskopts button:text-is('{CA[k]}')");await page.wait_for_timeout(560)
        r=await done(page,'desk');print('desk after',r);ok&=all(r)
        print('errors',errs[:3]);ok&=not errs
        await b.close()
    print('미션 점검 통과' if ok else '미션 점검 실패')
asyncio.run(main())
