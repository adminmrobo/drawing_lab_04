/* 구조 먼저 그리기 연구실 04 · 디테일 편 — 실험 패널 모음 (외부 라이브러리 없음) */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var C={teal:'#0f8f84',orange:'#e8731a',navy:'#1e2f6e',blue:'#2458d6',green:'#13733a',red:'#c9302c',purple:'#6b4fb0',grid:'#e3e8ee',muted:'#5b6874',ink:'#16212b'};
var KFONT='"IBM Plex Sans KR","Malgun Gothic","Noto Sans KR",sans-serif';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var P={};

/* ---------- 공용 도구 ---------- */
function el(tag,a,parent){var e=document.createElementNS(NS,tag);for(var k in a){if(a[k]!=null)e.setAttribute(k,a[k]);}if(parent)parent.appendChild(e);return e;}
function ktxt(p,x,y,s,a){a=a||{};var t=el('text',{x:x,y:y,'font-size':a.size||13,fill:a.fill||C.muted,'font-family':KFONT,'text-anchor':a.anchor||'start','font-weight':a.weight||'normal'},p);t.textContent=s;return t;}
function svgOf(h,W,H,label){h.innerHTML='';return el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'실험 그림: '+(label||noteOf(h))},h);}
function noteOf(h){var n=h.parentNode&&h.parentNode.querySelector('.ph small');return n?n.textContent:'';}
function canvasOf(h,W,H,mw){h.innerHTML='';var c=document.createElement('canvas');c.width=W;c.height=H;c.style.width='100%';c.style.maxWidth=(mw||W*1.2)+'px';c.style.margin='0 auto';c.style.height='auto';c.style.display='block';c.style.borderRadius='10px';c.setAttribute('role','img');c.setAttribute('aria-label','실험 그림: '+noteOf(h));h.appendChild(c);return c;}
function out(h){return h.parentNode.querySelector('.readout');}
function ctl(h){return h.parentNode.querySelector('.ctrl');}
function f2(v,d){d=d==null?2:d;if(d===0)return String(Math.round(v));var m=Math.pow(10,d);var s=(Math.round(v*m)/m).toFixed(d);s=s.replace(/\.?0+$/,'');if(s==='-0')s='0';return s;}
function num(v,d){return v<0?'−'+f2(-v,d):f2(v,d);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function hex(c){c=c.replace('#','');return[parseInt(c.substr(0,2),16),parseInt(c.substr(2,2),16),parseInt(c.substr(4,2),16)];}
function rgb(a){return 'rgb('+a.map(function(v){return Math.round(clamp(v,0,255));}).join(',')+')';}
function mix(c1,c2,t){var a=hex(c1),b=hex(c2);return rgb([lerp(a[0],b[0],t),lerp(a[1],b[1],t),lerp(a[2],b[2],t)]);}
function shade(c,k){var a=hex(c);return rgb([a[0]*k,a[1]*k,a[2]*k]);}
function rad(d){return d*Math.PI/180;}
function seg(h,sel,cb){var bs=ctl(h).querySelectorAll(sel);bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b);});});}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function onIn(inp,f){inp.addEventListener('input',f);}
function svgPt(s,e){var m=s.getScreenCTM().inverse();var q=s.createSVGPoint();q.x=e.clientX;q.y=e.clientY;return q.matrixTransform(m);}

function board(el_,items){el_.innerHTML=items.map(function(it){return '<div class="'+(it[2]?'good':'bad')+'"><span>'+it[0]+'</span><b>'+it[1]+'</b></div>';}).join('');}
function say(el_,lines){el_.innerHTML=lines.map(function(l){return '<div class="line"><img src="../assets/chars/'+l[0]+'_'+l[1]+'.webp" alt="" width="48" height="48"><div class="bub"><b>'+l[2]+'</b>'+l[3]+'</div></div>';}).join('');}
function missions(el_,state,touched){el_.querySelectorAll('li').forEach(function(li,i){if(touched&&state[i])li.classList.add('done');});}
var DONE={};
/* ===================== 디테일 그리기 도구 (SVG) ===================== */
var FC={ink:'#2a2230',skin:'#F8E3D3',skin2:'#EFCDB8',guide:'#e0337f',guide2:'#9aa5b1',iris:'#5b3f6e',hot:'#e8731a',hairP:'#E9A3C0',hairB:'#1E1B22',hairA:'#D8C09A'};
var UID=0;function uid(p){UID++;return (p||'u')+UID;}
function pth(s,d,a){a=a||{};return el('path',{d:d,fill:a.fill||'none',stroke:a.stroke||FC.ink,'stroke-width':a.w||2.2,'stroke-linecap':'round','stroke-linejoin':'round','stroke-dasharray':a.dash||null,opacity:a.op==null?null:a.op},s);}
function hline(s,x1,x2,y,lab,col,right){el('line',{x1:x1,y1:y,x2:x2,y2:y,stroke:col||FC.guide,'stroke-width':1.6,'stroke-dasharray':'6 4'},s);if(lab)ktxt(s,right?x2+6:x1-6,y+4,lab,{size:12.5,fill:col||FC.guide,anchor:right?'start':'end',weight:'bold'});}
function P2(x,y){return x.toFixed(1)+','+y.toFixed(1);}
function pick(h,sel){return ctl(h).querySelector(sel);}
function rv(h,name){var e=pick(h,'[name='+name+']');return e?(e.type==='checkbox'?e.checked:(e.tagName==='SELECT'?e.value:+e.value)):null;}
function allIn(h,f){ctl(h).querySelectorAll('input,select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
function bg(s,W,H){el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);}
function seg2(h,cb){var bs=ctl(h).querySelectorAll('button[data-v]');bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b.dataset.v);});});}
function verdict(ok,txt){return '<span style="color:'+(ok?C.green:C.red)+';font-weight:700">'+(ok?'✔ ':'⚠ ')+txt+'</span>';}
function deg(r){return r*180/Math.PI;}
function rgbA(a){return 'rgb('+a.map(function(v){return Math.round(clamp(v,0,255));}).join(',')+')';}
function avg3(a){return (a[0]+a[1]+a[2])/3;}

/* 눈 하나. cx,cy: 눈 가운데(눈머리·눈꼬리 높이의 기준), w: 눈 너비. o.side 1이면 눈머리가 왼쪽.
   o.inY/o.outY: 눈머리·눈꼬리 높이(눈 너비를 10으로 볼 때, 위가 +). o.open: 뜬 정도(1 기본) */
function eyeGeo(cx,cy,w,o){var side=o.side||1,u=w/10,inX=cx-side*w/2,outX=cx+side*w/2,yI=cy-(o.inY||0)*u,yO=cy-(o.outY==null?0.6:o.outY)*u,h=w*0.66*(o.open==null?1:o.open);
  function at(t,dy){return [lerp(inX,outX,t),lerp(yI,yO,t)+dy];}
  return {side:side,u:u,I:[inX,yI],O:[outX,yO],T1:at(0.27,-h*0.6),T2:at(0.7,-h*0.62),B2:at(0.7,h*0.4),B1:at(0.3,h*0.4),h:h,cx:(inX+outX)/2,cy:(yI+yO)/2};}
function hexD(g){return 'M'+P2(g.I[0],g.I[1])+' L'+P2(g.T1[0],g.T1[1])+' L'+P2(g.T2[0],g.T2[1])+' L'+P2(g.O[0],g.O[1])+' L'+P2(g.B2[0],g.B2[1])+' L'+P2(g.B1[0],g.B1[1])+'Z';}
function eyeD(g){/* 눈 윤곽(부드러운 육각형) */
  return 'M'+P2(g.I[0],g.I[1])+' Q'+P2(g.T1[0],g.T1[1]-g.h*0.05)+' '+P2((g.T1[0]+g.T2[0])/2,(g.T1[1]+g.T2[1])/2-g.h*0.02)+' Q'+P2(g.T2[0],g.T2[1]+g.h*0.02)+' '+P2(g.O[0],g.O[1])+
    ' Q'+P2(g.B2[0],g.B2[1]+g.h*0.02)+' '+P2((g.B1[0]+g.B2[0])/2,(g.B1[1]+g.B2[1])/2+g.h*0.03)+' Q'+P2(g.B1[0],g.B1[1])+' '+P2(g.I[0],g.I[1])+'Z';}
function eyeDraw(s,cx,cy,w,o){o=o||{};var g=eyeGeo(cx,cy,w,o),G=el('g',{},s),side=g.side;
  if(g.h<w*0.08){/* 거의 감은 눈 — 웃는 호 */
    pth(G,'M'+P2(g.I[0],g.I[1])+' Q'+P2(g.cx,g.cy-w*0.28)+' '+P2(g.O[0],g.O[1]),{w:Math.max(2.4,w*0.07)});return g;}
  var id=uid('ec');var cp=el('clipPath',{id:id},G);el('path',{d:eyeD(g)},cp);
  var scl=o.sclera||'#f6f2ef';el('path',{d:eyeD(g),fill:scl},G);
  var ix=g.cx+(o.look||0)*w*0.1,iy=g.cy-g.h*0.02,rx=w*0.26*(o.irisK||1),ry=Math.max(g.h*0.62,w*0.3);var ic=o.iris||FC.iris;
  var ig=el('g',{'clip-path':'url(#'+id+')'},G);
  if(o.paint){var gid=uid('ig');var df=el('defs',{},G);var lg=el('linearGradient',{id:gid,x1:0,y1:0,x2:0,y2:1},df);
    el('stop',{offset:'0','stop-color':o.paint.top},lg);el('stop',{offset:'0.48','stop-color':o.paint.mid},lg);el('stop',{offset:'1','stop-color':o.paint.bot},lg);
    el('ellipse',{cx:ix,cy:iy,rx:rx,ry:ry,fill:'url(#'+gid+')'},ig);
    if(o.paint.shadeLid)el('path',{d:'M'+P2(g.I[0]-5,g.I[1]-g.h)+' L'+P2(g.O[0]+5,g.O[1]-g.h)+' L'+P2(g.O[0]+5,g.O[1]-g.h*0.05)+' Q'+P2(g.cx,g.cy-g.h*0.25)+' '+P2(g.I[0]-5,g.I[1]-g.h*0.05)+'Z',fill:o.paint.shadeLid,opacity:o.paint.shadeOp==null?.35:o.paint.shadeOp},ig);}
  else el('ellipse',{cx:ix,cy:iy,rx:rx,ry:ry,fill:ic},ig);
  el('ellipse',{cx:ix,cy:iy,rx:rx,ry:ry,fill:'none',stroke:shade(ic.charAt(0)==='#'?ic:FC.iris,0.55),'stroke-width':1.4},ig);
  var pr=o.pupil==='slit'?[w*0.04,ry*0.55]:[rx*0.42,ry*0.42];el('ellipse',{cx:ix,cy:iy+ry*0.05,rx:pr[0],ry:pr[1],fill:o.pupilCol||'#1d1622'},ig);
  if(o.irisLines){for(var k=0;k<o.irisLines;k++){var a=-Math.PI*0.95+Math.PI*1.9*k/Math.max(1,o.irisLines-1);var r1=rx*0.48,r2=rx*0.92;el('line',{x1:ix+Math.cos(a)*r1,y1:iy+Math.sin(a)*r1*ry/rx,x2:ix+Math.cos(a)*r2,y2:iy+Math.sin(a)*r2*ry/rx,stroke:'rgba(20,10,25,.55)','stroke-width':1.1},ig);}}
  if(o.sparkle){var sx=ix,sy=iy;el('path',{d:'M'+P2(sx,sy-ry*0.7)+' Q'+P2(sx,sy)+' '+P2(sx+rx*0.7,sy)+' Q'+P2(sx,sy)+' '+P2(sx,sy+ry*0.7)+' Q'+P2(sx,sy)+' '+P2(sx-rx*0.7,sy)+' Q'+P2(sx,sy)+' '+P2(sx,sy-ry*0.7)+'Z',fill:'#fff'},ig);}
  var hl=o.hl==null?1:o.hl;if(hl>0){el('ellipse',{cx:ix-side*rx*0.38,cy:iy-ry*0.42,rx:rx*0.2*hl,ry:rx*0.16*hl,fill:'#fff'},ig);el('circle',{cx:ix+side*rx*0.42,cy:iy+ry*0.35,r:rx*0.08*hl,fill:'#fff',opacity:.9},ig);}
  if(o.tear){el('path',{d:'M'+P2(g.B1[0],g.B1[1]-2)+' Q'+P2(g.cx,g.B1[1]+g.h*0.05)+' '+P2(g.B2[0],g.B2[1]-2),stroke:'#9fd0f0','stroke-width':4,fill:'none',opacity:.9},G);el('path',{d:'M'+P2(g.B1[0]+3,g.B1[1])+' q -3,10 0,16 q 4,-4 0,-16',fill:'#bfe2f7',stroke:'#7fb7dc','stroke-width':1},G);}
  var lc=o.lineCol||FC.ink;
  /* 위 눈꺼풀(굵게)과 속눈썹 */
  var up='M'+P2(g.I[0],g.I[1])+' Q'+P2(g.T1[0],g.T1[1]-g.h*0.05)+' '+P2((g.T1[0]+g.T2[0])/2,(g.T1[1]+g.T2[1])/2-g.h*0.02)+' Q'+P2(g.T2[0],g.T2[1]+g.h*0.02)+' '+P2(g.O[0],g.O[1]);
  pth(G,up,{w:Math.max(3,w*0.075),stroke:lc});
  pth(G,'M'+P2(g.O[0],g.O[1])+' l'+P2(side*w*0.1,-w*0.07),{w:Math.max(2.4,w*0.05),stroke:lc});
  if(o.lash){for(var j=0;j<o.lash;j++){var t=0.12+0.82*j/Math.max(1,o.lash-1);var p=quadPt(g,t);el('line',{x1:p[0],y1:p[1],x2:p[0]+side*w*0.02,y2:p[1]-w*0.065,stroke:lc,'stroke-width':1},G);}}
  pth(G,'M'+P2(g.O[0],g.O[1])+' Q'+P2(g.B2[0],g.B2[1]+g.h*0.02)+' '+P2((g.B1[0]+g.B2[0])/2,(g.B1[1]+g.B2[1])/2+g.h*0.03)+' Q'+P2(g.B1[0],g.B1[1])+' '+P2(g.I[0],g.I[1]),{w:1.5,stroke:lc,op:.75});
  if(o.hex)el('path',{d:hexD(g),fill:'none',stroke:FC.guide,'stroke-width':1.8,'stroke-dasharray':'5 3'},s);
  g.ix=ix;g.iy=iy;g.rx=rx;g.ry=ry;g.G=G;return g;}
