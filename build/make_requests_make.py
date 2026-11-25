# -*- coding: utf-8 -*-
"""'프롬프트로 직접 만들어 보기'의 B 결과 그림 요청 꾸러미(docs/image_requests_make) 생성. A 결과를 먼저 받은 뒤 요청한다."""
import os, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_make import MAKE
from make_requests import PROMPTS, ATTACH_OF, CONV_OF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests_make")
os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
HEAD = ("해설 페이지의 '직접 만들어 보기' 비교 그림을 만들어 줘.\n- 첨부한 그림(이미 만든 A 결과)과 똑같은 캐릭터·구도·화풍·빛을 유지하고, 아래 'Change only'에 적힌 것만 바꿀 것\n"
        "- 비율은 첨부한 A 결과와 같게\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·교복 느낌·어려 보이는 얼굴 금지\n- 그림 안에 글자·숫자·로고 금지")
PAGES = ["", "01_eye_shape", "02_eye_paint", "03_nose_ear_mouth", "04_hair", "05_ai_detail", "06_failure_lab"]
rows = []; n = 0
for no in range(1, 7):
    cid = f"M0{no}_part{no}"
    md = f"# {cid[:3]} · {no}부 '직접 만들어 보기' 비교 그림\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD}\n```\n"
    for t in MAKE[no]:
        for k in t["b_imgs"]:
            n += 1; a = PROMPTS[t["key"]]; ratio = "16:9" if "16:9" in a[4].split("\n")[0] else "2:3"
            if k == "f2_fixed":
                att = "f2_far_eye.png (A 결과)"; how = "그림 생성이 아니라 '부분 수정(영역 칠하기)' 기능으로 — 안쪽 눈과 안쪽 눈썹만 칠하기"
            elif k in ("p1_moa_eye_closeup_b", "p2_haru_expressions_b"):
                att = f"{ATTACH_OF[CONV_OF[t['key']]]} (A 결과는 첨부하지 않음)"; how = "새 대화에서 A 프롬프트 + Change only 문장을 함께 넣어 처음부터(작은 차이라 같은 대화에서는 반영이 약함)"
            else:
                att = f"{t['key']}.png (A 결과) + {ATTACH_OF[CONV_OF[t['key']]]}"; how = "A 결과를 첨부하고 Change only 문장으로"
            rows.append([n, cid[:3], k, f"{PAGES[no]}.html#make", ratio, how, ""])
            md += f"\n---\n## {k} — {t['title']}\n첨부: {att}\n방법: {how}\n```\n{t['b_text']}\n```\n"
    open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "ratio", "how", "status"]); w.writerows(rows)
open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 2 — '프롬프트로 직접 만들어 보기' 비교 그림 ({n}장)

부마다 '프롬프트로 직접 만들어 보기' 실습의 **B 결과**(원리를 빼거나 바꾼 비교 그림)입니다. **꾸러미 1(docs/image_requests)의 A 결과를 먼저 받은 뒤** 요청합니다.

## 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 장수 | 방법 |
|---|---|---|---|
| 1 | prompts/M01_part1.md | 2 | 눈 모양 B는 **새 대화에서 처음부터**, 안쪽 눈 B는 A 첨부 |
| 2 | prompts/M02_part2.md | 2 | 칠하기 B는 A 첨부, 표정 시트 B는 **새 대화에서 처음부터** |
| 3 | prompts/M03_part3.md | 2 | A 결과를 첨부하고 Change only 문장 |
| 4 | prompts/M04_part4.md | 2 | 같음 |
| 5 | prompts/M05_part5.md | 2 | 같음 |
| 6 | prompts/M06_part6.md | 2 | f2는 **부분 수정(영역 칠하기)**, f7은 A 첨부 |

## 주의
- 'Change only' 문장만 바꾸고 나머지(캐릭터·구도·빛)는 A와 같아야 비교가 됩니다. 구도가 흔들리면 'keep the same framing'을 덧붙입니다.
- 비교 그림이 A와 거의 같게 나오면 새 대화에서 처음부터 한 번 더 시도해 주세요. 그래도 같으면 그대로 주셔도 됩니다(페이지에 있는 그대로 적습니다).
""")
print("make images", n)
