# Markdown Preview Palettes Project Tracker

| Field | Value |
| --- | --- |
| Owner | Sean Yang |
| Status | Active |
| Version | 2.2.0 |
| Last Updated | 2026-11-05 |
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
  - [4.5. Phase 5: Release 0.2.0](#45-phase-5-release-020)
- [5. Decisions](#5-decisions)
- [6. Progress Log](#6-progress-log)
- [7. Open Items](#7-open-items)
- [8. Sources](#8-sources)
- [9. Changelog](#9-changelog)

## 1. Key Points

- **Status:** version 0.1.0 is published on the Marketplace as `ToadishFrog67.markdown-preview-colours` ("Markdown Preview Palettes (Toadish)") and installed from there on the Linux machine and the Mac [S8](#8-sources) [S13](#8-sources). Version 0.2.0 (GitHub-style tables, 5 new presets) is merged on `main` and ready to build [S12](#8-sources).
- **Next:** Phase 5 on the Linux machine: build, test and upload 0.2.0; then the Mac updates from the Marketplace. The friend install (step 4.1) is still open.
- **Publishing:** the VS Code Marketplace lists no publishing fee. A `.vsix` can be uploaded on the publisher web page, so no access token is needed [S1](#8-sources).

## 2. Goal and Scope

| Item | Detail |
| --- | --- |
| Goal | Colour presets for the built-in VS Code Markdown preview, installable with one click from the Marketplace [S2](#8-sources) |
| Users | The owner (Sean Yang) and a friend using VS Code [S2](#8-sources) |
| Presets | `teal`, `plum`, `crimson`, `golden`, `mono` [S2](#8-sources); `phosphor`, `parchment`, `azure`, `ember`, `folio` from 0.2.0 [S10](#8-sources); plus `default` to restore the built-in look |
| In scope | Headings, bold text, inline code, quotes, links; body text colour, GitHub-style tables, link underlines (from 0.2.0) [S10](#8-sources); dark and light themes; CI with formatting, lint, tests and a package build [S2](#8-sources) |
| Out of scope | GitHub bots (Dependabot or similar), automated publishing, changes to Markdown files, code block colours [S2](#8-sources); fonts [S10](#8-sources) |

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
| 1.1 | Create the project folder | Sean Yang | Done | 2026-10-13 |
| 1.2 | Presets, generated stylesheet, contrast check | Sean Yang | Done | 2026-10-13 |
| 1.3 | Unit tests and CI workflow | Sean Yang | Done: Python tests and Ruff pass locally; Node tests and Markdown lint run in CI only [S5](#8-sources) | 2026-10-13 |
| 1.4 | Replace the old single-style build on the Mac with 0.1.0 (`teal` preset, same look) | Sean Yang | Done | 2026-10-13 |

### 4.2. Phase 2: Move to GitHub

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 2.1 | Create the repository with the personal account | Sean Yang | Done [S6](#8-sources) | 2026-10-14 |
| 2.2 | Give the Mac's GitHub account write access | Sean Yang | Done [S2](#8-sources) | 2026-10-14 |
| 2.3 | Push the project from the Mac, on top of the repository's first commit | Sean Yang | Done [S6](#8-sources) | 2026-10-14 |
| 2.4 | Check the first CI run in the Actions tab | Sean Yang | Done: all steps passed [S7](#8-sources) | 2026-10-14 |

### 4.3. Phase 3: Linux Setup and Publishing

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 3.1 | Keyboard for the Linux machine | Sean Yang | Open | |
| 3.2 | Clone the repository; install VS Code, Python 3, Git, Node.js LTS | Sean Yang | Done: VS Code 1.142.0, Node.js 24.18.0 [S9](#8-sources) | 2026-10-18 |
| 3.3 | Create the Marketplace publisher with a personal Microsoft account | Sean Yang | Done: `ToadishFrog67` [S8](#8-sources) | 2026-10-19 |
| 3.4 | Set the publisher ID in `package.json`, build, test | Sean Yang | Done: built with `vsce` 4.0.0, tests pass [S9](#8-sources) | 2026-10-19 |
| 3.5 | Upload the `.vsix` on the publisher web page | Sean Yang | Done: published and installed from the Marketplace [S8](#8-sources) | 2026-10-19 |

Steps 3.2 to 3.5 are detailed in `docs/release-guide.md`.

### 4.4. Phase 4: Install and Hand-Over

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 4.1 | Friend installs from the Extensions panel and picks a preset | Friend | Open | |
| 4.2 | On the Mac: uninstall the local build and install the Marketplace version | Sean Yang | Done: only the Marketplace version is installed [S13](#8-sources) | 2026-11-05 |

### 4.5. Phase 5: Release 0.2.0

| # | Step | Owner | Status | Date |
| --- | --- | --- | --- | --- |
| 5.1 | GitHub-style tables (pull request #1) | Sean Yang | Done: CI passed, merged [S12](#8-sources) | 2026-11-05 |
| 5.2 | Presets `phosphor`, `parchment`, `azure`, `ember`, `folio` and new preset keys (pull request #2) | Sean Yang | Done: CI passed, merged [S12](#8-sources) | 2026-11-05 |
| 5.3 | Version 0.2.0, dated changelog, release guide test step (release pull request) | Sean Yang | Done [S12](#8-sources) | 2026-11-05 |
| 5.4 | On Linux: pull `main`, `make test`, build with `npx @vscode/vsce@4.0.0 package` | Sean Yang | Open | |
| 5.5 | Test the `.vsix` in a throwaway VS Code profile (release guide, Build and Test) | Sean Yang | Open | |
| 5.6 | Upload with **Update** on the publisher page | Sean Yang | Open | |
| 5.7 | Mac and Linux update to 0.2.0 from the Marketplace | Sean Yang | Open | |

## 5. Decisions

| # | Decision | Choice | Status |
| --- | --- | --- | --- |
| D1 | Ownership | Sean Yang, sole owner [S2](#8-sources) | Decided |
| D2 | Preset mechanism | A setting picks the preset; a hidden marker plus one generated stylesheet apply it [S2](#8-sources) [S3](#8-sources) | Decided |
| D3 | Preset list | `teal`, `plum` (Slack-style), `crimson` (red, Arasaka-style), `golden` (black and gold, Arasaka-style), `mono`, `default` [S2](#8-sources) | Decided |
| D4 | Brand names | Not used in names, descriptions or keywords, to avoid trademark complaints | ⚠️ Inferred from trademark risk; Unconfirmed, Sean Yang can confirm |
| D5 | Preset for new installs | `teal` [S2](#8-sources) | Decided |
| D6 | Extension name and setting key | Name `markdown-preview-colours`, display name "Markdown Preview Palettes (Toadish)", setting `markdownPreviewPalettes.preset` (unchanged). The original name `markdown-preview-palettes` was removed from the Marketplace and is permanently reserved [S1](#8-sources) [S8](#8-sources) | Decided |
| D7 | Publisher ID | `ToadishFrog67`. A second publisher held the first, removed upload [S8](#8-sources) | Decided |
| D8 | Publishing route | `.vsix` uploaded on the Marketplace publisher web page; no access token [S1](#8-sources) | Decided |
| D9 | Moving files to GitHub | Direct push from the Mac with a GitHub account that has write access; the owner account's credentials are not stored on the Mac [S2](#8-sources) | Decided |
| D10 | CI | GitHub Actions: formatting, lint, tests, package build; no bots, no publishing [S2](#8-sources) | Decided |
| D11 | Licence | MIT, holder "Warm Frog", from the repository's own `LICENSE`. The package build requires the file [S6](#8-sources) | Decided |
| D12 | Near-black backgrounds for `crimson` and `golden` (dark theme) | Yes [S2](#8-sources) | Decided |
| D13 | Repository history | Clean start: the project commits sit on top of the repository's first commit; no earlier history is kept [S2](#8-sources) | Decided |
| D14 | Published build | Packaged with Microsoft's `vsce`, not `scripts/build.py`; `activationEvents` set to `onLanguage:markdown`, which `vsce` requires [S9](#8-sources) | Decided |
| D15 | Colours from outside sources | `ember` and `parchment` use the palette in the Apache 2.0 brand-guidelines skill, credited in the README; `folio` uses colours sampled from the Claude Platform Docs; no Anthropic or Claude names in preset names or descriptions [S10](#8-sources) [S11](#8-sources) | Decided |
| D16 | `ember` dark background | Pure black `#000000`, not the palette's `#141413` [S10](#8-sources) | Decided |
| D17 | Fonts | Not part of 0.2.0; options researched, no decision [S10](#8-sources) | Deferred |

## 6. Progress Log

| Date | Entry |
| --- | --- |
| 2026-10-13 | Project created. Version 0.1.0 built: 5 presets plus `default`, all passing the contrast check [S5](#8-sources). |
| 2026-10-13 | Teal light theme: H3, H4 and H5 darkened to pass the contrast minimum; the dark theme is unchanged [S5](#8-sources). |
| 2026-10-13 | CI added with pinned tools at least 2 weeks old [S4](#8-sources). |
| 2026-10-13 | Mac switched from the old single-style build to 0.1.0. |
| 2026-10-14 | Restarted on a new repository with a clean history. Upload-only build code and local leftovers removed; project pushed from the Mac [S2](#8-sources) [S6](#8-sources). |
| 2026-10-19 | First upload went to a second publisher and was then removed, which reserved the name `markdown-preview-palettes` for good. Republished under `ToadishFrog67` as `markdown-preview-colours` with the icon; installed from the Marketplace on Linux [S8](#8-sources) [S9](#8-sources). |
| 2026-11-05 | Tables switched to the GitHub style; 5 presets added, with optional keys for body text, inline-code box and link underline; all 10 presets pass the contrast check. Merged as pull requests #1 and #2; version set to 0.2.0 [S10](#8-sources) [S12](#8-sources). |

## 7. Open Items

| # | Item | Owner | Next action |
| --- | --- | --- | --- |
| O4 | Visual check of every preset in both themes | Sean Yang | Open `test/sample.md` and switch presets |
| O5 | Unused second publisher | Sean Yang | Delete it on the publisher page if no longer needed |

Closed 2026-10-19: O1 (publisher ID, see D7); O2 (published build uses `vsce`, see D14; whether the Marketplace accepts the `scripts/build.py` package was never tested); O3 (`icon.png`, 128 px PNG).

## 8. Sources

| ID | Supports | Evidence | Source | Status |
| --- | --- | --- | --- | --- |
| S1 | [1. Key Points](#1-key-points), [D8](#5-decisions), [O3](#7-open-items): publishing cost, web upload, icon rules | No publishing fee mentioned; `.vsix` can be uploaded on the publisher management page; global Azure DevOps access tokens retire on December 1, 2026; no SVG icons; names must be unique; a removed extension's name "is permanently reserved and cannot be reused, even by the original publisher" | "Publishing Extensions", <https://code.visualstudio.com/api/working-with-extensions/publishing-extension>, read 2026-10-13 and 2026-10-19 | Sourced |
| S2 | [2. Goal and Scope](#2-goal-and-scope), [4.2. Phase 2](#42-phase-2-move-to-github), [5. Decisions](#5-decisions): goal, users, presets, CI scope, GitHub route | Sole owner; presets and their themes; account setup on the Linux machine; CI without bots; decisions D5, D6, D7, D12; O2 deferred (2026-10-13). New repository; a second GitHub account given push access and used to push from the Mac; start from scratch with no earlier history (2026-10-14) | Sean Yang, 2026-10-13 and 2026-10-14 | Sourced |
| S3 | [D2](#5-decisions): how presets reach the preview | Links use `--vscode-textLink-foreground`; preview body background is transparent; the Markdown extension activates plugin extensions and renders with `renderer.render` | VS Code 1.141.0 built-in files (`markdown-language-features`, webview `index.html`), observed 2026-10-13 | Sourced |
| S4 | [6. Progress Log](#6-progress-log): pinned tool versions | Ruff 0.16.8 (2026-09-16); markdownlint-cli2 0.23.3 (2026-09-20); `actions/checkout`, `setup-python`, `setup-node`, `upload-artifact` major version 7 | PyPI, npm registry and GitHub releases, read 2026-10-13 | Sourced |
| S5 | [1. Key Points](#1-key-points), [6. Progress Log](#6-progress-log): contrast results and test runs | All presets pass; old Teal light H3 3.12:1, H4 2.75:1, H5 4.48:1 (minimum 4.5:1); 10 Python tests pass; Ruff clean | `scripts/build.py check` and `python3 -m unittest`, run 2026-10-13 and 2026-10-14 | Sourced |
| S6 | [4.2. Phase 2](#42-phase-2-move-to-github), [D11](#5-decisions): repository and licence | Repository created 2026-10-14 with one "Initial commit" holding an MIT `LICENSE`, "Copyright (c) 2026 Warm Frog"; project commits pushed on top | GitHub, toadish-frog/markdown-preview-palettes, observed 2026-10-14 | Sourced |
| S7 | [1. Key Points](#1-key-points), [4.2. Phase 2](#42-phase-2-move-to-github): first CI run | Conclusion "success" on every step: Ruff, Markdown lint, syntax, Python and extension tests, CSS up to date, package build, artifact upload | GitHub Actions run 38507586464, toadish-frog/markdown-preview-palettes, commit `6695fec` (hash before the 2026-10-19 history rewrite), 2026-10-14 | Sourced |
| S8 | [1. Key Points](#1-key-points), [4.3. Phase 3](#43-phase-3-linux-setup-and-publishing), [D6](#5-decisions), [D7](#5-decisions): publishing | Two publishers created, `ToadishFrog67` and a second one; first upload removed; republished under `ToadishFrog67` as `markdown-preview-colours`; installed from the Marketplace | Sean Yang, 2026-10-19 | Sourced |
| S9 | [4.3. Phase 3](#43-phase-3-linux-setup-and-publishing), [D14](#5-decisions): Linux tools and build | VS Code 1.142.0, Node.js 24.18.0; `vsce` 4.0.0 refused the manifest without `activationEvents`, then packaged it; Python and extension tests pass | `code --version`, `npx @vscode/vsce@4.0.0 package`, `make test`, run 2026-10-18 and 2026-10-19 | Sourced |
| S10 | [2. Goal and Scope](#2-goal-and-scope), [D15](#5-decisions) to [D17](#5-decisions), [6. Progress Log](#6-progress-log): 0.2.0 scope | GitHub-style tables requested; 3 presets modelled on another extension's themes, then an orange preset and a preset in the Claude docs colours; brand colours only if not restricted; `ember` dark kept black; fonts set aside | Sean Yang, 2026-11-05 | Sourced |
| S11 | [D15](#5-decisions): palette licence | Palette listed as Light `#faf9f5`, Dark `#141413`, Mid Gray `#b0aea5`, Light Gray `#e8e6dc`, Orange `#d97757`, Blue `#6a9bcc`, Green `#788c5d`; folder licence is Apache 2.0, which grants no trademark rights; Claude docs colours read from the rendered pages | brand-guidelines `SKILL.md` and `LICENSE.txt`, <https://github.com/anthropics/skills/tree/main/skills/brand-guidelines>; <https://platform.claude.com/docs/en/intro> and `/build-with-claude/streaming`; read 2026-11-05 | Sourced |
| S12 | [1. Key Points](#1-key-points), [4.5. Phase 5](#45-phase-5-release-020): pull requests | Pull requests #1 and #2: CI passed, squash-merged; release pull request sets 0.2.0 | GitHub, toadish-frog/markdown-preview-palettes, pull requests #1 and #2, 2026-11-05 | Sourced |
| S13 | [1. Key Points](#1-key-points), [4.4. Phase 4](#44-phase-4-install-and-hand-over): Mac install | `toadishfrog67.markdown-preview-colours@0.1.0` is the only copy of the extension | `code --list-extensions --show-versions` on the Mac, run 2026-11-05 | Sourced |

Gaps: step 3.1 (keyboard) and O4 (visual check) have no record yet.

## 9. Changelog

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| 2.2.0 | 2026-11-05 | Phase 5 (release 0.2.0) added; step 4.2 done; scope, Key Points and log updated; D15 to D17 and S10 to S13 added | Tables and 5 presets merged; version 0.2.0 prepared for the Linux build |
| 2.1.0 | 2026-10-19 | Steps 3.2 to 3.5 done; D6 and D7 decided, D14 added; O1 to O3 closed, O5 added; log entry; S1 updated, S8 and S9 added; account details removed from 1.1, 2.2, 2.3, D9, the log and S2; S7 hash marked as pre-rewrite | First publish on the Marketplace; commit history rewritten to a no-reply email |
| 2.0.1 | 2026-10-14 | Step 2.4 done; first CI result added as S7; open items renumbered | First CI run on the new repository passed |
| 2.0.0 | 2026-10-14 | Phase 2 rewritten for a direct push to a new repository; browser-upload steps, staging, rollback copy and earlier-repository records removed; D9 and D11 updated, D13 added; open items renumbered; sources renumbered (GitHub upload limits and the earlier CI run removed, new repository added); step owners set to Sean Yang | Sean Yang restarted the project on a new repository with a clean history |
| 1.0.2 | 2026-10-13 | First CI result recorded | First CI run failed at Markdown lint |
| 1.0.1 | 2026-10-13 | Phase 2 steps and decisions D5, D6, D7, D11, D12 updated | Sean Yang confirmed decisions |
| 1.0.0 | 2026-10-13 | Created: scope, structure, phases, decisions, log, open items, sources | Sean Yang asked for a tracked, documented project |
