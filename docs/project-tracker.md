# Markdown Preview Palettes Project Tracker

| Field | Value |
| --- | --- |
| Owner | Sean Yang |
| Status | Active |
| Version | 2.0.1 |
| Last Updated | 2026-10-14 |
| Audience | Sean Yang (personal notes) |
| Source(s) | See [Sources](#8-sources) |

## Contents <!-- omit from toc -->

- [1. Key Points](#1-key-points)
- [2. Goal and Scope](#2-goal-and-scope)
- [3. Project Structure](#3-project-structure)
- [4. Workflow and Progress](#4-workflow-and-progress)
  - [4.1. Phase 1: Build on the Mac](#41-phase-1-build-on-the-mac)
  - [4.2. Phase 2: Move to GitHub](#42-phase-2-move-to-github)
  - [4.3. Phase 3: Linux Setup and Publishing](#43-phase-3-linux-setup-and-publishing)
  - [4.4. Phase 4: Install and Hand-Over](#44-phase-4-install-and-hand-over)
- [5. Decisions](#5-decisions)
- [6. Progress Log](#6-progress-log)
- [7. Open Items](#7-open-items)
- [8. Sources](#8-sources)
- [9. Changelog](#9-changelog)

## 1. Key Points

- **Status:** version 0.1.0 is built, tested and installed on the Mac with the `teal` preset [S5](#8-sources). The project is on GitHub with a clean history, pushed from the Mac by the work account; the first CI run passed [S2](#8-sources) [S6](#8-sources) [S7](#8-sources).
- **Next:** continue on the Linux machine: publisher ID, build with Microsoft's tool, publish (Phase 3).
- **Publishing:** the VS Code Marketplace lists no publishing fee. A `.vsix` can be uploaded on the publisher web page, so no access token is needed [S1](#8-sources).

## 2. Goal and Scope

| Item | Detail |
| --- | --- |
| Goal | Colour presets for the built-in VS Code Markdown preview, installable with one click from the Marketplace [S2](#8-sources) |
| Users | The owner (Sean Yang) and a friend using VS Code [S2](#8-sources) |
| Presets | `teal`, `plum`, `crimson`, `golden`, `mono`, plus `default` to restore the built-in look [S2](#8-sources) |
| In scope | Headings, bold text, inline code, quotes, links; dark and light themes; CI with formatting, lint, tests and a package build [S2](#8-sources) |
| Out of scope | GitHub bots (Dependabot or similar), automated publishing, changes to Markdown files, code block colours [S2](#8-sources) |

## 3. Project Structure

| Path | Purpose | Shared on GitHub |
| --- | --- | --- |
| `package.json` | Extension manifest and the preset setting | Yes |
| `extension.js` | Adds a hidden preset marker to each preview | Yes |
| `media/preview.css` | Generated stylesheet; never edited by hand | Yes |
| `palettes/palettes.json` | Single source of every preset colour | Yes |
| `scripts/build.py` | Generates CSS, checks contrast, builds the `.vsix` | Yes |
| `test/` | Unit tests and `sample.md` for visual checks | Yes |
| `docs/` | This tracker and the release guide | Yes |
| `.github/workflows/ci.yml` | CI: formatting, lint, tests, package build | Yes |
| `README.md`, `CHANGELOG.md`, `LICENSE` | Marketplace page, release notes, MIT licence | Yes |
| `dist/` | Build output; ignored by Git | No |
| `private/` | Reserved for machine-specific notes; ignored by Git | No |

## 4. Workflow and Progress

### 4.1. Phase 1: Build on the Mac

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 1.1 | Create the project folder outside the work notes folder | Sean Yang | Done | 2026-10-13 |
| 1.2 | Presets, generated stylesheet, contrast check | Sean Yang | Done | 2026-10-13 |
| 1.3 | Unit tests and CI workflow | Sean Yang | Done: Python tests and Ruff pass locally; Node tests and Markdown lint run in CI only [S5](#8-sources) | 2026-10-13 |
| 1.4 | Replace the old single-style build on the Mac with 0.1.0 (`teal` preset, same look) | Sean Yang | Done | 2026-10-13 |

### 4.2. Phase 2: Move to GitHub

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 2.1 | Create the repository with the personal account | Sean Yang | Done [S6](#8-sources) | 2026-10-14 |
| 2.2 | Give the work account write access | Sean Yang | Done [S2](#8-sources) | 2026-10-14 |
| 2.3 | Push the project from the Mac with the work account, on top of the repository's first commit | Sean Yang | Done [S6](#8-sources) | 2026-10-14 |
| 2.4 | Check the first CI run in the Actions tab | Sean Yang | Done: all steps passed [S7](#8-sources) | 2026-10-14 |

### 4.3. Phase 3: Linux Setup and Publishing

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 3.1 | Keyboard for the Linux machine | Sean Yang | Open | |
| 3.2 | Clone the repository; install VS Code, Python 3, Git, Node.js LTS | Sean Yang | Open | |
| 3.3 | Create the Marketplace publisher with a personal Microsoft account | Sean Yang | Open | |
| 3.4 | Set the publisher ID in `package.json`, build, test | Sean Yang | Open | |
| 3.5 | Upload the `.vsix` on the publisher web page | Sean Yang | Open | |

Steps 3.2 to 3.5 are detailed in `docs/release-guide.md`.

### 4.4. Phase 4: Install and Hand-Over

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 4.1 | Friend installs from the Extensions panel and picks a preset | Friend | Open | |
| 4.2 | On the Mac: uninstall the local build and install the Marketplace version | Sean Yang | Open | |

## 5. Decisions

| # | Decision | Choice | Status |
| --- | --- | --- | --- |
| D1 | Ownership | Sean Yang, sole owner [S2](#8-sources) | Decided |
| D2 | Preset mechanism | A setting picks the preset; a hidden marker plus one generated stylesheet apply it [S2](#8-sources) [S3](#8-sources) | Decided |
| D3 | Preset list | `teal`, `plum` (Slack-style), `crimson` (red, Arasaka-style), `golden` (black and gold, Arasaka-style), `mono`, `default` [S2](#8-sources) | Decided |
| D4 | Brand names | Not used in names, descriptions or keywords, to avoid trademark complaints | ⚠️ Inferred from trademark risk; Unconfirmed, Sean Yang can confirm |
| D5 | Preset for new installs | `teal` [S2](#8-sources) | Decided |
| D6 | Extension name and setting key | `markdown-preview-palettes`, `markdownPreviewPalettes.preset`. Renaming later also renames the setting [S2](#8-sources) | Decided for now; review before the first publish |
| D7 | Publisher ID | Not chosen; `local` is a placeholder for local builds. To be chosen on the Linux machine after the keyboard arrives [S2](#8-sources) | Open: Sean Yang |
| D8 | Publishing route | `.vsix` uploaded on the Marketplace publisher web page; no access token [S1](#8-sources) | Decided |
| D9 | Moving files to GitHub | Direct push from the Mac with the work GitHub account, which has write access; no personal credentials on the Mac [S2](#8-sources) | Decided |
| D10 | CI | GitHub Actions: formatting, lint, tests, package build; no bots, no publishing [S2](#8-sources) | Decided |
| D11 | Licence | MIT, holder "Warm Frog", from the repository's own `LICENSE`. The package build requires the file [S6](#8-sources) | Decided |
| D12 | Near-black backgrounds for `crimson` and `golden` (dark theme) | Yes [S2](#8-sources) | Decided |
| D13 | Repository history | Clean start: the project commits sit on top of the repository's first commit; no earlier history is kept [S2](#8-sources) | Decided |

## 6. Progress Log

| Date | Entry |
| --- | --- |
| 2026-10-13 | Project created. Version 0.1.0 built: 5 presets plus `default`, all passing the contrast check [S5](#8-sources). |
| 2026-10-13 | Teal light theme: H3, H4 and H5 darkened to pass the contrast minimum; the dark theme is unchanged [S5](#8-sources). |
| 2026-10-13 | CI added with pinned tools at least 2 weeks old [S4](#8-sources). |
| 2026-10-13 | Mac switched from the old single-style build to 0.1.0. |
| 2026-10-14 | Restarted on a new repository with a clean history. Upload-only build code and local leftovers removed; project pushed with the work account [S2](#8-sources) [S6](#8-sources). |

## 7. Open Items

| # | Item | Owner | Next action |
| --- | --- | --- | --- |
| O1 | Decision D7 (publisher ID) | Sean Yang | On the Linux machine, before the first publish |
| O2 | Whether the Marketplace accepts the `.vsix` built by `scripts/build.py` | Sean Yang | Deferred [S2](#8-sources). Unconfirmed; the release guide uses Microsoft's packaging tool `vsce` for the published build |
| O3 | Optional icon (128 px PNG; SVG is not allowed) [S1](#8-sources) | Sean Yang | Decide before the first publish |
| O4 | Visual check of every preset in both themes | Sean Yang | Open `test/sample.md` and switch presets |

## 8. Sources

| ID | Supports | Evidence | Source | Status |
| --- | --- | --- | --- | --- |
| S1 | [1. Key Points](#1-key-points), [D8](#5-decisions), [O3](#7-open-items): publishing cost, web upload, icon rules | No publishing fee mentioned; `.vsix` can be uploaded on the publisher management page; global Azure DevOps access tokens retire on December 1, 2026; no SVG icons; names must be unique | "Publishing Extensions", <https://code.visualstudio.com/api/working-with-extensions/publishing-extension>, read 2026-10-13 | Sourced |
| S2 | [2. Goal and Scope](#2-goal-and-scope), [4.2. Phase 2](#42-phase-2-move-to-github), [5. Decisions](#5-decisions): goal, users, presets, CI scope, GitHub route | Sole owner; presets and their themes; account setup on the Linux machine; CI without bots; decisions D5, D6, D7, D12; O2 deferred (2026-10-13). New repository; work account given push access and used as the contributor; start from scratch with no earlier history (2026-10-14) | Sean Yang, 2026-10-13 and 2026-10-14 | Sourced |
| S3 | [D2](#5-decisions): how presets reach the preview | Links use `--vscode-textLink-foreground`; preview body background is transparent; the Markdown extension activates plugin extensions and renders with `renderer.render` | VS Code 1.141.0 built-in files (`markdown-language-features`, webview `index.html`), observed 2026-10-13 | Sourced |
| S4 | [6. Progress Log](#6-progress-log): pinned tool versions | Ruff 0.16.8 (2026-09-16); markdownlint-cli2 0.23.3 (2026-09-20); `actions/checkout`, `setup-python`, `setup-node`, `upload-artifact` major version 7 | PyPI, npm registry and GitHub releases, read 2026-10-13 | Sourced |
| S5 | [1. Key Points](#1-key-points), [6. Progress Log](#6-progress-log): contrast results and test runs | All presets pass; old Teal light H3 3.12:1, H4 2.75:1, H5 4.48:1 (minimum 4.5:1); 10 Python tests pass; Ruff clean | `scripts/build.py check` and `python3 -m unittest`, run 2026-10-13 and 2026-10-14 | Sourced |
| S6 | [4.2. Phase 2](#42-phase-2-move-to-github), [D11](#5-decisions): repository and licence | Repository created 2026-10-14 with one "Initial commit" holding an MIT `LICENSE`, "Copyright (c) 2026 Warm Frog"; project commits pushed on top | GitHub, toadish-frog/markdown-preview-palettes, observed 2026-10-14 | Sourced |
| S7 | [1. Key Points](#1-key-points), [4.2. Phase 2](#42-phase-2-move-to-github): first CI run | Conclusion "success" on every step: Ruff, Markdown lint, syntax, Python and extension tests, CSS up to date, package build, artifact upload | GitHub Actions run 38507586464, toadish-frog/markdown-preview-palettes, commit `6695fec`, 2026-10-14 | Sourced |

Gaps: whether a Marketplace upload accepts the self-built `.vsix` has no source (see O2).

## 9. Changelog

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| 2.0.1 | 2026-10-14 | Step 2.4 done; first CI result added as S7; open items renumbered | First CI run on the new repository passed |
| 2.0.0 | 2026-10-14 | Phase 2 rewritten for a direct push to a new repository; browser-upload steps, staging, rollback copy and earlier-repository records removed; D9 and D11 updated, D13 added; open items renumbered; sources renumbered (GitHub upload limits and the earlier CI run removed, new repository added); step owners set to Sean Yang | Sean Yang restarted the project on a new repository with a clean history |
| 1.0.2 | 2026-10-13 | First CI result recorded | First CI run failed at Markdown lint |
| 1.0.1 | 2026-10-13 | Phase 2 steps and decisions D5, D6, D7, D11, D12 updated | Sean Yang confirmed decisions |
| 1.0.0 | 2026-10-13 | Created: scope, structure, phases, decisions, log, open items, sources | Sean Yang asked for a tracked, documented project |
