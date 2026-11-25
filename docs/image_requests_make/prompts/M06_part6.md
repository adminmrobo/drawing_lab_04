# M06 · 6부 '직접 만들어 보기' 비교 그림

**Genspark에 먼저 붙여 넣기 ↓**
```
해설 페이지의 '직접 만들어 보기' 비교 그림을 만들어 줘.
- 첨부한 그림(이미 만든 A 결과)과 똑같은 캐릭터·구도·화풍·빛을 유지하고, 아래 'Change only'에 적힌 것만 바꿀 것
- 비율은 첨부한 A 결과와 같게
- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·교복 느낌·어려 보이는 얼굴 금지
- 그림 안에 글자·숫자·로고 금지
```

---
## f2_fixed — 실패 그림 고치기 — 안쪽 눈만 좁히기
첨부: f2_far_eye.png (A 결과)
방법: 그림 생성이 아니라 '부분 수정(영역 칠하기)' 기능으로 — 안쪽 눈과 안쪽 눈썹만 칠하기
```
Inpainting only the far eye and its eyebrow: make the far eye noticeably narrower (about 60% of the near eye) and closer to the center line of the face, following the curve of the head. Keep the iris color, the near eye and everything else unchanged.
```

---
## f7_fixed — 실패 그림 고치기 — 칠하기 다섯 조각 더하기
첨부: f7_sticker_eyes.png (A 결과) + 해당 캐릭터의 refs/*_anime_base.png 또는 *_sheet.png
방법: A 결과를 첨부하고 Change only 문장으로
```
Same image, keep the same framing. Change only the eyes: off-white sclera slightly warmer than pure white, darker upper iris under the eyelid, subtle warm glow on the lower iris (the iris stays gray), one large and one small highlight, line art around light areas tinted brown. Still no text.
```
