from __future__ import annotations

import zipfile
from pathlib import Path

from campaign_copilot.analyze import analyze_trends
from campaign_copilot.collectors import build_collectors
from campaign_copilot.config import AppConfig, current_week_window, week_label
from campaign_copilot.generate import generate_assets
from campaign_copilot.models import CollectContext, CollectorResult, JsonDict, WorkflowResult
from campaign_copilot.normalize import normalize_results
from campaign_copilot.plan import plan_campaign
from campaign_copilot.report import write_report
from campaign_copilot.utils import read_jsonl, timestamp_slug, write_json, write_jsonl


def run_weekly_campaign(config: AppConfig) -> WorkflowResult:
    week_start, week_end = current_week_window()
    week = week_label(week_start)
    context = CollectContext(
        week_start=week_start,
        week_end=week_end,
        output_dir=config.data_dir / "raw",
        use_live=config.use_live,
        use_sample=config.use_sample,
        max_items_per_source=config.max_items_per_source,
    )
    results = collect_all(config, context)
    save_raw_results(config.data_dir / "raw", results)
    contents, signals = normalize_results(results)
    write_jsonl(config.data_dir / "normalized" / "content_items.jsonl", [item.to_dict() for item in contents])
    write_jsonl(config.data_dir / "normalized" / "public_signals.jsonl", [item.to_dict() for item in signals])
    recommendations = analyze_trends(contents, signals)
    if not recommendations:
        raise RuntimeError("No recommendation could be generated from available evidence")
    campaign = plan_campaign(week, recommendations)
    generated = generate_assets(campaign, recommendations)
    recommendation_rows = [item.to_dict() for item in recommendations]
    collector_status = collector_status_rows(results)
    write_report(
        report_dir=config.report_dir,
        week=week,
        campaign=campaign,
        recommendations=recommendation_rows,
        contents=contents,
        signals=signals,
        generated=generated,
        collector_status=collector_status,
    )
    submission_path = build_submission_zip(config) if config.package_submission else None
    issues = workflow_issues(results)
    return WorkflowResult(
        week=week,
        report_dir=config.report_dir,
        recommendation_path=config.report_dir / "recommendation.json",
        campaign_path=config.report_dir / "campaign.json",
        submission_path=submission_path,
        issues=issues,
    )


def collect_all(config: AppConfig, context: CollectContext) -> list[CollectorResult]:
    results: list[CollectorResult] = []
    for collector in build_collectors(config.sample_dir):
        try:
            results.append(collector.collect(context))
        except Exception as exc:
            results.append(
                CollectorResult(
                    source=collector.name,
                    ok=False,
                    collected_at=context.week_end.isoformat(),
                    items=[],
                    error=str(exc),
                )
            )
    return results


def save_raw_results(raw_dir: Path, results: list[CollectorResult]) -> None:
    stamp = timestamp_slug()
    for result in results:
        write_json(raw_dir / f"{result.source}_{stamp}.json", result.to_dict())


def collector_status_rows(results: list[CollectorResult]) -> list[JsonDict]:
    rows: list[JsonDict] = []
    for result in results:
        rows.append(
            {
                "source": result.source,
                "ok": result.ok,
                "source_mode": result.meta.get("source_mode", "failed"),
                "item_count": len(result.items),
                "error": result.error,
                "public_url": result.meta.get("public_url"),
                "tls_verified": result.meta.get("tls_verified"),
                "tls_policy": result.meta.get("tls_policy"),
            }
        )
    return rows


def workflow_issues(results: list[CollectorResult]) -> list[str]:
    issues: list[str] = []
    for result in results:
        mode = result.meta.get("source_mode")
        if result.source in {"instagram", "facebook"} and mode == "sample":
            issues.append(
                f"{korean_source_name(result.source)} 게시글 단위 데이터는 소유 계정 내보내기 파일이나 공식 API가 없으면 샘플을 사용합니다."
            )
        if result.error:
            issues.append(f"{korean_source_name(result.source)} 참고: {result.error}")
        if not result.ok:
            issues.append(f"{korean_source_name(result.source)} 수집기가 사용할 수 있는 데이터를 반환하지 못했습니다.")
    return issues


def korean_source_name(source: str) -> str:
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
    return labels.get(source, source)


def build_submission_zip(config: AppConfig) -> Path:
    destination = config.root / "submission.zip"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        add_top_level_files(archive, config.root)
        add_src_tree(archive, config.root)
        add_logs(archive, config.root / "logs")
    return destination


def add_top_level_files(archive: zipfile.ZipFile, root: Path) -> None:
    readme = root / "README.md"
    if readme.exists():
        archive.write(readme, "README.md")


def add_src_tree(archive: zipfile.ZipFile, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "submission.zip":
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.relative_to(root).parts[0] == "logs":
            continue
        archive.write(path, Path("src") / path.relative_to(root))


def add_logs(archive: zipfile.ZipFile, logs_dir: Path) -> None:
    if not logs_dir.exists():
        return
    for path in sorted(logs_dir.rglob("*")):
        if path.is_file():
            archive.write(path, Path("logs") / path.relative_to(logs_dir))


def load_normalized(config: AppConfig) -> tuple[list[JsonDict], list[JsonDict]]:
    contents = read_jsonl(config.data_dir / "normalized" / "content_items.jsonl")
    signals = read_jsonl(config.data_dir / "normalized" / "public_signals.jsonl")
    return contents, signals
