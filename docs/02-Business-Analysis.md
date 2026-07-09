# 02. Business Analysis

# Business Analysis (PRD)

## 목적

이 플러그인은 여행객을 위한 서비스가 아니다.

사용자는 다음과 같다.

- 마케팅팀
- 콘텐츠팀
- MD
- 상품기획자

---

# 현재 업무(AS-IS)

매주 반복된다.

1. 외부 여행 트렌드 조사
2. 자사 SNS 분석
3. 홍보할 여행 상품 선정
4. SNS별 콘텐츠 제작
5. 내부 보고서 작성

이 과정은 사람이 여러 사이트를 방문하며 수행한다.

---

# 문제점

- 데이터가 여러 곳에 흩어져 있음
- 사람마다 판단 기준이 다름
- SNS마다 콘텐츠를 반복 제작
- 보고서 작성 시간이 많이 소요됨

---

# TO-BE

Codex Plugin

↓

공개 데이터 수집

↓

정규화

↓

트렌드 분석

↓

추천 상품 선정

↓

캠페인 생성

↓

HTML Report 생성

---

# CEO 관점

CEO가 원하는 것은
'게시글 생성 AI'가 아니다.

원하는 것은

- 매출 가능성이 높은 상품 추천
- 근거 기반 캠페인
- 반복 업무 감소
- 빠른 실행

---

# KPI

Input KPI

- 수집 성공률
- 정규화 성공률

Business KPI

- 캠페인 기획 시간 단축
- 플랫폼별 초안 자동 생성
- Weekly Report 자동 생성

---

# 공개 데이터 활용

내부 공개

- Instagram
- Facebook
- 네이버 블로그

외부 공개

- 뉴스
- 환율
- 날씨
- 공휴일
- Google Trends
- 관광 통계

---

# 차별성

일반 생성형 AI

→ 글 생성

본 플러그인

→ 데이터 기반 의사결정
→ 캠페인 설계
→ 콘텐츠 생성
→ HTML 보고서 생성

---

# 산출물

report/
├── index.html
├── report.md
├── instagram.md
├── facebook.md
├── naver_blog.md
├── image_prompt.md
