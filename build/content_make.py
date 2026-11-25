# -*- coding: utf-8 -*-
"""부마다 '프롬프트로 직접 만들어 보기' 실습. A 프롬프트는 make_requests.py(이 페이지 그림을 만드는 프롬프트)에서 가져온다.
res: 실제 결과 기록. 그림을 만들기 전에는 '아직 만들지 않음'을 그대로 적고, 그림이 들어오면 A·B를 나란히 보고 실제로 달라진 점을 적는다."""

PENDING = "실제 결과: 아직 그림을 만들지 않았습니다. A·B 그림이 들어오면 나란히 놓고 실제로 무엇이 달라졌는지(또는 달라지지 않았는지) 이 자리에 적습니다."

def T(key, title, goal, b_title, b_text, check, tip=None, b_key=None, res=PENDING):
    return dict(key=key, title=title, goal=goal, b_title=b_title, b_text=b_text, check=check, tip=tip, img=key, b_imgs=[b_key or key + "_b"], res=res)

TIP_SMALL = "눈 기울기·눈썹 방향처럼 작은 차이는 같은 대화에서 잘 반영되지 않습니다(03 얼굴 편의 실제 결과). 차이가 약하면 새 대화에서 만들되, 'Same image'로 시작하는 B 문장만 넣지 마세요. 이번 편 실습 1·2의 B처럼 가리킬 그림이 없어 캐릭터가 사라질 수 있습니다. A 프롬프트 안의 해당 문장을 직접 고쳐 한 덩어리로 넣고, 참고 그림을 첨부하세요."

