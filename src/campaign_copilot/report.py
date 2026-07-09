from __future__ import annotations

import json
from pathlib import Path

from campaign_copilot.models import Campaign, ContentItem, GeneratedAssets, JsonDict, PublicSignal
from campaign_copilot.normalize import summarize_sns
from campaign_copilot.utils import write_json, write_text


def write_report(
    report_dir: Path,
    week: str,
    campaign: Campaign,
    recommendations: list[JsonDict],
    contents: list[ContentItem],
    signals: list[PublicSignal],
    generated: GeneratedAssets,
    collector_status: list[JsonDict],
) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "assets").mkdir(parents=True, exist_ok=True)
    data = build_dashboard_data(
        week=week,
        campaign=campaign,
        recommendations=recommendations,
        contents=contents,
        signals=signals,
        collector_status=collector_status,
    )
    write_json(report_dir / "data.json", data)
    write_text(report_dir / "index.html", render_index_html(data))
    write_text(report_dir / "style.css", render_css())
    write_text(report_dir / "app.js", render_js())
    write_text(report_dir / "result.md", render_result_summary(data))
    write_text(report_dir / "report.md", render_markdown_report(data))
    write_json(report_dir / "campaign.json", campaign.to_dict())
    write_json(report_dir / "recommendation.json", {"week": week, "top_candidates": recommendations})
    write_text(report_dir / "instagram.md", generated.instagram)
    write_text(report_dir / "facebook.md", generated.facebook)
    write_text(report_dir / "naver_blog.md", generated.naver_blog)
    write_text(report_dir / "image_prompt.md", generated.image_prompt)
    write_text(report_dir / "landing_summary.md", generated.landing_summary)
    write_json(report_dir / "assets.json", generated.assets)


def build_dashboard_data(
    week: str,
    campaign: Campaign,
    recommendations: list[JsonDict],
    contents: list[ContentItem],
    signals: list[PublicSignal],
    collector_status: list[JsonDict],
) -> JsonDict:
    top = recommendations[0]
    return {
        "week": week,
        "summary": {
            "top_destination": top["destination"],
            "trend_score": top["score"],
            "opportunity": top["opportunity"],
            "risk": top["risk"],
            "confidence": top["confidence"],
        },
        "signals": [signal.to_dict() for signal in signals],
        "recommendations": recommendations,
        "campaigns": [campaign.to_dict()],
        "sns": summarize_sns(contents),
        "evidence": top["evidence"],
        "collector_status": collector_status,
        "generated_files": [
            "instagram.md",
            "facebook.md",
            "naver_blog.md",
            "image_prompt.md",
            "result.md",
        ],
    }