function quadPt(g,t){var a=g.I,b=[(g.T1[0]+g.T2[0])/2,(g.T1[1]+g.T2[1])/2-g.h*0.06],c=g.O;var m=1-t;return [m*m*a[0]+2*m*t*b[0]+t*t*c[0],m*m*a[1]+2*m*t*b[1]+t*t*c[1]];}
/* 눈썹: ang(+면 눈썹 끝이 올라감), arc(+면 위로 볼록) */
function browDraw(s,x,y,w,side,ang,arc,thick){var a=rad(ang||0),hx=w/2;var ix=x-side*hx,ox=x+side*hx;var iy=y+Math.tan(a)*hx,oy=y-Math.tan(a)*hx;var mx=(ix+ox)/2,my=(iy+oy)/2-(arc==null?4:arc*6);
  return pth(s,'M'+P2(ix,iy)+' Q'+P2(mx,my)+' '+P2(ox,oy),{w:thick||3.2});}
/* 코: 정보량 1~5 */
function noseDraw(s,x,y,sz,lv,side){side=side||1;var g=el('g',{},s);
  if(lv<=1){el('ellipse',{cx:x,cy:y,rx:sz*0.06,ry:sz*0.05,fill:FC.ink},g);}
  else if(lv===2){el('path',{d:'M'+P2(x+side*sz*0.04,y-sz*0.6)+' L'+P2(x+side*sz*0.2,y-sz*0.05)+' Q'+P2(x,y+sz*0.12)+' '+P2(x-side*sz*0.16,y)+' L'+P2(x-side*sz*0.02,y-sz*0.55)+'Z',fill:'rgba(120,90,90,.22)'},g);}
  else if(lv===3){pth(g,'M'+P2(x+side*sz*0.05,y-sz*0.55)+' L'+P2(x+side*sz*0.12,y-sz*0.3),{w:1.4,op:.8});pth(g,'M'+P2(x-side*sz*0.12,y-sz*0.02)+' L'+P2(x+side*sz*0.02,y+sz*0.03),{w:2});}
  else if(lv===4){for(var i=0;i<5;i++)el('line',{x1:x+side*(sz*0.02+i*2.2),y1:y-sz*0.62,x2:x+side*(sz*0.02+i*2.2),y2:y-sz*0.32,stroke:FC.ink,'stroke-width':1},g);pth(g,'M'+P2(x+side*sz*0.08,y-sz*0.3)+' Q'+P2(x+side*sz*0.18,y-sz*0.05)+' '+P2(x,y+sz*0.04)+' M'+P2(x-side*sz*0.14,y)+' l'+P2(side*sz*0.06,sz*0.02),{w:1.8});}
  else{pth(g,'M'+P2(x+side*sz*0.02,y-sz*0.75)+' L'+P2(x+side*sz*0.08,y-sz*0.2)+' Q'+P2(x+side*sz*0.22,y-sz*0.02)+' '+P2(x+side*sz*0.12,y+sz*0.05),{w:2});pth(g,'M'+P2(x-side*sz*0.22,y-sz*0.02)+' q '+P2(side*sz*0.04,sz*0.06)+' '+P2(side*sz*0.1,sz*0.03)+' M'+P2(x+side*sz*0.02,y+sz*0.04)+' q '+P2(side*sz*0.05,sz*0.02)+' '+P2(side*sz*0.1,-sz*0.01),{w:1.6});}
  return g;}
/* 입 모양 */
var MOUTHS={smile:'웃는 입',open:'벌린 입',closed:'다문 입',wide:'크게 벌린 입',half:'반쯤 연 입',grin:'씩 웃는 입'};
function mouthDraw(s,x,y,w,type){var g=el('g',{},s),hw=w/2;
  if(type==='smile')pth(g,'M'+P2(x-hw,y)+' Q'+P2(x,y+w*0.32)+' '+P2(x+hw,y),{w:2.4});
  else if(type==='closed')pth(g,'M'+P2(x-hw*0.6,y+w*0.06)+' Q'+P2(x,y-w*0.1)+' '+P2(x+hw*0.6,y+w*0.06),{w:2.4});
  else if(type==='half'){el('path',{d:'M'+P2(x-hw*0.6,y)+' L'+P2(x+hw*0.6,y)+' L'+P2(x+hw*0.5,y+w*0.1)+' L'+P2(x-hw*0.5,y+w*0.1)+'Z',fill:'#5a2a35',stroke:FC.ink,'stroke-width':1.8},g);}
  else if(type==='open'){el('path',{d:'M'+P2(x-hw*0.6,y)+' Q'+P2(x,y-w*0.06)+' '+P2(x+hw*0.6,y)+' Q'+P2(x+hw*0.55,y+w*0.55)+' '+P2(x,y+w*0.6)+' Q'+P2(x-hw*0.55,y+w*0.55)+' '+P2(x-hw*0.6,y)+'Z',fill:'#5a2a35',stroke:FC.ink,'stroke-width':2},g);el('ellipse',{cx:x,cy:y+w*0.45,rx:hw*0.35,ry:w*0.1,fill:'#d9707f'},g);}
  else if(type==='wide'){el('path',{d:'M'+P2(x-hw,y-w*0.02)+' L'+P2(x+hw,y-w*0.02)+' Q'+P2(x+hw*0.85,y+w*0.75)+' '+P2(x,y+w*0.8)+' Q'+P2(x-hw*0.85,y+w*0.75)+' '+P2(x-hw,y-w*0.02)+'Z',fill:'#5a2a35',stroke:FC.ink,'stroke-width':2.2},g);el('rect',{x:x-hw*0.85,y:y-w*0.02,width:hw*1.7,height:w*0.12,fill:'#fff',stroke:FC.ink,'stroke-width':1},g);el('ellipse',{cx:x,cy:y+w*0.6,rx:hw*0.45,ry:w*0.12,fill:'#d9707f'},g);}
  else if(type==='grin'){el('path',{d:'M'+P2(x-hw,y-w*0.05)+' Q'+P2(x,y+w*0.18)+' '+P2(x+hw,y-w*0.05)+' Q'+P2(x,y+w*0.42)+' '+P2(x-hw,y-w*0.05)+'Z',fill:'#fff',stroke:FC.ink,'stroke-width':2},g);var zz='M'+P2(x-hw*0.8,y+w*0.05);for(var i=1;i<=8;i++)zz+=' L'+P2(x-hw*0.8+hw*1.6*i/8,y+w*(i%2?0.14:0.07));pth(g,zz,{w:1.2});}
  return g;}
/* 앞에서 본 머리(표정용). o: hair, brow(기울기°), arc, open, eye(normal|sparkle|tear|tired|angry), mouth, nose */
function headF(s,cx,top,H,o){o=o||{};var R=H*0.47,cy=top+R,chin=top+H,ey=top+H*0.5,ew=R*0.38,gap=ew*1.1,g=el('g',{},s);
  var hc=o.hair||FC.hairP;
  if(!o.noHair)el('path',{d:'M'+P2(cx-R*1.12,ey+H*0.32)+' Q'+P2(cx-R*1.28,top-H*0.07)+' '+P2(cx,top-H*0.07)+' Q'+P2(cx+R*1.28,top-H*0.07)+' '+P2(cx+R*1.12,ey+H*0.32)+'Z',fill:hc,stroke:FC.ink,'stroke-width':2},g);
  [-1,1].forEach(function(d){var ex=cx+d*R*0.86;pth(g,'M'+P2(ex,ey+ew*0.2)+' C'+P2(ex+d*H*0.1,ey)+' '+P2(ex+d*H*0.1,ey+H*0.16)+' '+P2(ex,ey+H*0.15),{fill:FC.skin,w:2});});
  el('path',{d:'M'+P2(cx,top)+' C'+P2(cx-R*0.56,top)+' '+P2(cx-R*0.88,cy-R*0.62)+' '+P2(cx-R*0.88,cy)+' C'+P2(cx-R*0.88,cy+R*0.55)+' '+P2(cx-R*0.36,chin-R*0.1)+' '+P2(cx,chin)+' C'+P2(cx+R*0.36,chin-R*0.1)+' '+P2(cx+R*0.88,cy+R*0.55)+' '+P2(cx+R*0.88,cy)+' C'+P2(cx+R*0.88,cy-R*0.62)+' '+P2(cx+R*0.56,top)+' '+P2(cx,top)+'Z',fill:FC.skin,stroke:FC.ink,'stroke-width':2.4},g);
  if(o.blush)[-1,1].forEach(function(d){el('ellipse',{cx:cx+d*(gap/2+ew/2),cy:ey+ew*0.85,rx:ew*0.36,ry:ew*0.14,fill:'rgba(240,120,140,.35)'},g);});
  var et=o.eye||'normal',op=o.open==null?1:o.open;var ang=o.brow||0;if(et==='angry'&&o.brow==null)ang=14;if(et==='tear'&&o.brow==null)ang=-14;
  var outY=0.6,inY=0;if(et==='tired'){op=Math.min(op,0.45);}
  [-1,1].forEach(function(d){var x=cx+d*(gap/2+ew/2);eyeDraw(g,x,ey+ew*0.2,ew,{side:d,open:op,inY:inY+(et==='angry'?0.6:0),outY:outY+(et==='angry'?0.8:et==='tear'?-0.6:0),sparkle:et==='sparkle',tear:et==='tear',hl:et==='tired'?0:1,iris:o.iris,look:0});
    browDraw(g,x+d*ew*0.05,ey-ew*(0.62+(et==='tired'?0:0.05))-(op-1)*ew*0.25,ew*1.05,d,ang,o.arc,2.8);});
  if(o.nose!==false)noseDraw(g,cx,ey+H*0.2,H*0.12,o.nose||1);
  mouthDraw(g,cx,chin-H*0.14,H*0.14,o.mouth||'smile');
  /* 앞머리 */
  if(o.noHair)return {g:g,R:R,ey:ey,ew:ew,chin:chin,top:top,cx:cx};
  var bd='M'+P2(cx-R*1.02,ey-ew*0.1)+' Q'+P2(cx-R*1.05,top-H*0.05)+' '+P2(cx,top-H*0.06)+' Q'+P2(cx+R*1.05,top-H*0.05)+' '+P2(cx+R*1.02,ey-ew*0.1);var n=9;
  var prev=[cx+R*1.02,ey-ew*0.1];for(var i=0;i<=n;i++){var x=cx+R*(1.0-2*i/n);var tip=i%2===1;var tipy=tip?ey-ew*(1.0+0.1*((i*7)%3)):top+H*(0.2+0.03*Math.abs(i-n/2)/n*4);if(i===0||i===n)tipy=ey-ew*0.1;
    var cxp=tip?(prev[0]*0.25+x*0.75):(prev[0]*0.75+x*0.25),cyp=tip?(prev[1]*0.35+tipy*0.65):(prev[1]*0.65+tipy*0.35);bd+=' Q'+P2(cxp,cyp)+' '+P2(x,tipy);prev=[x,tipy];}
  el('path',{d:bd+'Z',fill:hc,stroke:FC.ink,'stroke-width':2,'stroke-linejoin':'round'},g);
  if(o.buns)[-1,1].forEach(function(d){el('circle',{cx:cx+d*R*0.55,cy:top-H*0.02,r:R*0.28,fill:hc,stroke:FC.ink,'stroke-width':2},g);});
  return {g:g,R:R,ey:ey,ew:ew,chin:chin,top:top,cx:cx};}

