# -*- coding: utf-8 -*-
"""부마다 '프롬프트로 직접 만들어 보기' 실습. A 프롬프트는 make_requests.py(이 페이지 그림을 만드는 프롬프트)에서 가져온다.
res: 실제 결과 기록. 그림을 만들기 전에는 '아직 만들지 않음'을 그대로 적고, 그림이 들어오면 A·B를 나란히 보고 실제로 달라진 점을 적는다."""

PENDING = "실제 결과: 아직 그림을 만들지 않았습니다. A·B 그림이 들어오면 나란히 놓고 실제로 무엇이 달라졌는지(또는 달라지지 않았는지) 이 자리에 적습니다."

def T(key, title, goal, b_title, b_text, check, tip=None, b_key=None, res=PENDING):
    return dict(key=key, title=title, goal=goal, b_title=b_title, b_text=b_text, check=check, tip=tip, img=key, b_imgs=[b_key or key + "_b"], res=res)

TIP_SMALL = "눈 기울기·눈썹 방향처럼 작은 차이는 같은 대화에서 잘 반영되지 않습니다(03 얼굴 편의 실제 결과). 차이가 약하면 새 대화에서 B 문장을 처음부터 넣어 만들고, 비교할 두 그림을 서로 다른 대화에서 받으세요."

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
