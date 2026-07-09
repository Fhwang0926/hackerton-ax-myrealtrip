# 05. Data Collector Spec

# 목적

이 문서는 MyRealTrip Weekly Campaign Copilot의 데이터 수집기 설계를 정의한다.

이 플러그인의 핵심은 "캠페인 초안 생성"이 아니라, 공개 데이터에서 이번 주에 팔아야 할 상품의 근거를 찾는 것이다.

따라서 Collector는 다음 목표를 만족해야 한다.

1. API Key 없이도 기본 실행 가능
2. 공개 데이터 기반으로 동작
3. 실패해도 전체 Workflow가 중단되지 않음
4. 수집 결과를 원본 그대로 저장
5. 이후 Normalizer가 처리할 수 있는 JSON 구조로 반환

---

# Collector 기본 원칙

## 1. 모든 Collector는 동일한 인터페이스를 따른다

```python
class BaseCollector:
    name: str

    def collect(self, context: CollectContext) -> CollectorResult:
        ...
```

---

## 2. Collector는 판단하지 않는다

Collector는 데이터를 가져오기만 한다.

잘못된 예:

```python
if "일본" in title:
    score += 10
```

좋은 예:

```python
return RawItem(
    source="news",
    title=title,
    body=body,
    published_at=published_at,
    url=url
)
```

분석과 판단은 Analyzer가 담당한다.

---

## 3. Collector 실패는 전체 실패가 아니다

예를 들어 Instagram 수집이 실패해도 News, Naver Blog, Weather 수집은 계속 진행되어야 한다.

```python
try:
    result = collector.collect(context)
except Exception as e:
    result = CollectorResult(
        source=collector.name,
        ok=False,
        error=str(e),
        items=[]
    )
```

---

# CollectContext

```python
@dataclass
class CollectContext:
    week_start: date
    week_end: date
    locale: str = "ko-KR"
    target_market: str = "KR"
    output_dir: Path = Path("data/raw")
    use_live: bool = False
    use_sample: bool = True
    max_items_per_source: int = 100
```

---

# CollectorResult

```python
@dataclass
class CollectorResult:
    source: str
    ok: bool
    collected_at: str
    items: list[dict]
    error: str | None = None
    meta: dict = field(default_factory=dict)
```

---

# RawItem 공통 필드

모든 Collector는 최소한 아래 필드를 반환해야 한다.

```json
{
  "source": "naver_blog",
  "source_type": "owned_channel",
  "title": "세부 여행 추천",
  "body": "본문 내용",
  "url": "https://...",
  "published_at": "2026-07-01",
  "collected_at": "2026-07-09T12:00:00+09:00",
  "raw": {}
}
```

---

# 수집 대상

## 1. Instagram Collector

### 목적

마이리얼트립 공식 Instagram 콘텐츠를 수집하거나 샘플 데이터를 로드한다.

### URL

```text
https://www.instagram.com/myrealtrip
```

### 수집 항목

- 게시일
- 캡션
- 해시태그
- 이미지/릴스 여부
- 여행지
- 프로모션 키워드
- CTA
- 좋아요/댓글 수가 확인 가능하면 수집

### 현실적 제한

Instagram은 로그인 제한과 동적 렌더링 이슈가 있다.

따라서 MVP에서는 다음 전략을 사용한다.

1. 기본 모드: 샘플 JSON 사용
2. 선택 모드: 사용자가 export한 게시글 CSV/JSON 업로드
3. 확장 모드: 공식 API 또는 수동 저장 HTML 파싱

### 출력 예시

```json
{
  "source": "instagram",
  "source_type": "owned_channel",
  "platform": "instagram",
  "title": "청도 맥주축제",
  "body": "아시아의 옥토버페스트...",
  "hashtags": ["청도맥주축제", "중국여행"],
  "media_type": "reel",
  "published_at": "2026-07-08",
  "metrics": {
    "likes": null,
    "comments": null
  },
  "url": "https://www.instagram.com/..."
}
```

---

## 2. Facebook Collector

### 목적

마이리얼트립 Facebook 게시글을 수집하거나 샘플 데이터를 로드한다.

### URL

```text
https://www.facebook.com/myRealTrip
```

### 수집 항목

- 게시일
- 본문
- 링크
- 이벤트 여부
- 프로모션 여부
- 이미지/영상 여부
- 반응 수치가 확인 가능하면 수집

### 현실적 제한

Facebook도 로그인 제한이 있으므로 MVP에서는 샘플 데이터 또는 사용자가 저장한 HTML/CSV를 처리한다.

### 출력 예시

```json
{
  "source": "facebook",
  "source_type": "owned_channel",
  "platform": "facebook",
  "title": "제주 숙소 이벤트",
  "body": "여름 제주 여행 지원 이벤트...",
  "media_type": "image",
  "published_at": "2026-07-07",
  "campaign_type": "event",
  "url": "https://www.facebook.com/..."
}
```

---

## 3. Naver Blog Collector

### 목적

마이리얼트립 공식 네이버 블로그의 최근 글을 수집한다.

### URL

```text
https://blog.naver.com/myrealtrip
```

### 수집 항목

- 제목
- 본문
- 게시일
- 이미지 수
- 태그
- 여행지
- 상품 링크
- CTA

### 구현 전략

Naver Blog는 페이지 구조가 비교적 명확하지만 iframe 구조가 있을 수 있다.

MVP 전략:

1. 입력 URL 목록을 받는다.
2. requests로 HTML 수집
3. iframe 또는 본문 URL 탐색
4. BeautifulSoup으로 제목/본문 추출
5. 실패 시 샘플 데이터 사용

### 입력 예시

```text
https://blog.naver.com/myrealtrip/224341711951
```

### 출력 예시