/* ===================== 1부 눈의 모양(모아) ===================== */
P.p1_hex=function(h){var W=520,H=330;
  function draw(){var a=rv(h,'inY')/10,b=rv(h,'outY')/10;var s=svgOf(h,W,H);bg(s,W,H);
    var g=eyeDraw(s,260,190,300,{inY:a,outY:b,hex:true,iris:'#8a5a2b',lash:0});
    el('line',{x1:g.I[0],y1:g.I[1],x2:g.O[0],y2:g.O[1],stroke:C.blue,'stroke-width':2.2,'stroke-dasharray':'7 4'},s);
    el('circle',{cx:g.I[0],cy:g.I[1],r:7,fill:C.blue},s);el('circle',{cx:g.O[0],cy:g.O[1],r:7,fill:C.blue},s);
    ktxt(s,g.I[0],g.I[1]+28,'눈머리',{size:13,anchor:'middle',fill:C.blue,weight:'bold'});ktxt(s,g.O[0],g.O[1]+28,'눈꼬리',{size:13,anchor:'middle',fill:C.blue,weight:'bold'});
    hline(s,90,430,190,'',FC.guide2);
    var ang=deg(Math.atan((b-a)/10));var lab=ang>=8?'올라간 눈 — 날카롭고 강한 인상':ang>=0?'기본 눈 — 눈꼬리가 조금 위':'처진 눈 — 부드럽고 순한 인상';
    out(h).innerHTML='눈 너비를 10으로 보면 눈꼬리가 눈머리보다 <b>'+num(b-a,1)+'</b> 높습니다 → 기울기 '+num(b-a,1)+' ÷ 10 = <b>'+num((b-a)/10,2)+'</b>, 각도 약 <b>'+num(ang,1)+'°</b> → <b>'+lab+'</b>. '+
      (a<0&&ang>=8?'눈머리까지 내려 더 날카롭습니다.':'')+' <span class="hint">눈동자·속눈썹은 그대로이고 꼭짓점 두 개만 움직였습니다.</span>';}
  allIn(h,draw);draw();};
P.p1_cornea=function(h){var W=520,H=340;
  function draw(){var v=rv(h,'pupil');var s=svgOf(h,W,H);bg(s,W,H);var cx=300,cy=170,r=110;
    el('path',{d:'M'+P2(cx-60,cy-150)+' Q'+P2(cx-180,cy-150)+' '+P2(cx-190,cy-40)+' L'+P2(cx-150,cy+10)+' L'+P2(cx-180,cy+150)+' L'+P2(cx-60,cy+160)+'Z',fill:'#cfe3f4',opacity:.6},s);
    ktxt(s,cx-205,cy-120,'눈두덩·코 쪽(옆에서 본 얼굴)',{size:11.5,fill:C.muted});
    el('circle',{cx:cx,cy:cy,r:r,fill:'#fbf6f2',stroke:FC.ink,'stroke-width':2},s);
    var ix=cx-r*0.82,ih=r*0.56;
    var corn='M'+P2(ix,cy-ih)+' Q'+P2(ix-r*0.42,cy)+' '+P2(ix,cy+ih);el('path',{d:corn+' Z',fill:'rgba(160,210,240,.35)'},s);pth(s,corn,{stroke:C.blue,w:2.4});
    el('line',{x1:ix,y1:cy-ih,x2:ix,y2:cy+ih,stroke:'#8a5a2b','stroke-width':6},s);
    var px=ix-v*r*0.025;el('ellipse',{cx:px,cy:cy,rx:5,ry:ih*0.38,fill:'#1d1622'},s);
    ktxt(s,ix-r*0.5,cy-ih-10,'각막(맑은 막)',{size:12.5,fill:C.blue,weight:'bold',anchor:'middle'});ktxt(s,ix+14,cy+ih+20,'홍채',{size:12.5,fill:'#8a5a2b',weight:'bold'});ktxt(s,px-14,cy+ih*0.55,'동공',{size:12.5,fill:C.ink,weight:'bold',anchor:'end'});
    var surf=ix-r*0.21;var st=v<=2?0:(px>surf+3?1:2);var txt=['동공이 각막 안쪽(홍채 면 위)에 있습니다 — 맞는 구조','동공이 각막 면에 달라붙었습니다','동공이 각막 밖으로 튀어나왔습니다'];
    out(h).innerHTML='동공 위치 <b>'+v+'</b>(0 = 홍채 면). 각막 표면까지 <b>'+f2(Math.max(0,px-surf),0)+'px</b>. '+verdict(st===0,txt[st])+'. <span class="hint">순서는 바깥부터 각막 → 홍채 → 동공(홍채 가운데 구멍)입니다.</span>';}
  allIn(h,draw);draw();};
P.p1_sphere=function(h){var W=520,H=380;
  function draw(){var th=rv(h,'turn'),k=rv(h,'far')/100;var s=svgOf(h,W,H);bg(s,W,H);var cx=260,cy=190,R=150,al=25;
    el('circle',{cx:cx,cy:cy,r:R,fill:FC.skin,stroke:FC.ink,'stroke-width':2.2},s);
    if(th===0)el('line',{x1:cx,y1:cy-R,x2:cx,y2:cy+R,stroke:FC.guide,'stroke-width':1.8,'stroke-dasharray':'6 4'},s);
    else{el('path',{d:'M'+P2(cx,cy-R)+' A'+R*Math.sin(rad(th))+','+R+' 0 0 0 '+P2(cx,cy+R),fill:'none',stroke:FC.guide,'stroke-width':1.8,'stroke-dasharray':'6 4'},s);}
    hline(s,cx-R,cx+R,cy-8,'',FC.guide2);
    var near=Math.cos(rad(th-al)),far=Math.cos(rad(th+al)),ratio=far/near,ew=R*0.42;
    var xN=cx+R*Math.sin(rad(al-th)),xF=cx-R*Math.sin(rad(al+th));
    eyeDraw(s,xN,cy,ew*near/0.906,{side:1,iris:'#3d6fb0',hex:true});eyeDraw(s,xF,cy,ew*near/0.906*k,{side:-1,iris:'#3d6fb0',hex:true});
    ktxt(s,xN,cy+ew*0.7,'앞쪽 눈',{size:12,anchor:'middle',fill:C.ink});ktxt(s,xF,cy+ew*0.7,'안쪽 눈',{size:12,anchor:'middle',fill:C.ink});
    var ok=Math.abs(k-ratio)<=0.08;
    out(h).innerHTML='고개를 <b>'+th+'°</b> 돌렸을 때 공 위의 두 눈(가운데에서 ±'+al+'°)은 너비가 cos('+(th-al)+'°) = <b>'+f2(near,3)+'</b>, cos('+(th+al)+'°) = <b>'+f2(far,3)+'</b>로 보입니다 → 안쪽 눈은 앞쪽 눈의 <b>'+f2(ratio*100,0)+'%</b>. 지금 안쪽 눈 너비 <b>'+f2(k*100,0)+'%</b>. '+
      verdict(ok,ok?'공을 따라 알맞게 좁혔습니다':k>ratio?'안쪽 눈이 넓어 얼굴이 정면을 보는 것처럼 어긋납니다':'안쪽 눈을 너무 좁혔습니다');}
  allIn(h,draw);draw();};
P.p1_hatch=function(h){var W=520,H=320;
  function draw(){var L=rv(h,'lash'),I=rv(h,'iris');var s=svgOf(h,W,H);bg(s,W,H);eyeDraw(s,260,180,300,{lash:L,irisLines:I,iris:'#c7c0cc',pupilCol:'#5a4a62',hl:1});
    var ok=I>0&&I<=L*0.7,flat=I===0;
    out(h).innerHTML='속눈썹 선 <b>'+L+'</b>개, 홍채 선 <b>'+I+'</b>개 → 홍채 ÷ 속눈썹 = <b>'+f2(L?I/L:0,2)+'</b>. '+
      (flat?verdict(L<=10,L<=10?'홍채 선이 없는 단순한 눈 — 데포르메 화풍엔 어울립니다':'속눈썹만 진해 홍채가 비어 보입니다'):verdict(ok,ok?'홍채를 속눈썹보다 성기게 — 눈동자가 맑아 보입니다':'홍채 선이 속눈썹만큼 빽빽해 눈동자가 탁해 보입니다'))+
      ' <span class="hint">선 방향: 속눈썹은 눈꺼풀을 따라, 홍채는 동공에서 바깥으로 퍼지게.</span>';}
  allIn(h,draw);draw();};

/* ===================== 2부 눈 칠하기와 표정(하루) ===================== */
var SKIN=[247,224,206];
P.p2_sclera=function(h){var W=520,H=300,tint='warm';seg2(h,function(v){tint=v;draw();});
  function draw(){var L=rv(h,'light');var T={white:[1,1,1],warm:[1,0.965,0.945],cool:[0.955,0.97,1]}[tint];var sc=[L*T[0],L*T[1],L*T[2]].map(function(v){return Math.min(255,v);});
    var s=svgOf(h,W,H);bg(s,W,H);el('rect',{x:20,y:20,width:480,height:260,rx:14,fill:rgbA(SKIN)},s);eyeDraw(s,260,165,300,{sclera:rgbA(sc),iris:'#4a6fb5',lash:6});
    var a=avg3(sc),k=avg3(SKIN);var pure=sc[0]>=254&&sc[1]>=254&&sc[2]>=254;var ok=!pure&&a>k+2&&a<=246;
    out(h).innerHTML='흰자 RGB <b>'+sc.map(function(v){return Math.round(v);}).join(', ')+'</b> · 밝기(세 값의 평균) <b>'+f2(a,1)+'</b> · 피부 밝기 <b>'+f2(k,1)+'</b>. '+
      (pure?verdict(false,'순백 — 종이를 오려 붙인 것처럼 눈만 떠 보입니다'):a<=k+2?verdict(false,'흰자가 피부만큼 어두워 눈이 탁합니다'):a>246?verdict(false,'거의 순백 — 조금 더 낮추세요'):verdict(true,'피부보다 조금 밝고 순백은 아님 — 얼굴에 녹아듭니다'))+(tint==='warm'?' · 따뜻한 쪽으로 기울인 흰자는 피부색과 잘 어울립니다.':'');}
  allIn(h,draw);draw();};
