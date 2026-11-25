# -*- coding: utf-8 -*-
"""구조 먼저 그리기 연구실 04 · 디테일 편 — 페이지 빌드.
python3 build/build.py 로 index.html, 01~06 페이지, practice/index.html 을 다시 만든다.
그림 파일(assets/img/{키}.webp)이 있으면 넣고, 없으면 '그림 준비 중' 자리만 둔다."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2, P3
from content_b import P4, P5, P6
from content_make import MAKE
from make_requests import PROMPTS, CONV_OF, ATTACH_OF
from img_notes import ALT, DRILL_RES, RETRY_RES, RETRY3_RES
from content_drill import DRILL, RETRY, BASE_OF, RETRY3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = "v1.0"
DATE = "2026-11-25"
SITE = "https://adminmrobo.github.io/drawing_lab_04/"
PREV_SITE = "https://adminmrobo.github.io/drawing_lab_03/"
CLOTH_SITE = "https://adminmrobo.github.io/structure_first_drawing_lab_01/"
FIRST_SITE = "https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"
REPO = "https://github.com/adminmrobo/drawing_lab_04"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
RENDER = "https://adminmrobo.github.io/ai_rendering/"
CHARREPO = "https://github.com/adminmrobo/fruitfly-lab-expressions"
SERIES = "구조 먼저 그리기 연구실 04 · 디테일 편"
E = html.escape
PARTS = [P1, P2, P3, P4, P5, P6]

CH = {
 "doctor": ("박사", "해설 + 손님 모델(3부 웃는 입). 짙은 머리의 흰 줄, 굵은 눈썹, 청록 사각 안경"),
 "haru": ("조수 하루", "모델(2부 눈 칠하기·표정) + 수식 상자 담당. 정수리 번 두 개, 앞머리 가운데 남색 줄"),
 "sia": ("시아", "인턴1 · 모델(3부 코·귀). 흑발, 머리 장식 없음, 작은 은색 귀걸이"),
 "moa": ("모아", "인턴2 · 모델(1부 눈). 흰 프릴 머리띠와 왼쪽 귀 위 흰 리본"),
 "jupanbot": ("주판봇", "화가 A. 동그라미·가닥·하얀색부터, 결과부터 서두른다 — 흔한 실수 담당"),
 "fruitfly": ("초파리 연구원", "화가 B. 꼭짓점·덩어리·순서부터 의심한다. \"이걸 눌러 봐\""),
 "x1": ("X1", "평가단. 닮음을 본다"),
 "x2": ("X2", "평가단. 원리를 본다"),
 "x3": ("X3", "평가단. 자연스러움을 본다"),
}
COLOR = {"doctor": "doc", "haru": "asst", "fruitfly": "fly", "jupanbot": "robo", "sia": "sia", "moa": "moa", "x1": "x", "x2": "x", "x3": "x"}

def face(k, e="e13", pre="", cls=""):
    n = CH[k][0]
    return f'<img src="{pre}assets/chars/{k}_{e}.webp" alt="{E(n)}" width="96" height="96" loading="lazy"{(" class=%s" % cls) if cls else ""}>'

def has_img(key):
    return os.path.exists(os.path.join(ROOT, "assets", "img", key + ".webp"))

def art(key, alt, ar="16/9", cap=None, pre="", cls=""):
    if key in ALT:
        if cap == alt:
            cap = ALT[key]
        alt = ALT[key]
    cap_html = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    if has_img(key):
        return f'<figure class="art {cls}" data-img="{key}"><img src="{pre}assets/img/{key}.webp" alt="{E(alt)}" loading="lazy" decoding="async">{cap_html}</figure>'
    return (f'<figure class="art {cls}" data-img="{key}"><div class="ph-art" style="--ar:{ar}" role="img" aria-label="{E(alt)}">'
            f'<b>그림 준비 중 · {key}</b><span>{E(alt)}</span></div>{cap_html}</figure>')

def head(title, desc, og, path, pre=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/og/{og}"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
<meta name="author" content="안상선">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/lab.css">
</head>
<body data-root="{pre}">
<div id="prog"></div>
"""

def nav(links, pre=""):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="{pre}index.html">구조 먼저 그리기 <i>· 디테일 편</i></a><div class="links">{a}</div></div></nav>\n'

