[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/pastikaiwayan28-cpu/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261119/pastikaiwayan28-cpu/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Day — Thursday 19 November 2026

A [make.fun](https://make.fun/bounty/news-image-20261119) news-image entry: one image that sums up Thursday 19 November 2026's world news.

**43 stories, 7 regions, a UTC timeline and a date check** — Trump, Xi & Putin meet in Shenzhen (first-ever trilateral), the Anthropic IPO, the ICJ ruling on Myanmar, APEC opens, GTA VI launches, and more, drawn as a newspaper front page legible at thumbnail size.

## How it works

`main.py` (Python 3.13, stdlib only) copies the drawn front page `entry.png` to `/output/entry.png`, byte for byte. The image was drawn by a build script (Pillow + DejaVu fonts) from the day's reporting; the program runs with no network, so the picture ships in the repo.

## Files

- `main.py` — entrypoint: copies `entry.png` to the output dir, validates PNG header, size and dimensions first.
- `entry.png` — the front page (1024×1024, ~220 KB).
- `LICENSE` — MIT.
