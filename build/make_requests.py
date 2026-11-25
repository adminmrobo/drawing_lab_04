# -*- coding: utf-8 -*-
"""Genspark 그림 요청 꾸러미(docs/image_requests) 생성. python3 build/make_requests.py
페이지의 '프롬프트로 직접 만들어 보기' A 프롬프트도 여기서 가져간다(이 파일이 원본)."""
import os, csv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests")
PIX = "Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2–3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.\nMatch the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.\nBright daytime laboratory mood, soft natural sunlight through large windows, clean white walls, light lavender, mint and pink accents."
ANI = "Art style: high-quality anime illustration, clean confident lineart, two-tone cel shading, natural adult proportions.\nMatch the attached reference images exactly (face, hair, colors, accessories). All characters are adults in their twenties (the Professor is an adult man in his thirties); modest outfits exactly as described."
END = "No text, no letters, no numbers, no logos, no watermark, no revealing clothing, not childlike, no school uniform, not resembling any famous anime character."
ENDC = "No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands."
SAFE = "Composition: every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); bottom-left corner plain and bright."
CH = {
 "haru": "Haru (adult lab assistant, long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top, small ahoge, big blue eyes)",
 "sia": "Sia (adult maid intern, long straight jet-black hair, no headdress, gray eyes, small silver earrings)",
 "moa": "Moa (adult maid intern, long ash-beige wavy hair, white frilled maid headband with a white ribbon over her LEFT ear, amber eyes)",
 "doctor": "the Professor (adult male scientist in his thirties, dark charcoal spiky hair with a white streak at the front, very thick black eyebrows, teal rectangular glasses)",
 "fly": "the Fruit Fly researcher (tiny cartoon fruit fly, large red compound eyes, retro dark blue helmet with a yellow-white stripe, colorful dangling cables, tiny white lab coat, translucent wings)",
 "bot": "AbaBot (boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, small tank treads)",
 "judges": "three small cute dark navy silhouette judges with white dot eyes (one with a pink side-ponytail bow, one with a beret and teal round glasses, one with a cat-ear hood and yellow pompoms) holding blank score paddles",
}
OUT = {"haru": "lavender hoodie with white drawstrings over a white t-shirt, open white knee-length lab coat",
       "sia": "charcoal-black long-sleeved maid dress, large gray bow at the collar, long white frilled apron",
       "moa": "camel knit cardigan over a white blouse, red and navy plaid bow tie, white frilled apron",
       "doctor": "white lab coat over a black vest, white shirt and black tie"}
def who(k, outfit=None): return CH[k] + ", wearing " + (outfit or OUT[k])
def cover(file, page, part, alt, scene, chars, meta, mood):
    p = f"Website top cover illustration, wide 16:9.\n{PIX}\nScene: {scene}\nCharacters:\n  " + ";\n  ".join(chars) + f".\nVisual metaphor: {meta}\n{SAFE}\nMood: {mood}\n{ENDC}"
    return (file, page, part, alt, p, "pixel")
def body(file, page, part, alt, ratio, scene, extra=""):
    p = ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\n{ANI}\n{scene}\n" + (extra + "\n" if extra else "") + "Plain off-white studio background.\n" + END)
    return (file, page, part, alt, p, "anime")