var IRIS=[170,45,70],GLOW=[230,150,70];
P.p2_layers=function(h){var W=520,H=320;
  function draw(){var m=rv(h,'mult'),op=rv(h,'add')/100;var top=IRIS.map(function(v){return v*m/255;}),bot=IRIS.map(function(v,i){return Math.min(255,v+GLOW[i]*op);});
    var s=svgOf(h,W,H);bg(s,W,H);el('rect',{x:20,y:20,width:480,height:220,rx:14,fill:rgbA(SKIN)},s);
    eyeDraw(s,190,140,250,{sclera:'rgb(238,230,226)',paint:{top:rgbA(top),mid:rgbA(IRIS),bot:rgbA(bot),shadeLid:m<250?'rgb(70,40,70)':null,shadeOp:(255-m)/255*0.7},lash:6});
    [['밑색',IRIS],['곱하기 후(위쪽)',top],['더하기 후(아래쪽)',bot]].forEach(function(q,i){el('rect',{x:360,y:40+i*62,width:44,height:44,rx:8,fill:rgbA(q[1]),stroke:'#d0d6de'},s);ktxt(s,412,58+i*62,q[0],{size:12,fill:C.ink,weight:'bold'});ktxt(s,412,76+i*62,q[1].map(function(v){return Math.round(v);}).join(','),{size:11.5});});
    var okM=m>=130&&m<=205,okA=op>=0.4&&op<=0.7,blown=bot.some(function(v){return v>=255;});
    out(h).innerHTML='곱하기: 빨강 '+IRIS[0]+' × '+m+' ÷ 255 = <b>'+f2(top[0],1)+'</b>(어두워짐) · 더하기: 빨강 '+IRIS[0]+' + '+GLOW[0]+' × '+f2(op,2)+' = <b>'+f2(IRIS[0]+GLOW[0]*op,1)+'</b>'+(IRIS[0]+GLOW[0]*op>255?' → 255에서 멈춤':'')+'. '+
      verdict(okM,okM?'위쪽 그림자 알맞음':m>205?'곱하기 색이 밝아 그림자가 거의 안 보입니다':'곱하기 색이 어두워 눈동자 위가 시커멓습니다')+' · '+verdict(okA&&!blown,okA&&!blown?'아래쪽 빛 알맞음':blown?'빛이 하얗게 날아갔습니다 — 불투명도를 낮추세요':op<0.4?'빛이 약해 눈동자가 평평합니다':'빛이 강해 눈동자가 번쩍입니다');}
  allIn(h,draw);draw();};
var EMO=[['조용한 기쁨','joy','low'],['들뜬 기쁨','joy','high'],['참는 화','anger','low'],['터진 화','anger','high'],['참는 슬픔','sad','low'],['북받친 슬픔','sad','high']];
function readEmo(ang,open){var kind=ang>=8?'anger':ang<=-8?'sad':'joy';var high=kind==='sad'?open<0.7:open>1.0;var mid=kind==='sad'?open>=0.7&&open<0.95:open>=0.7&&open<=1.0;return {kind:kind,high:high,mid:mid};}
function emoName(r){var K={joy:['조용한 기쁨','들뜬 기쁨'],anger:['참는 화','터진 화'],sad:['참는 슬픔','북받친 슬픔']}[r.kind];return r.mid?K[0].replace('조용한','보통의').replace('참는','보통의')+'(중간)':K[r.high?1:0];}
P.p2_brow=function(h){var W=520,H=380;
  function draw(){var ang=rv(h,'brow'),op=rv(h,'open')/100,tg=+rv(h,'target');var s=svgOf(h,W,H);bg(s,W,H);
    var r=readEmo(ang,op);var et=r.kind==='anger'?'normal':r.kind==='sad'?'normal':(op<0.45?'normal':'sparkle');
    headF(s,260,40,320,{brow:ang,open:op,eye:et,mouth:'closed',hair:FC.hairP,buns:true,arc:r.kind==='joy'?1:0.3});
    var T=EMO[tg],got=!r.mid&&r.kind===T[1]&&(T[2]==='high')===r.high;
    out(h).innerHTML='눈썹 끝 기울기 <b>'+num(ang,0)+'°</b>(+면 끝이 올라감) · 눈 뜬 정도 <b>'+f2(op*100,0)+'%</b> → 읽히는 표정: <b>'+emoName(r)+'</b>. 목표 <b>'+T[0]+'</b>: '+verdict(got,got?'맞았습니다':'아직 다릅니다')+
      '. <span class="hint">입은 다문 채 그대로 — 눈썹 방향으로 감정의 종류를, 눈 뜬 정도로 세기를 고릅니다. 슬픔은 반대로 눈을 가늘게 뜰수록 북받쳐 보입니다.</span>';}
  allIn(h,draw);draw();};
var EYES={sparkle:['반짝이는 눈','기대·기쁨'],angry:['화난 눈','화'],tear:['눈물 고인 눈','슬픔'],tired:['지친 눈','기운 없음']};
var READ={sparkle:{smile:'기쁨과 기대가 크다',open:'놀라며 감탄한다',closed:'설렘을 꾹 누른다',wide:'환호한다',half:'멍하니 넋을 놓았다',grin:'신나는 꿍꿍이가 있다'},
 angry:{smile:'웃으며 화를 참는다(무섭다)',open:'따지며 언성을 높인다',closed:'뾰로통한 작은 화',wide:'화가 폭발했다',half:'어이없어 말을 잃었다',grin:'못된 꿍꿍이가 있다'},
 tear:{smile:'안도해서 운다',open:'흐느낀다',closed:'꾹 참으며 운다(투정으로도 읽힌다)',wide:'소리 내어 운다',half:'멍하니 눈물만 흐른다',grin:'울면서 억지로 웃는다'},
 tired:{smile:'지쳤지만 웃어 보인다',open:'하품하듯 기운 없다',closed:'말없이 버틴다',wide:'지쳐서 소리친다',half:'아무 생각이 없다',grin:'지쳤는데 수상하게 웃는다'}};
P.p2_mouth=function(h){var W=520,H=380,eye='sparkle',mouth='smile';
  ctl(h).querySelectorAll('button[data-e]').forEach(function(b){b.addEventListener('click',function(){ctl(h).querySelectorAll('button[data-e]').forEach(function(x){x.classList.remove('on');});b.classList.add('on');eye=b.dataset.e;draw();});});
  ctl(h).querySelectorAll('button[data-m]').forEach(function(b){b.addEventListener('click',function(){ctl(h).querySelectorAll('button[data-m]').forEach(function(x){x.classList.remove('on');});b.classList.add('on');mouth=b.dataset.m;draw();});});
  function draw(){var s=svgOf(h,W,H);bg(s,W,H);headF(s,260,40,320,{eye:eye,mouth:mouth,hair:FC.hairP,buns:true,open:eye==='angry'?0.85:1});
    out(h).innerHTML='<b>'+EYES[eye][0]+'</b> + <b>'+MOUTHS[mouth]+'</b> → <b>'+READ[eye][mouth]+'</b>. <span class="hint">눈은 그대로 두고 입만 바꿔 보세요. 눈으로 감정의 바탕을, 입으로 그 감정을 밖으로 내는 정도를 고릅니다.</span>';}
  draw();};

/* ===================== 3부 코·귀·입(시아·박사) ===================== */
var NLV=['','코끝 점','그림자만','코끝 + 콧날 조금','콧날에 빗금','콧날·콧방울 뚜렷'];
P.p3_nose=function(h){var W=540,H=330;
  function draw(){var n=rv(h,'nose'),f=rv(h,'face');var s=svgOf(h,W,H);bg(s,W,H);
    [140,400].forEach(function(cx,i){var lvN=i?n:3;el('rect',{x:cx-110,y:20,width:220,height:290,rx:16,fill:i?'#fff':'#f5f7fa',stroke:'#e3e8ee'},s);
      var lash=[0,2,4,8,14,20][f];[-1,1].forEach(function(d){eyeDraw(s,cx+d*52,110,74,{side:d,lash:i?lash:6,irisLines:i?Math.round(lash*0.5):3,iris:'#3a3a44',open:0.9});});
      noseDraw(s,cx,190,90,lvN);mouthDraw(s,cx,240,40,'closed');ktxt(s,cx,300,i?'지금 고른 코':'비교: 중간(3)',{size:12,anchor:'middle',fill:C.muted});});
    var d=Math.abs(n-f),ok=d<=1;
    out(h).innerHTML='코 정보량 <b>'+n+'</b>('+NLV[n]+') · 눈 정보량 <b>'+f+'</b> · 차이 <b>'+d+'</b>. '+verdict(ok,ok?'코와 눈의 그려 넣은 양이 맞습니다':n>f?'코만 실감 나게 진해 얼굴에서 튑니다':'눈은 자세한데 코가 너무 간단해 얼굴 가운데가 비어 보입니다')+
      ' <span class="hint">실제 코 → 모서리 선만 남기기 → 그중 몇 개를 고르기. 고르는 선이 적을수록 단순한(데포르메) 코입니다.</span>';}
  allIn(h,draw);draw();};
P.p3_ear=function(h){var W=540,H=360;
  function draw(){var ey=rv(h,'ear')/100,th=rv(h,'view');var s=svgOf(h,W,H);bg(s,W,H);var cx=210,cy=170,r=120,top=cy-r,chin=cy+r*0.82,HH=chin-top,eyeY=top+HH*0.5,noseY=top+HH*0.72;
    var d='M'+P2(cx+r*0.15,chin+r*0.55)+' L'+P2(cx+r*0.18,chin-r*0.05)+' C'+P2(cx+r*0.95,cy+r*0.4)+' '+P2(cx+r*1.05,cy-r*0.2)+' '+P2(cx+r*0.7,cy-r*0.75)+' C'+P2(cx+r*0.3,top-r*0.05)+' '+P2(cx-r*0.6,top)+' '+P2(cx-r*0.92,cy-r*0.4)+' L'+P2(cx-r*0.95,eyeY-r*0.1)+' L'+P2(cx-r*1.12,noseY)+' L'+P2(cx-r*0.94,noseY+r*0.08)+' L'+P2(cx-r*0.97,noseY+r*0.24)+' L'+P2(cx-r*0.9,noseY+r*0.32)+' L'+P2(cx-r*0.86,chin-r*0.04)+' Q'+P2(cx-r*0.7,chin+r*0.03)+' '+P2(cx-r*0.35,chin-r*0.12)+' L'+P2(cx-r*0.2,chin+r*0.55);
    el('path',{d:d,fill:FC.skin,stroke:FC.ink,'stroke-width':2.4},s);
    el('path',{d:'M'+P2(cx-r*0.88,eyeY-r*0.02)+' l '+P2(r*0.14,-r*0.05)+' l '+P2(-r*0.06,r*0.16)+'Z',fill:'#3a3a44'},s);
    hline(s,cx-r*1.25,cx+r*1.02,eyeY,'눈',FC.guide,true);hline(s,cx-r*1.25,cx+r*1.02,noseY,'코끝',FC.guide,true);
    var eh=HH*0.24,ecy=top+HH*ey,ex=cx+r*0.12;el('path',{d:'M'+P2(ex,ecy-eh/2)+' C'+P2(ex+eh*0.55,ecy-eh*0.62)+' '+P2(ex+eh*0.5,ecy+eh*0.35)+' '+P2(ex+eh*0.05,ecy+eh/2)+' Q'+P2(ex-eh*0.1,ecy)+' '+P2(ex,ecy-eh/2)+'Z',fill:'#f2c9bd',stroke:FC.ink,'stroke-width':2},s);
    pth(s,'M'+P2(ex+eh*0.08,ecy-eh*0.3)+' Q'+P2(ex+eh*0.32,ecy-eh*0.28)+' '+P2(ex+eh*0.28,ecy+eh*0.1),{w:1.5});
    var midT=(eyeY+noseY)/2;var ok=Math.abs(ecy-midT)<=HH*0.035;
    /* 보는 각도에 따른 귀 너비 */
    var ox=450,oy=60,w=10*Math.abs(Math.sin(rad(th)))+1.5;el('rect',{x:ox-70,y:oy-30,width:140,height:250,rx:12,fill:'#fff',stroke:'#e3e8ee'},s);
    el('ellipse',{cx:ox,cy:oy+90,rx:w*4.5,ry:62,fill:'#f2c9bd',stroke:FC.ink,'stroke-width':2},s);ktxt(s,ox,oy+180,(th<30?'정면':th<=150?(th>60&&th<120?'옆':'비스듬히'):'뒤')+' '+th+'°',{size:12.5,anchor:'middle',fill:C.ink,weight:'bold'});ktxt(s,ox,oy+200,'귀 너비 '+f2(w,1),{size:12.5,anchor:'middle',fill:C.teal,weight:'bold'});
    out(h).innerHTML='귀 가운데 높이 <b>'+f2(ey*100,0)+'%</b>(머리 높이 기준) · 눈과 코끝 사이 가운데는 <b>'+f2((0.5+0.72)/2*100,0)+'%</b>. '+verdict(ok,ok?'귀가 눈과 코끝 사이에 — 알맞은 자리':ecy<midT?'귀가 높아 얼굴이 위를 향한 것처럼 보입니다':'귀가 낮아 얼굴이 아래를 향한 것처럼 보입니다')+
      ' · 보는 각도 <b>'+th+'°</b>: 귀 너비 = 10 × |sin '+th+'°| + 두께 1.5 = <b>'+f2(w,1)+'</b>.';}
  allIn(h,draw);draw();};