def cover(key, cap, cast, pre=""):
    if has_img(key):
        return f'<div class="cover"><div class="frame" data-img="{key}"><img class="art" src="{pre}assets/img/{key}.webp" alt="{E(cap)}" width="1600" height="900" fetchpriority="high" decoding="async"></div></div>\n'
    # 그림이 오기 전 픽셀 대체 표지: 네모 격자 + 상자·원기둥 마네킹(픽셀 블록) + 픽셀 캐릭터
    cells = []
    for x in range(0, 1600, 40):
        for y in range(0, 900, 40):
            if (x // 40 + y // 40) % 2 == 0:
                cells.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="#f3f6fa"/>')
    px = []
    import math as _m
    for gx in range(1040, 1400, 20):
        for gy in range(120, 600, 20):
            dx, dy = gx + 10 - 1220, gy + 10 - 330
            if abs(_m.hypot(dx, dy * 1.0) - 170) < 11 and gy < 400 or (gy >= 400 and abs(abs(dx) - (170 - (gy - 400) * 0.85)) < 11 and gy < 580):
                px.append(f'<rect x="{gx}" y="{gy}" width="20" height="20" fill="#1e2f6e"/>')
    for gy in range(140, 580, 20): px.append(f'<rect x="1210" y="{gy}" width="20" height="20" fill="#e0337f" opacity=".55"/>')
    for gx in range(1060, 1380, 20): px.append(f'<rect x="{gx}" y="330" width="20" height="20" fill="#e0337f" opacity=".55"/>')
    bl = "".join(px)
    easel = '<rect x="240" y="180" width="300" height="380" fill="#ffffff" stroke="#8a5a2b" stroke-width="12"/><rect x="270" y="560" width="20" height="260" fill="#8a5a2b"/><rect x="490" y="560" width="20" height="260" fill="#8a5a2b"/>' + \
            "".join(f'<rect x="{300+i*40}" y="{240+j*40}" width="40" height="40" fill="{c}"/>' for i, j, c in [(1,0,"#d8c09a"),(2,0,"#d8c09a"),(0,1,"#d8c09a"),(1,1,"#f8e3d3"),(2,1,"#f8e3d3"),(3,1,"#d8c09a"),(1,2,"#4a3b5c"),(2,2,"#4a3b5c"),(0,2,"#f8e3d3"),(3,2,"#f8e3d3"),(1,3,"#f8e3d3"),(2,3,"#f8e3d3"),(1,4,"#f8e3d3"),(2,4,"#f8e3d3")])
    imgs = "".join(face(k, e, pre) for k, e in cast)
    return f"""<div class="cover"><div class="frame" data-img="{key}"><svg class="grid" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" shape-rendering="crispEdges">{''.join(cells)}{easel}{bl}</svg>
<span class="cap">{E(cap)}</span><span class="badge">표지 그림 준비 중 · {key}</span><div class="cast" style="image-rendering:pixelated">{imgs}</div></div></div>
"""

def three(a, b, c, abbr):
    dl = "".join(f"<dt>{E(x)}</dt><dd>{E(y)}</dd>" for x, y in abbr)
    return f"""<div class="three"><h2>처음 오신 분께 — 세 줄 요약</h2><ul>
<li><b>무엇을</b>: {E(a)}</li><li><b>왜 알아야 하나</b>: {E(b)}</li><li><b>어디에 쓰나</b>: {E(c)}</li></ul>
<p>그림 실력·코드·수식을 몰라도 됩니다. 실험을 눌러 보며 따라오세요.</p>
<details class="abbr"><summary>낱말·약어 풀이 (펼치기)</summary><dl>{dl}</dl></details></div>\n"""

ABBR = [("육각형 밑그림", "눈을 그리기 전에 눈 자리에 그리는 여섯 꼭짓점 도형. 눈머리·눈꼬리 높이로 인상을 정한다"), ("눈머리·눈꼬리", "눈의 코 쪽 끝과 바깥쪽 끝"),
        ("각막·홍채·동공", "눈 맨 앞의 맑은 막, 그 안쪽 색 있는 원판, 원판 가운데 검은 구멍"), ("빗금(해칭)", "가는 선을 나란히 겹쳐 그어 그늘과 입체를 만드는 방법"),
        ("곱하기 레이어", "밑색에 위 색을 곱해(÷255) 같은 비율로 어둡게 하는 칠하기 층"), ("더하기(발광) 레이어", "밑색에 빛을 더해 밝게 하는 칠하기 층. 불투명도를 낮춰 쓴다"),
        ("정보량", "한 부위에 그려 넣은 선·면의 양. 단순할수록 적고, 실감 날수록 많다"), ("데포르메", "실제 모양을 줄이거나 과장해 단순하게 그리는 것"),
        ("모서리 선", "면이 꺾이는 곳의 선. 코의 콧날·콧방울 같은 선"), ("덩어리(머리 다발 묶음)", "머리카락을 앞·옆·뒤처럼 크게 나눈 묶음"),
        ("가르마·정수리", "머리카락이 갈라지는 선과 머리 꼭대기 소용돌이(가마)"), ("가림 영역(마스크)", "AI가 다시 그릴 부분을 표시한 영역"),
        ("부분 수정(인페인팅)", "가림 영역만 다시 그리고 나머지는 그대로 두는 AI 기능")]

def talk(lines, pre=""):
    out = []
    for k, e, t in lines:
        side = " r" if k in ("moa", "sia") else ""
        out.append(f'<div class="line{side}">{face(k, e, pre)}<div class="bub"><b style="color:var(--c-{COLOR[k]})">{E(CH[k][0])}</b>{E(t)}</div></div>')
    return '<div class="talk">' + "".join(out) + "</div>"

def quiz(q, opts, ans, ok, no):
    b = "".join(f'<button type="button">{E(o)}</button>' for o in opts)
    return f'<div class="quiz" data-ans="{ans}"><div class="qq">확인 퀴즈 — {E(q)}</div><div class="opts">{b}</div><div class="fb" aria-live="polite"></div><span class="qok" hidden>{E(ok)}</span><span class="qno" hidden>{E(no)}</span></div>'

def panel(no, i, p):
    return (f'<div class="panel"><div class="ph"><b>실험 {no}-{i}</b><small>{E(p["note"])}</small></div>'
            f'<div id="pp-{p["key"]}" data-panel="{p["key"]}"></div><div class="ctrl">{p["ctrl"]}</div><div class="readout" aria-live="polite"></div></div>')

def mathbox(m):
    tries = "".join(f"<div>{E(t)}</div>" for t in m["tries"])
    pcs = "".join(f"<tr><td class='m'>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in m["pieces"])
    return f"""<div class="box mathbox"><h4>수식이 어려운 조수가 대신 묻습니다</h4>
<div class="q">{face('haru','e04')}<div><b>조수</b> {E(m['ask'])}</div></div>
<div class="easy"><b>말로 하면</b> — {E(m['words'])}</div>
<div class="try"><b>숫자로 한 번 해 보기</b>{tries}</div>
<p><b>학교 수학으로 보면</b> — {E(m['school'])}</p>
<div class="fx">{E(m['formula'])}</div>
<table><thead><tr><th>식 조각</th><th>뜻</th></tr></thead><tbody>{pcs}</tbody></table>
<div class="q">{face('haru','e16')}<div><b>조수</b> {E(m['comment'])}</div></div></div>"""

def step(P, i, s):
    no = P["no"]
    labels = ["무엇이 문제인가", "그냥 하면 막히는 곳", "이렇게 푼다"]
    why = "".join(f"<li><b>{labels[k]}</b> — {E(x)}</li>" for k, x in enumerate(s["why"]))
    whybox = f'<div class="box why"><h4>왜 이렇게 하나</h4><ol>{why}</ol><div class="easy"><b>쉽게 말하면</b> — {E(s["easy"])}</div></div>'
    calm = talk([("doctor", "e08", "여기서 한 번 멈춰도 괜찮아요. 식이 낯설면 건너뛰고 아래 실험부터 눌러 보세요. 숫자는 실험이 대신 계산해 줍니다.")])
    duo = f'<div class="duo">{whybox}{mathbox(s["math"])}</div>{calm}' if s.get("math") else f'<div style="margin:16px 0">{whybox}</div>'
    solve = "".join(f"<p>{E(x)}</p>" for x in s["solve"])
    extra = ""
    img = art(s["img"][0], s["img"][1], s["img"][2], s["img"][1], cls="tall" if s["img"][2] == "2/3" else "") if s.get("img") else ""
    q = s["quiz"]
    return f"""<section class="room" id="{s['id']}"><div class="wrap">
<div class="roomno">{no}부 · {i}단계</div>
<h2>{E(s['title'])}</h2><p class="muted">{E(s['sub'])}</p>
<div class="tags"><span class="tag how">{E(s['how'])}</span><span class="tag day">{E(s['day'])}</span></div>
{duo}
<div class="pair"><div class="box"><h4>일상으로 치면</h4><p>{E(s['daily'])}</p></div><div class="box ml"><h4>그림·VFX 현장에서는</h4><p>{E(s['field'])}</p></div></div>
{talk(s['talk'])}
{panel(no, i, s['panel'])}
<div class="solve"><h4>풀이</h4>{solve}</div>
{extra}{img}
<div class="solve"><h4>AI 결과, 그대로 써도 될까?</h4><p>{E(s['ai'][0])}</p><details class="code"><summary>답 보기</summary><p>{E(s['ai'][1])}</p></details></div>
<div class="limit"><b>주의할 점</b> — {E(s['limit'])}</div>
{quiz(q[0], q[1], q[2], q[3], q[4])}
</div></section>
"""

def judge(J):
    rows = ""
    for idx, item in enumerate(J["items"]):
        a, b = J["a"][1][idx], J["b"][1][idx]
        mx = 8 if "8개" in item else 10
        rows += f'<span>{E(item)}</span><span class="bar" title="{J["a"][0]} {a}"><i style="width:{a/mx*100:.0f}%"></i></span><span class="bar" title="{J["b"][0]} {b}"><i style="width:{b/mx*100:.0f}%;background:var(--teal)"></i></span>'
    sa, sb = sum(J["a"][1]), sum(J["b"][1])
    tbl = "".join(f"<tr><td>{E(it)}</td><td>{J['a'][1][k]}</td><td>{J['b'][1][k]}</td></tr>" for k, it in enumerate(J["items"]))
    return f"""<section class="room" id="judge"><div class="wrap"><div class="roomno">평가단 채점</div><h2>{E(J['title'])}</h2>
{talk(J['setup'])}
<div class="judge"><h4>평가단 X1·X2·X3 채점</h4>
<div class="score"><span></span><b>{E(J['a'][0])}</b><b>{E(J['b'][0])}</b>{rows}</div>
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>항목</th><th>{E(J['a'][0])}</th><th>{E(J['b'][0])}</th></tr></thead><tbody>{tbl}<tr><th>합계</th><th>{sa}</th><th>{sb}</th></tr></tbody></table></div>
{talk(J['comments'])}</div>
{talk(J['result'])}
<p class="hint">점수는 이야기 속 예시입니다. 실제 그림을 평가한 값이 아닙니다.</p>
</div></section>
"""

def summary(P):
    rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in P["summary"])
    return f"""<section id="sum"><div class="wrap"><h2>{P['no']}부 정리</h2>
<div class="tbl"><table><thead><tr><th>주제</th><th>한 줄</th><th>작업에서는</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
"""

def outro(P):
    return f"""<section id="outro"><div class="wrap"><h2>다음으로</h2>{talk(P['outro'])}
<div class="next"><a href="{P['prev'][0]}">{E(P['prev'][1])}</a><a href="{P['next'][0]}">{E(P['next'][1])}</a></div></div></section>
"""

def failcard(f):
    note = f'<p class="hint">{E(f["note"])}</p>' if f.get("note") else ""
    return f"""<div class="failcard" id="{f['key'].split('_')[0]}"><h3>{E(f['title'])}</h3><div class="failgrid">
{art(f['key'], f['alt'], f['ar'])}
<div><p><span class="chip">증상</span>{E(f['symptom'])}</p>
{quiz(f['q'], f['opts'], f['ans'], f['ok'], f['no'])}
<p><span class="chip">연결된 원리</span><a href="{f['link'][0]}">{E(f['link'][1])}</a></p>
<div class="promptbox"><b>고치는 프롬프트 조각</b><pre>{E(f['fix'])}</pre></div>{note}</div></div></div>"""

# ---------------- 지식 색인
KG = [
 ("method/eye-hexagon", "Method", "육각형 밑그림", "Hexagon eye construction", "01_eye_shape.html", "#s1", "눈의 기울기 = (눈꼬리 높이 − 눈머리 높이) ÷ 눈 너비, 0~8°면 기본 눈"),
 ("concept/cornea-order", "Concept", "각막·홍채·동공의 앞뒤", "Cornea, iris and pupil depth order", "01_eye_shape.html", "#s2", "바깥부터 각막 → 홍채 → 동공, 동공은 각막 안쪽"),
 ("concept/eye-sphere", "Concept", "공 위의 눈", "Eyes on a sphere", "01_eye_shape.html", "#s3", "안쪽 눈 ÷ 앞쪽 눈 = cos(고개+25°) ÷ cos(고개−25°)"),
 ("method/hatching-density", "Method", "부위별 빗금 밀도", "Hatching density by part", "01_eye_shape.html", "#s4", "속눈썹은 빽빽하게, 홍채는 0.7배 이하로 성기게"),
 ("concept/off-white-sclera", "Concept", "흰자는 순백이 아니다", "Off-white sclera", "02_eye_paint.html", "#s1", "흰자 밝기는 피부보다 조금 높고 순백보다 낮게"),
 ("method/blend-layers", "Method", "곱하기·더하기 레이어", "Multiply and add blend layers", "02_eye_paint.html", "#s2", "곱하기 = 밑색 × 위 색 ÷ 255, 더하기 = 밑색 + 색 × 불투명도"),
 ("concept/brow-and-eye-emotion", "Concept", "눈썹은 종류, 눈은 세기", "Eyebrow angle and eye openness", "02_eye_paint.html", "#s3", "눈썹 끝 올라감 = 화, 내려감 = 슬픔, 눈 뜬 정도 = 세기(슬픔은 반대)"),
 ("concept/mouth-expression", "Concept", "입은 감정을 밖으로 내는 정도", "Mouth as expression intensity", "02_eye_paint.html", "#s4", "같은 눈에 다문 입은 삼킴, 크게 벌린 입은 터뜨림"),
 ("method/nose-detail", "Method", "코 정보량 맞추기", "Matching nose detail", "03_nose_ear_mouth.html", "#s1", "모서리 선 중 몇 개를 고르는지 = 정보량, 눈과 1 이내로"),
 ("concept/ear-placement", "Concept", "귀 자리와 각도별 너비", "Ear placement and apparent width", "03_nose_ear_mouth.html", "#s2", "귀는 눈~코끝 사이, 너비 = 10 × |sin 각도| + 두께"),
 ("concept/open-mouth-teeth", "Concept", "위 이 一, 아래 이 U", "Teeth in an open mouth", "03_nose_ear_mouth.html", "#s3", "아래 이줄이 보이는 깊이 = 이줄 깊이 × sin(벌린 각도)"),
 ("method/hidden-molars", "Method", "보이지 않는 어금니 이어 그리기", "Drawing hidden molar rows", "03_nose_ear_mouth.html", "#s4", "위·아래 어금니 줄은 안쪽 한 점으로 모인다"),
 ("concept/hair-volume", "Concept", "머리카락 부피", "Hair volume", "04_hair.html", "#s1", "바깥선 = 머리 밑그림 × 1.05~1.15, 넓이는 k²배"),
 ("method/hair-blocks", "Method", "머리 덩어리 나누기", "Hair clump blocking", "04_hair.html", "#s2", "앞·옆·뒤로 나누고 덩어리 수 ≈ 얼굴 정보량 + 1"),
 ("concept/hair-growth", "Concept", "머리가 나는 자리와 흐름", "Hair growth and flow", "04_hair.html", "#s3", "두피 전체에서 나고 가르마·정수리에서 흐름. 단순한 그림만 한 점 허용"),
 ("method/strand-variety", "Method", "다발 굵기 섞기", "Varying strand thickness", "04_hair.html", "#s4", "굵기 차이 30~80%, 가는 한 가닥 몇 개"),
 ("method/detail-prompt", "Method", "디테일 문장", "Per-part detail prompt", "05_ai_detail.html", "#s1", "부위별 정보량을 적고 차이를 1 이내로, consistent level of detail"),
 ("method/paint-prompt", "Method", "칠하기 문장", "Eye painting prompt", "05_ai_detail.html", "#s2", "흰자 색·위 그림자·아래 빛·하이라이트 둘·갈색 선 다섯 조각"),
 ("method/part-inpaint", "Method", "부위만 가림 영역", "Inpainting one facial part", "05_ai_detail.html", "#s3", "다시 그려지는 몫 = 가린 넓이 ÷ 전체 × 100, 여유 10~20%"),
 ("method/keep-structure", "Method", "화풍이 바뀌어도 남길 구조", "Keeping structure across styles", "05_ai_detail.html", "#s4", "구조(육각형·동공 자리·이줄·머리 실루엣)는 남기고 정보량만 바꾼다"),
 ("method/detail-diagnosis", "Method", "디테일 진단 순서", "Detail diagnosis order", "06_failure_lab.html", "#s1", "자리와 각도 → 구조 → 정보량 → 칠하기 → 표정"),
 ("application/detail-failures", "Application", "디테일 실패 8종", "Eight detail failures", "06_failure_lab.html", "#fails", "튀어나온 동공·같은 너비의 두 눈·낮은 귀·정면 어금니·납작한 머리·혼자 진한 코·스티커 눈·어긋난 눈썹"),
 ("open/age-drift", "OpenQuestion", "표정·디테일 요청의 나이 쏠림", "Apparent age drift in expression prompts", "06_failure_lab.html", "#drift", "큰 눈·큰 웃음·홍조가 겹치면 어려 보인다. 성인 나이와 비율을 적어 막는다"),
 ("application/practice", "Application", "실전 연습장", "Practice simulator", "practice/index.html", "#bench", "눈 작업대·표정 조합판·디테일 문장 공방·진단 데스크"),
 ("analogy/umbrella", "Analogy", "우산 살대 끝", "Umbrella rib tips", "01_eye_shape.html", "#s1", "끝점 두 개만 기울여도 전체 모양이 따라온다"),
 ("analogy/watch-glass", "Analogy", "손목시계 유리", "Watch crystal", "01_eye_shape.html", "#s2", "바늘은 유리 밖으로 나오지 않는다"),
 ("analogy/sunglasses-flashlight", "Analogy", "선글라스와 손전등", "Sunglasses and a flashlight", "02_eye_paint.html", "#s2", "곱하기는 같은 비율로 어둡게, 더하기는 비춘 곳에 빛을"),
 ("analogy/map-scale", "Analogy", "지도 축척", "Map scale", "03_nose_ear_mouth.html", "#s1", "한 장 안에서는 축척(정보량)이 같아야 읽힌다"),
 ("analogy/railway", "Analogy", "기찻길", "Railway tracks", "03_nose_ear_mouth.html", "#s4", "멀어질수록 두 줄이 한 점으로 모인다"),
 ("analogy/melody", "Analogy", "같은 노래 다른 편곡", "Same melody, different arrangement", "05_ai_detail.html", "#s4", "구조가 멜로디, 화풍은 편곡"),
]
KG_EDGES = [("method/eye-hexagon","motivates","concept/cornea-order"),("concept/cornea-order","motivates","concept/eye-sphere"),("concept/eye-sphere","motivates","method/hatching-density"),
 ("method/hatching-density","motivates","concept/off-white-sclera"),("concept/off-white-sclera","motivates","method/blend-layers"),("method/blend-layers","motivates","concept/brow-and-eye-emotion"),("concept/brow-and-eye-emotion","motivates","concept/mouth-expression"),
 ("concept/mouth-expression","motivates","method/nose-detail"),("method/nose-detail","motivates","concept/ear-placement"),("concept/ear-placement","motivates","concept/open-mouth-teeth"),("concept/open-mouth-teeth","motivates","method/hidden-molars"),
 ("method/hidden-molars","motivates","concept/hair-volume"),("concept/hair-volume","motivates","method/hair-blocks"),("method/hair-blocks","motivates","concept/hair-growth"),("concept/hair-growth","motivates","method/strand-variety"),
 ("method/strand-variety","motivates","method/detail-prompt"),("method/detail-prompt","motivates","method/paint-prompt"),("method/paint-prompt","motivates","method/part-inpaint"),("method/part-inpaint","motivates","method/keep-structure"),
 ("method/keep-structure","motivates","method/detail-diagnosis"),("method/detail-diagnosis","usedIn","application/detail-failures"),("method/detail-prompt","explains","open/age-drift"),("concept/brow-and-eye-emotion","explains","open/age-drift"),
 ("method/nose-detail","explains","method/detail-prompt"),("method/hair-blocks","explains","method/detail-prompt"),("method/blend-layers","explains","method/paint-prompt"),("method/eye-hexagon","explains","method/keep-structure"),
 ("concept/eye-sphere","explains","application/detail-failures"),("analogy/umbrella","explains","method/eye-hexagon"),("analogy/watch-glass","explains","concept/cornea-order"),("analogy/sunglasses-flashlight","explains","method/blend-layers"),
 ("analogy/map-scale","explains","method/nose-detail"),("analogy/railway","explains","method/hidden-molars"),("analogy/melody","explains","method/keep-structure"),
 ("method/detail-prompt","usedIn","application/practice"),("method/eye-hexagon","usedIn","application/practice")]
REFS = [
 dict(id="kawaiisensei_2023_parts", title="いいトコどり! 人物パーツの描き方", author="KawaiiSensei", year=2023, note="マイナビ出版, ISBN 978-4-8399-8077-1. 1장 「顔を描こう」(p.12~46: 얼굴 각도·남녀·눈·눈 칠하기·코·귀·입과 이·머리카락)의 원리를 참고. 책의 그림·문장·도식·색 값·구성 순서는 옮기지 않고 연구실 캐릭터와 실험으로 새로 구성"),
 dict(id="porter_duff_1984", title="Compositing Digital Images", author="Thomas Porter, Tom Duff", year=1984, note="SIGGRAPH 1984 — 그림 층을 겹쳐 합치는 계산의 기초(곱하기·더하기 레이어 설명의 배경)"),
 dict(id="w3c_2015_blending", title="Compositing and Blending Level 1", author="W3C (R. Cabanier, N. Andronikos)", year=2015, note="W3C 후보 권고안 — multiply(곱하기) 등 혼합 모드의 식. 이 페이지의 더하기 식은 이보다 단순한 예시"),
 dict(id="lugmayr_2022_repaint", title="RePaint: Inpainting using Denoising Diffusion Probabilistic Models", author="Andreas Lugmayr et al.", year=2022, note="CVPR 2022. arXiv:2201.09865 — 가림 영역만 다시 그리는 방식"),
 dict(id="rombach_2022_ldm", title="High-Resolution Image Synthesis with Latent Diffusion Models", author="Robin Rombach et al.", year=2022, note="CVPR 2022. arXiv:2112.10752 — 글 지시로 그림을 만드는 확산 모델(부분 수정 포함)"),
 dict(id="prev_03", title="구조 먼저 그리기 연구실 03 · 얼굴 편", author="안상선", year=2026, note="앞 편. 얼굴 비율·남녀 차이·옆얼굴과 AI 얼굴 문장. https://adminmrobo.github.io/drawing_lab_03/"),
 dict(id="prev_01", title="구조 먼저 그리기 연구실 01 · 옷장 편", author="안상선", year=2026, note="옷 주름·그림자와 AI·VFX. https://adminmrobo.github.io/structure_first_drawing_lab_01/"),
 dict(id="prev_series", title="구조 먼저 보는 캐릭터 그리기 연구실", author="안상선", year=2026, note="첫 시리즈. 구조·빛·주름 기초와 확산 모델·프롬프트 기초. https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"),
]

def kg_block(page, pages):
    nodes = [dict(id="lab:" + i, type=t, label=dict(ko=ko, en=en), page=p, anchor=a, definition=dict(ko=d), source="lab:work/structure_first_drawing_04")
             for i, t, ko, en, p, a, d in KG if p in pages]
    ids = {n["id"] for n in nodes}
    edges = [dict(s="lab:" + s, p=p, o="lab:" + o) for s, p, o in KG_EDGES if "lab:" + s in ids and "lab:" + o in ids]
    raw = dict(version="1.3", page=page, series=SERIES, nodes=nodes, edges=edges)
    ld = {"@context": {"@vocab": "urn:lab:", "skos": "http://www.w3.org/2004/02/skos/core#", "schema": "https://schema.org/"},
          "@graph": [{"@id": "urn:" + n["id"], "@type": n["type"], "skos:prefLabel": [{"@value": n["label"]["ko"], "@language": "ko"}, {"@value": n["label"]["en"], "@language": "en"}],
                      "skos:definition": n["definition"]["ko"], "schema:url": SITE + n["page"] + n["anchor"]} for n in nodes]}
    meta = dict(title=page, series=SERIES, creator=[dict(name="안상선", role="author", affiliation="(주)M-Robo")], date=DATE, version=VER, license="캐릭터·그림 무단 사용 금지")
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section id="kg"><div class="wrap"><h2>지식 색인 — 이 페이지의 낱말 찾기</h2>
<p class="muted">이 페이지에 나온 개념·방법·비유·쓰임을 모았습니다. 검색하고, "설명 보러 가기"로 본문에 돌아갑니다.</p><div id="kg-mount"></div></div></section>
<section id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미 내려받기</h2>
<p class="muted">지식 색인을 출처와 함께 파일로 내려받습니다. 서지 관리는 BibTeX·RIS, 온톨로지 편집은 Turtle, 그래프 도구는 CSV, 여러 페이지 합치기는 kg.json입니다.</p><div id="export-mount"></div></div></section>
<script type="application/json" id="kg-raw">{J(raw)}</script>
<script type="application/ld+json" id="kg-ld">{J(ld)}</script>
<script type="application/json" id="refs-csl">{J(REFS)}</script>
<script type="application/json" id="page-meta">{J(meta)}</script>
"""

FOOT_LINKS = [("index.html", "목차")] + [(P["file"], f"{P['no']}부") for P in PARTS] + [("practice/index.html", "7부 실전 연습장")]

def footer(pre=""):
    links = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in FOOT_LINKS) + f' · <a href="{REPO}">저장소</a>'
    refs = "".join(f"<tr><td>[{i+1}]</td><td>{E(r['author'])} ({r['year']}). {E(r['title'])}</td><td>{E(r['note'])}</td></tr>" for i, r in enumerate(REFS))
    return f"""<footer><div class="wrap">
<h3>출처·참고</h3>
<div class="tbl"><table><thead><tr><th>#</th><th>자료</th><th>어디에 썼나</th></tr></thead><tbody>{refs}</tbody></table></div>
<h3>예시값·설명용 숫자</h3>
<p>눈 기울기 경계(8°), 눈의 자리(±25°), 빗금 밀도 비율(0.7), 흰자·눈동자 RGB 값, 곱하기·더하기 값과 불투명도 범위, 눈썹 각도와 눈 뜬 정도의 경계, 정보량 1~5 단계, 귀 높이와 너비, 이줄 깊이, 머리 부피 배수, 덩어리 수 규칙, 다발 굵기 범위, 가림 영역 크기, 평가단 점수는 모두 원리를 보이기 위한 예시값입니다. 실제 사람과 화풍마다 다릅니다. 책에 실린 색 값은 옮기지 않았고, 이 페이지의 색 값은 새로 정한 예시입니다.</p>
<p>등장인물은 모두 성인 연구원입니다(하루·시아·모아는 20대, 박사는 30대 성인 남성). 실사풍 그림은 캐릭터를 코스프레한 가상의 성인 모델이며 실존 인물이 아닙니다. 다른 작품의 캐릭터를 닮은 그림은 만들지 않습니다.</p>
<p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: <a href="{CHARREPO}">fruitfly-lab-expressions</a>.</p>
<p>글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p>
<p>{links}</p>
</div></footer>
<script src="{pre}assets/panels.js"></script>
</body></html>
"""

REFS_DL = ["haru_anime_base.png", "sia_anime_base.png", "moa_anime_base.png", "haru_sheet.png", "sia_sheet.png", "moa_sheet.png", "doctor_sheet.png", "fruitfly_sprites_6.png", "jupanbot_ref_genspark_v0.png", "pixel_style_ref_prev_cover.png"]
def make_section(P):
    tasks = MAKE.get(P["no"])
    if not tasks:
        return ""
    refs = " · ".join(f'<a href="assets/refs/{f}" download>{f.replace(".png", "")}</a>' for f in REFS_DL)
    out = f"""<section class="room" id="make"><div class="wrap"><div class="roomno">{P['no']}부 · 직접 만들기</div><h2>프롬프트로 직접 만들어 보기</h2>
<div class="box"><p>이 부에서 배운 원리를 그림 생성 AI(Genspark 등)로 직접 확인합니다. <b>A</b>는 이 페이지 그림을 실제로 만든 프롬프트, <b>B</b>는 원리를 하나 빼거나 바꾼 비교용 문장입니다.</p>
<ol style="margin:6px 0 0;padding-left:20px"><li>새 대화를 열고 아래 '첨부'에 적힌 참고 그림을 올립니다.</li><li>A를 붙여 넣어 만들고, 확인표로 결과를 점검합니다.</li><li>같은 대화에 B를 이어 붙여 다시 만들고, A 결과와 나란히 비교합니다. 구도가 흔들리면 'keep the same framing'을 덧붙입니다.</li><li>같은 대화에서 차이가 약하면 새 대화에서 처음부터 만들어 보세요. 결과는 매번 다릅니다.</li></ol>
<p class="hint" style="margin-top:8px">참고 그림 내려받기: {refs}</p></div>"""
    for i, t in enumerate(tasks, 1):
        A = PROMPTS[t["key"]][4]
        att = ATTACH_OF[CONV_OF[t["key"]]]
        ar = "16/9" if "16:9" in A.split("\n")[0] else "2/3"
        alt = PROMPTS[t["img"]][3]
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in t["check"])
        k = t["b_imgs"][0]
        bbox = f'<div class="promptbox"><b>{E(t["b_title"])}</b><pre>{E(t["b_text"])}</pre><button type="button" class="btn copy">복사하기</button></div>'
        bpart = f'<div class="pair">{bbox}<div>{art(k, "비교 결과 — " + t["b_title"], ar, "B 결과")}</div></div>'
        res = f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t["res"])}</p>' if t.get("res") else ""
        tip = f'<p class="hint">{E(t["tip"])}</p>' if t.get("tip") else ""
        out += f"""<div class="failcard" id="make{i}"><h3>실습 {i} · {E(t['title'])}</h3><p>{E(t['goal'])}</p>
<div class="pair"><div class="promptbox"><b>A — 이 페이지 그림을 실제로 만든 프롬프트</b><p class="hint">첨부: {E(att)}</p><pre>{E(A)}</pre><button type="button" class="btn copy">복사하기</button></div>
<div>{art(t['img'], alt, ar, "A 결과 — Genspark로 만든 그림")}</div></div>
{bpart}<h4>결과에서 확인할 것</h4><ol>{chk}</ol>{res}{tip}</div>"""
    return out + "</div></section>"

def res_html(no, did):
    t = DRILL_RES.get(f"{no}-{did}")
    if t and f"{no}-{did}" in RETRY:
        t = t.replace("실제 결과:", "1차 시도 결과:", 1)
    return f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t)}</p>' if t else ""

def retry_html(no, did, shown):
    r = RETRY.get(f"{no}-{did}")
    if not r:
        return ""
    out = f'<div class="box" style="border-left:4px solid var(--blue);margin-top:14px"><h4 style="margin-top:0">다시 시도 — 1차 결과는 위에 그대로 두고, 방법을 바꿔 다시 받습니다</h4><p>{E(r["why"])}</p>'
    for lab, how, pr, key, alt, ar, ok in r["items"]:
        pic = "" if key in shown else f"<div>{art(key, alt, ar, alt)}</div>"
        out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div>{pic}</div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
    rr = RETRY_RES.get(f"{no}-{did}")
    if rr:
        col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[rr[0]]
        out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">다시 시도 결과 · {rr[0]}</b> — {E(rr[1])}</p>'
    r3 = RETRY3.get(f"{no}-{did}")
    if r3:
        out += f'<h4>3차 시도 — 새 대화에서 크게 과장해 다시 받습니다</h4><p>{E(r3["why"])}</p>'
        for lab, how, pr, key, alt, ar, ok in r3["items"]:
            out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
        r3r = RETRY3_RES.get(f"{no}-{did}")
        if r3r:
            col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[r3r[0]]
            out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">3차 시도 결과 · {r3r[0]}</b> — {E(r3r[1])}</p>'
    return out + "</div>"

def drill_section(P):
    ds = DRILL.get(P["no"])
    if not ds:
        return ""
    keys = [p[2] for d in ds for p in d["prompts"]]
    made = "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다. 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다." if all(has_img(k) for k in keys) else "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다(아직 받지 않은 그림은 '그림 준비 중'). 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다."
    out = f"""<section class="room" id="drill"><div class="wrap"><div class="roomno">{P['no']}부 · 연습 과제</div><h2>프롬프트 연습 과제</h2>
<div class="box"><p>이 부의 원리를 내 손으로 프롬프트에 옮겨 보는 과제 두 개입니다. 과제마다 <b>목표 → 순서 → 넣을 프롬프트 → 확인할 것 → 예상 결과 → 자주 생기는 문제</b> 순서로 적었습니다. {made} 결과는 매번 조금씩 다르니, 그림이 똑같지 않아도 '확인할 것'이 맞으면 성공입니다.</p></div>"""
    for i, d in enumerate(ds, 1):
        steps = "".join(f"<li>{E(x)}</li>" for x in d["steps"])
        prs = ""
        for lab, pr, key, alt, ar in d["prompts"]:
            prs += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>"""
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in d["check"])
        tr = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in d["trouble"])
        out += f"""<div class="failcard" id="{d['id']}"><h3>연습 {i} · {E(d['title'])}</h3>
<p><span class="chip">목표</span>{E(d['goal'])}</p><p><span class="chip">왜 이 연습인가</span>{E(d['why'])}</p>
<p class="hint">첨부할 참고 그림: {E(d['attach'])} — 참고 그림은 위 <a href="#make">직접 만들어 보기</a>에서 내려받을 수 있습니다.</p>
<h4>순서</h4><ol>{steps}</ol>
<h4>넣을 프롬프트와 예상 결과</h4>{prs}
<h4>확인할 것</h4><ol>{chk}</ol>
<div class="easy"><b>예상 결과</b> — {E(d['expect'])}</div>{res_html(P['no'], d['id'])}{retry_html(P['no'], d['id'], [p[2] for p in d['prompts']])}
<h4>자주 생기는 문제와 대처</h4><div class="tbl"><table><thead><tr><th>문제</th><th>이렇게 고칩니다</th></tr></thead><tbody>{tr}</tbody></table></div>
<p><span class="chip">더 해 보기</span>{E(d['more'])}</p></div>"""
    return out + "</div></section>"