C1 = [
 cover("cover_index", "index.html", "목차", "낮의 연구실 작업실에서 하루·시아·모아·박사가 큰 돋보기 앞에 모이고, 초파리와 주판봇이 이젤 앞에서 눈·입·머리카락을 확대해 그리며, 평가단이 뒤에 앉은 장면",
   "a bright laboratory art studio with a giant standing magnifying glass, two easels seen from the back, a small table with color swatches and fine brushes.",
   [who("haru") + ", in the center smiling, looking through the giant magnifying glass", who("sia") + ", on the left touching her small silver earring", who("moa") + ", on the right holding a big hexagon-shaped card", who("doctor") + ", at the back center with a clipboard",
    CH["fly"] + ", on the left facing right at the left easel painting one large eye", CH["bot"] + ", on the right facing left at the right easel painting many hair strands", CH["judges"] + " sitting at a small table in the back right"],
   "one giant eye seen through a magnifying glass, built on a hexagon.", "cheerful, curious, the moment before a close-up session."),
 cover("cover_01", "01_eye_shape.html", "1부 눈의 모양", "모아가 큰 육각형 판을 눈 옆에 대고, 초파리가 판 꼭짓점에 점을 찍는 장면",
   "a mirror corner in the lab studio with a tall standing mirror and a large transparent hexagon card.",
   [who("moa") + ", in the center facing the viewer, holding a large transparent hexagon card beside her eye", CH["fly"] + ", on the left facing right, marking two corners of the hexagon with a teal marker", CH["bot"] + ", on the right facing left, drawing two big circles with many eyelashes on its canvas", who("doctor") + ", at the back nodding"],
   "a hexagon with two corners marked, and a ball-shaped eye model on the table.", "calm, focused."),
 cover("cover_02", "02_eye_paint.html", "2부 눈 칠하기와 표정", "하루가 큰 눈 그림에 붓으로 빛을 얹고, 초파리가 색 견본을 들고 있으며, 뒤 벽에 표정 그림 여섯 장이 걸린 장면",
   "a color workbench in the lab with a large canvas of a single anime eye, glass jars of paint, color swatch cards, six small expression sketches pinned on the wall behind (no text).",
   [who("haru") + ", in the center facing the viewer, painting a warm glow on the lower part of the big eye with a brush", CH["fly"] + ", on the left facing right, holding up an off-white color swatch next to the eye's white", CH["bot"] + ", on the right facing left, holding a can of pure white paint proudly", who("doctor") + ", at the back pointing at the expression sketches"],
   "an eye painted in layers: off-white, shadow on top, glow below.", "warm, bright."),
 cover("cover_03", "03_nose_ear_mouth.html", "3부 코·귀·입", "창가에서 시아가 옆으로 서 있고 초파리가 귀 높이를 재며, 박사가 크게 웃고 있는 장면",
   "a sunny window side of the lab, sheer curtains, a small dental model of teeth on the table.",
   [who("sia") + ", standing in side view facing left", CH["fly"] + ", hovering beside her head holding a yellow measuring tape from her eye level to her nose tip level next to her ear", who("doctor") + ", on the right facing the viewer, laughing with his mouth wide open", CH["bot"] + ", at the front right holding the dental model upside down, puzzled"],
   "an ear between two level lines, and an open mouth showing a straight upper row of teeth.", "calm, airy, a bit funny."),
]
C2 = [
 cover("cover_04", "04_hair.html", "4부 머리카락", "연구실 미용 의자 셋에 하루·시아·모아가 앉고, 초파리가 머리 위에 색깔 덩어리 표시를 띄우는 장면",
   "a hair salon corner set up in the lab: three salon chairs, a big mirror, combs and a hair dryer on a cart.",
   [who("haru") + ", in the left chair, her two hair buns clearly visible", who("sia") + ", in the middle chair, long black hair flowing", who("moa") + ", in the right chair, wavy hair", CH["fly"] + ", hovering above, projecting colorful translucent blocks over their hair to show hair clumps", CH["bot"] + ", at the back trying to count single hair strands with a tiny comb"],
   "hair divided into a few big colorful clumps.", "fun, light."),
 cover("cover_05", "05_ai_detail.html", "5부 AI로 디테일 살리기", "연구실 조종 책상의 큰 모니터에 눈 하나가 크게 떠 있고, 하루가 그 눈 위에 분홍 가림 영역을 칠하며 시아·모아가 바라보는 장면",
   "the lab control desk with a big monitor showing a large anime eye with a pink rectangle highlighted over it, and a second monitor showing four simple level bars (no text).",
   [who("haru") + ", in the center using a stylus on the monitor", who("sia") + ", on the left", who("moa") + ", on the right", CH["bot"] + ", typing at the desk", CH["fly"] + ", hovering near the monitor", who("doctor") + ", at the back"],
   "one part masked, the rest kept.", "focused, hopeful."),
 cover("cover_06", "06_failure_lab.html", "6부 실패 사례 실험실", "검수 책상 위에 어색한 눈·입·머리 그림이 쌓이고, 초파리가 돋보기로 살피며 주판봇이 머리를 긁는 장면",
   "an inspection desk covered with sheets of close-up sketches of eyes, mouths and hair, some with red circles (no readable text), a desk lamp.",
   [CH["fly"] + ", on the left facing right, holding a big magnifying glass over a sketch", CH["bot"] + ", on the right facing left, scratching its head with one arm", CH["judges"] + " at the back holding blank score paddles", who("haru") + ", sorting the sketches into piles"],
   "a pile of near-miss close-ups being sorted from big to small.", "playful, investigative."),
 cover("cover_07", "practice/index.html", "7부 실전 연습장", "연구실 조종 책상에 네 개의 작업대(눈 작업대·표정 조합판·문장 공방·진단 데스크)가 놓이고 모두가 둘러선 장면",
   "the lab control room with four small workstations in a row, each screen showing a simple diagram — an eye on a hexagon, a face with eyebrows, a panel of sliders, a magnifier (no text).",
   [who("haru") + ", in the center at a workstation", who("doctor") + ", on the right with folded arms", CH["fly"] + ", on the left facing right", CH["bot"] + ", next to the fly, raising one arm in excitement", who("sia") + " and " + who("moa") + ", at the back"],
   "four stations, one face in detail.", "energetic, final-stage feeling."),
]
C3 = [
 body("p1_moa_eye_closeup", "01_eye_shape.html", "1부 1단계", "모아의 정면 얼굴 클로즈업 — 두 눈 위에 연한 분홍 육각형 밑그림이 겹쳐 있고, 눈꼬리가 눈머리보다 조금 높은 기본 눈", "16:9",
   "Two panels side by side of the same adult woman's face, front view, close-up from the eyebrows to the chin: LEFT a clean construction sketch — each eye drawn first as a pale pink hexagon, the outer corner slightly higher than the inner corner, the eye shape drawn inside the hexagon; RIGHT the finished close-up of " + who("moa") + " with exactly the same eye shape.",
   "Upper eyelid line thick, lower eyelid line thin, irises amber. Construction lines thin and pale pink. Light from the upper left."),
 body("p1_moa_three_quarter", "01_eye_shape.html", "1부 3단계", "비스듬히 고개를 돌린 모아 — 앞쪽 눈은 넓고, 안쪽 눈은 얼굴 가운데선 쪽으로 좁게 그려진 얼굴", "2:3",
   "Three-quarter view chest-up portrait of " + who("moa") + ", head turned about 30 degrees to her right (our left), gentle smile.",
   "Treat the eyes as sitting on a ball: the near eye is wide, the far eye is clearly narrower (about 60% of the near eye) and closer to the center line of the face; the far eyebrow is also shorter. Light from the upper left."),
 body("p2_haru_eye_paint", "02_eye_paint.html", "2부 2단계", "하루의 눈 클로즈업 채색 — 흰자는 옅은 미색, 파란 눈동자 위쪽은 어둡고 아래쪽은 밝게 빛나며, 하이라이트가 크고 작게 두 개", "16:9",
   "Extreme close-up of the eyes of " + who("haru") + ", front view, from the eyebrows to the nose tip, filling the frame.",
   "Painted in layers: off-white sclera slightly warmer than pure white with a soft shadow under the upper eyelid; blue irises darker on the upper part and with a subtle warm glow on the lower part, the iris color stays blue; one large and one small highlight in each eye; line art around the light areas tinted brown, not pure black."),
 body("p2_haru_expressions", "02_eye_paint.html", "2부 3단계", "하루의 표정 여섯 개 — 위 줄은 조용한 기쁨·참는 화·참는 슬픔, 아래 줄은 들뜬 기쁨·터진 화·북받친 슬픔. 눈썹 방향과 눈 뜬 정도만 다르게 그린 표정 시트", "16:9",
   "Expression sheet of " + who("haru") + ", six head-and-shoulders portraits, front view, in two rows of three, same size. Top row (mild): quiet joy (softly arched eyebrows, eyes narrowed), restrained anger (eyebrows raised at the outer ends, eyes narrowed), restrained sadness (eyebrows lowered at the outer ends, eyes wide open holding back tears). Bottom row (strong): excited joy (softly arched eyebrows, eyes wide open), explosive anger (eyebrows raised at the outer ends, eyes wide open), overflowing sadness (eyebrows lowered at the outer ends, eyes narrowed with tears).",
   "Mouths closed or gently set in all six so that the eyebrows and eye openness carry the emotion. Same person, adult. Light from the upper left."),
 body("p3_sia_profile_ear", "03_nose_ear_mouth.html", "3부 2단계", "왼쪽을 보는 시아의 옆얼굴 — 귀가 눈 높이와 코끝 높이 사이에 있고 작은 은색 귀걸이, 콧날은 짧게 코끝만", "2:3",
   "Side-profile chest-up portrait facing LEFT of " + who("sia") + ", hair tucked behind the ear so the whole ear is visible.",
   "The ear sits between eye level and nose-tip level, a little behind the middle of the head; the outer rim and the inner fold of the ear are drawn as two clear lines; small silver earring on the earlobe. The nose is simple: a short bridge and a small tip. Light from the upper left."),
 body("p3_doctor_laugh", "03_nose_ear_mouth.html", "3부 3·4단계", "비스듬히 서서 크게 웃는 박사 — 위 이는 가로 일자로, 아래 이는 둥근 U자로 보이고, 입속 깊은 곳의 어금니가 안쪽으로 모여 보이는 얼굴", "16:9",
   "Three-quarter view chest-up portrait of " + who("doctor") + ", laughing heartily with his mouth wide open.",
   "Inside the mouth: the upper teeth appear as a nearly straight horizontal row, the lower teeth curve as a U seen slightly from above, the back teeth recede inward toward the jaw hinge (not facing the viewer), the upper front teeth slightly larger than the lower ones, tongue visible. Adult male. Light from the upper left."),
]
C4 = [
 body("p4_hair_three", "04_hair.html", "4부 1단계", "하루·시아·모아 세 사람의 정면 가슴 위 그림 — 하루는 정수리 번 두 개, 시아는 곧은 긴 흑발, 모아는 웨이브. 세 사람 모두 머리카락이 머리보다 한 둘레 크게 부피 있게 그려짐", "16:9",
   "Three front-view chest-up portraits in a row: " + who("haru") + "; " + who("sia") + "; " + who("moa") + ".",
   "Every hairstyle has natural volume, the hair silhouette clearly larger than the skull; hair grows from the whole hairline and the part line, grouped into four or five clear clumps with a few finer strands. Light from the upper left."),
 body("p4_sia_wind", "04_hair.html", "4부 4단계", "바람에 긴 흑발이 날리는 시아의 옆모습 — 바람이 닿는 정수리 근처 한 점에서 머리 다발이 퍼지며, 굵고 가는 다발이 섞이고 몇 가닥이 따로 날림", "16:9",
   "Side view chest-up portrait facing LEFT of " + who("sia") + ", strong wind blowing from the left, her long black hair streaming to the right.",
   "The hair spreads from one point near the top of the head where the wind hits; hair clumps of varied thickness (thick and thin mixed), long clumps waving, both the front and back sides of the twisting clumps visible, a few loose single strands. Light from the upper left."),
 body("p5_haru_sheet", "05_ai_detail.html", "5부 1단계", "하루의 얼굴 설정 시트 — 정면·비스듬히·옆 얼굴 세 개와 기쁨·화·슬픔·놀람 표정 네 개를 한 장에 모은 그림. 모든 얼굴의 눈·코·입·머리 그려 넣은 양이 같음", "16:9",
   "Face design sheet of " + who("haru") + ": top row three head-and-shoulders views (front, three-quarter, side profile facing left) on one level line; bottom row four small expression heads (joy, anger, sadness, surprise).",
   "The same level of detail on eyes, nose, mouth and hair in every head: anime eyes with soft lashes and two highlights, nose as a small tip with a short bridge line, simple mouth, hair in four or five clumps. Same person, adult. Light from the upper left."),
 body("p5_moa_detail_levels", "05_ai_detail.html", "5부 4단계", "같은 모아의 얼굴을 단순한 그림·애니풍·반실사 세 화풍으로 나란히 그린 그림 — 세 얼굴 모두 눈꼬리 기울기와 머리 실루엣은 같고, 코·속눈썹·하이라이트의 그려 넣은 양만 다름", "16:9",
   "Three front-view head-and-shoulders portraits of " + who("moa") + " in a row, in three levels of detail: 1) simple deformed style (nose as a tiny dot, one thick lash line, large highlights, hair as one or two shapes); 2) anime style (small nose tip with a short bridge, a few lash strands, two highlights, hair in four clumps); 3) semi-realistic painting (nose bridge with soft shading, many fine lashes and iris lines, small highlights, hair with fine strands).",
   "Keep the same structure in all three: outer eye corners slightly higher than the inner corners, same hair silhouette, white frilled headband and the ribbon over her LEFT ear. All clearly adult. Light from the upper left."),
]
FAILNOTE = "This is an intentional FAILURE example for a teaching page: draw the mistake described below clearly and convincingly, while everything else stays correct."
def fail(file, alt, scene, mistake):
    p = f"Illustration, vertical 2:3.\n{ANI}\n{FAILNOTE}\n{scene}\nIntentional mistake: {mistake}\nPlain off-white studio background.\n{END}"
    return (file, "06_failure_lab.html", "6부 실패", alt, p, "anime")