def render_index_html(data: JsonDict) -> str:
    embedded = json.dumps(data, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>마이리얼트립 주간 캠페인 코파일럿</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">마이리얼트립 주간 캠페인 코파일럿</p>
      <h1>{data["summary"]["top_destination"]} 주간 캠페인</h1>
      <p class="intro">공개 데이터와 자사 공개 채널 신호를 모아 이번 주 어떤 여행 상품을 밀어야 하는지 설명하는 내부 의사결정 리포트입니다.</p>
    </div>
    <div class="score">
      <span>트렌드 점수 <button class="tip" title="뉴스, 자사 채널, 환율, 날씨, 휴일, 항공권 신호를 합산한 캠페인 추천 점수입니다.">?</button></span>
      <strong>{data["summary"]["trend_score"]}</strong>
    </div>
  </header>
  <main>
    <section id="summary" class="grid metrics"></section>
    <section>
      <h2>추천 캠페인 <button class="tip" title="가장 점수가 높은 여행지를 실제 캠페인으로 바꾼 결과입니다. 대상 고객, 목표, 채널, 행동 유도 문구를 보여줍니다.">?</button></h2>
      <div id="campaigns" class="grid"></div>
    </section>
    <section>
      <h2>공개 신호 <button class="tip" title="뉴스, 환율, 날씨처럼 누구나 확인 가능한 공개 데이터를 정규화한 목록입니다.">?</button></h2>
      <div id="signals" class="table-wrap"></div>
    </section>
    <section>
      <h2>자사 공개 채널 분석 <button class="tip" title="인스타그램, 페이스북, 네이버 블로그에서 확인한 게시물 수와 주요 여행지입니다. 샘플은 실데이터가 아닌 대체 데이터임을 뜻합니다.">?</button></h2>
      <div id="sns" class="table-wrap"></div>
    </section>
    <section>
      <h2>추천 근거 <button class="tip" title="추천 점수에 실제로 연결된 근거입니다. 실데이터와 샘플 여부를 함께 표시합니다.">?</button></h2>
      <div id="evidence" class="grid"></div>
    </section>
    <section>
      <h2>데이터 수집 상태 <button class="tip" title="각 수집기가 어떤 방식으로 데이터를 가져왔는지 보여줍니다. 실데이터는 실제 공개 URL에서 수집, 샘플은 대체 데이터를 뜻합니다.">?</button></h2>
      <div id="collector-status" class="table-wrap"></div>
    </section>
    <section>
      <h2>생성 결과 <button class="tip" title="실제 캠페인 실행에 사용할 채널별 초안과 이미지 생성 프롬프트입니다.">?</button></h2>
      <div id="files" class="file-list"></div>
    </section>
  </main>
  <script id="embedded-data" type="application/json">{embedded}</script>
  <script src="app.js"></script>
</body>
</html>
"""


def render_css() -> str:
    return """*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f7f8fb;color:#172033}a{color:#1d4ed8}.topbar{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;padding:32px 40px;background:#101828;color:white}.eyebrow{margin:0 0 8px;color:#9fd1ff;font-size:13px}.intro{max-width:760px;margin:12px 0 0;color:#d8e5f6;line-height:1.6}h1{margin:0;font-size:32px;line-height:1.15}h2{margin:0 0 14px;font-size:20px;display:flex;align-items:center;gap:6px}main{max-width:1180px;margin:0 auto;padding:28px 24px 48px}section{margin-bottom:28px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.card{background:white;border:1px solid #e3e8ef;border-radius:8px;padding:16px;box-shadow:0 1px 2px rgba(16,24,40,.04)}.card h3{margin:0 0 8px;font-size:16px}.card p{margin:0 0 8px;line-height:1.5}.score{min-width:160px;text-align:right}.score span{display:block;color:#c8d7eb}.score strong{font-size:44px}.metric{border-left:4px solid #1d4ed8}.badge{display:inline-flex;align-items:center;border-radius:999px;background:#eaf2ff;color:#174ea6;padding:3px 9px;font-size:12px;margin:2px 4px 2px 0}.tip{width:20px;height:20px;border:0;border-radius:50%;background:#dbeafe;color:#174ea6;font-weight:700;cursor:help}.score .tip{vertical-align:middle}.hint{color:#526173;font-size:13px}.table-wrap{overflow:auto;background:white;border:1px solid #e3e8ef;border-radius:8px}table{width:100%;border-collapse:collapse;min-width:720px}th,td{padding:10px 12px;border-bottom:1px solid #edf1f7;text-align:left;font-size:14px;vertical-align:top}th{background:#f0f4f8;color:#344054}.file-list{display:flex;flex-wrap:wrap;gap:8px}.file-list a{display:inline-flex;padding:9px 12px;border-radius:8px;background:#172033;color:white;text-decoration:none}@media(max-width:640px){.topbar{padding:24px;display:block}.score{text-align:left;margin-top:18px}h1{font-size:26px}main{padding:22px 16px}table{min-width:640px}}@media(prefers-color-scheme:dark){body{background:#0f172a;color:#e5e7eb}.card,.table-wrap{background:#111827;border-color:#273449}th{background:#1e293b;color:#d7dee9}td{border-color:#273449}.topbar{background:#020617}.badge{background:#1e3a5f;color:#bfdbfe}.hint{color:#a7b4c7}.tip{background:#1e3a5f;color:#bfdbfe}}"""


def render_js() -> str:
    return """async function loadData(){const embedded=document.getElementById("embedded-data");try{const response=await fetch("data.json",{cache:"no-store"});if(response.ok)return await response.json()}catch(error){}return JSON.parse(embedded.textContent)}const labelMap={news:"뉴스",exchange_rate:"환율",weather:"날씨",holiday:"휴일",flight_price:"항공권 가격",owned_channel:"자사 공개 채널",sns_gap:"자사 채널 공백",instagram:"인스타그램",facebook:"페이스북",naver_blog:"네이버 블로그",live:"실데이터",sample:"샘플",Japan:"일본",Korea:"한국",Vietnam:"베트남",Philippines:"필리핀",Thailand:"태국","United States":"미국",China:"중국",General:"공통"};const fileLabels={\"instagram.md\":\"인스타그램 초안\",\"facebook.md\":\"페이스북 초안\",\"naver_blog.md\":\"네이버 블로그 초안\",\"image_prompt.md\":\"이미지 프롬프트\",\"result.md\":\"요약 리포트\"};function label(value){if(Array.isArray(value))return value.map(label).join(\", \");return labelMap[value]||(value??\"\")}function help(text){return `<button class=\"tip\" title=\"${text}\">?</button>`}function card(title,body,meta=\"\",tip=\"\"){const icon=tip?help(tip):\"\";return `<article class=\"card\"><h3>${title} ${icon}</h3><p>${body}</p>${meta}</article>`}function renderTable(rows,columns){if(!rows.length)return \"<p class='card'>데이터가 없습니다.</p>\";const head=columns.map(c=>`<th>${c.label} ${c.tip?help(c.tip):\"\"}</th>`).join(\"\");const body=rows.map(row=>`<tr>${columns.map(c=>`<td>${c.format?c.format(row[c.key],row):label(row[c.key])}</td>`).join(\"\")}</tr>`).join(\"\");return `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`}function badges(items){return items.map(item=>`<span class=\"badge\">${label(item)}</span>`).join(\"\")}function modeText(row){if(row.source_mode===\"live\")return \"실데이터\";if(row.source_mode===\"sample\")return \"샘플\";return \"실패\"}function render(data){document.getElementById(\"summary\").innerHTML=[card(\"추천 여행지\",data.summary.top_destination,\"<span class='badge'>최우선 후보</span>\",\"이번 주 캠페인 후보 중 점수가 가장 높은 여행지입니다.\"),card(\"기회 점수\",data.summary.opportunity,\"\",\"환율, 뉴스, 항공권, 휴일처럼 캠페인에 유리한 신호를 점수화한 값입니다.\"),card(\"리스크\",data.summary.risk,\"\",\"날씨나 위험 신호처럼 캠페인 메시지에서 조심해야 할 요소입니다. 낮을수록 좋습니다.\"),card(\"신뢰도\",data.summary.confidence,\"\",\"추천 근거 수와 출처 상태를 바탕으로 계산한 참고 지표입니다.\")].join(\"\");document.getElementById(\"campaigns\").innerHTML=data.campaigns.map(c=>card(c.theme,`${c.target}<br>${c.objective}<br>${c.cta}`,badges(c.channels),\"추천 여행지를 실제 캠페인 실행안으로 바꾼 결과입니다.\")).join(\"\");document.getElementById(\"signals\").innerHTML=renderTable(data.signals.slice(0,20),[{key:\"signal_type\",label:\"신호 종류\",tip:\"뉴스, 환율, 날씨처럼 점수 계산에 들어간 공개 데이터 종류입니다.\"},{key:\"region\",label:\"지역\",tip:\"이 신호가 연결된 국가 또는 지역입니다.\"},{key:\"metric\",label:\"측정 항목\",tip:\"기사 검색어, 통화, 날씨 상태처럼 원본 데이터의 기준입니다.\"},{key:\"value\",label:\"값\",tip:\"수집한 신호를 계산에 쓰기 위해 숫자로 바꾼 값입니다.\"},{key:\"source_mode\",label:\"출처 상태\",tip:\"실데이터는 공개 URL에서 수집, 샘플은 대체 데이터를 뜻합니다.\"}]);document.getElementById(\"sns\").innerHTML=renderTable(data.sns,[{key:\"platform\",label:\"채널\",tip:\"분석한 자사 공개 채널입니다.\"},{key:\"post_count\",label:\"게시물 수\",tip:\"이번 실행에서 정규화된 게시물 개수입니다.\"},{key:\"top_destination\",label:\"주요 여행지\",tip:\"해당 채널에서 가장 자주 잡힌 여행지입니다.\"},{key:\"promotion_count\",label:\"프로모션 수\",tip:\"할인, 특가, 혜택 등 프로모션 성격으로 분류된 게시물 수입니다.\"},{key:\"source_modes\",label:\"출처 상태\",tip:\"실데이터와 샘플 중 어떤 데이터가 섞였는지 보여줍니다.\"}]);document.getElementById(\"evidence\").innerHTML=data.evidence.map(e=>card(label(e.type),e.title,`<p class='hint'>${e.detail??\"\"}</p><span class='badge'>${label(e.source_mode)}</span>`,\"추천 점수에 연결된 실제 근거입니다.\")).join(\"\");document.getElementById(\"collector-status\").innerHTML=renderTable(data.collector_status,[{key:\"source\",label:\"수집기\",tip:\"데이터를 가져온 채널 또는 공개 데이터 소스입니다.\"},{key:\"source_mode\",label:\"수집 방식\",tip:\"실데이터 또는 샘플 여부입니다.\"},{key:\"item_count\",label:\"수집 수\",tip:\"이번 실행에서 확보한 항목 수입니다.\"},{key:\"public_url\",label:\"공개 주소\",tip:\"확인 가능한 원본 또는 대표 공개 주소입니다.\"},{key:\"error\",label:\"참고\",tip:\"샘플 사용 이유나 수집 제한 설명입니다.\",format:(value,row)=>value||modeText(row)}]);document.getElementById(\"files\").innerHTML=data.generated_files.map(file=>`<a href=\"${file}\" title=\"${file}\">${fileLabels[file]||file}</a>`).join(\"\")}loadData().then(render);"""


def render_result_summary(data: JsonDict) -> str:
    summary = data["summary"]
    recommendation = data["recommendations"][0]
    reasons = first_three(recommendation.get("reasons", []))
    while len(reasons) < 3:
        reasons.append("추천 근거가 HTML 리포트에 연결되어 있습니다.")

    return (
        "생성 완료했습니다.\n\n"
        f"이번 주 추천 1순위는 {summary['top_destination']}입니다.\n"
        f"추천 점수는 {summary['trend_score']}점이고, 주요 근거는 다음과 같습니다.\n\n"
        f"1. {reasons[0]}\n"
        f"2. {reasons[1]}\n"
        f"3. {reasons[2]}\n\n"
        "데이터 기준:\n"
        f"- 실데이터: {live_source_summary(data)}\n"
        f"- 샘플 사용: {sample_source_summary(data)}\n\n"
        "먼저 볼 파일:\n"
        "- HTML 리포트: reports/index.html\n"
        "- 인스타그램 초안: reports/instagram.md\n"
        "- 페이스북 초안: reports/facebook.md\n"
        "- 네이버 블로그 초안: reports/naver_blog.md\n\n"
        "상세 검증 데이터는 reports/data.json, reports/recommendation.json, reports/campaign.json에 저장됩니다.\n"
        "일반 사용자는 위 JSON 파일을 열지 않아도 됩니다.\n"
    )


def first_three(items: list[str]) -> list[str]:
    return [public_result_reason(item) for item in items if item][:3]


def public_result_reason(text: str) -> str:
    if "공개 신호와 자사 채널" in text:
        return "최근 여행 관심과 마이리얼트립 공개 콘텐츠 반응에서 관련 흐름이 확인됐습니다."
    if "환율, 항공권, 뉴스" in text:
        return "여행 준비에 영향을 주는 가격, 뉴스, 일정 관련 신호도 함께 참고했습니다."
    if "evidence 섹션" in text:
        return "여러 근거를 종합했을 때 이번 주 캠페인 우선순위가 높게 산정됐습니다."
    return text


def collector_count(data: JsonDict, source: str) -> int:
    for row in data["collector_status"]:
        if row["source"] == source:
            return int(row["item_count"])
    return 0


def live_source_summary(data: JsonDict) -> str:
    labels = []
    for source in ["naver_blog", "news", "exchange", "weather"]:
        if collector_mode(data, source) == "live":
            labels.append(f"{korean_source(source)} {collector_count(data, source)}건")
    return ", ".join(labels) if labels else "없음"


def collector_mode(data: JsonDict, source: str) -> str:
    for row in data["collector_status"]:
        if row["source"] == source:
            return str(row["source_mode"])
    return "unknown"


def sample_source_summary(data: JsonDict) -> str:
    labels = []
    for row in data["collector_status"]:
        if row["source_mode"] == "sample":
            labels.append(sample_source_label(row["source"]))
    return ", ".join(labels) if labels else "없음"


def sample_source_label(source: str) -> str:
    labels = {
        "instagram": "인스타그램 게시글 단위 데이터",
        "facebook": "페이스북 게시글 단위 데이터",
        "holiday": "휴일 데이터",
        "flight_price": "항공권 가격",
    }
    return labels.get(source, korean_source(source))


def render_markdown_report(data: JsonDict) -> str:
    summary = data["summary"]
    evidence = "\n".join(
        f"- {item['title']} ({korean_source_mode(item.get('source_mode', 'unknown'))})"
        for item in data["evidence"]
    )
    recommendations = "\n".join(
        f"- {row['destination']}: {row['score']}점, {', '.join(row['reasons'])}"
        for row in data["recommendations"]
    )
    statuses = "\n".join(
        f"- {korean_source(row['source'])}: {korean_source_mode(row['source_mode'])} / {row['item_count']}개"
        for row in data["collector_status"]
    )
    return (
        f"# {data['week']} 주간 캠페인 리포트\n\n"
        f"추천 여행지: {summary['top_destination']}\n\n"
        f"트렌드 점수: {summary['trend_score']}\n\n"
        "## 추천 결과\n"
        f"{recommendations}\n\n"
        "## 추천 근거\n"
        f"{evidence}\n\n"
        "## 데이터 수집 상태\n"
        f"{statuses}\n"
    )


def korean_source(value: str) -> str:
    labels = {
        "instagram": "인스타그램",
        "facebook": "페이스북",
        "naver_blog": "네이버 블로그",
        "news": "뉴스",
        "exchange": "환율",
        "weather": "날씨",
        "holiday": "휴일",
        "flight_price": "항공권 가격",
    }
    return labels.get(value, value)


def korean_source_mode(value: str) -> str:
    labels = {"live": "실데이터", "sample": "샘플", "unknown": "알 수 없음"}
    return labels.get(value, value)
