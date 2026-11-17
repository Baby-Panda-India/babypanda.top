# babypanda.top

The Baby Panda Treks website: a trek journal plus a page for Thadam, our offline trail companion. It's served by GitHub Pages from `main` at https://babypanda.top.

## Editing

The pages are plain static HTML generated from one data file:

- `_src/treks.py` holds every trek (name, place, range, date, story, facts, Instagram links, approximate map pin).
- `_src/build.py` holds the page templates.

After changing either file, rebuild and commit the output:

```bash
python _src/build.py
```

The script writes `index.html`, `treks/index.html`, one `treks/<slug>.html` per trek, and `404.html`. GitHub Pages' Jekyll ignores `_src/`.

Styles are in `assets/css/site.css` and the small progressive-enhancement script is `assets/js/site.js`. The trek map lazy-loads MapLibre with OpenFreeMap tiles, which are free and need no API key.

## Adding a trek

Add an entry to `_TREKS` in `_src/treks.py` with the next `num` (BPT number; the list is sorted by it), run the build, and commit.
