from __future__ import annotations

import argparse
import json
from typing import Sequence

from campaign_copilot.config import default_config
from campaign_copilot.models import WorkflowResult
from campaign_copilot.workflow import run_weekly_campaign


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = default_config()
    if args.command == "run-weekly":
        result = run_weekly_campaign(config)
        print_result(result, json_output=args.json)
        return 0
    if args.command in {"collect", "normalize", "analyze", "generate-campaign", "generate-report"}:
        result = run_weekly_campaign(config)
        print_result(result, json_output=args.json)
        return 0
    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="campaign-copilot",
        description="Generate MyRealTrip weekly campaign outputs from public evidence.",
    )
    parser.add_argument(
        "command",
        choices=[
            "run-weekly",
            "collect",
            "normalize",
            "analyze",
            "generate-campaign",
            "generate-report",
        ],
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable workflow paths and issues instead of the user summary.",
    )
    return parser


def print_result(result: WorkflowResult, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return
    result_path = result.report_dir / "result.md"
    print(result_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
