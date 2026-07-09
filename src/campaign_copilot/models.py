from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class CollectContext:
    week_start: date
    week_end: date
    output_dir: Path
    use_live: bool = True
    use_sample: bool = True
    max_items_per_source: int = 100


@dataclass(frozen=True)
class CollectorResult:
    source: str
    ok: bool
    collected_at: str
    items: list[JsonDict]
    error: str | None = None
    meta: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class ContentItem:
    id: str
    platform: str
    source: str
    published_at: str
    title: str
    body: str
    country: str | None
    city: str | None
    travel_type: str | None
    season: str | None
    campaign_type: str | None
    promotion: bool
    cta: str | None
    hashtags: list[str]
    media_type: str | None
    topics: list[str]
    sentiment: str | None
    url: str
    source_mode: str

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class PublicSignal:
    signal_type: str
    region: str
    metric: str
    value: float
    observed_at: str
    title: str
    url: str
    change_7d: float | None = None
    source: str = "public_signal"
    source_mode: str = "sample"

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class Recommendation:
    destination: str
    score: float
    confidence: float
    opportunity: float
    risk: float
    reasons: list[str]
    recommended_channels: list[str]
    evidence: list[JsonDict]

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class Campaign:
    campaign_id: str
    theme: str
    target: str
    destination: str
    objective: str
    channels: list[str]
    cta: str
    evidence: list[str]

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass(frozen=True)
class GeneratedAssets:
    instagram: str
    facebook: str
    naver_blog: str
    image_prompt: str
    landing_summary: str
    assets: JsonDict


@dataclass(frozen=True)
class WorkflowResult:
    week: str
    report_dir: Path
    recommendation_path: Path
    campaign_path: Path
    submission_path: Path | None
    issues: list[str]

    def to_dict(self) -> JsonDict:
        data = asdict(self)
        data["report_dir"] = str(self.report_dir)
        data["recommendation_path"] = str(self.recommendation_path)
        data["campaign_path"] = str(self.campaign_path)
        data["submission_path"] = str(self.submission_path) if self.submission_path else None
        return data