def build_part(P):
    t = f"{SERIES} {P['no']}부 — {P['title']}"
    s = head(t, P["desc"], P["og"], P["file"])
    navl = [(f"#{x['id']}", f"{k+1}단계") for k, x in enumerate(P["steps"])]
    if P.get("fails"): navl += [("#fails", "실패 8종")]
    navl += [("#make", "직접 만들기"), ("#drill", "연습 과제"), ("#judge", "평가"), ("#sum", "정리"), (P["next"][0], "다음 →")]
    s += nav(navl)
    s += cover(P["cover_key"], P["cover_cap"], P["cover_cast"])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">{E(P['kicker'])}</span><h1>{E(P['title'])}</h1><p class="lead">{E(P['lead'])}</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three(*P['three'], ABBR)}</div></section>
<section><div class="wrap"><h2>오늘의 과제</h2>{talk(P['intro'])}{flow_strip(P['no'])}</div></section>
"""
    for k, st in enumerate(P["steps"]):
        s += step(P, k + 1, st)
    if P.get("fails"):
        s += '<section class="room" id="fails"><div class="wrap"><div class="roomno">6부 · 2단계</div><h2>디테일 그림 실패 8종 진단</h2><p class="muted">그림마다 증상을 보고 처음 걸리는 점검 항목을 고른 뒤, 연결된 원리와 고치는 프롬프트 조각을 확인합니다.</p>'
        s += "".join(failcard(f) for f in P["fails"])
        d = P["drift"]
        s += f'<div class="failcard" id="drift"><h3>{E(d["title"])}</h3>' + "".join(f"<p>{E(x)}</p>" for x in d["body"]) + '<p><span class="chip">연결된 원리</span><a href="05_ai_detail.html#s1">5부 1단계 디테일 문장</a> · <a href="02_eye_paint.html#s3">2부 3단계 눈썹과 눈</a></p></div></div></section>'
    s += make_section(P)
    s += drill_section(P)
    s += judge(P["judge"]) + summary(P) + outro(P)
    s += kg_block(P["file"].replace(".html", ""), [P["file"]])
    s += footer()
    open(os.path.join(ROOT, P["file"]), "w").write(s)

FLOW = [
 (1, "눈의 모양", "동그라미로 그린 눈은 각도를 바꾸면 무너진다", "육각형·각막·공·선 밀도"),
 (2, "눈 칠하기와 표정", "선이 맞아도 칠하기와 눈썹이 틀리면 스티커 눈·엇갈린 표정이 된다", "흰자·곱하기·더하기·눈썹·입"),
 (3, "코·귀·입", "눈만 자세하면 다른 부위가 튀거나 방향이 흔들린다", "정보량·귀 자리·이줄·어금니"),
 (4, "머리카락", "얼굴 부위가 맞아도 머리가 납작하거나 가발 같으면 얼굴 크기가 흔들린다", "부피·덩어리·나는 자리·굵기"),
 (5, "AI로 디테일 살리기", "AI는 '디테일하게'를 부위별로 나누지 않는다", "디테일 문장·칠하기 문장·가림 영역·화풍"),
 (6, "실패 사례 실험실", "문장을 써도 디테일은 틀릴 수 있다", "진단 순서와 고치는 조각, 나이 쏠림"),
 (7, "실전 연습장", "배운 것을 한 화면에서 함께 다뤄 본다", "눈 작업대·표정 조합판·문장 공방·진단"),
]
def flow_strip(cur=None, pre=""):
    files = {P["no"]: P["file"] for P in PARTS}
    files[7] = "practice/index.html"
    cells = []
    for n, t, _, _ in FLOW:
        mark = ' style="border-color:var(--orange);background:var(--orange-soft)"' if n == cur else ""
        cells.append(f'<a href="{pre}{files[n]}"{mark}><b>{n}부</b>{E(t)}</a>')
    return '<div class="flowgrid" style="grid-template-columns:repeat(auto-fit,minmax(130px,1fr));margin-top:16px">' + "".join(cells) + "</div>"

def build_index():
    t = f"{SERIES} — 육각형 하나, 덩어리 몇 개"
    d = "눈을 육각형에서, 머리카락을 덩어리에서 시작해 눈·눈 칠하기·표정·코·귀·입·머리카락의 디테일을 실험으로 익히고, 부위마다 정보량을 맞춘 AI 디테일 문장과 부분 수정으로 옮깁니다. 디테일 실패 8종 진단까지."
    s = head(t, d, "og_index.jpg", "index.html")
    s += nav([("#howto", "읽는 법"), ("#parts", "편 목록"), ("#map", "전체 흐름"), ("#cast", "등장인물"), ("#source", "원리와 출처")])
    s += cover("cover_index", "연구실 작업실 · 큰 돋보기 앞에 모인 모델 넷, 화가 둘, 평가단 셋", [("fruitfly", "e09"), ("haru", "e01"), ("sia", "e13"), ("moa", "e19"), ("doctor", "e16"), ("jupanbot", "e16")])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">연구실 특별편 · 그리기와 렌더링 · 네 번째 편</span>
<h1>구조 먼저 그리기 연구실 04<br>디테일 편 — 육각형 하나, 덩어리 몇 개</h1>
<p class="lead">얼굴 편에서 원과 기준선으로 얼굴의 자리를 잡았다면, 이번에는 그 자리에 얹는 <b>디테일</b>입니다. 눈은 <b>육각형 하나</b>에서, 머리카락은 <b>덩어리 몇 개</b>에서 시작합니다. 디테일은 '많이'가 아니라 <b>'고르게'</b> 그리는 것이라는 점을 실험으로 확인하고, 마지막에는 그 원리를 <b>AI에게 부위별 문장과 가림 영역으로 알려 주는 법</b>까지 갑니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three("눈(육각형·각막·공·선 밀도), 눈 칠하기(흰자 색·곱하기·더하기), 표정(눈썹·눈 뜬 정도·입), 코·귀·입(정보량·귀 자리·이줄), 머리카락(부피·덩어리·나는 자리·굵기)을 실험으로 익히고, AI 디테일 문장과 부분 수정으로 옮깁니다.", "디테일은 얼굴에서 가장 먼저 눈에 띄지만, 한 부위만 자세하거나 구조가 틀리면 아무리 그려 넣어도 어색합니다. AI에게 '디테일하게'라고만 하면 이런 실패가 자주 나옵니다.", "캐릭터 눈·표정 설정, 표정 시트, 헤어스타일 설정, AI 그림의 디테일 검수와 부분 수정에 씁니다.", ABBR)}</div></section>
<section id="howto"><div class="wrap"><h2>읽는 순서와 시간</h2><div class="box"><ul style="margin:0;padding-left:20px">
<li><b>처음부터 차례로</b>(권장): 부마다 실험을 눌러 보며 20~30분, 전체 3시간 안팎입니다.</li>
<li><b>앞 편을 안 봤다면</b>: 바로 읽어도 됩니다. 낱말은 다시 설명합니다. 얼굴의 자리(원·기준선)는 <a href="{PREV_SITE}">03 얼굴 편</a>, 옷 주름은 <a href="{CLOTH_SITE}">01 옷장 편</a>, 빛·그림자 기초는 <a href="{FIRST_SITE}">구조 먼저 보는 캐릭터 그리기 연구실</a>에 있습니다.</li>
<li><b>손 그림 원리만</b>: 1~4부. <b>AI가 급하다면</b>: 5부 → 6부 → 7부, 막히는 낱말은 각 단계의 링크로 되짚어 보세요.</li>
<li>각 부 끝의 <b>평가단 채점</b>은 이야기 속 예시 점수입니다. 확인 퀴즈와 실전 연습장 미션으로 스스로 점검하세요.</li></ul></div></div></section>
<section id="parts"><div class="wrap"><h2>편 목록</h2>
<p class="muted">모델은 모아(1부)·하루(2부)·시아와 박사(3부)·하루·시아·모아(4부)·모두(5부), 화가는 주판봇과 초파리, 평가단은 X1·X2·X3, 해설은 박사입니다. 부마다 두 화가가 겨루고 평가단이 점수를 매깁니다.</p>
<div class="cards">
<a class="card" href="01_eye_shape.html">{face("moa","e01")}<span class="n">1부 · 모델 모아</span><h3>눈의 모양</h3><p>육각형 밑그림, 각막·홍채·동공, 공 위의 눈, 선 밀도.</p></a>
<a class="card" href="02_eye_paint.html">{face("haru","e19")}<span class="n">2부 · 모델 하루</span><h3>눈 칠하기와 표정</h3><p>흰자 색, 곱하기·더하기 레이어, 눈썹과 눈 뜬 정도, 같은 눈 다른 입.</p></a>
<a class="card" href="03_nose_ear_mouth.html">{face("sia","e13")}<span class="n">3부 · 모델 시아 · 손님 박사</span><h3>코·귀·입</h3><p>코 정보량, 귀 자리와 각도별 너비, 위 이 一·아래 이 U, 보이지 않는 어금니.</p></a>
<a class="card" href="04_hair.html">{face("haru","e01")}<span class="n">4부 · 모델 하루·시아·모아</span><h3>머리카락</h3><p>부피, 덩어리 나누기, 나는 자리와 흐름, 다발 굵기 섞기.</p></a>
<a class="card" href="05_ai_detail.html">{face("moa","e19")}<span class="n">5부 · 모델 모두</span><h3>AI로 디테일 살리기</h3><p>디테일 문장, 칠하기 문장, 부위만 가림 영역, 화풍별 남길 구조.</p></a>
<a class="card" href="06_failure_lab.html">{face("jupanbot","e20")}<span class="n">6부 · 의도적 실패 8종</span><h3>실패 사례 실험실</h3><p>증상 → 처음 걸린 곳 → 원리 → 고치는 조각. 나이 쏠림 막기.</p></a>
<a class="card" href="practice/index.html">{face("x2","e16")}<span class="n">7부 · 마지막 장</span><h3>실전 연습장</h3><p>눈 작업대·표정 조합판·디테일 문장 공방·진단 데스크.</p></a>
</div></div></section>
<section id="map"><div class="wrap"><h2>전체 흐름 — 1부부터 7부까지 이어지는 순서</h2>{flow_strip()}
<div class="tbl" style="margin-top:16px"><table><thead><tr><th>부</th><th>제목</th><th>이 부를 배우는 까닭</th><th>핵심</th></tr></thead><tbody>
{''.join(f"<tr><td>{n}</td><td>{E(t)}</td><td>{E(a)}</td><td>{E(b)}</td></tr>" for n, t, a, b in FLOW)}</tbody></table></div>
<h3 style="margin-top:22px">한눈에 보는 디테일 기준값 (예시값)</h3>
<div class="tbl"><table><thead><tr><th>부위</th><th>기준</th><th>계산·규칙</th><th>배우는 곳</th></tr></thead><tbody>
<tr><td>눈 모양</td><td>눈꼬리가 눈머리보다 조금 높으면 기본 눈</td><td>기울기 = 높이 차 ÷ 눈 너비, 0~8°</td><td><a href="01_eye_shape.html#s1">1부 1단계</a></td></tr>
<tr><td>비스듬한 얼굴의 안쪽 눈</td><td>고개 30°면 앞쪽 눈의 약 58%</td><td>cos(고개+25°) ÷ cos(고개−25°)</td><td><a href="01_eye_shape.html#s3">1부 3단계</a></td></tr>
<tr><td>흰자</td><td>피부보다 조금 밝고 순백보다 낮게</td><td>세 값의 평균으로 비교</td><td><a href="02_eye_paint.html#s1">2부 1단계</a></td></tr>
<tr><td>눈동자 그림자·빛</td><td>위는 곱하기, 아래는 더하기 40~70%</td><td>밑색 × 위 색 ÷ 255 · 밑색 + 색 × 불투명도</td><td><a href="02_eye_paint.html#s2">2부 2단계</a></td></tr>
<tr><td>표정</td><td>눈썹 = 종류, 눈 뜬 정도 = 세기</td><td>슬픔은 가늘게 뜰수록 북받침</td><td><a href="02_eye_paint.html#s3">2부 3단계</a></td></tr>
<tr><td>코</td><td>눈과 정보량 차이 1 이내</td><td>모서리 선 중 몇 개를 고르나</td><td><a href="03_nose_ear_mouth.html#s1">3부 1단계</a></td></tr>
<tr><td>귀</td><td>눈 높이~코끝 높이 사이</td><td>너비 = 10 × |sin 각도| + 1.5</td><td><a href="03_nose_ear_mouth.html#s2">3부 2단계</a></td></tr>
<tr><td>벌린 입</td><td>위 이 一, 아래 이 U, 어금니는 안쪽 한 점으로</td><td>아래 이줄 깊이 × sin(벌린 각도)</td><td><a href="03_nose_ear_mouth.html#s3">3부 3·4단계</a></td></tr>
<tr><td>머리카락</td><td>머리 밑그림의 1.05~1.15배, 덩어리 ≈ 얼굴 정보량 + 1</td><td>넓이는 k²배</td><td><a href="04_hair.html#s1">4부 1·2단계</a></td></tr>
</tbody></table></div>
<p class="hint">이 편은 얼굴 부위의 디테일이 중심입니다. 얼굴 전체의 비율(원·기준선·남녀 차이)과 올려다보기·내려다보기의 큰 틀은 <a href="{PREV_SITE}">03 얼굴 편</a>에 맡기고, 여기서는 그 위에 얹는 부위만 다룹니다.</p>
<p class="muted" style="margin-top:12px">같은 시리즈: <a href="{PREV_SITE}">03 얼굴 편(얼굴 비율·남녀)</a> · <a href="{CLOTH_SITE}">01 옷장 편(옷 주름·그림자)</a> · <a href="{FIRST_SITE}">구조 먼저 보는 캐릭터 그리기 연구실(구조·빛·확산 모델)</a> · <a href="{RENDER}">AI 렌더링 연구실</a></p></div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2><div class="cast-grid">{''.join(f'<div class="who">{face(k, "e01" if k in ("haru","sia","moa") else "e13")}<b>{E(CH[k][0])}</b><span>{E(CH[k][1])}</span></div>' for k in ["doctor","haru","sia","moa","jupanbot","fruitfly","x1","x2","x3"])}</div>
<p class="hint" style="margin-top:10px">하루·시아·모아는 20대 성인 연구원, 박사는 30대 성인 남성입니다. 표정·눈 실험에서도 모두 성인 얼굴을 기준으로 합니다.</p></div></section>
<section id="source"><div class="wrap"><h2>원리와 출처</h2>
<p>1~4부의 그리기 원리(육각형 밑그림과 눈머리·눈꼬리, 각막·홍채·동공의 앞뒤, 공 위의 눈, 빗금 밀도, 흰자 색과 레이어 칠하기, 눈썹·눈·입으로 만드는 표정, 코를 단순하게 하는 정도, 귀의 자리와 각도, 벌린 입의 이줄, 머리카락의 부피·덩어리·나는 자리·다발 굵기)는 일반적인 캐릭터 그리기 원리이며, KawaiiSensei의 작법서 『いいトコどり! 人物パーツの描き方』(マイナビ出版, 2023) 1장 「顔を描こう」(p.12~46)를 참고해 정리했습니다. 책의 그림·문장·도식·색 값·구성 순서는 옮기지 않았고, 연구실 캐릭터와 직접 움직이는 실험으로 새로 구성했습니다. 얼굴 전체의 비율과 각도는 앞 편 03에서 다뤘으므로 이 편에서는 부위의 디테일만 다룹니다.</p>
<p>레이어를 겹치는 계산은 Porter·Duff(1984)와 W3C 혼합 모드 규격, 가림 영역 다시 그리기는 확산 모델 연구를 바탕으로 쉽게 풀었습니다(아래 출처). 페이지의 그림(표지 8장은 픽셀아트, 본문·실패·비교 그림은 애니풍)은 Genspark로 만들 예정이며, 그림이 들어오기 전에는 '그림 준비 중' 자리로 둡니다. 실험 패널은 모두 페이지 안에서 직접 계산해 그리므로 그림 없이도 동작합니다.</p></div></section>
"""
    s += kg_block("index", [P["file"] for P in PARTS] + ["practice/index.html"])
    s += footer()
    open(os.path.join(ROOT, "index.html"), "w").write(s)

