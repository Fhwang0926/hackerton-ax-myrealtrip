---
name: weekly-campaign-copilot
description: Generate MyRealTrip weekly campaign recommendations, channel drafts, and a static HTML report from public travel signals.
---

# Weekly Campaign Copilot

Use this skill when MyRealTrip marketing, MD, product, or content teams need a weekly travel campaign plan backed by public evidence.

## Data Policy

- Use public sources by default.
- Naver Blog RSS is the primary owned-channel live source.
- Instagram and Facebook profile URLs are public references, but post-level collection requires an owned-account export or API access. Without that input, use clearly labeled samples.
- Never present sample or fallback data as live evidence.
- Do not log API keys, tokens, passwords, or private customer data.

## Workflow

Run:

```bash
python -m campaign_copilot.cli run-weekly
```

After the command finishes, answer the user from `reports/result.md`.
Do not make the user inspect JSON files unless they explicitly ask for developer or validation data.

If Codex image generation is available and the user asks for images or image-ready assets:

- Use the prompts inside `reports/instagram.md`, `reports/facebook.md`, and `reports/naver_blog.md`.
- Save generated images to these exact paths:
  - `reports/assets/instagram-campaign.png`
  - `reports/assets/facebook-campaign.png`
  - `reports/assets/naver-blog-campaign.png`
- The markdown files already contain image preview links to those paths. Once the files are saved, the images display in the "이미지 표시 영역".
- If image generation is unavailable, leave the prompts in place and tell the user they can generate images from those prompts later.

Pipeline:

Collector -> Normalizer -> Trend Engine -> Campaign Planner -> Content Generator -> HTML Report

## User Response Template

Reply in Korean and keep the result readable for non-developers.
Use this order:

1. 생성 완료
2. 이번 주 추천 1순위와 점수
3. 추천 이유 3개
4. 먼저 볼 파일: `reports/index.html`, `reports/instagram.md`, `reports/facebook.md`, `reports/naver_blog.md`
5. 참고사항: 실데이터와 샘플 사용 여부

Mention `reports/data.json`, `reports/recommendation.json`, and `reports/campaign.json` only as developer or validation files.
Do not include them in the default "main outputs" list.

## Outputs

The command writes:

- `reports/index.html`
- `reports/style.css`
- `reports/app.js`
- `reports/data.json`
- `reports/result.md`
- `reports/report.md`
- `reports/campaign.json`
- `reports/recommendation.json`
- `reports/instagram.md`
- `reports/facebook.md`
- `reports/naver_blog.md`
- `reports/image_prompt.md`
- `reports/assets/*.png` when Codex image generation is available and image assets are generated
- `submission.zip`

## Verification

Run the Python tests and the weekly command from the plugin root. The HTML report is static and does not require Node.js, a browser server, or internet access after generation.
