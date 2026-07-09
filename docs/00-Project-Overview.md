# 00. Project Overview

# MyRealTrip Weekly Campaign Copilot

## 프로젝트 목표

마이리얼트립 마케팅팀과 MD가 매주 수행하는 캠페인 기획 업무를 Codex Plugin으로 자동화한다.

---

## 해결하려는 문제

현재 마케팅 담당자는 아래 업무를 반복한다.

1. 이번 주 어떤 여행 상품을 홍보할지 결정
2. 외부 트렌드 조사
3. 기존 SNS 분석
4. 캠페인 초안 작성
5. 플랫폼별 콘텐츠 제작
6. 보고서 작성

이 과정은 반복적이며 사람이 직접 수행한다.

---

## 대상 사용자

- 마케팅팀
- 콘텐츠팀
- MD
- 상품기획자

여행객은 사용자가 아니다.

---

## 입력 데이터

### 내부 공개 데이터
- 마이리얼트립 Instagram
- 마이리얼트립 Facebook
- 마이리얼트립 네이버 블로그

### 외부 공개 데이터
- 뉴스
- Google Trends
- 환율
- 날씨
- 공휴일
- 관광공사 통계
- (선택) 항공권 가격

---

## 출력

- Weekly Report (HTML)
- Instagram 초안
- Facebook 초안
- 네이버 블로그 초안
- 이미지 프롬프트
- 캠페인 제안서(Markdown)

---

## 성공 기준

- 5분 이내 Weekly Campaign 생성
- HTML 보고서 생성
- 플랫폼별 콘텐츠 초안 생성
- Codex Plugin으로 실행 가능

---

## Codex 구현 원칙

- TODO를 남기지 않는다.
- Stub이라도 모든 기능을 구현한다.
- docs 문서를 순서대로 읽고 구현한다.
- 각 Task 완료 후 테스트한다.
