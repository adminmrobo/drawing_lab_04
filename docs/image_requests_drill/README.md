# 그림 요청 꾸러미 3 — '프롬프트 연습 과제' 예상 결과 (36장)

부마다 연습 과제 5개(모두 30개)의 **예상 결과 그림**입니다. D01~D04는 v1.1에서 받은 그림(14장), **D05~D09가 v1.2에 더한 그림(22장)**입니다. 페이지의 과제 프롬프트와 이 요청문의 프롬프트는 같습니다(원본: `build/content_drill.py`).

## 요청 순서
| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
| 1 | prompts/D01_part1.md | 3 | refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |
| 2 | prompts/D02_part2.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png |
| 3 | prompts/D03_part3_4.md | 4 | refs/moa_anime_base.png, refs/moa_sheet.png, refs/doctor_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |
| 4 | prompts/D04_part5_6.md | 4 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png |
| 5 | prompts/D05_part1_more.md | 4 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png |
| 6 | prompts/D06_part2_more.md | 5 | refs/sia_anime_base.png, refs/sia_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png, refs/doctor_sheet.png |
| 7 | prompts/D07_part3_more.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/sia_anime_base.png, refs/sia_sheet.png, refs/doctor_sheet.png |
| 8 | prompts/D08_part4_more.md | 3 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/doctor_sheet.png, refs/moa_anime_base.png, refs/moa_sheet.png |
| 9 | prompts/D09_part5_6_more.md | 7 | refs/haru_anime_base.png, refs/haru_sheet.png, refs/doctor_sheet.png + 부분 수정 바탕 그림 d9·d11(v1.1에서 받은 그림) |

## 03 얼굴 편에서 배운 것을 처음부터 반영
- 짝 그림(d1·d4·d15·d16·d17·d29의 ①·②)은 **서로 다른 새 대화**에서 만듭니다(같은 대화면 둘째 그림이 첫째를 따라 그림).
- 바뀌는 곳은 **'most important'로 표시하고 과장**해 적었습니다.
- d10·d25·d27은 그림 생성이 아니라 **부분 수정(영역 칠하기)** 기능으로 만듭니다. 바탕은 v1.1에서 받은 d9(d10·d25)와 d11(d27) 결과입니다.
- 새 대화에서는 'Same image'로 시작하는 문장을 쓰지 않습니다(v1.1 비교 그림 두 장에서 캐릭터가 사라진 실제 결과). 모든 프롬프트는 그 자체로 완결된 한 덩어리입니다.
- d11은 실패 그림 f8을 **첨부하지 않고** 새 대화에서 만듭니다.
- d12·d15①·d30이 어려 보이게 나오면 쓰지 않고 다시 만듭니다.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png·jpg).