def build_practice():
    pre = "../"
    t = f"{SERIES} 7부 — 실전 연습장"
    d = "눈 작업대(육각형·공·동공), 표정 조합판(눈썹·눈·입), 디테일 문장 공방(AI 문장), 진단 데스크(실패 맞히기) 네 곳을 직접 운영하며 1~6부를 함께 연습합니다."
    s = head(t, d, "og_07.jpg", "practice/index.html", pre)
    s += nav([("#bench", "눈 작업대"), ("#expr", "표정 조합판"), ("#workshop", "공방"), ("#desk", "진단 데스크"), ("#wrap", "마무리")], pre)
    s += cover("cover_07", "연구실 조종 책상 · 실전 연습장", [("haru", "e19"), ("doctor", "e16"), ("fruitfly", "e09"), ("jupanbot", "e16")], pre)
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">7부 · 마지막 장</span><h1>실전 연습장</h1>
<p class="lead">네 곳의 작업대를 직접 운영합니다. <span style="color:var(--green)">초록 조작판</span>은 주어진 환경, <span style="color:var(--blue)">파랑 조작판</span>은 내 결정입니다. 미션은 직접 조작해야 판정됩니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section id="practice"><div class="wrap">
<div class="tabs" role="tablist"><button type="button" data-t="bench">눈 작업대</button><button type="button" data-t="expr">표정 조합판</button><button type="button" data-t="workshop">디테일 문장 공방</button><button type="button" data-t="desk">진단 데스크</button></div>
"""
    def sc(id_, title, situ, env, me, missions, back, extra_g1=""):
        ms = "".join(f"<li>{E(m)}</li>" for m in missions)
        bk = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in back)
        return f"""<div class="scene" id="{id_}"><h2>{E(title)}</h2><div class="box"><b>상황</b> — {E(situ)}</div>
