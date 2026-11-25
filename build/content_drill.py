# -*- coding: utf-8 -*-
"""부마다 '프롬프트 연습 과제' 2개씩(모두 12개). 과제의 프롬프트는 예상 결과 그림을 실제로 만드는 프롬프트와 같다(이 파일이 원본).
python3 build/content_drill.py → docs/image_requests_drill/ 요청 꾸러미 생성.
03 얼굴 편에서 배운 것을 처음부터 반영했다: ① 비교할 두 그림은 서로 다른 새 대화에서 ② 여러 얼굴 시트보다 한 장씩 ③ 바뀌는 곳은 크게 과장해 ④ 바로잡을 그림은 첨부하지 않기."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import who, ANI, END, CH

def P(ratio, scene, extra=""):
    return ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\n{ANI}\n{scene}\n" + (extra + "\n" if extra else "") + "Plain off-white studio background.\n" + END)

LESSON = "03 얼굴 편에서는 같은 대화에서 작은 변화를 요청하면 도구가 앞 그림을 그대로 따라 그려 차이가 거의 나지 않았습니다. 그래서 비교할 두 그림은 서로 다른 새 대화에서 만들고, 바뀌는 곳을 분명하게 과장해 적습니다."

# 과제 하나: id, title, goal, why, attach, steps, prompts[(라벨, 프롬프트, 결과 그림 key, 결과 그림 설명, 비율)], check[(문장, 링크)], expect, trouble[(문제, 대처)], more
DRILL = {
1: [
 dict(id="d1", title="눈꼬리 높이를 문장으로 — 올라간 눈과 처진 눈", goal="1부 1단계의 육각형 원리(눈머리·눈꼬리 높이)를 문장으로 적어, 같은 모아를 올라간 눈과 처진 눈으로 따로 만들고 인상 차이를 봅니다.",
      why="'날카로운 눈', '순한 눈' 같은 말은 도구마다 다르게 받아들입니다. 눈꼬리가 눈머리보다 '높다/낮다'처럼 두 꼭짓점의 위치로 적으면 같은 인상이 더 잘 나옵니다. " + LESSON,
      attach="refs/moa_anime_base.png, refs/moa_sheet.png",
      steps=["Genspark에서 새 대화를 열고 참고 그림 두 장을 첨부합니다.", "프롬프트 ①로 첫 그림을 만듭니다(올라간 눈).",
             "새 대화를 하나 더 열고 같은 참고 그림을 첨부한 뒤, 프롬프트 ②로 둘째 그림을 만듭니다(처진 눈).",
             "두 그림의 두 눈에 각각 눈머리와 눈꼬리를 잇는 선을 긋고, 선이 어느 쪽으로 기우는지 봅니다.", "기울기가 반대로 나왔으면 성공입니다. 차이가 약하면 'Make the change much stronger.'를 덧붙여 같은 대화에서 한 번 더 만듭니다."],
      prompts=[("① 새 대화 A — 올라간 눈", P("2:3", "Front view, chest-up portrait of " + who("moa") + ", calm closed-mouth expression, looking at the viewer.",
                "Eye shape (most important): SHARP UPTURNED EYES — the outer corners of both eyes are clearly higher than the inner corners, and the inner corners sit slightly lower than usual; a line from the inner corner to the outer corner tilts up by about ten degrees. Light from the upper left."),
                "d1_moa_up", "예상 결과 ① — 눈꼬리를 눈머리보다 분명히 높인 모아. 같은 사람인데 날카롭고 강한 인상", "2/3"),
               ("② 새 대화 B — 처진 눈", P("2:3", "Front view, chest-up portrait of " + who("moa") + ", calm closed-mouth expression, looking at the viewer.",
                "Eye shape (most important): GENTLE DROOPY EYES — the outer corners of both eyes are clearly lower than the inner corners; a line from the inner corner to the outer corner tilts down by about five degrees. Light from the upper left."),
                "d1_moa_down", "예상 결과 ② — 눈꼬리를 눈머리보다 낮춘 모아. 같은 사람인데 부드럽고 순한 인상", "2/3")],
      check=[("①의 눈머리→눈꼬리 선이 위로 기우나", "#s1"), ("②의 선이 아래로 기우나", "#s1"), ("두 그림 모두 머리띠·왼쪽 리본이 같은 모아인가", None)],
      expect="같은 모아가 두 가지 인상으로 나옵니다. ①은 눈매가 또렷하고 강해 보이고, ②는 순하고 차분해 보입니다. 눈 크기와 머리·옷은 거의 같고 눈의 기울기만 달라야 합니다.",
      trouble=[("두 그림의 눈이 거의 같다", "같은 대화에서 만들었는지 확인하고, 새 대화에서 다시 만듭니다. 'about ten degrees'를 'about fifteen degrees'로 키웁니다."),
               ("①이 화난 표정이 됐다", "눈썹까지 올라간 경우입니다. 'relaxed eyebrows, calm expression'을 덧붙입니다."),
               ("리본이 오른쪽으로 갔다", "'white ribbon over her LEFT ear, as in the reference'를 맨 앞에 다시 적습니다.")],
      more="①·②의 문장에서 'moa'만 시아로 바꿔, 흑발 캐릭터에서도 같은 차이가 나는지 비교해 보세요."),
 dict(id="d2", title="비스듬한 얼굴에서 안쪽 눈 좁히기", goal="1부 3단계의 공 원리(고개 30°면 안쪽 눈 약 58%)를 문장으로 적어 시아의 비스듬한 얼굴을 만들고, 받은 그림에서 두 눈 너비를 재 봅니다.",
      why="도구는 비스듬한 얼굴에서도 두 눈을 똑같이 그리는 일이 잦습니다(6부 f2). 안쪽 눈의 너비를 앞쪽 눈에 대한 비율로 적으면 공 위의 눈이 더 잘 나옵니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림에서 두 눈의 눈머리~눈꼬리 길이를 각각 잽니다(픽셀 수 또는 자).", "안쪽 눈 ÷ 앞쪽 눈을 계산해 0.5~0.7 사이인지 봅니다. 1부 3단계 실험에서 고개 30°일 때 58%와 비교합니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Three-quarter view chest-up portrait of " + who("sia") + ", head turned about 30 degrees to her right (our left), gentle neutral expression.",
                "Eyes on a ball (most important): the near eye is wide; the far eye is clearly narrower, about 60% of the near eye's width, and sits close to the center line of the face; the far eyebrow is also shorter. Light from the upper left."),
                "d2_sia_threequarter", "예상 결과 — 고개를 돌린 시아. 안쪽 눈이 앞쪽 눈의 60% 안팎으로 좁고, 안쪽 눈썹도 짧음", "2/3")],
      check=[("안쪽 눈 ÷ 앞쪽 눈이 0.5~0.7인가", "#s3"), ("안쪽 눈썹도 짧게 줄었나", "#s3"), ("눈동자가 얼굴과 같은 방향을 보나", "#s3")],
      expect="자연스럽게 고개를 돌린 시아가 나옵니다. 안쪽 눈은 콧대 쪽으로 좁게 붙고, 앞쪽 눈은 넓습니다. 재 보면 안쪽 눈이 앞쪽 눈의 절반을 조금 넘는 정도입니다.",
      trouble=[("두 눈이 같은 너비다", "새 대화에서 'the far eye clearly narrower'를 'the far eye only half as wide as the near eye'로 바꿔 과장합니다."),
               ("안쪽 눈이 콧대에 가려 사라졌다", "고개 각도를 'about 20 degrees'로 줄입니다."),
               ("눈동자가 정면만 본다", "'looking in the same direction as the face'를 덧붙입니다.")],
      more="고개 각도를 15°와 45°로 바꿔 두 장을 더 만들고, 안쪽 눈 비율이 78%·36%에 가까워지는지 보세요."),
],
2: [
 dict(id="d1", title="칠하기 순서를 문장으로", goal="2부의 칠하기 순서(흰자 색 → 위 그림자 → 아래 빛 → 하이라이트 → 갈색 선)를 다섯 조각의 문장으로 적어 하루의 눈을 만듭니다.",
      why="'beautiful sparkling eyes'만 쓰면 흰자가 순백이고 눈동자가 한 색인 스티커 눈이 자주 나옵니다(6부 f7). 칠하기를 순서대로 적으면 레이어로 칠한 듯한 눈이 나옵니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 눈 클로즈업 한 장을 만듭니다.",
             "받은 그림의 흰자에서 색을 뽑아(스포이트) 순백(255, 255, 255)이 아닌지 봅니다.", "눈동자 위·아래의 밝기를 비교하고, 하이라이트 개수를 셉니다."],
      prompts=[("넣을 프롬프트", P("16:9", "Close-up of the face of " + who("haru") + ", front view, from the eyebrows to the chin, gentle smile.",
                "Eye painting (most important): 1) off-white sclera slightly warmer than pure white with a soft shadow under the upper eyelid; 2) the upper part of each blue iris darker; 3) a subtle warm glow on the lower part of the iris while the iris stays blue; 4) one large and one small highlight in each eye; 5) line art around the light areas tinted brown, not pure black. Light from the upper left."),
                "d3_haru_eye_layers", "예상 결과 — 다섯 조각으로 칠한 하루의 눈. 흰자는 옅은 미색, 눈동자 위는 어둡고 아래는 밝으며 하이라이트 두 개", "16/9")],
      check=[("흰자가 순백이 아닌가(스포이트로 확인)", "#s1"), ("눈동자 위는 어둡고 아래는 밝은가", "#s2"), ("눈 색이 여전히 파란가", "#s2")],
      expect="얼굴에 녹아든 부드러운 눈이 나옵니다. 흰자는 하얗게 보이지만 스포이트로 찍으면 약간 미색이고, 파란 눈동자는 위가 짙고 아래로 갈수록 맑게 밝아집니다.",
      trouble=[("아래쪽 빛이 너무 세서 눈이 주황이다", "'subtle warm glow, the iris stays blue'를 'very subtle'로 바꾸고, 'blue irises' 를 맨 앞에 한 번 더 적습니다."),
               ("흰자가 여전히 새하얗다", "'not pure white'를 덧붙이고 'cream-tinted sclera'로 바꿔 봅니다."),
               ("하이라이트가 하나뿐이다", "'exactly two highlights per eye, one large and one small'로 개수를 숫자로 적습니다.")],
      more="1번 조각(흰자 색)만 빼고 새 대화에서 다시 만들어, 흰자 색 하나가 얼마나 차이를 내는지 비교해 보세요."),
 dict(id="d2", title="같은 화, 다른 세기", goal="2부 3단계의 원리(눈썹 방향 = 종류, 눈 뜬 정도 = 세기)대로, 눈썹은 같게 두고 눈 뜬 정도만 바꿔 하루의 '참는 화'와 '터진 화'를 따로 만듭니다.",
      why="'angry'만 쓰면 도구가 세기를 마음대로 정합니다. 눈썹은 같은 문장으로, 눈 뜬 정도만 다르게 적으면 세기만 바뀐 두 그림이 나옵니다. " + LESSON,
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화 A를 열고 참고 그림을 첨부해 프롬프트 ①을 넣습니다.", "새 대화 B를 열고 같은 참고 그림을 첨부해 프롬프트 ②를 넣습니다.",
             "두 그림을 나란히 놓고, 눈썹 모양이 비슷하고 눈 뜬 정도만 다른지 봅니다.", "어느 쪽이 '꾹 참는' 얼굴인지, 어느 쪽이 '폭발한' 얼굴인지 다른 사람에게 물어봅니다."],
      prompts=[("① 새 대화 A — 참는 화", P("2:3", "Front view, chest-up portrait of " + who("haru") + ", restrained anger.",
                "Expression (most important): eyebrows raised at the outer ends and pulled together at the inner ends; eyes NARROWED to about half open; mouth firmly closed. A quiet, held-in anger. Light from the upper left."),
                "d4_haru_anger_low", "예상 결과 ① — 눈썹 끝을 올리고 눈을 가늘게 뜬 하루. 화를 꾹 참는 얼굴", "2/3"),
               ("② 새 대화 B — 터진 화", P("2:3", "Front view, chest-up portrait of " + who("haru") + ", explosive anger.",
                "Expression (most important): eyebrows raised at the outer ends and pulled together at the inner ends, the same eyebrow shape as a restrained anger; eyes OPENED VERY WIDE, whites visible around the irises; mouth open shouting. Light from the upper left."),
                "d4_haru_anger_high", "예상 결과 ② — 같은 눈썹에 눈을 크게 뜨고 입을 벌린 하루. 화가 터진 얼굴", "2/3")],
      check=[("두 그림 모두 눈썹 끝이 올라갔나", "#s3"), ("①은 눈이 가늘고, ②는 크게 떴나", "#s3"), ("두 그림 모두 20대 성인으로 보이나", "06_failure_lab.html#drift")],
      expect="두 장 모두 화난 하루지만, ①은 차갑게 참는 얼굴, ②는 폭발한 얼굴로 읽힙니다. 눈썹 모양은 거의 같고 눈 뜬 정도와 입만 다릅니다.",
      trouble=[("①도 크게 화낸다", "'mouth firmly closed, calm posture'를 덧붙이고, 'eyes narrowed to about half open'을 맨 앞으로 옮깁니다."),
               ("②가 놀란 얼굴이 됐다", "놀람은 눈썹이 올라갑니다. 'eyebrows pulled DOWN at the inner ends'를 분명히 적습니다."),
               ("두 그림의 머리 모양이 다르다", "참고 그림을 두 대화 모두에 첨부했는지 확인합니다.")],
      more="같은 방법으로 슬픔을 만들어 보세요. 슬픔은 반대로 눈을 크게 뜨면 참는 쪽, 가늘게 뜨면 북받친 쪽입니다."),
],
3: [
 dict(id="d1", title="코를 눈에 맞추기", goal="3부 1단계의 정보량 원리대로, 눈의 그려 넣은 양에 맞춰 코를 '코끝 + 짧은 콧날'로 적어 모아의 정면 얼굴을 만듭니다.",
      why="코에 대해 아무것도 적지 않으면 도구가 코를 콧구멍까지 진하게 그리거나 아예 지우는 일이 있습니다(6부 f6). 코의 표현을 눈과 같은 수준으로 적으면 얼굴이 한 화풍으로 나옵니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림의 눈·코·입을 1부터 5까지 정보량으로 점수 매깁니다(3부 1단계 실험의 단계 참고).", "가장 높은 점수와 가장 낮은 점수의 차이가 1 이내인지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Front view, chest-up portrait of " + who("moa") + ", gentle smile, looking at the viewer.",
                "Level of detail (most important): anime eyes with a few soft lash strands and two highlights; the nose shown only as a small tip with a short faint bridge line, no nostrils; a simple mouth with a hint of the lower lip; the same level of detail on the eyes, nose and mouth. Light from the upper left."),
                "d5_moa_nose_match", "예상 결과 — 눈·코·입의 그려 넣은 양이 같은 모아. 코는 작은 코끝과 짧은 콧날만", "2/3")],
      check=[("코에 콧구멍이 없고 코끝·짧은 콧날 정도인가", "#s1"), ("눈·코·입 정보량 차이가 1 이내인가", "#s1"), ("얼굴이 하나의 화풍으로 읽히나", "05_ai_detail.html#s1")],
      expect="코가 얼굴에서 튀지 않는 평범한 애니풍 정면 얼굴이 나옵니다. 코는 거의 눈에 띄지 않지만, 짧은 선 하나로 코끝 자리가 분명합니다.",
      trouble=[("코가 아예 없다", "'small nose tip clearly visible'을 덧붙입니다."),
               ("콧구멍이 나왔다", "'no nostrils'를 맨 앞으로 옮기고 'nose as a tiny tip only'로 바꿉니다."),
               ("눈이 반실사처럼 자세하다", "'a few soft lash strands'를 'simple lashes'로 바꿔 눈도 낮춥니다.")],
      more="같은 문장에서 코만 'clearly drawn nose bridge and nostrils'로 바꿔 새 대화에서 만들고, 코가 얼마나 튀는지 비교해 보세요."),
 dict(id="d2", title="웃는 입의 이줄을 문장으로", goal="3부 3·4단계의 원리(위 이 一, 아래 이 U, 어금니는 안쪽으로)를 문장으로 적어 비스듬히 웃는 박사를 만듭니다.",
      why="크게 웃는 얼굴은 입속이 넓게 보여 실수가 잘 드러납니다. 이줄의 모양과 방향을 적지 않으면 위·아래 이가 같은 가로줄이 되거나 어금니가 정면을 봅니다(6부 f4).",
      attach="refs/doctor_sheet.png",
      steps=["새 대화를 열고 박사 설정 시트를 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림의 입속에서 위 이줄이 가로 일자인지, 아래 이줄이 둥근 U인지 봅니다.", "보이는 어금니의 줄을 연필로 길게 늘여, 위·아래 줄이 입 안쪽 한 점으로 모이는지 확인합니다."],
      prompts=[("넣을 프롬프트", P("16:9", "Three-quarter view chest-up portrait of " + who("doctor") + ", laughing heartily with his mouth wide open, head turned slightly to his left.",
                "Inside the mouth (most important): the upper teeth appear as a nearly straight horizontal row; the lower teeth curve as a U seen slightly from above; the back teeth recede inward toward the jaw hinge, never facing the viewer; the upper front teeth a little larger than the lower ones; tongue visible. Adult male. Light from the upper left."),
                "d6_doctor_teeth", "예상 결과 — 비스듬히 크게 웃는 박사. 위 이는 일자, 아래 이는 U자, 어금니는 안쪽으로 모임", "16/9")],
      check=[("위 이줄이 거의 가로 일자인가", "#s3"), ("아래 이줄이 둥근 U인가", "#s3"), ("늘인 어금니 줄이 안쪽 한 점으로 모이나", "#s4")],
      expect="시원하게 웃는 박사가 나옵니다. 입속은 깊어 보이고, 위 이는 윗입술 아래 일자로, 아래 이는 둥글게 보입니다. 안쪽 어금니는 작고 어둡게 보입니다.",
      trouble=[("아래 이도 일자다", "'the lower teeth curve as a U'를 'the lower teeth form a clear U-shaped arch'로 과장합니다."),
               ("이가 하나하나 너무 진하다", "'teeth as simple white shapes, no outlines between each tooth'를 덧붙입니다."),
               ("안경이 바뀌었다", "'keep the teal rectangular glasses exactly as in the reference'를 덧붙입니다.")],
      more="같은 문장에서 각도를 'front view'로 바꿔, 정면에서는 어금니가 어떻게 보이는지 비교해 보세요."),
],
4: [
 dict(id="d1", title="머리를 덩어리로 세우기", goal="4부 1·2단계의 원리(머리 밑그림보다 크게, 덩어리 네다섯 개)를 문장으로 적어 모아의 머리를 만들고, 받은 그림 위에 덩어리 경계를 그려 봅니다.",
      why="머리카락에 대해 아무것도 적지 않으면 가는 선만 빽빽하거나 두피에 붙은 머리가 나오기 쉽습니다(6부 f5). 부피와 덩어리 수를 적으면 머리가 입체로 섭니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림을 그림판에서 열고, 머리카락 위에 큰 덩어리 경계를 색연필 선으로 나눠 봅니다.", "덩어리가 네다섯 개로 나뉘는지, 머리 바깥선이 두개골보다 한 둘레 큰지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Front view, chest-up portrait of " + who("moa") + ", soft smile.",
                "Hair (most important): natural volume, the hair silhouette clearly larger than the skull; the hair grouped into four or five big clear clumps (bangs, two side clumps, back) with a few finer strands; the hair grows from the whole hairline and the part line, not from one point. Keep the white frilled headband and the ribbon over her LEFT ear. Light from the upper left."),
                "d7_moa_hair_blocks", "예상 결과 — 머리가 두개골보다 한 둘레 크고, 큰 덩어리 네다섯 개로 나뉜 모아", "2/3")],
      check=[("머리 바깥선이 두개골보다 한 둘레 큰가", "#s1"), ("덩어리 네다섯 개로 나뉘나", "#s2"), ("머리선·가르마에서 흘러내리나", "#s3")],
      expect="머리 모양이 또렷한 모아가 나옵니다. 앞머리·양옆·뒤 덩어리가 분명하고, 그 사이에 가는 가닥 몇 개가 섞입니다. 얼굴은 알맞은 크기로 보입니다.",
      trouble=[("머리가 너무 부풀었다", "'slightly larger than the skull'로 'clearly'를 'slightly'로 바꿉니다."),
               ("가는 선만 빽빽하다", "'four or five big clear clumps'를 맨 앞으로 옮기고 'fewer fine strands'를 덧붙입니다."),
               ("머리띠가 사라졌다", "'keep the white frilled headband'를 프롬프트 맨 앞에 다시 적습니다.")],
      more="같은 문장에서 덩어리 수를 'two or three'와 'seven or eight'로 바꿔 두 장을 더 만들고, 얼굴과 어울리는 덩어리 수를 비교해 보세요."),
 dict(id="d2", title="바람이 닿는 한 점 정하기", goal="4부 3·4단계의 원리(바람이 닿는 한 점에서 퍼짐, 다발 굵기 섞기)를 문장으로 적어 바람에 날리는 시아의 긴 흑발을 만듭니다.",
      why="'hair blowing in the wind'만 쓰면 모든 다발이 같은 방향·같은 굵기로 휘어 빗질한 무늬처럼 됩니다. 바람이 닿는 점과 굵기 섞기를 적으면 흐름이 살아납니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림에서 머리 다발마다 흐르는 방향으로 화살표를 그려 봅니다.", "화살표들이 정수리 근처 한 점에서 퍼져 나가는지, 굵고 가는 다발이 섞였는지 봅니다."],
      prompts=[("넣을 프롬프트", P("16:9", "Side view chest-up portrait facing LEFT of " + who("sia") + ", a strong wind blowing from the left side of the image.",
                "Hair in the wind (most important): her long black hair streams to the right, spreading from one point near the top of her head where the wind hits; hair clumps of varied thickness, thick and thin mixed; long clumps wave, showing both their front and back sides; a few loose single strands. Light from the upper left."),
                "d8_sia_wind_point", "예상 결과 — 왼쪽에서 바람을 맞은 시아. 정수리 근처 한 점에서 머리가 퍼지고, 굵고 가는 다발이 섞여 물결침", "16/9")],
      check=[("다발이 한 점에서 퍼져 나가나", "#s3"), ("굵고 가는 다발이 섞였나", "#s4"), ("다발의 앞면·뒷면이 보이나", "#s4")],
      expect="바람에 머리가 시원하게 날리는 시아가 나옵니다. 머리가 한 방향으로만 빗기지 않고 정수리에서 부채처럼 퍼지며, 굵은 다발 사이로 가는 가닥이 흩날립니다.",
      trouble=[("시아가 오른쪽을 본다", "'her nose points toward the LEFT edge; the back of her head is on the RIGHT side'처럼 화면 위치로 적습니다(03 얼굴 편의 실제 경험)."),
               ("다발이 모두 같은 굵기다", "'very different clump thicknesses'로 과장합니다."),
               ("머리가 얼굴을 다 가린다", "'the wind blows the hair away from her face'를 덧붙입니다.")],
      more="같은 문장에서 머리 길이만 'short hair'로 바꿔, 짧은 머리는 다발 끝이 튀는지 비교해 보세요."),
],
5: [
 dict(id="d1", title="디테일 문장을 처음부터 조립하기", goal="5부 1·2단계의 디테일 문장(부위별 정보량)과 칠하기 문장을 함께 넣어 하루의 정면 얼굴을 만듭니다. 7부 문장 공방에서 조립한 문장과 같은 꼴입니다.",
      why="부위별 정보량과 칠하기를 따로 적으면 '아주 자세하게' 한 마디보다 결과가 덜 흔들립니다. 여러 장을 만들 때 기준 문장이 됩니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림의 눈·코·입·머리에 1~5 정보량 점수를 매기고 차이가 1 이내인지 봅니다.", "눈의 흰자 색·위 그림자·아래 빛·하이라이트 수를 점검합니다. 이 그림은 다음 과제(d2)의 바탕 그림이 됩니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Front view, chest-up portrait of " + who("haru") + ", gentle smile, looking at the viewer.",
                "Detail sentence: anime eyes with soft lashes and two highlights; nose as a small tip with a short bridge line; simple mouth with a hint of lips; hair in four or five clumps with a few strands; consistent level of detail across the face.\nPainting sentence: off-white sclera; darker upper iris under the eyelid; subtle warm glow on the lower iris, the iris stays blue; line art around light areas tinted brown. Light from the upper left."),
                "d9_haru_detail_sentence", "예상 결과 — 디테일 문장과 칠하기 문장으로 만든 하루. 눈·코·입·머리의 그려 넣은 양이 고르고 눈이 얼굴에 녹아듦", "2/3")],
      check=[("눈·코·입·머리 정보량 차이가 1 이내인가", "#s1"), ("흰자가 순백이 아니고 눈동자에 위 그림자·아래 빛이 있나", "#s2"), ("번 두 개와 앞머리 남색 줄이 그대로인가", None)],
      expect="깔끔하고 고른 애니풍 하루가 나옵니다. 어느 한 곳이 튀지 않고, 눈은 맑게 빛나지만 얼굴에서 떠 보이지 않습니다.",
      trouble=[("눈만 반실사처럼 자세하다", "'soft lashes'를 'simple lashes'로 낮추고 'consistent level of detail'을 맨 앞으로 옮깁니다."),
               ("번이 하나로 합쳐졌다", "'two separate round hair buns on top, as in the reference'를 맨 앞에 적습니다."),
               ("눈 색이 보라색이 됐다", "'big blue eyes'를 칠하기 문장 앞에 한 번 더 적습니다.")],
      more="정보량을 모두 한 단계씩 올린 문장으로 새 대화에서 만들어, 같은 캐릭터의 반실사 판을 만들어 보세요(5부 4단계)."),
 dict(id="d2", title="눈만 부분 수정하기", goal="5부 3단계의 가림 영역 원리대로, d1 결과에서 두 눈만 칠해 '처진 눈'으로 바꾸고 나머지가 그대로인지 봅니다.",
      why="얼굴 전체를 다시 만들면 머리 모양까지 바뀝니다. 고칠 부위만 가리면 다시 그려지는 몫이 그림의 몇 %로 줄어, 나머지는 지켜집니다. 03 얼굴 편에서는 작은 변화가 부분 수정으로 잘 반영되지 않았으니, 바뀌는 모습을 분명하게 적습니다.",
      attach="d1 결과 그림(d9_haru_detail_sentence)",
      steps=["d1 결과 그림을 도구의 부분 수정(영역 칠하기) 기능으로 엽니다.", "두 눈과 두 눈썹을 칠합니다. 눈 바깥으로 여유를 조금(눈 너비의 10~20%) 두고, 앞머리·코는 빼고 칠합니다.",
             "프롬프트를 넣어 칠한 곳만 다시 그립니다.", "고친 그림과 d1 그림을 나란히 놓고, 눈 말고 다른 곳이 바뀌지 않았는지 봅니다."],
      prompts=[("넣을 프롬프트(부분 수정)", "Inside the painted area only: redraw both eyes as gentle droopy eyes — the outer corners clearly LOWER than the inner corners — with relaxed eyebrows. Keep the blue iris color, the eye size, the two highlights and the off-white sclera. Do not change anything outside the painted area. All characters are adults. No text, no letters, no numbers, no logos.",
                "d10_haru_eye_fix", "예상 결과 — 눈과 눈썹만 다시 그려 처진 눈이 된 하루. 머리·코·입·옷은 d1과 같음", "2/3")],
      check=[("눈꼬리가 눈머리보다 낮아졌나", "01_eye_shape.html#s1"), ("눈 색·하이라이트·흰자 색이 그대로인가", "#s2"), ("눈 밖(머리·코·입·옷)은 그대로인가", "#s3")],
      expect="같은 하루인데 눈매만 순해진 그림이 나옵니다. 칠한 곳 경계에 이음매가 거의 보이지 않고, 번과 앞머리 줄은 그대로입니다.",
      trouble=[("눈이 바뀌지 않았다", "칠한 영역을 눈 바깥으로 조금 더 넓히고, 'clearly LOWER'를 'much lower'로 과장합니다. 그래도 안 되면 새 대화에서 d1 문장에 처진 눈 조각을 넣어 처음부터 만듭니다."),
               ("눈썹 위 앞머리가 바뀌었다", "앞머리를 칠하지 않았는지 확인하고, 눈썹 바로 위까지만 칠합니다."),
               ("경계에 얼룩이 보인다", "여유를 10~20%로 넓혀 다시 칠합니다.")],
      more="같은 방법으로 입만 칠해 '반쯤 연 입'으로 바꿔 보고, 2부 4단계 실험의 읽힘과 비교해 보세요."),
],
6: [
 dict(id="d1", title="실패를 찾아 한 줄로 고치기", goal="6부의 진단 순서로 f8(어긋난 눈썹)이 ⑤ 표정에서 처음 걸리는 것을 확인하고, 고치는 조각 한 줄만 넣어 새로 만듭니다.",
      why="원인을 모른 채 다시 만들면 같은 실패가 다른 모양으로 나옵니다. 처음 걸린 항목의 조각만 더하면 무엇이 고쳤는지 분명합니다. 03 얼굴 편에서는 바로잡을 실패 그림을 첨부하면 실패를 따라 그렸으니, f8 그림은 첨부하지 않습니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png (f8 그림은 첨부하지 않음)",
      steps=["6부 1단계 실험에서 f8을 골라 점검표를 위에서부터 눌러, ⑤에서 처음 걸리는지 확인합니다.", "새 대화를 열고 참고 그림만 첨부합니다.",
             "프롬프트를 넣어 만듭니다. 고치는 조각(눈썹 문장)이 들어 있습니다.", "f8과 나란히 놓고, 눈썹만 달라졌는데 기쁨으로 읽히는지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Front view, chest-up portrait of " + who("moa") + ", a relaxed happy smile.",
                "Fix (most important): soft gently arched eyebrows, NOT raised at the outer ends; relaxed eyes; a warm happy expression. Light from the upper left."),
                "d11_moa_brow_fix", "예상 결과 — 눈썹을 완만한 산 모양으로 고친 모아. 같은 웃는 입인데 기쁨으로 읽힘", "2/3")],
      check=[("눈썹 끝이 올라가지 않고 완만한 산 모양인가", "02_eye_paint.html#s3"), ("f8과 나란히 두었을 때 기쁨으로 읽히나", "#f8"), ("머리띠·왼쪽 리본이 그대로인가", None)],
      expect="편안하게 웃는 모아가 나옵니다. f8과 같은 웃는 입이지만, 눈썹이 완만해 화나 보이지 않고 따뜻해 보입니다.",
      trouble=[("눈썹이 여전히 올라갔다", "'eyebrows lower at the outer ends than at the middle'처럼 위치를 비교로 적습니다."),
               ("표정이 너무 크다", "'gentle closed-mouth smile'로 입을 줄입니다."),
               ("어려 보인다", "아래 d2를 참고해 'an adult in her late twenties'를 맨 앞에 넣습니다.")],
      more="f1~f7 가운데 하나를 골라, 처음 걸린 항목의 조각만 넣어 같은 방법으로 고쳐 보세요."),
 dict(id="d2", title="반짝이는 큰 웃음, 그래도 성인", goal="6부 '나이 쏠림'을 막는 다섯 가지 방법을 문장으로 넣어, 반짝이는 눈과 큰 웃음을 쓰면서도 20대 성인으로 보이는 시아를 만듭니다.",
      why="반짝이는 큰 눈과 크게 벌린 웃음은 나이가 어려 보이는 쪽으로 쏠리는 신호입니다. 성인 나이와 비율을 숫자로 적고, 다른 신호(홍조·높이 묶은 머리)를 빼면 쏠림을 막을 수 있습니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "프롬프트를 넣어 한 장을 만듭니다.",
             "받은 그림이 20대 성인으로 보이는지 다른 사람에게 물어봅니다.", "어려 보이면 쓰지 않고, 'trouble'의 방법으로 다시 만듭니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Front view, chest-up portrait of " + who("sia") + ", an adult woman in her late twenties, laughing brightly.",
                "Age guard (most important): adult proportions, adult neck and shoulders, a slim oval face; bright sparkling eyes and a wide open laughing mouth, but no blush stickers, no pigtails, hair down as in the reference. Light from the upper left."),
                "d12_sia_adult_smile", "예상 결과 — 반짝이는 눈으로 크게 웃지만 20대 성인으로 보이는 시아. 갸름한 얼굴과 성인 목·어깨", "2/3")],
      check=[("20대 성인으로 보이나", "#drift"), ("눈은 반짝이고 입은 크게 웃나", "02_eye_paint.html#s4"), ("홍조 스티커·높이 묶은 머리가 없나", "#drift")],
      expect="환하게 웃는 시아가 나옵니다. 눈이 반짝이고 입이 크게 벌어져 있지만, 갸름한 얼굴선과 성인 목·어깨 덕분에 20대로 읽힙니다.",
      trouble=[("어려 보인다", "쓰지 않고 다시 만듭니다. 'laughing brightly'를 'smiling brightly'로 줄이고, 'eyes not oversized'를 덧붙입니다."),
               ("표정이 굳었다", "'natural joyful expression'을 덧붙입니다."),
               ("귀걸이가 사라졌다", "'small silver earrings as in the reference'를 덧붙입니다.")],
      more="같은 문장에서 'Age guard' 줄만 지우고 새 대화에서 만들어, 쏠림이 생기는지 비교해 보세요. 어려 보이는 결과는 공유하지 말고 지웁니다."),
],
}
RETRY = {}
BASE_OF = {}
RETRY3 = {}

CONV_D = [("D01_part1", "1부 연습 과제", "refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png", ["d1_moa_up", "d1_moa_down", "d2_sia_threequarter"]),
          ("D02_part2", "2부 연습 과제", "refs/haru_anime_base.png, refs/haru_sheet.png", ["d3_haru_eye_layers", "d4_haru_anger_low", "d4_haru_anger_high"]),
          ("D03_part3_4", "3·4부 연습 과제", "refs/moa_anime_base.png, refs/moa_sheet.png, refs/doctor_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png", ["d5_moa_nose_match", "d6_doctor_teeth", "d7_moa_hair_blocks", "d8_sia_wind_point"]),
          ("D04_part5_6", "5·6부 연습 과제", "refs/haru_anime_base.png, refs/haru_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png", ["d9_haru_detail_sentence", "d10_haru_eye_fix", "d11_moa_brow_fix", "d12_sia_adult_smile"])]
HOW = {"d1_moa_down": "d1_moa_up과 다른 새 대화에서", "d4_haru_anger_high": "d4_haru_anger_low와 다른 새 대화에서",
       "d10_haru_eye_fix": "d9_haru_detail_sentence 결과에서 '부분 수정(영역 칠하기)' — 두 눈과 두 눈썹만, 눈 바깥으로 10~20% 여유, 앞머리·코는 빼기",
       "d11_moa_brow_fix": "새 대화에서(f8 그림은 첨부하지 않음)"}

def items():
    out = {}
    for no, ds in DRILL.items():
        for d in ds:
            for lab, prompt, key, alt, ar in d["prompts"]:
                out[key] = (no, d["title"], lab, prompt, alt, ar)
    return out

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    D = os.path.join(ROOT, "docs", "image_requests_drill"); os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    IT = items(); rows = []; n = 0
    HEAD = ("해설 페이지의 '프롬프트 연습 과제' 예상 결과 그림을 한 장씩 차례로 만들어 줘.\n- 비율은 각 프롬프트 첫 줄을 따를 것(16:9는 가로 1920px 이상, 2:3은 세로 1536px 이상)\n"
            "- 첨부한 참고 이미지의 캐릭터 외형(얼굴·머리·색·장식)을 똑같이 지킬 것\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·과장된 체형·교복 느낌·어려 보이는 얼굴 금지\n"
            "- 그림 안에 글자·숫자·로고 금지\n- 'most important'로 적힌 부분을 가장 먼저, 분명하게 지킬 것\n- '다른 새 대화에서'라고 적힌 그림은 새 대화를 열어 따로 만들 것")
    for cid, title, att, keys in CONV_D:
        md = f"# {cid[:3]} · {title} — " + ", ".join(keys) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD}\n```\n"
        for k in keys:
            no, dt, lab, prompt, alt, ar = IT[k]; n += 1
            how = HOW.get(k, "새로 만들기")
            rows.append([n, cid[:3], k, f"0{no}", dt, lab, ar.replace("/", ":"), how, ""])
            md += f"\n---\n## {k} — {no}부 「{dt}」 {lab}\n방법: {how}\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "part", "drill", "prompt", "ratio", "how", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 3 — '프롬프트 연습 과제' 예상 결과 ({n}장)

부마다 연습 과제 2개(모두 12개)의 **예상 결과 그림**입니다. 페이지의 과제 프롬프트와 이 요청문의 프롬프트는 같습니다(원본: `build/content_drill.py`).

## 요청 순서
| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
""" + "".join(f"| {i+1} | prompts/{c[0]}.md | {len(c[3])} | {c[2]} |\n" for i, c in enumerate(CONV_D)) + """
## 03 얼굴 편에서 배운 것을 처음부터 반영
- 짝 그림(d1 ①·②, d4 ①·②)은 **서로 다른 새 대화**에서 만듭니다(같은 대화면 둘째 그림이 첫째를 따라 그림).
- 바뀌는 곳은 **'most important'로 표시하고 과장**해 적었습니다.
- d10_haru_eye_fix는 그림 생성이 아니라 **부분 수정(영역 칠하기)** 기능으로 만듭니다. 바탕은 d9 결과입니다.
- d11은 실패 그림 f8을 **첨부하지 않고** 새 대화에서 만듭니다.
- d12가 어려 보이게 나오면 쓰지 않고 다시 만듭니다.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png·jpg).
""")
    print("drill images", n)
