# 해커톤 제출 답변

이 문서는 Primer Hackathon 제출 폼에 입력한 답변을 저장소에 함께 남기기 위한 문서입니다.

## 문항 1. 무엇을, 누가, 어떤 상황에서 쓰나요?

마이리얼트립 주간 캠페인 코파일럿은 여행 마케팅 담당자, 콘텐츠 운영자, MD가 매주 어떤 여행지를 밀어야 할지 빠르게 판단하고 SNS 초안을 만드는 플러그인입니다. 주간 캠페인 회의나 프로모션 준비 시, 공개 여행 신호와 자사 공개 채널 반응이 흩어져 있어 추천 여행지 선정, 근거 정리, 인스타그램/페이스북/네이버 블로그 문안 작성이 반복 작업이 되는 상황에서 사용합니다. Codex에서 자연어로 요청하면 추천 여행지, 추천 근거, HTML 리포트, 채널별 복사 가능한 포스팅 초안, 이미지 프롬프트와 이미지 표시 영역을 생성합니다.

## 문항 2. 왜 이 문제를 선택했나요?

여행 상품 마케팅은 시즌, 환율, 날씨, 뉴스, SNS 반응에 따라 매주 우선순위가 바뀌지만, 담당자는 여러 공개 채널을 직접 확인하고 근거를 정리한 뒤 채널별 문안을 다시 작성해야 합니다. 마이리얼트립은 인스타그램, 페이스북, 네이버 블로그 등 공개 채널을 운영하고 있어 공개 자료 기반 문제 검증이 가능했습니다. 특히 네이버 블로그, 뉴스, 환율, 날씨는 실시간 공개 데이터로 수집할 수 있었고, Meta 계열 게시글 단위 데이터처럼 공개 페이지에서 안정적으로 얻기 어려운 부분은 샘플 사용 여부를 명확히 표시하도록 설계했습니다.

### 출처 URL

- https://www.instagram.com/myrealtrip
- https://www.facebook.com/myRealTrip
- https://blog.naver.com/myrealtrip
- https://rss.blog.naver.com/myrealtrip.xml
- https://news.google.com/rss
- https://api.frankfurter.app/latest
- https://open-meteo.com/

## 문항 3. 플러그인은 어떻게 작동하나요?

플러그인은 Codex에서 자연어 요청을 받으면 `python3 -m campaign_copilot.cli run-weekly` 흐름을 실행합니다. 구조는 Collector -> Normalizer -> Trend Engine -> Campaign Planner -> Content Generator -> HTML Report 순서입니다. Collector가 네이버 블로그 RSS, Google News RSS, 환율, 날씨 데이터를 수집하고, 인스타그램/페이스북처럼 공개 페이지에서 안정적인 게시글 단위 수집이 어려운 채널은 샘플로 대체하며 그 사유를 리포트에 표시합니다. Normalizer는 데이터를 콘텐츠와 공개 신호로 정규화하고, Trend Engine은 여행지별 점수를 계산합니다. Campaign Planner는 추천 여행지와 캠페인 방향을 만들고, Content Generator는 인스타그램/페이스북/네이버 블로그 초안과 이미지 프롬프트를 생성합니다. 마지막으로 HTML 리포트, `result.md`, JSON 검증 데이터, `submission.zip`을 생성합니다.

## 문항 4. AI를 어떻게 썼나요?

AI는 Codex를 통해 플러그인 설계, Python 모듈 구현, 테스트 작성, README 정리, 사용자용 결과 템플릿 개선, SNS 문안 품질 개선, 이미지 프롬프트 작성에 사용했습니다. 다만 AI가 임의로 사실을 꾸미지 않도록 실데이터와 샘플 데이터를 분리했고, 추천 근거가 없는 트렌드는 주장하지 않도록 했습니다. 처음에는 JSON 파일 목록이 사용자에게 너무 많이 노출됐지만, 일반 사용자는 `result.md`와 `index.html`을 먼저 보도록 바꿨습니다. 또한 AI스러운 SNS 초안은 실제 복사/붙여넣기 가능한 문안으로 다시 다듬었고, 공개 수집이 불안정한 Meta 데이터는 실데이터라고 주장하지 않도록 제한했습니다.

## 문항 5. 어떻게 검증했나요?

정상 동작은 `python3 -m unittest discover -s tests`로 단위 테스트 6개 통과를 확인했고, `python3 -m campaign_copilot.cli run-weekly`로 실제 주간 리포트 생성까지 확인했습니다. 생성 결과로 `reports/index.html`, `result.md`, `instagram.md`, `facebook.md`, `naver_blog.md`, `recommendation.json`, `campaign.json`이 만들어지는지 봤습니다. 플러그인 validator를 통과했고, `python3 -m zipfile -t submission.zip`로 제출 zip 무결성도 확인했습니다. 예외 상황은 인스타그램/페이스북 공개 페이지 제한, 항공권 가격/휴일 데이터 부족을 샘플 fallback으로 처리하고 리포트에 표시했습니다. `logs` 폴더에는 기존 대화 로그와 현재 Codex visible transcript를 넣었고, 실제 비밀값 패턴이 없는지도 검사했습니다.

## 제출 패키지 메모

- 로컬 제출 파일: `outputs/myrealtrip-weekly-campaign-copilot-plugin/submission.zip`
- GitHub에는 `outputs/`, `logs/`, `.local-codex-marketplace/`, `*.zip` 같은 생성 결과물을 올리지 않습니다.
- 실행 가능한 플러그인 소스는 `src/`에 보관합니다.