<div class="panel"><div class="ph"><b>조작판</b><small>초록 = 환경 · 파랑 = 내 결정</small></div>
<div class="ctrl ctl-env">{env}</div><div class="ctrl ctl-me">{me}</div>
<div class="board" aria-live="polite"></div>
<div class="pair"><div class="g1">{extra_g1}</div><div class="g2"></div></div>
<div class="talk"></div>
<h4>미션</h4><ol class="missions">{ms}</ol></div>
<p class="muted">배운 곳 다시 보기: {bk}</p></div>
"""
    s += sc("bench", "눈 작업대 — 육각형·공·동공 맞추기", "그릴 눈 모양과 고개 각도는 주어집니다. 눈머리·눈꼬리 높이, 안쪽 눈 너비, 동공 위치를 정해 맞춥니다.",
            '<label>목표 눈 <select name="target"><option value="up" selected>올라간 눈</option><option value="mid">기본 눈</option><option value="down">처진 눈</option></select></label><label>고개 <select name="turn"><option value="0" selected>정면</option><option value="1">비스듬히 30°</option></select></label>',
            '<label>눈머리 높이(×0.1) <input type="range" name="inY" min="-20" max="20" step="1" value="0"></label><label>눈꼬리 높이(×0.1) <input type="range" name="outY" min="-20" max="25" step="1" value="5"></label><label>안쪽 눈 너비(%) <input type="range" name="far" min="20" max="110" step="1" value="100"></label><label>동공 위치(0 = 홍채 면) <input type="range" name="pupil" min="-4" max="10" step="1" value="6"></label>',
            ["올라간 눈을 동공까지 맞춰 완성하기(정면이든 비스듬히든)", "비스듬히 30°에서 처진 눈 완성하기(안쪽 눈 58% 안팎)", "눈 모양 × 고개 조합 세 가지 완성하기"],
            [("01_eye_shape.html#s1", "1부 1단계 육각형"), ("01_eye_shape.html#s2", "1부 2단계 각막"), ("01_eye_shape.html#s3", "1부 3단계 공 위의 눈")])
    s += sc("expr", "표정 조합판 — 종류·세기·입 맞추기", "목표 표정이 주어집니다. 눈썹 기울기(종류), 눈 뜬 정도(세기), 입 모양(밖으로 내는 정도)을 골라 맞춥니다.",
            '<label>목표 표정 <select name="target"><option value="0">조용한 기쁨</option><option value="1">들뜬 기쁨</option><option value="2" selected>참는 화</option><option value="3">터진 화</option><option value="4">참는 슬픔</option><option value="5">북받친 슬픔</option></select></label>',
            '<label>눈썹 끝 기울기(°) <input type="range" name="brow" min="-25" max="25" step="1" value="0"></label><label>눈 뜬 정도(%) <input type="range" name="open" min="30" max="130" step="5" value="100"></label><label>입 <select name="mouth"><option value="smile" selected>웃는 입</option><option value="closed">다문 입</option><option value="half">반쯤 연 입</option><option value="open">벌린 입</option><option value="wide">크게 벌린 입</option><option value="grin">씩 웃는 입</option></select></label>',
            ["참는 화 완성하기", "북받친 슬픔 완성하기(슬픔은 가늘게 뜰수록 북받침)", "여섯 표정을 모두 한 번씩 완성하기"],
            [("02_eye_paint.html#s3", "2부 3단계 눈썹과 눈"), ("02_eye_paint.html#s4", "2부 4단계 같은 눈, 다른 입")])
    s += sc("workshop", "디테일 문장 공방 — 요청서 조립", "요청 상황에 맞춰 디테일 문장을 조립합니다. 점검표 6조각을 채우고, 상황에 꼭 필요한 조각을 넣습니다.",
            '<label>요청 상황 <select name="job"><option value="close">눈 클로즈업(눈 모양·칠하기 중요)</option><option value="sheet">표정 시트(입·눈 중요)</option><option value="hair">헤어 설정(머리·정보량 중요)</option></select></label>',
            '<div class="ow" style="width:100%"></div>',
            ["점검표 6 / 6을 충돌 경고 없이 채우기", "눈 클로즈업 상황에서 칠하기 조각 + 코끝 점 + 정보량 고르게로 조립하기", "크게 벌린 입과 눈 모양을 고르되 성인 나이를 적어 쏠림 경고 없애기"],
            [("05_ai_detail.html#s1", "5부 1단계 디테일 문장"), ("05_ai_detail.html#s2", "5부 2단계 칠하기 문장"), ("06_failure_lab.html#drift", "6부 나이 쏠림")],
            '<div class="promptbox"><b>조립된 디테일 문장</b><pre aria-live="polite"></pre><button type="button" class="btn copy">복사하기</button></div>')
    s += sc("desk", "진단 데스크 — 원인 맞히기", "디테일 그림 실패의 증상이 하나씩 들어옵니다. 원인을 고르세요. 순서: 자리와 각도 → 구조 → 정보량 → 칠하기 → 표정.",
            '<span class="hint">환경: 증상은 무작위로 들어옵니다.</span>',
            '<div style="width:100%"><p class="sym" style="font-weight:600"></p><div class="opts deskopts"></div></div>',
            ["3개 연속 정답", "8종 원인을 모두 한 번 이상 맞히기", "틀리지 않고 5개 맞히기"],
            [("06_failure_lab.html#s1", "6부 진단 순서"), ("06_failure_lab.html#fails", "6부 실패 8종")])
    s += f"""</div></section>
