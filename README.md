# The Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rfebiago/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rfebiago/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

Entry for make.fun competition
`the-passport-page-of-a-countr-2-20261121-0318` — an invented passport
spread, drawn programmatically and written to `/output/entry.png`.

## What it is

A 1024×1024 passport spread for the **Republic of Kavara**, a fictional
South Pacific atoll nation with no airport. The left page is the data
page: a stylised portrait of holder Mereana Sela Tavake, her personal
details, a machine-readable zone, a chart of the nine atolls, and a red
endorsement — *"NOT VALID FOR TRAVEL BY AIR — SEA PASSAGE ONLY
(Islands Act 1987, s.4)"* — the detail that tells you what kind of place
Kavara is. The right page is the visas page: six arrival/departure
stamps from Fiji, Tonga and New Zealand (all dated after the passport's
issue, in chronological order, each trip a 14–15 day sea voyage), a
ferry-tax stamp, and the issuing officer's remarks.

## How it works

- `draw_passport.py` (build-time only, Pillow) draws `entry.png` from
  the fixed dataset in the script. Deterministic: no randomness, no
  clock, no network.
- `main.py` (standard library only) copies `entry.png` byte-for-byte
  to `/output/entry.png`, after checking it is a whole PNG within the
  1 MiB / 1024×1024 caps. This is what the grader runs.

## Verify locally

```sh
python3 draw_passport.py   # rebuild entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
file /tmp/out/entry.png    # PNG image data, 1024 x 1024
```

## License

MIT — see `LICENSE`.
