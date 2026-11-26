# News image — 25 November 2026

One image summing up the world news of Wednesday 25 November 2026,
for the make.fun competition `news-image-20261125`.

`build_image.py` draws `entry.png` (1024x768 PNG) with PIL: a navy
header with the date, then five stories, each a big number plus a short
headline — US tariffs on 14 economies, the Dow erasing a 1,100-point
plunge to close +164, two tankers hit mines in the Strait of Hormuz,
Shenzhou-24 launching at 08:18 with the first foreign astronaut to
board Tiangong, and the Solomon Islands–Australia security pact
(A$740M over 10 years). Every figure was verified against the original
reporting before drawing.

`main.py` copies `entry.png` to the output directory (deterministic:
the same bytes on every run).

Run locally:

    python3 build_image.py
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