<section id="wrap"><div class="wrap"><h2>마무리 — 네 작업대를 하나로 묶으면</h2>
<div class="box"><p>눈 작업대에서 맞춘 눈머리·눈꼬리 높이는 공방의 '눈 모양' 조각이 되고, 표정 조합판의 눈썹·눈·입은 공방의 '입' 조각과 표정 시트가 됩니다. 진단 데스크에서 틀린 원인은 대부분 앞의 두 곳 중 하나가 빠진 경우입니다. 디테일 그림은 결국 <b>육각형 하나와 덩어리 몇 개 위에, 부위마다 같은 양을 고르게 얹는 일</b>입니다.</p>
<p><b>실제 그림으로 이어 가기</b> — 디테일 문장 공방에서 조립한 문장을 복사해 그림 생성 AI에 넣어 보세요. 결과는 각 부의 '프롬프트로 직접 만들어 보기' 확인표로 점검합니다: <a href="{pre}01_eye_shape.html#make">1부</a> · <a href="{pre}02_eye_paint.html#make">2부</a> · <a href="{pre}03_nose_ear_mouth.html#make">3부</a> · <a href="{pre}04_hair.html#make">4부</a> · <a href="{pre}05_ai_detail.html#make">5부</a> · <a href="{pre}06_failure_lab.html#make">6부</a></p>
<p class="hint">주의할 점: 이 연습장의 기준값(8°, 58%, 동공 위치, 눈썹 8°·눈 뜬 정도 경계)은 애니풍 기본 얼굴의 예시입니다. 판정 범위는 원리를 보이기 위해 정한 값이며, 실제 사람과 화풍마다 다릅니다.</p></div>
<div class="next"><a href="{pre}06_failure_lab.html">← 6부 실패 사례 실험실</a><a href="{pre}index.html">목차로</a></div></div></section>
"""
    s += kg_block("practice_index", ["practice/index.html"])
    s += footer(pre)
    open(os.path.join(ROOT, "practice", "index.html"), "w").write(s)

if __name__ == "__main__":
    JS = ["js_base.js", "js_practice_util.js", "js_detail.js", "js_tail.js"]
    os.makedirs(os.path.join(ROOT, "practice"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "panels.js"), "w").write("".join(open(os.path.join(ROOT, "build", f)).read() for f in JS))
    build_index()
    for P in PARTS:
        build_part(P)
    build_practice()
    print("built", len(PARTS) + 2, "pages")