P.p3_open=function(h){var W=520,H=360;
  function draw(){var a=rv(h,'jaw'),wrong=rv(h,'wrong');var s=svgOf(h,W,H);bg(s,W,H);var cx=260,y0=120,D=60,dep=D*Math.sin(rad(a)),drop=a*3.2;
    el('path',{d:'M'+P2(cx-170,40)+' L'+P2(cx-165,y0+40+drop*0.6)+' Q'+P2(cx-110,y0+150+drop)+' '+P2(cx,y0+175+drop)+' Q'+P2(cx+110,y0+150+drop)+' '+P2(cx+165,y0+40+drop*0.6)+' L'+P2(cx+170,40)+'Z',fill:FC.skin,stroke:FC.ink,'stroke-width':2.2},s);
    var mw=130,top=y0,bot=y0+18+drop;el('path',{d:'M'+P2(cx-mw,top)+' Q'+P2(cx,top-10)+' '+P2(cx+mw,top)+' Q'+P2(cx+mw*0.85,bot+12)+' '+P2(cx,bot+18)+' Q'+P2(cx-mw*0.85,bot+12)+' '+P2(cx-mw,top)+'Z',fill:'#5a2a35',stroke:FC.ink,'stroke-width':2.2},s);
    el('rect',{x:cx-mw*0.72,y:top-2,width:mw*1.44,height:16,rx:3,fill:'#fff',stroke:FC.ink,'stroke-width':1.4},s);for(var i=1;i<8;i++)el('line',{x1:cx-mw*0.72+mw*1.44*i/8,y1:top-1,x2:cx-mw*0.72+mw*1.44*i/8,y2:top+13,stroke:'#b9b1b8','stroke-width':1},s);
    var ly=bot+6;if(wrong){el('rect',{x:cx-mw*0.7,y:ly-14,width:mw*1.4,height:14,rx:3,fill:'#fff',stroke:FC.ink,'stroke-width':1.4},s);}
    else{var uw=mw*0.7,ud=dep;var dd='M'+P2(cx-uw,ly-ud-6)+' Q'+P2(cx-uw,ly+4)+' '+P2(cx,ly+4)+' Q'+P2(cx+uw,ly+4)+' '+P2(cx+uw,ly-ud-6);
      el('path',{d:dd,fill:'none',stroke:'#fff','stroke-width':14,'stroke-linecap':'round'},s);pth(s,dd,{w:1.2,stroke:'#8d8590'});}
    el('ellipse',{cx:cx,cy:ly-dep*0.5-2,rx:mw*0.38,ry:Math.max(4,dep*0.45),fill:'#d9707f'},s);
    ktxt(s,cx+mw+18,top+10,'위 이줄 — 一',{size:12.5,fill:C.ink,weight:'bold'});ktxt(s,cx+mw+18,ly,'아래 이줄 — '+(wrong?'一(오답)':'U'),{size:12.5,fill:wrong?C.red:C.teal,weight:'bold'});
    out(h).innerHTML='아래턱을 <b>'+a+'°</b> 벌림 → 아래 이줄(깊이 10)이 보이는 깊이 = 10 × sin '+a+'° = <b>'+f2(dep/6,1)+'</b>. '+(wrong?verdict(false,'아래 이도 一로 그려 입속이 납작한 판처럼 보입니다'):verdict(a>=8,a>=8?'위 이는 一, 아래 이는 U — 내려다보는 각도라 둥근 이줄이 보입니다':'아직 거의 다문 입 — 벌릴수록 U가 깊어집니다'))+'. <span class="hint">위턱은 머리에 붙어 움직이지 않고, 아래턱만 귀 앞을 축으로 돕니다.</span>';}
  allIn(h,draw);draw();};
P.p3_molar=function(h){var W=540,H=340;
  function draw(){var t=rv(h,'conv')/100;var s=svgOf(h,W,H);bg(s,W,H);var A=[150,140],B=[150,215],V=[420,178];
    el('path',{d:'M'+P2(110,130)+' Q'+P2(270,95)+' '+P2(430,160)+' Q'+P2(300,250)+' '+P2(110,230)+' Q'+P2(90,180)+' '+P2(110,130)+'Z',fill:'#5a2a35',stroke:FC.ink,'stroke-width':2.2},s);
    function dir(P0){var v=[lerp(1,V[0]-P0[0],t),lerp(0,V[1]-P0[1],t)];var L=Math.hypot(v[0],v[1]);return [v[0]/L,v[1]/L];}
    var du=dir(A),dl=dir(B);[[A,du,-1],[B,dl,1]].forEach(function(q){var P0=q[0],d=q[1];for(var i=0;i<6;i++){var x=P0[0]+d[0]*i*42,y=P0[1]+d[1]*i*42;var sz=22*(1-i*0.11);el('rect',{x:x-sz/2,y:y-(q[2]<0?0:sz*0.8),width:sz,height:sz*0.8,rx:3,fill:'#fff',stroke:FC.ink,'stroke-width':1.2,transform:'rotate('+deg(Math.atan2(d[1],d[0])).toFixed(1)+' '+x.toFixed(1)+' '+y.toFixed(1)+')'},s);}
      el('line',{x1:P0[0],y1:P0[1],x2:P0[0]+d[0]*420,y2:P0[1]+d[1]*420,stroke:FC.guide,'stroke-width':1.6,'stroke-dasharray':'6 4'},s);});
    var den=du[0]*dl[1]-du[1]*dl[0];var meet=null;if(Math.abs(den)>1e-4){var tt=((B[0]-A[0])*dl[1]-(B[1]-A[1])*dl[0])/den;if(tt>0)meet=[A[0]+du[0]*tt,A[1]+du[1]*tt];}
    el('circle',{cx:V[0],cy:V[1],r:8,fill:'none',stroke:C.teal,'stroke-width':2.4},s);ktxt(s,V[0]+12,V[1]-10,'턱 경첩 쪽',{size:12,fill:C.teal,weight:'bold'});
    if(meet&&meet[0]<W)el('circle',{cx:meet[0],cy:meet[1],r:6,fill:FC.guide},s);
    var dist=meet?Math.hypot(meet[0]-V[0],meet[1]-V[1]):Infinity;var ok=t>=0.75;
    out(h).innerHTML='모으는 정도 <b>'+f2(t*100,0)+'%</b> · 위·아래 어금니 줄을 늘인 선이 만나는 점까지 거리 <b>'+(isFinite(dist)?f2(dist,0)+'px':'만나지 않음(평행)')+'</b>. '+
      verdict(ok,ok?'두 줄이 안쪽 한 점으로 모입니다 — 입속 깊이가 보입니다':t<0.3?'어금니가 정면을 향해 서 있습니다 — 보이지 않는 안쪽 방향을 놓쳤습니다':'모이긴 하지만 만나는 점이 너무 멉니다')+'. <span class="hint">보이지 않는 이줄까지 이어 그려 보면, 위·아래 줄이 호두까기 인형처럼 나란히 열리고 안쪽에서 한 점으로 모입니다.</span>';}
  allIn(h,draw);draw();};

/* ===================== 4부 머리카락(하루·시아·모아) ===================== */
function bobHair(s,cx,top,H,k,col,blocks,lv){var R=H*0.47*k,hc=col;var g=el('g',{},s);var ey=top+H*0.5;
  var outer='M'+P2(cx-R*1.02,ey+H*0.36)+' Q'+P2(cx-R*1.18,top+H*0.47-R*1.05)+' '+P2(cx,top+H*0.47-R*1.06)+' Q'+P2(cx+R*1.18,top+H*0.47-R*1.05)+' '+P2(cx+R*1.02,ey+H*0.36)+'Z';
  el('path',{d:outer,fill:hc,stroke:FC.ink,'stroke-width':2.2},g);
  if(blocks){var cid=uid('hb');var cpp=el('clipPath',{id:cid},g);el('path',{d:outer},cpp);var bg2=el('g',{'clip-path':'url(#'+cid+')'},g);var cols=['#f2a7c3','#9db8f0','#a8dca0','#f5d08a','#c9a7f0','#9fe0dc','#f2b39d','#e7c0a0'];var cyw=top+H*0.47-R*1.0,yb=ey+H*0.4;
    for(var i=0;i<blocks;i++){var x0=cx-R*1.25+2*R*1.25*i/blocks,x1=cx-R*1.25+2*R*1.25*(i+1)/blocks;
      el('path',{d:'M'+P2(cx+(x0-cx)*0.18,cyw)+' L'+P2(cx+(x1-cx)*0.18,cyw)+' Q'+P2(x1,cyw+H*0.1)+' '+P2(x1,yb)+' L'+P2(x0,yb)+' Q'+P2(x0,cyw+H*0.1)+' '+P2(cx+(x0-cx)*0.18,cyw)+'Z',fill:cols[i%8],opacity:.75,stroke:'#fff','stroke-width':1.5},bg2);}
    el('path',{d:outer,fill:'none',stroke:FC.ink,'stroke-width':2.2},g);}
  if(lv){for(var j=0;j<lv*3;j++){var xx=cx-R*0.95+R*1.9*j/(lv*3-1+0.001);pth(g,'M'+P2(cx+(xx-cx)*0.2,top+H*0.47-R*0.95)+' Q'+P2(xx,ey-H*0.1)+' '+P2(xx*0.98+cx*0.02,ey+H*0.3),{w:1,op:.55});}}
  return g;}
P.p4_volume=function(h){var W=520,H=380;
  function draw(){var k=rv(h,'vol')/100;var s=svgOf(h,W,H);bg(s,W,H);var cx=260,top=60,HH=290;
    bobHair(s,cx,top,HH,k,'#2b2630');headF(s,cx,top,HH,{noHair:true,mouth:'smile',eye:'normal'});
    el('circle',{cx:cx,cy:top+HH*0.47,r:HH*0.47,fill:'none',stroke:FC.guide,'stroke-width':1.8,'stroke-dasharray':'6 4'},s);
    var area=k*k;var face=1/area;var ok=k>=1.05&&k<=1.15;
    out(h).innerHTML='머리카락 바깥선 = 머리 밑그림(분홍 점선) × <b>'+f2(k,2)+'</b> → 넓이는 '+f2(k,2)+'² = <b>'+f2(area,2)+'배</b>, 머리 전체에서 얼굴이 차지하는 몫은 <b>'+f2(face*100,0)+'%</b>로 보입니다. '+
      verdict(ok,ok?'머리 밑그림보다 조금 크게 — 얼굴이 알맞은 크기로 보입니다':k<1.05?'머리카락이 밑그림에 붙어 머리가 작고, 그만큼 얼굴이 커 보입니다':'머리카락이 헬멧처럼 부풀었습니다');}
  allIn(h,draw);draw();};
