# PEP Grade 6 English (Upper) · Integrated Knowledge Training Camp

**Sunshine Life Team (旭日长空光照人生)**

An **offline-first web learning system** for the 2024/2026 revised PEP Grade 6 English textbook (Book 1): bilingual reading, knowledge lectures, practice modules, wrong-answer book, dual-track points, and LAN multi-device sync. Run **`启动.bat`** (or `start.bat` equivalent) to serve at `http://localhost:8080`.

> **中文文档**：[README.md](./README.md) · **Changelog**：[CHANGELOG.md](./CHANGELOG.md) · **Contributing**：[CONTRIBUTING.md](./CONTRIBUTING.md)

---

## Quick start

| Step | Action |
|------|--------|
| 1 | Double-click **`启动.bat`** (imports cards, syncs reading content, starts server) |
| 2 | Open **`http://localhost:8080`** |
| 3 | Save nickname on the right → tap **「同步数据」** on other devices |

**Phone (same Wi‑Fi)**: `http://{PC-IPv4}:8080` — use `ipconfig`, not `localhost`.

**Distribution**: run `sync-release.bat`, then ZIP the `release/` folder.

---

## Modules

| Module | Description |
|--------|-------------|
| Flashcards | Appendix vocabulary; unit filter; parent grading |
| Grammar / Phrases | Sentence patterns and expressions |
| Quiz / Fill-in / Writing | Practice — **no auto TTS, no auto next question** |
| Irregular verbs | **47** verbs from Appendix 5 (`data/practice/irregular-verbs.json`) |
| Bilingual reading | Text + image; TTS only via **「朗读」** (chains within current page) |
| Knowledge lectures | 10-step structure; fill Q&A + writing models per U1–U6 Part |
| Wrong-answer book / Journal | Auto capture; unit filter |
| Points / Parent PIN | Auto scoring for drills; behavior points & redemption need PIN |

See [FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md) §1.5 for interaction rules.

---

## Documentation

| File | Audience |
|------|----------|
| [FINAL_PRODUCT_MANUAL.md](./FINAL_PRODUCT_MANUAL.md) | Teachers, parents, maintainers |
| [PARENT_GUIDE.md](./PARENT_GUIDE.md) | Parents only (do not share PIN rules with students) |
| [DEPLOY.md](./DEPLOY.md) | Static hosting (no LAN sync API on public web) |
| [data/question-banks/README.md](./data/question-banks/README.md) | Question bank maintenance |
| [data/study-hub/README.md](./data/study-hub/README.md) | Reading & lecture content |
| [CHANGELOG.md](./CHANGELOG.md) | **All notable changes (required on every merge)** |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | **PR workflow & review policy** |

---

## Project layout (summary)

```
├── 启动.bat, index.html, app.js, study-hub.js, styles.css
├── data/question-banks/     # Default quiz / fill / writing JSON
├── data/practice/           # supplement.json (OR-merge), irregular-verbs.json (47)
├── data/study-hub/          # reading + knowledge banks, 112 + 26 HTML pages
├── scripts/                 # Generators & validators (Python)
├── assets/images/textbook/  # ~131 MB page PNGs
├── release/                 # Distributable mirror
└── .cursor/skills/pep6-knowledge-lecture/
```

**Scale (approx.)**: ~398 MB total · ~790 files · 112 reading pages · 26 lecture pages.

---

## Maintenance commands

```powershell
python scripts/generate_u12_knowledge.py      # U1–U6 lectures (u3-k-part-b: append-only)
python scripts/build_practice_supplement.py   # Appendix 2–5 → supplement.json
python scripts/validate_appendix_coverage.py  # 142 / 55 / 47 coverage check
sync-release.bat
```

**Data safety**: merge banks **by id**; never wholesale overwrite. Protected benchmark: `u3-k-part-b.html` body.

---

## Governance (from 2026-08-01)

1. Every merge must update **`CHANGELOG.md`** under `[Unreleased]`.
2. Merges require **maintainer review** (see [CONTRIBUTING.md](./CONTRIBUTING.md)).
3. Use the [PR template](.github/pull_request_template.md) checklist.

---

## Cursor Skill & MCP

| Item | Location |
|------|----------|
| Skill `pep6-knowledge-lecture` | `.cursor/skills/pep6-knowledge-lecture/SKILL.md` |
| Project MCP | **None** in this repo (no `.cursor/mcp.json`) |

---

## Version

- **Current release**: [1.0.0] — 2026-08-01 (see [CHANGELOG.md](./CHANGELOG.md))
- **Textbook**: PEP Grade 6 English, Book 1 (2026 fall revision)

**Sunshine Life Team**