```json
{
  "source": "naver_blog",
  "source_type": "owned_channel",
  "platform": "naver_blog",
  "title": "세부 여행 코스 추천",
  "body": "세부 여행 준비 중이라면...",
  "published_at": "2026-07-05",
  "url": "https://blog.naver.com/myrealtrip/224341711951",
  "metrics": {
    "comment_count": null,
    "like_count": null
  }
}
```

---

## 4. News Collector

### 목적

이번 주 여행 관련 뉴스 신호를 수집한다.

### 기본 키워드

```text
여행
해외여행
일본 여행
동남아 여행
여름휴가
항공권
환율
휴가
축제
마이리얼트립
```

### 구현 전략

API Key 없이 동작해야 하므로 RSS 중심으로 구현한다.

후보:

- Google News RSS
- 네이버 뉴스 검색 RSS 대체
- Bing News RSS 대체
- 수동 샘플 데이터

### 출력 예시

```json
{
  "source": "news",
  "source_type": "public_signal",
  "title": "엔저에 일본 여행 수요 증가",
  "body": "최근 엔화 약세로...",
  "published_at": "2026-07-08",
  "url": "https://news.example.com/...",
  "keyword": "일본 여행"
}
```

---

## 5. Exchange Rate Collector

### 목적

환율 변화를 수집해 여행지 매력도 판단에 사용한다.

### 주요 통화

- JPY
- USD
- EUR
- THB
- VND
- PHP
- TWD
- CNY

### 기본 전략

API Key 없는 공개 환율 endpoint 또는 샘플 데이터 사용.

### 출력 예시

```json
{
  "source": "exchange_rate",
  "source_type": "public_signal",
  "currency": "JPY",
  "base": "KRW",
  "rate": 9.1,
  "change_7d": -1.8,
  "collected_at": "2026-07-09T12:00:00+09:00"
}
```

---

## 6. Weather Collector

### 목적

이번 주 여행 적합도를 판단한다.

### 대상 지역

기본 MVP:

- 서울
- 제주
- 오사카
- 도쿄
- 후쿠오카
- 방콕
- 다낭
- 세부
- 발리
- 타이베이

### 출력 예시

```json
{
  "source": "weather",
  "source_type": "public_signal",
  "city": "Jeju",
  "country": "KR",
  "date": "2026-07-11",
  "condition": "rain",
  "temperature_max": 28,
  "travel_suitability": null
}
```

Collector는 suitability를 계산하지 않는다. Analyzer가 계산한다.

---

## 7. Holiday Collector

### 목적

공휴일과 연휴 신호를 수집한다.

### 활용 이유

여행 캠페인은 연휴/주말/휴가 시즌에 크게 영향을 받는다.

### 출력 예시

```json
{
  "source": "holiday",
  "source_type": "public_signal",
  "country": "KR",
  "date": "2026-08-15",
  "name": "광복절",
  "is_long_weekend": true
}
```

---

## 8. Flight Price Collector

### 목적

항공권 가격 하락/상승 신호를 수집한다.

### MVP 전략

실시간 항공권 API는 제한이 많으므로 기본 모드에서는 샘플 데이터를 사용한다.

확장 모드:

- 마이리얼트립 Open API
- 파트너 API
- 사용자가 업로드한 CSV
- 수동 가격 스냅샷

### 출력 예시

```json
{
  "source": "flight_price",
  "source_type": "public_signal",
  "origin": "ICN",
  "destination": "FUK",
  "price": 148000,
  "change_7d": -12.5,
  "date_range": "2026-07-12/2026-07-14"
}
```

---

## 9. Sample Loader

### 목적

실제 사이트 수집이 막히더라도 플러그인이 실행되어야 한다.

### 샘플 파일

```text
src/data/samples/
├── instagram_sample.json
├── facebook_sample.json
├── naver_blog_sample.json
├── news_sample.json
├── exchange_sample.json
├── weather_sample.json
├── holiday_sample.json
└── flight_price_sample.json
```

### 요구사항

- 모든 샘플 데이터는 실제 구조와 동일해야 한다.
- 1주일 단위 데이터가 있어야 한다.
- 최소 20개 이상의 Content Item 필요
- 최소 30개 이상의 Public Signal 필요

---

# 저장 규칙

Collector 실행 후 원본 데이터는 반드시 저장한다.

```text
src/data/raw/{source}_{YYYY-MM-DD}.json
```

예시:

```text
src/data/raw/naver_blog_2026-07-09.json
src/data/raw/news_2026-07-09.json
```

---

# Collector 실행 CLI

```bash
python -m campaign_copilot.cli collect --source all
python -m campaign_copilot.cli collect --source naver_blog
python -m campaign_copilot.cli collect --source news
python -m campaign_copilot.cli collect --use-sample
```

---

# Error Handling

Collector는 다음 에러 타입을 구분한다.

```python
class CollectorError(Exception):
    pass

class RateLimitError(CollectorError):
    pass

class AuthRequiredError(CollectorError):
    pass

class ParseError(CollectorError):
    pass

class NetworkError(CollectorError):
    pass
```

에러는 `CollectorResult.error`에 저장하고 Workflow는 계속 진행한다.

---

# Logging

로그에는 다음을 남긴다.

- source
- started_at
- finished_at
- item_count
- error 여부
- 저장 경로

비밀정보는 절대 로그에 남기지 않는다.

---

# 완료 조건

- 모든 Collector가 BaseCollector 인터페이스를 따른다.
- API Key 없이 샘플 데이터로 전체 Workflow 실행 가능
- Naver Blog URL 입력 시 본문 추출 시도
- News RSS 수집 시도
- 실패 시에도 `CollectorResult(ok=False)` 반환
- raw JSON 저장
- 테스트 작성