P.p4_blocks=function(h){var W=520,H=380;
  function draw(){var b=rv(h,'blocks'),lv=rv(h,'level');var s=svgOf(h,W,H);bg(s,W,H);var cx=260,top=60,HH=290;
    bobHair(s,cx,top,HH,1.1,'#d9a7bd',b,0);var lash=[0,2,4,8,14,20][lv];var R=HH*0.47,ey=top+HH*0.5,ew=R*0.38;
    el('path',{d:'M'+P2(cx,top)+' C'+P2(cx-R*0.56,top)+' '+P2(cx-R*0.88,top+R*0.4)+' '+P2(cx-R*0.88,top+R)+' C'+P2(cx-R*0.88,top+R*1.55)+' '+P2(cx-R*0.36,top+HH-R*0.1)+' '+P2(cx,top+HH)+' C'+P2(cx+R*0.36,top+HH-R*0.1)+' '+P2(cx+R*0.88,top+R*1.55)+' '+P2(cx+R*0.88,top+R)+' C'+P2(cx+R*0.88,top+R*0.4)+' '+P2(cx+R*0.56,top)+' '+P2(cx,top)+'Z',fill:FC.skin,stroke:FC.ink,'stroke-width':2.2},s);
    [-1,1].forEach(function(d){eyeDraw(s,cx+d*(ew*1.05),ey+ew*0.2,ew,{side:d,lash:lash,irisLines:Math.round(lash/2),iris:'#4a3b5c'});});noseDraw(s,cx,ey+HH*0.2,HH*0.12,Math.min(5,lv));mouthDraw(s,cx,top+HH*0.86,HH*0.13,'smile');
    var want=lv+1,ok=Math.abs(b-want)<=1;
    out(h).innerHTML='머리 덩어리 <b>'+b+'</b>개 · 얼굴 정보량 <b>'+lv+'</b> → 어울리는 덩어리 수는 <b>'+want+'개 안팎</b>. '+verdict(ok,ok?'머리와 얼굴의 그려 넣은 양이 맞습니다':b>want?'머리만 잘게 나눠 얼굴보다 복잡합니다':'얼굴은 자세한데 머리가 큰 판 하나처럼 보입니다')+' <span class="hint">덩어리가 적으면 평면적(단순), 많으면 입체적(실감)입니다. 덩어리 안을 또 나누면 더 자세해집니다.</span>';}
  allIn(h,draw);draw();};
P.p4_flow=function(h){var W=520,H=360;
  function draw(){var mode=rv(h,'mode'),style=rv(h,'style'),part=rv(h,'part')/100;var s=svgOf(h,W,H);bg(s,W,H);var cx=260,cy=200,R=130;
    el('ellipse',{cx:cx,cy:cy,rx:R,ry:R*1.08,fill:'#dbe7f6',stroke:FC.ink,'stroke-width':2},s);hline(s,cx-R,cx+R,cy+10,'',FC.guide2);
    var px=cx+(part-0.5)*R*1.2;var crown=[px,cy-R*0.95];
    if(mode==='one'){for(var i=0;i<14;i++){var a=Math.PI*(0.05+0.9*i/13);var ex=cx-Math.cos(a)*R*1.05,ey2=cy-Math.sin(a)*R*0.2+R*0.35;pth(s,'M'+P2(crown[0],crown[1])+' Q'+P2((crown[0]+ex)/2,cy-R*0.9)+' '+P2(ex,ey2),{stroke:'#7a4fb0',w:2});}
      el('circle',{cx:crown[0],cy:crown[1],r:7,fill:FC.guide},s);}
    else{for(var j=0;j<16;j++){var t=j/15;var sx=lerp(cx-R*0.92,cx+R*0.92,t),sy=cy-R*0.55-Math.sin(Math.PI*t)*R*0.42;var dx=sx<px?-1:1;
        pth(s,'M'+P2(sx+dx*4,sy-12)+' Q'+P2(sx+dx*R*0.15,sy+R*0.2)+' '+P2(sx+dx*R*0.22,sy+R*0.75),{stroke:'#7a4fb0',w:2});}
      pth(s,'M'+P2(px,cy-R*1.0)+' L'+P2(px+(px-cx)*0.1,cy-R*0.45),{stroke:FC.guide,w:2.4,dash:'5 3'});}
    var ok=mode==='all'||style==='simple';
    out(h).innerHTML='나는 자리: <b>'+(mode==='one'?'정수리 한 점':'머리 전체(가르마·머리선에서)')+'</b> · 그림 성격: <b>'+(style==='simple'?'단순한 그림':'실감 나는 그림')+'</b>. '+
      verdict(ok,mode==='one'?(ok?'단순한 그림에서는 한 점에서 나는 머리도 약속으로 통합니다':'실감 나는 그림에서 한 점에서만 나면 머리카락이 머리 위에 얹힌 가발처럼 보입니다'):'머리 전체에서 나고, 가르마·정수리에서 흘러내립니다')+'.';}
  allIn(h,draw);draw();};
P.p4_strands=function(h){var W=520,H=320;
  function draw(){var v=rv(h,'vary')/100,n=rv(h,'thin'),style=rv(h,'style');var s=svgOf(h,W,H);bg(s,W,H);var r=rng(7);
    for(var i=0;i<9;i++){var x=60+i*48,w=lerp(26,10+32*r(),v);var x2=x+10+20*r();el('path',{d:'M'+P2(x-w/2,30)+' Q'+P2(x-w/2+6,170)+' '+P2(x2,290)+' Q'+P2(x+w/2+4,170)+' '+P2(x+w/2,30)+'Z',fill:i%2?'#9aa9e8':'#b8c4f2',stroke:FC.ink,'stroke-width':1.8},s);}
    for(var j=0;j<n;j++){var xx=80+j*52+r()*10;pth(s,'M'+P2(xx,40+r()*30)+' Q'+P2(xx+12,180)+' '+P2(xx+18+r()*10,280),{w:1,stroke:'#c0306a'});}
    var real=style==='real';var ok=real?(v>=0.3&&v<=0.8&&n>=1&&n<=6):v<=0.4;
    out(h).innerHTML='다발 굵기 차이 <b>'+f2(v*100,0)+'%</b> · 한 가닥 선 <b>'+n+'</b>개 · 화풍 <b>'+(real?'실감 나는 그림':'단순한 그림')+'</b>. '+
      verdict(ok,ok?(real?'굵고 가는 다발이 섞여 자연스럽고, 가는 선이 결을 더합니다':'굵기가 고른 다발 — 단순한 그림과 잘 맞습니다'):(real?(v<0.3?'다발 굵기가 똑같아 단조롭습니다':v>0.8?'굵기 차이가 너무 커 지저분합니다':n<1?'가는 한 가닥 선을 조금 더하면 머리결이 살아납니다':'가는 선이 너무 많아 산만합니다'):'단순한 그림에 굵기 차이가 커서 혼자 튑니다'))+'.';}
  allIn(h,draw);draw();};

/* ===================== 5부 AI로 디테일 살리기 ===================== */
var LVW={eye:['','simple dot-like eyes','simple eyes with one highlight','anime eyes with soft lashes and two highlights','detailed eyes with fine lash strands and iris lines','highly detailed realistic eyes'],
 nose:['','nose as a tiny dot','nose shown only by a soft shadow','small nose tip with a short bridge line','nose bridge with light hatching','clearly drawn nose bridge and nostrils'],
 mouth:['','simple line mouth','simple mouth','mouth with a hint of lips','mouth with lips and soft shading','fully rendered lips and teeth'],
 hair:['','hair as one flat shape','hair in two or three big clumps','hair in four or five clumps with a few strands','hair in many clumps with fine strands','highly detailed hair with individual strands']};
P.p5_detail=function(h){var W=520,H=230;
  function draw(){var v={eye:rv(h,'eye'),nose:rv(h,'nose'),mouth:rv(h,'mouth'),hair:rv(h,'hair')};var s=svgOf(h,W,H);bg(s,W,H);
    var keys=['eye','nose','mouth','hair'],lab={eye:'눈',nose:'코',mouth:'입',hair:'머리'};keys.forEach(function(k,i){el('rect',{x:80,y:20+i*50,width:v[k]*80,height:32,rx:6,fill:C.teal,opacity:.25+v[k]*0.15},s);ktxt(s,70,41+i*50,lab[k],{size:13,anchor:'end',fill:C.ink,weight:'bold'});ktxt(s,90+v[k]*80,41+i*50,String(v[k]),{size:13,fill:C.ink});});
    var arr=keys.map(function(k){return v[k];});var spread=Math.max.apply(null,arr)-Math.min.apply(null,arr);var ok=spread<=1;
    var txt=keys.map(function(k){return LVW[k][v[k]];}).join(', ')+(ok?', consistent level of detail across the face':'');
    out(h).innerHTML='가장 자세한 곳과 가장 단순한 곳의 차이 <b>'+spread+'</b>. '+verdict(ok,ok?'부위의 정보량이 고릅니다':'한 부위만 튑니다 — 차이를 1 이하로')+'<div class="promptbox" style="margin-top:8px"><b>조립된 디테일 문장</b><pre>'+txt+'</pre></div>';}
  allIn(h,draw);draw();};
var PAINT=[['sc','흰자는 순백이 아니게','off-white sclera slightly warmer than pure white'],['mul','눈동자 위쪽에 곱하기 그림자','darker shadow on the upper part of the iris under the eyelid'],['add','눈동자 아래쪽에 빛','warm glow on the lower part of the iris'],['hl','하이라이트 두 개','one large and one small highlight in each eye'],['line','밝은 곳 둘레 선은 갈색','line art around light areas tinted brown, not pure black']];
P.p5_paint=function(h){var W=520,H=280;
  function draw(){var on={};PAINT.forEach(function(p){on[p[0]]=rv(h,p[0]);});var s=svgOf(h,W,H);bg(s,W,H);el('rect',{x:20,y:20,width:480,height:240,rx:14,fill:rgbA(SKIN)},s);
    var base=[70,110,170];eyeDraw(s,260,165,290,{sclera:on.sc?'rgb(238,230,226)':'#ffffff',paint:{top:on.mul?rgbA(base.map(function(v){return v*0.55;})):rgbA(base),mid:rgbA(base),bot:on.add?rgbA([140,170,215]):rgbA(base),shadeLid:on.mul?'rgb(70,50,80)':null,shadeOp:.3},hl:on.hl?1.2:0,lash:8,lineCol:on.line?'#5a3a30':FC.ink});
    var n=PAINT.filter(function(p){return on[p[0]];}).length;var txt=PAINT.filter(function(p){return on[p[0]];}).map(function(p){return p[2];}).join(', ');
    out(h).innerHTML='칠하기 조각 <b>'+n+' / 5</b>. '+verdict(n>=4,n>=4?'눈이 얼굴에 녹아들고 깊이가 생겼습니다':'조각이 적어 눈이 스티커처럼 평평합니다')+'<div class="promptbox" style="margin-top:8px"><b>조립된 칠하기 문장</b><pre>'+(txt||'(조각을 골라 보세요)')+'</pre></div>';}
  allIn(h,draw);draw();};
P.p5_mask=function(h){var W=520,H=380;var REG={eyes:[360,120,'눈 두 개(눈썹 포함)'],mouth:[200,110,'입'],face:[620,700,'얼굴 전체']};
  function draw(){var reg=rv(h,'reg'),pad=rv(h,'pad')/100;var R=REG[reg];var mw=R[0]*(1+pad),mh=R[1]*(1+pad);var s=svgOf(h,W,H);bg(s,W,H);var sc=H/1536*0.92,ox=(W-1024*sc)/2,oy=14;
    el('rect',{x:ox,y:oy,width:1024*sc,height:1536*sc,fill:'#fff',stroke:'#d0d6de'},s);headF(s,ox+512*sc,oy+300*sc,620*sc,{hair:FC.hairB,eye:'normal',mouth:'smile'});
    var cy={eyes:oy+(300+620*0.53)*sc,mouth:oy+(300+620*0.86)*sc,face:oy+(300+620*0.5)*sc}[reg];
    el('rect',{x:ox+512*sc-mw*sc/2,y:cy-mh*sc/2,width:mw*sc,height:mh*sc,fill:'rgba(224,51,127,.25)',stroke:FC.guide,'stroke-width':2},s);
    var ratio=mw*mh/(1024*1536);var ok=reg!=='face'&&ratio<=0.06&&pad>=0.1;
    out(h).innerHTML='그림 1024 × 1536 = <b>1,572,864</b>픽셀 · 가림 영역 '+f2(mw,0)+' × '+f2(mh,0)+' = <b>'+Math.round(mw*mh).toLocaleString()+'</b> → 다시 그려지는 몫 <b>'+f2(ratio*100,2)+'%</b>. '+
      verdict(ok,reg==='face'?'얼굴 전체를 가리면 사람이 바뀝니다 — 고칠 부위만':ok?R[2]+'만 가렸고 둘레 여유도 있습니다':pad<0.1?'경계에 여유가 없어 이음매가 보일 수 있습니다':'가린 곳이 넓어 다른 부위까지 바뀝니다');}
  allIn(h,draw);draw();};