C5 = [
 fail("f1_pupil", "왼쪽을 보는 모아 옆얼굴 클로즈업 — 검은 동공이 눈 앞면보다 앞으로 튀어나와 보이는 그림", "Side-profile close-up facing LEFT of " + who("moa") + ", from the forehead to the chin.", "seen from the side, the dark pupil sticks out in front of the eye surface instead of sitting behind the clear cornea, so the eyeball looks like it is bulging out."),
 fail("f2_far_eye", "비스듬히 고개를 돌린 시아 — 안쪽 눈이 앞쪽 눈과 똑같은 너비라 눈만 정면을 보는 듯한 그림", "Three-quarter view chest-up portrait of " + who("sia") + ", head turned about 30 degrees.", "both eyes are drawn exactly the same width as in a front view, the far eye NOT narrowed, so the eyes look pasted on and seem to face the viewer while the head is turned."),
 fail("f3_ear_low", "왼쪽을 보는 박사의 옆얼굴 — 귀가 턱선 가까이 내려와 고개를 숙인 듯 보이는 그림", "Side-profile chest-up portrait facing LEFT of " + who("doctor") + ".", "the ear is placed far too low, down near the jawline below the nose-tip level, so the head looks tilted down."),
 fail("f4_molars", "비스듬히 서서 크게 웃는 하루 — 입속 안쪽 어금니가 이쪽을 향해 서 있어 입속만 정면을 보는 그림", "Three-quarter view chest-up portrait of " + who("haru") + ", laughing with her mouth wide open.", "inside the mouth the back teeth face the viewer flat like front teeth, lined up parallel to the picture instead of receding inward, so the inside of the mouth looks like it faces front while the head is turned."),
]
C6 = [
 fail("f5_flat_hair", "모아의 정면 얼굴 — 머리카락이 두피에 딱 붙어 머리가 작고 얼굴이 유난히 커 보이는 그림", "Front-view chest-up portrait of " + who("moa") + ".", "the hair is drawn flat and tight against the skull with no volume at all, so the head looks small and the face looks unusually large."),
 fail("f6_nose", "하루의 단순한 애니풍 얼굴 — 눈·입은 단순한데 코만 콧구멍과 콧날이 진해 사진처럼 튀는 그림", "Front-view chest-up portrait of " + who("haru") + " in a simple anime style with simple eyes and a simple line mouth.", "only the nose is drawn in a detailed realistic way with dark nostrils, a strongly shaded bridge and nose wings, so the nose stands out like a photo pasted on the simple face."),
 fail("f7_sticker_eyes", "시아의 정면 얼굴 — 흰자가 새하얗고 회색 눈동자가 한 가지 색이라 눈만 오려 붙인 듯 보이는 그림", "Front-view chest-up portrait of " + who("sia") + ".", "the whites of the eyes are pure bright white with hard edges and the gray irises are one flat color with no shadow and no glow, so the eyes look like flat stickers pasted on the face."),
 fail("f8_brow", "웃는 입의 모아 — 눈썹 끝이 올라가 기쁨이 아니라 화가 나거나 꿍꿍이가 있는 듯 보이는 그림", "Front-view chest-up portrait of " + who("moa") + ", meant to be a relaxed happy smile.", "the eyebrows are sharply raised at the outer ends (angry eyebrows) while the mouth smiles, so she looks angry or scheming instead of happy."),
]
CONV = [("C01_covers_A", "표지 A (픽셀아트, 16:9)", "16:9", "refs 전부", C1), ("C02_covers_B", "표지 B (픽셀아트, 16:9)", "16:9", "refs 전부 + C01에서 받은 cover_index", C2),
        ("C03_part1_3", "1·2·3부 눈·칠하기·코귀입", "16:9", "refs/moa_anime_base.png, refs/moa_sheet.png, refs/haru_anime_base.png, refs/sia_anime_base.png, refs/doctor_sheet.png", C3),
        ("C04_part4_5", "4·5부 머리카락·AI", "16:9", "refs/haru_anime_base.png, refs/sia_anime_base.png, refs/moa_anime_base.png", C4),
        ("C05_fail_A", "6부 실패 A", "2:3", "해당 캐릭터의 refs/*_anime_base.png 또는 *_sheet.png", C5), ("C06_fail_B", "6부 실패 B", "2:3", "해당 캐릭터의 refs/*_anime_base.png 또는 *_sheet.png", C6)]
