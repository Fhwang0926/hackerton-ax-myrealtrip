from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from campaign_copilot import cli
from campaign_copilot.analyze import analyze_trends
from campaign_copilot.collectors import NaverBlogCollector
from campaign_copilot.config import AppConfig, plugin_root
from campaign_copilot.generate import generate_assets
from campaign_copilot.models import CollectContext
from campaign_copilot.normalize import normalize_results
from campaign_copilot.plan import plan_campaign
from campaign_copilot.workflow import run_weekly_campaign


class PipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = plugin_root()
        self.week_start = __import__("datetime").date(2026, 7, 6)
        self.week_end = __import__("datetime").date(2026, 7, 12)

    def test_naver_blog_sample_collector_returns_items(self) -> None:
        collector = NaverBlogCollector(self.root / "data" / "samples")
        context = CollectContext(
            week_start=self.week_start,
            week_end=self.week_end,
            output_dir=self.root / "data" / "raw",
            use_live=False,
            use_sample=True,
        )
        result = collector.collect(context)
        self.assertTrue(result.ok)
        self.assertGreaterEqual(len(result.items), 5)
        self.assertEqual(result.meta["source_mode"], "sample")

    def test_normalizer_splits_owned_content_and_public_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config_for(Path(tmp), package_submission=False)
            result = run_weekly_campaign(config)
            self.assertTrue(result.recommendation_path.exists())
            content_path = config.data_dir / "normalized" / "content_items.jsonl"
            signal_path = config.data_dir / "normalized" / "public_signals.jsonl"
            self.assertTrue(content_path.exists())
            self.assertTrue(signal_path.exists())

    def test_analyzer_recommends_evidence_backed_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config_for(Path(tmp), package_submission=False)
            results = run_weekly_campaign(config)
            self.assertTrue(results.campaign_path.exists())
            self.assertGreaterEqual(len(results.issues), 1)

    def test_content_generator_includes_cta(self) -> None:
        collector = NaverBlogCollector(self.root / "data" / "samples")
        context = CollectContext(
            week_start=self.week_start,
            week_end=self.week_end,
            output_dir=self.root / "data" / "raw",
            use_live=False,
            use_sample=True,
        )
        contents, signals = normalize_results([collector.collect(context)])
        recommendations = analyze_trends(contents, signals)
        campaign = plan_campaign("2026-W28", recommendations)
        assets = generate_assets(campaign, recommendations)
        self.assertIn(campaign.cta, assets.instagram)
        self.assertIn(campaign.cta, assets.facebook)
        self.assertIn(campaign.cta, assets.naver_blog)
        for body in [assets.instagram, assets.facebook, assets.naver_blog]:
            self.assertIn("## 첨부 이미지", body)
            self.assertIn("## 복사 영역", body)
            self.assertIn("## 이미지 생성 프롬프트", body)
            self.assertIn("## 이미지 표시 영역", body)
        self.assertIn("Instagram 4:5", assets.image_prompt)
        self.assertIn("Facebook 1.91:1", assets.image_prompt)
        self.assertIn("Naver Blog 16:9", assets.image_prompt)
        self.assertIn("assets/instagram-campaign.png", assets.instagram)
        self.assertIn("![인스타그램 캠페인 이미지](./assets/instagram-campaign.png)", assets.instagram)
        self.assertIn("assets/facebook-campaign.png", assets.facebook)
        self.assertIn("![페이스북 캠페인 이미지](./assets/facebook-campaign.png)", assets.facebook)
        self.assertIn("assets/naver-blog-campaign.png", assets.naver_blog)
        self.assertIn("![네이버 블로그 대표 이미지](./assets/naver-blog-campaign.png)", assets.naver_blog)
        self.assertIn("reports/assets/instagram-campaign.png", assets.image_prompt)

    def test_weekly_workflow_writes_required_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config_for(Path(tmp), package_submission=False)
            result = run_weekly_campaign(config)
            required = [
                "index.html",
                "style.css",
                "app.js",
                "data.json",
                "result.md",
                "report.md",
                "campaign.json",
                "recommendation.json",
                "instagram.md",
                "facebook.md",
                "naver_blog.md",
                "image_prompt.md",
            ]
            for filename in required:
                self.assertTrue((result.report_dir / filename).exists(), filename)
            self.assertTrue((result.report_dir / "assets").is_dir())
            result_text = (result.report_dir / "result.md").read_text(encoding="utf-8")
            self.assertIn("이번 주 추천 1순위", result_text)
            self.assertIn("먼저 볼 파일:", result_text)
            self.assertNotIn("추천 JSON", result_text)

    def test_cli_prints_user_summary_by_default_and_json_on_request(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config_for(Path(tmp), package_submission=False)
            with patch("campaign_copilot.cli.default_config", return_value=config):
                text_output = io.StringIO()
                with contextlib.redirect_stdout(text_output):
                    self.assertEqual(cli.main(["run-weekly"]), 0)
                self.assertIn("생성 완료했습니다.", text_output.getvalue())
                self.assertIn("먼저 볼 파일:", text_output.getvalue())
                self.assertNotIn('"recommendation_path"', text_output.getvalue())

                json_output = io.StringIO()
                with contextlib.redirect_stdout(json_output):
                    self.assertEqual(cli.main(["run-weekly", "--json"]), 0)
                self.assertIn('"recommendation_path"', json_output.getvalue())

    def config_for(self, tmp: Path, package_submission: bool) -> AppConfig:
        return AppConfig(
            root=self.root,
            data_dir=tmp / "data",
            sample_dir=self.root / "data" / "samples",
            report_dir=tmp / "reports",
            use_live=False,
            use_sample=True,
            package_submission=package_submission,
        )


if __name__ == "__main__":
    unittest.main()