var STY={chibi:['단순(데포르메)',1,0,'코는 점, 속눈썹 굵은 선 하나, 하이라이트 크게'],anime:['애니풍',3,2,'코끝 + 콧날 조금, 속눈썹 몇 가닥, 하이라이트 두 개'],semi:['반실사',4,4,'콧날 빗금, 속눈썹·홍채 선 많이, 하이라이트 작게']};
P.p5_style=function(h){var W=540,H=300,st='anime';seg2(h,function(v){st=v;draw();});
  function draw(){var p=STY[st];var s=svgOf(h,W,H);bg(s,W,H);var lash=[0,2,4,8,14,20][p[1]];
    [-1,1].forEach(function(d){var g=eyeDraw(s,270+d*95,120,150,{side:d,inY:0,outY:0.6,lash:lash,irisLines:p[2]*2,hl:st==='chibi'?1.5:st==='semi'?0.6:1,iris:'#3d6fb0',hex:true});});
    noseDraw(s,270,215,90,p[1]);mouthDraw(s,270,262,60,'closed');
    out(h).innerHTML='<b>'+p[0]+'</b>: '+p[3]+'. 분홍 육각형(눈머리·눈꼬리 자리)과 각막 → 홍채 → 동공 순서, 위 이 一·아래 이 U 같은 <b>구조는 화풍이 바뀌어도 그대로</b>이고, 바뀌는 것은 <b>그려 넣는 양</b>입니다.';}
  draw();};

/* ===================== 6부 진단 ===================== */
var CHECK6=['① 자리와 각도(부위 위치·고개 방향)','② 구조(육각형·각막·이줄·머리 부피·나는 자리)','③ 정보량(부위끼리 맞춤)','④ 칠하기(흰자·그림자·빛·하이라이트)','⑤ 표정(눈썹·눈·입 조합)'];
var FAIL6=[1,0,0,1,1,2,3,4];var FAILWHY6=['동공이 각막 밖으로 튀어나왔습니다.','비스듬한 얼굴인데 두 눈의 너비가 같습니다.','귀가 눈~코끝 사이보다 낮습니다.','벌린 입의 어금니가 정면을 향합니다.','머리카락이 머리 밑그림에 붙어 부피가 없습니다.','코만 실감 나게 진해 다른 부위와 정보량이 다릅니다.','흰자가 순백이고 눈동자가 한 색이라 스티커 같습니다.','눈썹 끝이 올라가 기쁨이 아니라 화로 읽힙니다.'];
P.p6_check=function(h){var c=ctl(h),sel=c.querySelector('select');h.innerHTML='';var list=document.createElement('div');list.style.cssText='display:flex;flex-direction:column;gap:6px';h.appendChild(list);var done=0;
  function build(){list.innerHTML='';done=0;CHECK6.forEach(function(t,i){var b=document.createElement('button');b.type='button';b.className='btn';b.style.textAlign='left';b.textContent=t;b.addEventListener('click',function(){press(i,b);});list.appendChild(b);});out(h).innerHTML='점검표를 <b>위에서부터</b> 눌러 보세요.';}
  function press(i,b){var f=+sel.value,at=FAIL6[f];if(i!==done){out(h).innerHTML='순서대로! 먼저 <b>'+CHECK6[done]+'</b>을 보세요. 큰 것에서 작은 것 순서입니다.';return;}
    if(i<at){b.style.borderColor=C.green;b.style.background='#ecf7ef';b.textContent=CHECK6[i]+' — 통과';done++;out(h).innerHTML=CHECK6[i]+' 통과. 다음 항목으로.';}
    else{b.style.borderColor=C.red;b.style.background='#fdeceb';b.textContent=CHECK6[i]+' — 여기서 걸림';done=99;out(h).innerHTML='<b>'+CHECK6[i]+'</b>에서 처음 걸렸습니다: '+FAILWHY6[f]+' 아래 실패 카드 f'+(f+1)+'에서 고치는 조각을 보세요.';}}
  sel.addEventListener('change',build);build();};

/* ===================== 실전 연습장 ===================== */
function practice(){var root=document.getElementById('practice');if(!root)return;var tabs=root.querySelectorAll('.tabs button'),scenes=root.querySelectorAll('.scene');
  function show(id){tabs.forEach(function(b){b.classList.toggle('on',b.dataset.t===id);});scenes.forEach(function(s){s.classList.toggle('on',s.id===id);});if(history.replaceState)history.replaceState(null,'','#'+id);}
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});var hsh=(location.hash||'').slice(1);show([].some.call(scenes,function(s){return s.id===hsh;})?hsh:'bench');
  bench();expr();workshop();desk();}
function wire(S,f){S.querySelectorAll('.ctrl input,.ctrl select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
function bench(){var S=document.getElementById('bench');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var touched=false,hit={};
  function upd(e){if(e)touched=true;var tgt=q('target').value,turn=+q('turn').value,a=+q('inY').value/10,b=+q('outY').value/10,far=+q('far').value/100,pup=+q('pupil').value;
    var ang=deg(Math.atan((b-a)/10));var shapeOk=tgt==='up'?ang>=8:tgt==='down'?ang<0:(ang>=0&&ang<8);var ratio=turn?Math.cos(rad(55))/Math.cos(rad(5)):1;var farOk=Math.abs(far-ratio)<=0.08;var pupOk=pup<=2;
    if(touched&&shapeOk&&farOk&&pupOk)hit[tgt+turn]=1;
    board(S.querySelector('.board'),[['눈 모양',f2(ang,1)+'°',shapeOk],['안쪽 눈 너비',f2(far*100,0)+'% (목표 '+f2(ratio*100,0)+'%)',farOk],['동공 위치',pup<=2?'각막 안쪽':'각막에 붙음/밖',pupOk],['완성한 조합',Object.keys(hit).length+' / 6',Object.keys(hit).length>=6]]);
    var s=el('svg',{viewBox:'0 0 430 300',role:'img','aria-label':'눈 작업대'});var g1=S.querySelector('.g1');g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:430,height:300,fill:'#fbfcfd'},s);
    eyeDraw(s,310,150,150,{side:1,inY:a,outY:b,hex:true,iris:'#3d6fb0'});eyeDraw(s,215-150*far*0.5-20,150,150*far,{side:-1,inY:a,outY:b,hex:true,iris:'#3d6fb0'});
    var s2=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'옆에서 본 동공'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s2);el('circle',{cx:220,cy:100,r:80,fill:'#fbf6f2',stroke:FC.ink,'stroke-width':2},s2);
    var ix=220-66;pth(s2,'M'+P2(ix,60)+' Q'+P2(ix-34,100)+' '+P2(ix,140),{stroke:C.blue,w:2.2});el('line',{x1:ix,y1:60,x2:ix,y2:140,stroke:'#8a5a2b','stroke-width':5},s2);el('ellipse',{cx:ix-pup*2,cy:100,rx:4,ry:16,fill:'#1d1622'},s2);ktxt(s2,20,190,'옆에서 본 눈 — 동공은 각막 안쪽',{size:12});
    var M=[!!(hit.up0||hit.up1),!!hit.down1,Object.keys(hit).length>=3];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','목표: '+{up:'올라간 눈',mid:'기본 눈',down:'처진 눈'}[tgt]+', '+(turn?'비스듬히 30°':'정면')+'.'],['moa','e10','모아',shapeOk?'눈 모양은 맞았어요.':'눈꼬리와 눈머리 높이를 다시 봐요.'],['fruitfly','e09','초파리',farOk?(pupOk?'안쪽 눈 너비도, 동공도 좋아.':'동공이 각막 밖이야. 안쪽으로 밀어.'):'공 위의 눈이야. 안쪽 눈은 '+f2(ratio*100,0)+'%쯤.']]);}
  wire(S,upd);upd();}
function expr(){var S=document.getElementById('expr');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var touched=false,hit={};
  function upd(e){if(e)touched=true;var tg=+q('target').value,ang=+q('brow').value,op=+q('open').value/100,m=q('mouth').value;var r=readEmo(ang,op);var T=EMO[tg];
    var kindOk=r.kind===T[1],powOk=!r.mid&&(T[2]==='high')===r.high;var mouthOk={joy:T[2]==='high'?['smile','wide','open']:['smile','closed'],anger:T[2]==='high'?['wide','open']:['closed','half'],sad:T[2]==='high'?['wide','open']:['closed','half']}[T[1]].indexOf(m)>=0;
    if(touched&&kindOk&&powOk&&mouthOk)hit[tg]=1;
    board(S.querySelector('.board'),[['눈썹(감정 종류)',num(ang,0)+'°',kindOk],['눈 뜬 정도(세기)',f2(op*100,0)+'%',powOk],['입',MOUTHS[m],mouthOk],['완성한 표정',Object.keys(hit).length+' / 6',Object.keys(hit).length===6]]);
    var s=el('svg',{viewBox:'0 0 360 330',role:'img','aria-label':'표정 조합 결과'});var g1=S.querySelector('.g1');g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:360,height:330,fill:'#fbfcfd'},s);
    headF(s,180,25,290,{brow:ang,open:op,eye:r.kind==='joy'&&op>=0.5?'sparkle':'normal',mouth:m,hair:FC.hairB});
    var s2=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'완성한 표정'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s2);
    EMO.forEach(function(t,i){el('rect',{x:12+(i%3)*116,y:20+Math.floor(i/3)*86,width:108,height:70,rx:8,fill:hit[i]?'#e8f6ec':'#f2f4f7',stroke:hit[i]?C.green:'#d5dbe2'},s2);ktxt(s2,66+(i%3)*116,60+Math.floor(i/3)*86,t[0]+(hit[i]?' ✓':''),{size:12,anchor:'middle',fill:C.ink});});
    var M=[!!hit[2],!!hit[5],Object.keys(hit).length===6];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','목표: '+T[0]+'. 지금은 '+emoName(r)+'으로 읽힌다.'],['haru','e10','조수',kindOk?(powOk?'세기도 맞았어요!':'종류는 맞았고, 눈 뜬 정도로 세기를 맞춰요.'+(T[1]==='sad'?' 슬픔은 가늘게 뜰수록 북받쳐요.':'')):'눈썹 방향부터 바꿔요.'],['x3','e09','평가단 X3',mouthOk?'입도 표정과 어울려요.':'입이 표정과 따로 놀아요.']]);}
  wire(S,upd);upd();}
var WF=[['eye','눈 모양',[['','고르기'],['up','올라간 눈(눈꼬리 높게)'],['mid','기본 눈'],['down','처진 눈(눈꼬리 낮게)']]],['paint','눈 칠하기',[['','고르기'],['none','한 색으로'],['layer','흰자 순백 아님 + 위 그림자 + 아래 빛']]],['nose','코',[['','고르기'],['dot','코끝 점'],['shadow','그림자만'],['bridge','콧날 뚜렷']]],
 ['mouth','입',[['','고르기'],['closed','다문 입'],['smile','웃는 입'],['wide','크게 벌린 입(위 이 一, 아래 이 U)']]],['hair','머리',[['','고르기'],['vol','머리 밑그림보다 조금 크게, 전체에서 나는 머리'],['flat','두피에 붙은 머리']]],['level','정보량',[['','고르기'],['even','부위끼리 고르게'],['mixed','부위마다 제각각']]],['age','나이',[['','고르기'],['adult','20대 성인으로 명시']]]];
var WFT={eye:{up:'sharp eyes with the outer corners clearly higher than the inner corners',mid:'eyes with the outer corners slightly higher than the inner corners',down:'gentle droopy eyes with the outer corners lower than the inner corners'},paint:{none:'flat single-color irises',layer:'off-white sclera, darker upper iris under the eyelid, warm glow on the lower iris, two highlights'},nose:{dot:'nose as a tiny dot',shadow:'nose shown only by a soft shadow',bridge:'clearly drawn nose bridge'},
 mouth:{closed:'closed mouth',smile:'gentle smile',wide:'wide open laughing mouth, upper teeth as a straight row, lower teeth curving as a U'},hair:{vol:'hair with natural volume slightly larger than the skull, growing from the whole scalp',flat:'hair flat against the scalp'},level:{even:'the same level of detail on eyes, nose, mouth and hair',mixed:''},age:{adult:'an adult in her twenties, adult proportions'}};