MAKE = {
1: [
 T("p1_moa_eye_closeup", "육각형 밑그림과 완성 눈을 한 장에", "육각형 밑그림 위에 눈이 얹히는지, 눈꼬리가 눈머리보다 조금 높은지 눈으로 확인합니다.",
   "B — 원리 빼기: 눈머리와 눈꼬리를 같은 높이로", "Same image, keep the same framing. Change only: in both panels make each eye a perfectly symmetrical oval with the inner and outer corners at exactly the same height, and remove the hexagon guides. Still no text.",
   [("오른쪽 완성 눈의 눈꼬리가 눈머리보다 조금 높은가", "#s1"), ("위 눈꺼풀이 굵고 아래 눈꺼풀이 가는가", "#s1"), ("B 결과에서 인상이 밋밋하거나 달라 보이는지 비교", "#s1")], tip=TIP_SMALL),
 T("p1_moa_three_quarter", "비스듬한 얼굴의 안쪽 눈", "고개를 돌린 모아의 안쪽 눈이 앞쪽 눈보다 좁게 그려졌는지 봅니다.",
   "B — 원리 빼기: 두 눈을 같은 너비로", "Same image, keep the same framing. Change only: draw the far eye exactly as wide as the near eye, like a front view. Still no text.",
   [("안쪽 눈이 앞쪽 눈의 60% 안팎인가", "#s3"), ("안쪽 눈썹도 짧게 줄었나", "#s3"), ("B 결과에서 눈만 정면을 보는 듯 어색한지 비교(6부 f2와 같은 실패)", "06_failure_lab.html#f2")]),
],
2: [
 T("p2_haru_eye_paint", "레이어로 칠한 하루의 눈", "흰자 색, 위쪽 그림자, 아래쪽 빛, 하이라이트 두 개가 들어갔는지 봅니다.",
   "B — 원리 빼기: 순백 흰자와 한 색 눈동자", "Same image, keep the same framing. Change only: make the whites of the eyes pure bright white and the irises one flat blue with no shadow and no glow, a single highlight. Still no text.",
   [("흰자가 피부보다 조금 밝고 순백이 아닌가", "#s1"), ("눈동자 위는 어둡고 아래는 밝은가(파란색은 유지)", "#s2"), ("B 결과가 스티커처럼 떠 보이는지 비교(6부 f7)", "06_failure_lab.html#f7")]),
 T("p2_haru_expressions", "눈썹과 눈만으로 만든 표정 여섯", "입은 그대로 두고 눈썹 방향과 눈 뜬 정도만으로 여섯 감정이 구별되는지 봅니다.",
   "B — 원리 빼기: 눈썹을 모두 같게", "Same image, keep the same framing. Change only: give all six faces the same flat neutral eyebrows; keep the eyes and mouths as they are. Still no text.",
   [("위 줄 세 표정이 아래 줄보다 약한 감정으로 읽히나", "#s3"), ("슬픔은 위 줄(참는 슬픔)이 눈을 크게 떴나", "#s3"), ("B 결과에서 감정의 종류가 흐려지는지 비교", "#s3")], tip=TIP_SMALL),
],
3: [
 T("p3_sia_profile_ear", "귀 자리와 단순한 코", "시아 옆얼굴의 귀가 눈~코끝 사이에 있고, 코가 다른 부위만큼 단순한지 봅니다.",
   "B — 원리 빼기: 귀를 턱선 가까이", "Same image, keep the same framing. Change only: move the ear down so it sits near the jawline, below the nose-tip level. Still no text.",
   [("귀 윗부분이 눈 높이, 아랫부분이 코끝 높이쯤인가", "#s2"), ("코가 짧은 콧날과 코끝 정도로 단순한가", "#s1"), ("B 결과에서 고개를 숙인 듯 보이는지 비교(6부 f3)", "06_failure_lab.html#f3")]),
 T("p3_doctor_laugh", "웃는 박사의 이줄", "위 이는 一, 아래 이는 U, 어금니는 안쪽으로 모이는지 봅니다.",
   "B — 원리 빼기: 아래 이도 一로", "Same image, keep the same framing. Change only: draw the lower teeth as a straight flat horizontal row exactly like the upper teeth, and the back teeth facing the viewer. Still no text.",
   [("위 이줄이 거의 가로 일자인가", "#s3"), ("아래 이줄이 내려다본 U로 둥근가", "#s3"), ("B 결과에서 입속이 납작한 판처럼 보이는지 비교", "#s4")]),
],
4: [
 T("p4_hair_three", "세 사람의 머리 부피와 덩어리", "세 헤어스타일 모두 머리 밑그림보다 크게, 덩어리로 나뉘어 그려졌는지 봅니다.",
   "B — 원리 빼기: 두피에 붙은 머리", "Same image, keep the same framing. Change only: make all three hairstyles flat and tight against the skull with no volume. Still no text.",
   [("머리카락 바깥선이 머리보다 한 둘레 큰가", "#s1"), ("머리가 큰 덩어리 네다섯 개로 읽히나", "#s2"), ("B 결과에서 얼굴이 커 보이는지 비교(6부 f5)", "06_failure_lab.html#f5")]),
 T("p4_sia_wind", "바람에 날리는 긴 흑발", "바람이 닿는 한 점에서 퍼지는 흐름과 다발 굵기 섞기를 봅니다.",
   "B — 원리 빼기: 같은 굵기의 다발", "Same image, keep the same framing. Change only: make every hair clump exactly the same thickness, all bending the same way, no loose single strands. Still no text.",
   [("다발이 정수리 근처 한 점에서 퍼져 나가나", "#s3"), ("굵고 가는 다발이 섞였나", "#s4"), ("B 결과가 빗질한 무늬처럼 단조로운지 비교", "#s4")]),
],
5: [
 T("p5_haru_sheet", "정보량이 고른 얼굴 설정 시트", "일곱 개 얼굴의 눈·코·입·머리 그려 넣은 양이 모두 같은지 봅니다.",
   "B — 원리 빼기: 코만 실감 나게", "Same image, keep the same framing. Change only: in every head draw the nose in a detailed realistic way with nostrils and a shaded bridge; keep everything else simple. Still no text.",
   [("일곱 얼굴의 눈 정보량이 같은가", "#s1"), ("세 각도 얼굴의 눈 높이가 같은 가로선 위에 있나", "#s1"), ("B 결과에서 코만 튀는지 비교(6부 f6)", "06_failure_lab.html#f6")]),
 T("p5_moa_detail_levels", "세 화풍, 같은 구조", "화풍이 바뀌어도 눈 기울기와 머리 실루엣이 그대로인지 봅니다.",
   "B — 원리 빼기: 구조까지 바꾸기", "Same image, keep the same framing. Change only: in the semi-realistic face make the eyes droopy (outer corners lower than inner corners) and the hair silhouette much flatter. Still no text.",
   [("세 얼굴의 눈꼬리가 모두 눈머리보다 조금 높은가", "#s4"), ("리본이 세 얼굴 모두 왼쪽 귀 위에 있나", None), ("B 결과에서 반실사 얼굴이 다른 사람처럼 보이는지 비교", "#s4")]),
],
6: [
 T("f2_far_eye", "실패 그림 고치기 — 안쪽 눈만 좁히기", "f2(같은 너비의 두 눈)를 부분 수정으로 고쳐, 처음 걸린 항목 하나만 바꾸면 되는지 확인합니다.",
   "B — 고치기: 안쪽 눈만 칠해 부분 수정", "Inpainting only the far eye and its eyebrow: make the far eye noticeably narrower (about 60% of the near eye) and closer to the center line of the face, following the curve of the head. Keep the iris color, the near eye and everything else unchanged.",
   [("고친 뒤 안쪽 눈이 앞쪽 눈보다 좁은가", "01_eye_shape.html#s3"), ("앞쪽 눈·머리·옷은 그대로인가", "05_ai_detail.html#s3"), ("가림 영역 경계에 이음매가 보이지 않나", "05_ai_detail.html#s3")], b_key="f2_fixed"),
 T("f7_sticker_eyes", "실패 그림 고치기 — 칠하기 다섯 조각 더하기", "f7(스티커 눈)에 칠하기 문장만 더해, 눈이 얼굴에 녹아드는지 봅니다.",
   "B — 고치기: 칠하기 조각을 더해 눈만 다시", "Same image, keep the same framing. Change only the eyes: off-white sclera slightly warmer than pure white, darker upper iris under the eyelid, subtle warm glow on the lower iris (the iris stays gray), one large and one small highlight, line art around light areas tinted brown. Still no text.",
   [("흰자가 순백이 아니게 되었나", "02_eye_paint.html#s1"), ("눈동자에 위 그림자와 아래 빛이 생겼나", "02_eye_paint.html#s2"), ("눈 모양·얼굴은 그대로인가", None)], b_key="f7_fixed"),
],
}

