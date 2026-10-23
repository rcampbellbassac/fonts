# Fonts

**Every font in one place:** {{COUNT}} free display fonts for Lao, Thai, Khmer and English, each with
samples, its own page, its source repo and a download. All are licensed under the
[SIL Open Font License 1.1](https://openfontlicense.org).

**See them all:** https://rcampbellbassac.github.io/fonts/

| Font | Native name | Style | Scripts | Version | Links |
|---|---|---|---|---|---|
{{TABLE}}

## Adding or updating a font

`fonts.json` is the registry; the page and this table are built from it. When a font is made public, or a
new version is released, register it in the same change:

```sh
python3 tools/register.py --id MyFont --name "My Font" --native "..." --native-lang lo \
    --category painted --scripts lo,th,km,latn --version 0.100 --status beta \
    --description "One line about the font" --made-by "Robert Campbell, Claude"
python3 tools/register.py --id MyFont --version 0.200          # a later release: only what changed
python3 tools/register.py --check                               # validate before committing
```

The defaults assume the usual layout: GitHub Pages at `https://rcampbellbassac.github.io/<Id>/`, a web
font at `docs/fonts/<Id>-Regular.woff2`, and a release asset `<Id>.zip`. Pass `--site`, `--woff2` or
`--download` if a font differs. Commit `fonts.json` and `README.md` together.
