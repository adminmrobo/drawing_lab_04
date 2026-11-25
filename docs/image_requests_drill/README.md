# 그림 요청 꾸러미 3 — '프롬프트 연습 과제' 예상 결과 (14장)

부마다 연습 과제 2개(모두 12개)의 **예상 결과 그림**입니다. 페이지의 과제 프롬프트와 이 요청문의 프롬프트는 같습니다(원본: `build/content_drill.py`).

## 요청 순서
| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
| 1 | prompts/D01_part1.md | 3 | refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |
| 2 | prompts/D02_part2.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png |
| 3 | prompts/D03_part3_4.md | 4 | refs/moa_anime_base.png, refs/moa_sheet.png, refs/doctor_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |
| 4 | prompts/D04_part5_6.md | 4 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |

## 03 얼굴 편에서 배운 것을 처음부터 반영
- 짝 그림(d1 ①·②, d4 ①·②)은 **서로 다른 새 대화**에서 만듭니다(같은 대화면 둘째 그림이 첫째를 따라 그림).
- 바뀌는 곳은 **'most important'로 표시하고 과장**해 적었습니다.
- d10_haru_eye_fix는 그림 생성이 아니라 **부분 수정(영역 칠하기)** 기능으로 만듭니다. 바탕은 d9 결과입니다.
- d11은 실패 그림 f8을 **첨부하지 않고** 새 대화에서 만듭니다.
- d12가 어려 보이게 나오면 쓰지 않고 다시 만듭니다.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png·jpg).