HEAD_PIX = "웹페이지 맨 위에 거는 표지 그림을 한 장씩 차례로 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)\n- 첨부한 참고 이미지의 캐릭터를 같은 외형으로 그릴 것\n- 그림 안에 글자·숫자·로고 금지\n- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게\n아래 영어 프롬프트를 하나씩 써 줘."
HEAD_ANI = "해설 페이지 본문에 넣을 그림을 한 장씩 차례로 만들어 줘.\n- 비율은 각 프롬프트 첫 줄을 따를 것(16:9는 가로 1920px 이상, 2:3은 세로 1536px 이상)\n- 첨부한 참고 이미지의 캐릭터 외형(얼굴·머리·색·장식)을 똑같이 지킬 것\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·과장된 체형·교복 느낌·어려 보이는 얼굴 금지\n- 그림 안에 글자·숫자·로고 금지, 유명 애니 캐릭터와 닮으면 다시 만들 것\n아래 영어 프롬프트를 하나씩 써 줘."
PROMPTS = {it[0]: it for _c in CONV for it in _c[4]}
CONV_OF = {it[0]: _c[0] for _c in CONV for it in _c[4]}
ATTACH_OF = {_c[0]: _c[3] for _c in CONV}

README = """# 그림 요청 꾸러미 — 구조 먼저 그리기 연구실 04 · 디테일 편

저장소: `adminmrobo/drawing_lab_04` (페이지는 완성 — 그림 자리는 '그림 준비 중'으로 비어 있음)
만드는 도구: Genspark 이미지 · 받은 그림은 zip으로 돌려주시면 됩니다(대화 단위로 나눠 여러 번 주셔도 됩니다).

## 1. 그림 규칙
| 항목 | 규칙 |
|---|---|
| 그림체 | **표지 8장은 16비트 픽셀아트**. **본문·실패 그림은 애니풍(5부 화풍 비교만 단순·반실사 포함)** |
| 배경 | 흰색·밝은 낮 분위기 |
| 캐릭터 고정값 | 하루: 정수리 번 2개 + 앞머리 가운데 남색 줄 / 시아: 흑발·머리 장식 없음·작은 은색 귀걸이 / 모아: 흰 프릴 머리띠 + **왼쪽** 귀 위 흰 리본 / 박사: 흰 줄 있는 짙은 머리, 굵은 눈썹, 청록 사각 안경 |
| 나이·노출 | 모두 20대 성인(박사는 30대 성인 남성, 꼬마 체형 아님). **어려 보이는 얼굴·교복 느낌·노출 금지** |
| 글자 | 그림 안에 글자·숫자·로고 금지(연한 분홍·회색 밑그림 선은 허용) |

## 2. 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 그림 수 | 비율 | 첨부 |
|---|---|---|---|---|
| 1 | `prompts/C01_covers_A.md` | 4 | 16:9 픽셀 | refs 전부 |
| 2 | `prompts/C02_covers_B.md` | 4 | 16:9 픽셀 | refs 전부 + C01의 cover_index |
| 3 | `prompts/C03_part1_3.md` | 6 | 16:9·2:3 | moa·haru·sia anime_base, moa_sheet, doctor_sheet |
| 4 | `prompts/C04_part4_5.md` | 4 | 16:9 | haru·sia·moa anime_base |
| 5 | `prompts/C05_fail_A.md` | 4 | 2:3 | 해당 캐릭터 기준 그림 |
| 6 | `prompts/C06_fail_B.md` | 4 | 2:3 | 해당 캐릭터 기준 그림 |

## 3. 저장 이름
`checklist.csv`의 `file` 열 이름 그대로(png·jpg). 받으면 WebP로 바꿔 `assets/img/`에 넣습니다(표지 1600×900, 가로 1200×675, 세로 600×900).

## 4. 실패 그림 주의
도구가 실수를 자동으로 고쳐 그리면 두 번까지만 다시 시도해 주세요. 그래도 안 되면 그대로 주셔도 됩니다(페이지에서 '결과는 매번 다르다'는 사례로 설명합니다).
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for cid, title, ratio, att, items in CONV:
        pix = items[0][5] == "pixel"
        md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD_PIX if pix else HEAD_ANI}\n```\n"
        for k, (file, page, part, alt, prompt, style) in enumerate(items):
            n += 1; rows.append([n, cid[:3], file, page, part, "16:9" if "16:9" in prompt.split("\n")[0] else "2:3", style, ""])
            md += f"\n---\n## {k+1}) {file} — {part}\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(README)
    print("prompts", len(CONV), "images", n)
