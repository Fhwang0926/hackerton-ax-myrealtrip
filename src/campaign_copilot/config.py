from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    root: Path
    data_dir: Path
    sample_dir: Path
    report_dir: Path
    use_live: bool = True
    use_sample: bool = True
    package_submission: bool = True
    max_items_per_source: int = 80


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_config() -> AppConfig:
    root = plugin_root()
    return AppConfig(
        root=root,
        data_dir=root / "data",
        sample_dir=root / "data" / "samples",
        report_dir=root / "reports",
    )


def current_week_window(today: date | None = None) -> tuple[date, date]:
    basis = today or date.today()
    start = basis - timedelta(days=basis.weekday())
    end = start + timedelta(days=6)
    return start, end


def week_label(day: date | None = None) -> str:
    basis = day or date.today()
    iso_year, iso_week, _ = basis.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"
