# English interface

The interface is written in Spanish. In English, every text that reaches the page (HTML, tables, charts, messages,
the Excel report and the text copied for Excel) goes through `tr()`, which looks it up in `en.tsv`:

- one line per phrase: Spanish, a TAB, English; lines starting with `#` are comments;
- `{0}`, `{1}`… mark variable parts and may change order in English; `{#0}` matches only a number and `{t0}` a short
  name (one to three words);
- continuation fragments that start with `· ` also work on their own.

Whatever is not in the dictionary (taxon and site names, for instance) is left as is. `scripts/build.py` checks the
file (two columns, same placeholders on both sides, no pattern without fixed text) and embeds it in the page.
To add a language, the same mechanism would take a second dictionary.