# 2026-11-25 받은 A·B 그림을 나란히 보고 적은 실제 결과
RES = {
    "p1_moa_eye_closeup": "실제 결과: B는 새 대화에서 만들었는데 모아가 사라지고, 실사 사람의 두 눈을 찍은 사진 같은 그림이 위아래 두 줄로 나왔습니다. 눈머리·눈꼬리 높이가 거의 같은 동그란 눈이라 요청한 원리 빼기 자체는 들어갔지만, 화풍과 사람이 바뀌어 A와 비교하기 어렵습니다. 'Same image'가 가리킬 그림이 없어 도구가 처음부터 새로 해석한 것으로 보입니다. 비교하려면 A 프롬프트의 눈 문장을 직접 고쳐 참고 그림과 함께 다시 넣어야 합니다.",
    "p1_moa_three_quarter": "실제 결과: 안쪽 눈이 앞쪽 눈만큼 넓어졌지만, 도구가 얼굴도 함께 정면 쪽으로 돌려 그렸습니다. 그래서 '비스듬한 얼굴에 정면 눈'이라는 어색함은 생기지 않고, 조금 더 정면에 가까운 모아가 나왔습니다. 도구는 고개 각도와 눈 너비를 서로 맞추려 한다는 뜻이니, 눈 너비를 고칠 때 고개 각도가 같이 바뀌지 않았는지도 확인하세요.",
    "p2_haru_eye_paint": "실제 결과: 요청이 그대로 반영됐습니다. B는 흰자가 새하얗고 눈동자가 그림자·빛 없는 한 가지 파랑, 하이라이트 하나라서 눈만 오려 붙인 스티커처럼 납작합니다. 나머지(머리·코·구도)는 A와 같아 칠하기 조각의 효과를 가장 깨끗하게 비교할 수 있는 쌍입니다.",
    "p2_haru_expressions": "실제 결과: B는 새 대화에서 만들었는데 하루가 사라지고, 서로 다른 실사 인물 여섯 명의 표정 사진이 나왔습니다. 눈썹을 같게 하라는 요청도 반영되지 않아 표정마다 눈썹이 다릅니다. 실습 1과 같은 까닭으로 보입니다. 이 비교는 A 프롬프트의 표정 문장에서 눈썹 부분을 'same flat neutral eyebrows'로 직접 바꾸고 하루 참고 그림을 첨부해 다시 만들어야 합니다.",
    "p3_sia_profile_ear": "실제 결과: 귀가 반 개쯤 아래로 내려갔지만 요청한 턱선까지는 가지 않았습니다. 그래도 귀 아랫끝이 코끝보다 내려가 A보다 목이 길어 보이고 고개가 조금 숙여진 듯 읽힙니다. 차이가 작으니 두 그림의 귀 윗끝에 가로선을 그어 눈 높이와 비교해 보세요.",
    "p3_doctor_laugh": "실제 결과: 거의 반영되지 않았습니다. 입이 조금 더 벌어지고 위 이가 흰 띠 하나로 단순해졌지만, 아래 이는 여전히 둥근 U이고 어금니도 안쪽으로 들어갑니다. 도구가 이줄을 바르게 그리려는 쪽으로 강하게 기울어 있다는 사례입니다(6부 f4도 같은 까닭으로 재현되지 않았습니다).",
    "p4_hair_three": "실제 결과: 모아만 가운데 가르마의 곧고 납작한 머리로 바뀌어 얼굴이 커 보이고, 하루와 시아는 거의 그대로입니다. 한 번에 셋을 바꾸라고 하면 한 사람에게만 반영될 수 있습니다. 모아의 A·B를 나란히 보면 머리 부피에 따라 얼굴 크기가 얼마나 달라 보이는지 알 수 있습니다.",
    "p4_sia_wind": "실제 결과: 요청보다 크게 반영됐습니다. 머리 다발이 같은 굵기의 매끈한 띠 일곱 줄로 바뀌어 똑같은 물결로 휘어지고, 따로 노는 가닥이 사라졌습니다. 머리카락이라기보다 리본처럼 보여, 다발 굵기를 섞어야 하는 까닭이 한눈에 보이는 쌍입니다.",
    "p5_haru_sheet": "실제 결과: 반영되지 않았습니다. B의 코도 A처럼 작은 코끝뿐이고 시트 전체가 거의 같습니다. 같은 대화에서 '코만 실감 나게'처럼 화풍을 깨는 요청은 도구가 화풍을 지키려고 무시하는 일이 많습니다. 실패 그림 f6처럼 처음부터 새 대화에서 만들면 반영됩니다.",
    "p5_moa_detail_levels": "실제 결과: 반실사 얼굴만 바뀌었습니다. 머리가 곧고 납작해졌고 눈이 조금 가늘고 처져, 세 얼굴을 나란히 보면 반실사만 같은 모아가 아니라 다른 사람처럼 읽힙니다. 화풍이 바뀌어도 눈꼬리 기울기와 머리 실루엣을 남겨야 하는 까닭을 이 쌍에서 알 수 있습니다.",
    "f2_far_eye": "실제 결과: 거의 달라지지 않았습니다. A에서 안쪽 눈이 이미 앞쪽 눈의 약 0.8배로 조금 좁게 나와 있었고, 부분 수정 뒤에도 약 0.8배로 같습니다. 요청한 60%까지 좁히려면 가림 영역을 눈썹·눈 주변까지 넓히고 '눈 너비를 절반 가까이'처럼 더 과장해 적어야 합니다.",
    "f7_sticker_eyes": "실제 결과: 눈만 바뀌고 나머지는 그대로입니다. 흰자가 피부 쪽으로 따뜻해지고, 눈동자 위가 어두워지며 하이라이트가 늘어 눈이 얼굴에 녹아듭니다. 아래쪽 따뜻한 빛은 약하게만 들어갔고 눈 색은 회색 그대로입니다.",
}
for _ts in MAKE.values():
    for _t in _ts:
        if _t["key"] in RES:
            _t["res"] = RES[_t["key"]]
