# Markdown Preview Palettes Release Guide

| Field | Value |
| --- | --- |
| Owner | Sean Yang |
| Status | Active |
| Version | 1.1.1 |
| Last Updated | 2026-11-05 |
| Audience | Sean Yang (personal notes) |
| Source(s) | See [Sources](#9-sources) |

## Contents <!-- omit from toc -->

- [1. Key Points](#1-key-points)
- [2. Prerequisites](#2-prerequisites)
- [3. First-Time Setup on Linux](#3-first-time-setup-on-linux)
- [4. Create the Marketplace Publisher](#4-create-the-marketplace-publisher)
- [5. Build and Test](#5-build-and-test)
- [6. Publish](#6-publish)
- [7. Release an Update](#7-release-an-update)
- [8. Install and Switch Machines](#8-install-and-switch-machines)
  - [8.1. Friend](#81-friend)
  - [8.2. Mac with the Local Build](#82-mac-with-the-local-build)
- [9. Sources](#9-sources)
- [10. Changelog](#10-changelog)

## 1. Key Points

- **Live:** `ToadishFrog67.markdown-preview-colours`, listed as "Markdown Preview Palettes (Toadish)", published 2026-10-19 [S3](#9-sources).
- **Cost:** none found. A personal Microsoft account and a publisher ID are enough [S1](#9-sources).
- **Route:** build the `.vsix`, then upload it on the publisher web page. No access token is stored anywhere [S1](#9-sources).
- **Credentials:** never written into this repository; `private/` and `.env` files are ignored by Git.

## 2. Prerequisites

| Tool | Needed for |
| --- | --- |
| VS Code | Testing the extension |
| Git | Cloning; `scripts/build.py` also uses it to read `.gitignore` and `.vscodeignore` |
| Python 3.8+ | Building and Python tests |
| Node.js LTS | Extension tests, Markdown lint and Microsoft's packaging tool `vsce` |
| Ruff 0.16.8 (optional) | Python formatting, same version as CI [S2](#9-sources) |

## 3. First-Time Setup on Linux

1. Sign in to GitHub with the personal account and clone the repository.
2. Run `make all` (lint, tests, package). Without Ruff installed, run `make test package` instead.
3. Open the folder in VS Code and press `F5`. A development window opens `test/sample.md` with the extension loaded.

## 4. Create the Marketplace Publisher

1. Sign in at <https://marketplace.visualstudio.com/manage> with a personal Microsoft account [S1](#9-sources).
2. Create a publisher. The publisher ID cannot be changed later [S1](#9-sources).
3. In `package.json`, set `publisher` to the ID. Done: `ToadishFrog67` [S3](#9-sources).
4. Confirm the extension name (`name`, `displayName`) is still free; names are unique [S1](#9-sources).
5. Never remove a listed extension; unpublish it instead. A removed extension's name is permanently reserved, even for the same publisher [S1](#9-sources). The original name `markdown-preview-palettes` was lost this way [S3](#9-sources).

## 5. Build and Test

1. `make css` after any colour change in `palettes/palettes.json`.
2. `make test`, then `make lint`.
3. Build the published package with Microsoft's tool [S1](#9-sources):
   - Check the package on the official registry first: `npm view @vscode/vsce`
   - `npx @vscode/vsce@4.0.0 package` writes `markdown-preview-colours-<version>.vsix` in the project root [S4](#9-sources).
   - `vsce` requires `activationEvents` when `main` is set; `scripts/build.py` does not check this, so use `vsce` for the published build [S4](#9-sources).
4. Test the `.vsix` in a throwaway VS Code profile, then switch every preset in dark and light themes [S5](#9-sources):
   - `T=$(mktemp -d)`
   - `code --user-data-dir "$T/data" --extensions-dir "$T/ext" --install-extension markdown-preview-colours-<version>.vsix`
   - `code --user-data-dir "$T/data" --extensions-dir "$T/ext" test/sample.md`
   - Do not install the `.vsix` in the normal profile: it has the same ID as the Marketplace copy, replaces it, and that machine then never receives the Marketplace update.

## 6. Publish

1. On the publisher page, choose **New extension**, then **Visual Studio Code**, and upload the `.vsix` [S1](#9-sources).
2. The status shows **Verifying** for a few minutes. Then search for the ID `ToadishFrog67.markdown-preview-colours` in the VS Code Extensions panel [S3](#9-sources).

## 7. Release an Update

1. Raise `version` in `package.json` (Major.Minor.Patch).
2. Add an entry to `CHANGELOG.md`.
3. Build and test (see [5. Build and Test](#5-build-and-test)).
4. On the publisher page, choose **Update** on the extension and upload the new `.vsix`.

## 8. Install and Switch Machines

### 8.1. Friend

1. Extensions panel: search `ToadishFrog67.markdown-preview-colours` or **Markdown Preview Palettes (Toadish)**, then **Install**.
2. Settings: search **Markdown Preview Palettes** and pick a preset.

### 8.2. Mac with the Local Build

1. Uninstall the local build: `code --uninstall-extension local.markdown-preview-palettes`
2. Install the Marketplace version: `code --install-extension ToadishFrog67.markdown-preview-colours`
3. The two have different IDs, so both can be installed at once and would apply the colours twice. Remove the local one first.

## 9. Sources

| ID | Supports | Evidence | Source | Status |
| --- | --- | --- | --- | --- |
| S1 | [1. Key Points](#1-key-points), [4. Create the Marketplace Publisher](#4-create-the-marketplace-publisher), [5. Build and Test](#5-build-and-test), [6. Publish](#6-publish) | No publishing fee mentioned; publisher created on the management page; `.vsix` upload on that page; publisher ID cannot change; names and display names unique; a removed extension's name "is permanently reserved and cannot be reused, even by the original publisher"; unpublishing keeps the extension and its statistics | "Publishing Extensions", <https://code.visualstudio.com/api/working-with-extensions/publishing-extension>, read 2026-10-13 and 2026-10-19 | Sourced |
| S2 | [2. Prerequisites](#2-prerequisites) | Ruff 0.16.8 released 2026-09-16 | PyPI, read 2026-10-13 | Sourced |
| S3 | [1. Key Points](#1-key-points), [4. Create the Marketplace Publisher](#4-create-the-marketplace-publisher), [6. Publish](#6-publish) | Two publishers created, `ToadishFrog67` and a second one; the first upload, named `markdown-preview-palettes`, removed; republished under `ToadishFrog67` as `markdown-preview-colours`; status showed **Verifying**; installed from the Marketplace on Linux | Sean Yang, 2026-10-19 | Sourced |
| S4 | [5. Build and Test](#5-build-and-test) | `vsce` 4.0.0 (npm, Microsoft maintainers) refused the manifest without `activationEvents`; packaged after `onLanguage:markdown` was added; `make test` passed | `npx @vscode/vsce@4.0.0 package` and `make test`, run 2026-10-19 | Sourced |
| S5 | [5. Build and Test](#5-build-and-test): throwaway profile | `code --help` lists `--user-data-dir`, `--extensions-dir` and `--install-extension` | `code --help`, VS Code 1.144.1 on the Mac, run 2026-11-05 | Sourced |

Gaps: the exact button names on the publisher page (**New extension**, **Update**) are not quoted in S1. They are Unconfirmed until the first upload; Sean Yang can confirm.

## 10. Changelog

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| 1.1.1 | 2026-11-05 | Build and Test step 4: test the `.vsix` in a throwaway profile instead of the normal one; S5 added | The `.vsix` and the Marketplace copy share one ID, so a normal install would block the Marketplace update |
| 1.1.0 | 2026-10-19 | Final publisher and extension ID; warning against removing a listing; `vsce` command pinned, `--allow-missing-repository` dropped, `activationEvents` note; install steps use the new ID; S3 and S4 added | First publish done |
| 1.0.0 | 2026-10-13 | Created: setup, publisher, build, publish, update and install steps | Sean Yang asked for documented steps for the Linux machine |
