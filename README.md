# 구조 먼저 그리기 연구실 04 · 디테일 편 — 육각형 하나, 덩어리 몇 개

눈을 육각형 하나에서, 머리카락을 덩어리 몇 개에서 시작해 눈·눈 칠하기·표정·코·귀·입·머리카락의 디테일을 실험으로 익히고, 부위마다 그려 넣을 양을 맞춘 AI 디테일 문장과 부분 수정으로 옮겨 봅니다. 디테일 실패 8종 진단과 실전 연습장까지.

- 사이트: https://adminmrobo.github.io/drawing_lab_04/
- 글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 구성
| 부 | 페이지 | 내용 |
|---|---|---|
| 목차 | `index.html` | 세 줄 요약, 편 목록, 전체 흐름, 한눈에 보는 디테일 기준값, 등장인물, 원리와 출처 |
| 1부 | `01_eye_shape.html` | 눈의 모양 — 육각형 밑그림, 각막·홍채·동공, 공 위의 눈, 선 밀도 (모델 모아) |
| 2부 | `02_eye_paint.html` | 눈 칠하기와 표정 — 흰자 색, 곱하기·더하기 레이어, 눈썹과 눈 뜬 정도, 같은 눈 다른 입 (모델 하루) |
| 3부 | `03_nose_ear_mouth.html` | 코·귀·입 — 코 정보량, 귀 자리와 각도별 너비, 위 이 一·아래 이 U, 보이지 않는 어금니 (시아·박사) |
| 4부 | `04_hair.html` | 머리카락 — 부피, 덩어리 나누기, 나는 자리와 흐름, 다발 굵기 섞기 (하루·시아·모아) |
| 5부 | `05_ai_detail.html` | AI로 디테일 살리기 — 디테일 문장, 칠하기 문장, 부위만 가림 영역, 화풍별 남길 구조 |
| 6부 | `06_failure_lab.html` | 실패 사례 실험실 — 진단 순서, 실패 8종, 나이 쏠림 |
| 7부 | `practice/index.html` | 실전 연습장 — 눈 작업대, 표정 조합판, 디테일 문장 공방, 진단 데스크 |

## 원리와 출처
그리기 원리는 KawaiiSensei 『いいトコどり! 人物パーツの描き方』(マイナビ出版, 2023) 1장 「顔を描こう」(p.12~46)를 참고해 정리했습니다. 책의 그림·문장·도식·색 값·구성 순서는 옮기지 않았고, 연구실 캐릭터와 직접 움직이는 실험으로 새로 구성했습니다. 얼굴 전체 비율은 앞 편 [03 얼굴 편](https://adminmrobo.github.io/drawing_lab_03/)에서 다뤘으므로 이 편은 부위의 디테일만 다룹니다. 그 밖의 출처(Porter·Duff 1984, W3C 혼합 모드 2015, RePaint 2022, 잠재 확산 모델 2022)는 각 페이지 바닥글에 있습니다. 비율·각도·색 숫자는 모두 설명용 예시값입니다.

## 빌드와 점검
```
python3 build/build.py && python3 build/check_numbers.py && python3 build/make_og.py
python3 build/make_requests.py && python3 build/make_requests_make.py && python3 build/content_drill.py   # 그림 요청 꾸러미
python3 -m http.server 8765 &   # 아래 두 점검용
python3 build/check_pages.py && python3 build/check_missions.py
```
작성 방침: `docs/WRITING_POLICY.md` · 그림 요청문: `docs/image_requests/`(표지·본문·실패 36장, v1.2 단계 그림 10장 포함), `docs/image_requests_make/`(비교 12장), `docs/image_requests_drill/`(연습 과제 36장, v1.2 추가 22장 포함) · 받은 그림 설명은 `build/img_notes.py` · 페르소나 검사: `docs/persona_review.md`

그림 52장(표지 8 · 본문·실패 18 · 비교 12 · 연습 과제 14)은 Genspark로 만들어 v1.1(2026-11-25)에 넣었습니다. 요청과 다르게 나온 그림은 그림 설명과 '실제 결과'에 있는 그대로 적었습니다. v1.2(2026-11-25)에서 그림이 없던 단계 10곳에 단계 그림을, 부마다 연습 과제 3개(모두 18개)를 더했습니다. 새 그림 32장은 요청 중이라 '그림 준비 중' 자리로 보입니다(요청 꾸러미: `docs/구조먼저그리기연구실_04_디테일편_추가그림요청_v1.2.zip`). 실험 패널은 그림 없이도 모두 동작합니다.

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions).
