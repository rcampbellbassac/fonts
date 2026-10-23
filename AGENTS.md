# Rules for AI agents (Claude, Codex, Antigravity/agy, Copilot)

This repo is the master list of Robert's public fonts. Its page is https://rcampbellbassac.github.io/fonts/.

- **New public font:** in the same session that makes a font repo public, register it:
  `python3 tools/register.py --id <Repo> --name ... --native ... --native-lang lo|th|km --category ... --scripts lo,th,km,latn --version ... --description ... --made-by ...`
- **New release or version:** update its entry (`python3 tools/register.py --id <Repo> --version <new>`, plus any changed field).
  A renamed, moved or retired font gets updated too (`--status retired` keeps the history; `--remove` deletes the entry).
- Run `python3 tools/register.py --check`, then commit `fonts.json` and `README.md` together and push.
- Only public fonts belong here. Drafts awaiting Robert's approval stay off this list.
- Check that the font's woff2 and download URLs answer 200 before pushing.