function workshop(){var S=document.getElementById('workshop');if(!S)return;var touched=false;var box=S.querySelector('.ow');
  box.innerHTML=WF.map(function(f){return '<label>'+f[1]+' <select name="'+f[0]+'">'+f[2].map(function(o){return '<option value="'+o[0]+'">'+o[1]+'</option>';}).join('')+'</select></label>';}).join('');
  var job=S.querySelector('[name=job]');S.querySelectorAll('select').forEach(function(x){x.addEventListener('change',function(){touched=true;upd();});});
  function upd(){var o={};WF.forEach(function(f){o[f[0]]=S.querySelector('[name='+f[0]+']').value;});var parts=['Front view, chest-up anime portrait of '+(o.age?WFT.age.adult:'a woman')];
    ['eye','paint','nose','mouth','hair','level'].forEach(function(k){if(o[k]&&WFT[k][o[k]])parts.push(WFT[k][o[k]]);});var text=parts.join(', ')+'. No text.';S.querySelector('.g1 pre').textContent=text;
    var score=['eye','paint','nose','mouth','hair','level'].filter(function(k){return o[k]&&o[k]!=='none'&&o[k]!=='flat'&&o[k]!=='mixed';}).length;var warn=[];
    if(o.nose==='bridge'&&o.eye&&o.paint!=='layer'&&o.level==='even')warn.push('콧날은 뚜렷한데 눈은 한 색 — 정보량이 어긋납니다.');
    if(o.nose==='dot'&&o.paint==='layer'&&o.level!=='even')warn.push('코는 점인데 눈은 자세합니다. 정보량을 맞추라는 조각을 넣으세요.');
    if(o.eye&&o.mouth==='wide'&&!o.age)warn.push('반짝이는 큰 웃음은 나이가 어려 보이는 쪽으로 쏠립니다. 성인 나이를 적으세요.');
    warn=warn.filter(Boolean);var need={close:['eye','paint'],sheet:['mouth','eye'],hair:['hair','level']}[job.value];var jobOk=need.every(function(k){return o[k]&&o[k]!=='none'&&o[k]!=='flat'&&o[k]!=='mixed';});
    board(S.querySelector('.board'),[['점검표',score+' / 6',score===6],['요청 상황 맞춤',jobOk?'맞음':'부족',jobOk],['충돌 경고',warn.length+'개',warn.length===0],['나이 표기',o.age?'성인 명시':'없음',!!o.age]]);
    var s=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'점검표 막대'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s);['눈 모양','칠하기','코','입','머리','정보량'].forEach(function(t,i){var k=['eye','paint','nose','mouth','hair','level'][i];var ok=o[k]&&o[k]!=='none'&&o[k]!=='flat'&&o[k]!=='mixed';el('rect',{x:76,y:14+i*30,width:ok?260:40,height:20,rx:4,fill:ok?C.teal:'#e3e8ee'},s);ktxt(s,70,29+i*30,t,{size:12.5,anchor:'end',fill:C.ink});});
    var M=[score===6&&warn.length===0,job.value==='close'&&o.paint==='layer'&&o.nose==='dot'&&o.level==='even',o.age==='adult'&&o.mouth==='wide'&&o.eye&&warn.length===0];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','요청 상황: '+job.options[job.selectedIndex].text+'. '+(jobOk?'필요한 조각이 들어 있다.':'이 상황에 꼭 필요한 조각이 빠졌다.')],['haru','e10','조수','점검표 '+score+' / 6'],['fruitfly','e09','초파리',warn.length?warn[0]:'충돌 없음. 조각끼리 맞아.']]);}
  job.addEventListener('change',function(){touched=true;upd();});
  var cp=S.querySelector('.copy');if(cp)cp.addEventListener('click',function(){var t=S.querySelector('.g1 pre').textContent;if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){cp.textContent='복사했습니다';},function(){cp.textContent='직접 선택해 복사하세요';});});upd();}
var DESK_CA=['동공이 각막 밖','안쪽 눈 너비 그대로','귀가 낮음','어금니가 정면','머리 부피 없음','코만 진함','순백 흰자·한 색 눈동자','눈썹 방향 어긋남'];
var DESK_SYM=['옆에서 본 눈의 동공이 눈 표면보다 앞으로 나와 있다','비스듬히 돌린 얼굴인데 두 눈이 똑같이 크다','옆얼굴의 귀가 턱선 가까이 내려와 있다','비스듬히 본 웃는 입의 안쪽 이가 이쪽을 보고 서 있다','얼굴이 유난히 커 보이고 머리가 작아 보인다','눈·입은 단순한데 코에만 콧구멍과 콧날이 진하다','눈만 하얗게 떠 보이고 눈동자가 납작한 스티커 같다','기쁜 얼굴을 원했는데 화가 난 듯 보인다'];
function desk(){var S=document.getElementById('desk');if(!S)return;var CA=DESK_CA,SYM=DESK_SYM;
  var cur=0,streak=0,seen={},wrong=0,right=0,touched=false;var r=rng(Date.now()%9999+1);
  function next(){cur=Math.floor(r()*8);S.querySelector('.sym').textContent='증상: '+SYM[cur];var o=S.querySelector('.deskopts');o.innerHTML='';
    var opts=[cur];while(opts.length<4){var k=Math.floor(r()*8);if(opts.indexOf(k)<0)opts.push(k);}opts.sort(function(){return r()-.5;});
    opts.forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=CA[k];b.addEventListener('click',function(){touched=true;if(k===cur){streak++;right++;seen[cur]=1;b.classList.add('ok');setTimeout(next,500);}else{streak=0;wrong++;b.classList.add('no');}upd();});o.appendChild(b);});}
  function upd(){var n=Object.keys(seen).length;board(S.querySelector('.board'),[['연속 정답',streak,streak>=3],['맞힌 종류',n+' / 8',n===8],['맞힘',right,right>0],['틀림',wrong,wrong===0]]);
    var M=[streak>=3,n===8,right>=5&&wrong===0];if(touched)missions(S.querySelector('.missions'),M,true);
    var s=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'맞힌 실패 종류'});var g=S.querySelector('.g2');g.innerHTML='';g.appendChild(s);CA.forEach(function(t,i){el('rect',{x:16+(i%4)*86,y:20+Math.floor(i/4)*90,width:78,height:70,rx:8,fill:seen[i]?'#e8f6ec':'#f2f4f7',stroke:seen[i]?C.green:'#d5dbe2'},s);ktxt(s,55+(i%4)*86,60+Math.floor(i/4)*90,'f'+(i+1)+(seen[i]?' ✓':''),{size:14,anchor:'middle',fill:C.ink});});
    say(S.querySelector('.talk'),[['doctor','e10','박사','순서: 자리와 각도 → 구조 → 정보량 → 칠하기 → 표정.'],['haru','e10','조수','연속 '+streak+'개, 맞힌 종류 '+n+' / 8이에요.'],['x2','e09','평가단 X2',wrong?'틀린 건 6부 실패 카드에서 다시 보세요.':'아직 틀린 게 없어요!']]);}
  next();upd();}
/* 프롬프트 복사 버튼 */
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.promptbox .copy');if(!b||b.closest('#workshop'))return;var pre=b.parentNode.querySelector('pre');if(!pre)return;var t=pre.textContent;
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent='복사했습니다';},function(){b.textContent='직접 선택해 복사하세요';});else b.textContent='직접 선택해 복사하세요';});
/* ===================== 퀴즈·지식 색인·꾸러미 ===================== */
function quiz(q){var ans=+q.getAttribute('data-ans');var fb=q.querySelector('.fb');var OK=q.querySelector('.qok'),NO=q.querySelector('.qno');q.querySelectorAll('.opts button').forEach(function(b,i){b.addEventListener('click',function(){q.querySelectorAll('.opts button').forEach(function(x){x.classList.remove('ok','no');});b.classList.add(i===ans?'ok':'no');fb.innerHTML=i===ans?'⭕ '+OK.innerHTML:'❌ '+NO.innerHTML;});});}
function kg(){var raw=document.getElementById('kg-raw');var mount=document.getElementById('kg-mount');if(!raw||!mount)return;var K=JSON.parse(raw.textContent);
  mount.innerHTML='<input class="kg-search" type="search"><div class="kg-list"></div>';var list=mount.querySelector('.kg-list'),inp=mount.querySelector('input');inp.placeholder='개념 찾기 (예: 육각형, 각막, 정보량)';inp.setAttribute('aria-label','지식 색인 검색');
  var TY={Concept:'개념',Method:'방법',Analogy:'비유',Application:'쓰임',OpenQuestion:'열린 질문'};var pre=document.body.getAttribute('data-root')||'';
  function render(){var qv=inp.value.trim().toLowerCase();list.innerHTML=K.nodes.filter(function(n){return !qv||(n.label.ko+' '+n.label.en+' '+n.definition.ko).toLowerCase().indexOf(qv)>=0;}).map(function(n){
    var nb=K.edges.filter(function(e){return e.s===n.id||e.o===n.id;}).map(function(e){var o=e.s===n.id?e.o:e.s;var m=K.nodes.filter(function(x){return x.id===o;})[0];return m?m.label.ko:'';}).filter(Boolean);
    return '<div class="kg-item"><span class="t">'+(TY[n.type]||n.type)+'</span><b>'+n.label.ko+'</b><span class="muted">'+n.label.en+'</span><div>'+n.definition.ko+'</div>'+(nb.length?'<div class="muted" style="font-size:12.5px">이웃: '+nb.join(', ')+'</div>':'')+'<a href="'+pre+n.page+n.anchor+'">설명 보러 가기 →</a></div>';}).join('');}
  inp.addEventListener('input',render);render();var ex=document.getElementById('export-mount');if(!ex)return;
  ex.innerHTML='<div class="exp-btns"><button class="btn" data-x="json">kg.json</button><button class="btn" data-x="ld">JSON-LD</button><button class="btn" data-x="ttl">Turtle (Protégé)</button><button class="btn" data-x="csv">CSV (Neo4j·Gephi)</button><button class="btn" data-x="bib">BibTeX</button><button class="btn" data-x="ris">RIS</button></div>';
  function dl(name,text,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
  var base=K.page;var refs=JSON.parse((document.getElementById('refs-csl')||{textContent:'[]'}).textContent);
  ex.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){var x=b.getAttribute('data-x');
    if(x==='json')dl(base+'.kg.json',JSON.stringify(K,null,2),'application/json');
    if(x==='ld')dl(base+'.jsonld',document.getElementById('kg-ld').textContent,'application/ld+json');
    if(x==='ttl'){var t='@prefix lab: <urn:lab:> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n';K.nodes.forEach(function(n){t+='<urn:'+n.id+'> a lab:'+n.type+' ;\n  skos:prefLabel "'+n.label.ko+'"@ko , "'+n.label.en+'"@en ;\n  rdfs:comment "'+n.definition.ko.replace(/"/g,'\\"')+'"@ko .\n\n';});K.edges.forEach(function(e){t+='<urn:'+e.s+'> lab:'+e.p+' <urn:'+e.o+'> .\n';});dl(base+'.ttl',t,'text/turtle');}
    if(x==='csv'){var c='id,type,label_ko,label_en,anchor\n'+K.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.page+n.anchor].map(function(v){return '"'+String(v).replace(/"/g,'""')+'"';}).join(',');}).join('\n');c+='\n\nsource,relation,target\n'+K.edges.map(function(e){return [e.s,e.p,e.o].join(',');}).join('\n');dl(base+'.csv',c,'text/csv');}
    if(x==='bib')dl(base+'.bib',refs.map(function(r){return '@misc{'+r.id+',\n  title = {'+r.title+'},\n  author = {'+r.author+'},\n  note = {'+(r.note||'')+'},\n  year = {'+r.year+'}\n}';}).join('\n\n'));
    if(x==='ris')dl(base+'.ris',refs.map(function(r){return 'TY  - GEN\nTI  - '+r.title+'\nAU  - '+r.author+'\nPY  - '+r.year+'\nN1  - '+(r.note||'')+'\nER  - ';}).join('\n'));});});}

function boot(){document.querySelectorAll('[data-panel]').forEach(function(h){var k=h.getAttribute('data-panel');if(P[k]){try{P[k](h);}catch(e){h.textContent='실험을 불러오지 못했습니다.';if(window.console)console.warn(k,e);}}});
  document.querySelectorAll('.quiz').forEach(quiz);kg();practice();
  var pr=document.getElementById('prog');if(pr)window.addEventListener('scroll',function(){var d=document.documentElement;pr.style.width=(100*d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
