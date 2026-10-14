# Markdown Preview Palettes Release Guide

| Field | Value |
| --- | --- |
| Owner | Sean Yang |
| Status | Active |
| Version | 1.0.0 |
| Last Updated | 2026-10-13 |
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
3. In `package.json`, replace `"publisher": "local"` with the new ID.
4. Confirm the extension name (`name`, `displayName`) is still free; names are unique and removed names stay reserved [S1](#9-sources).

## 5. Build and Test

1. `make css` after any colour change in `palettes/palettes.json`.
2. `make test`, then `make lint`.
3. Build the published package with Microsoft's tool [S1](#9-sources):
   - Check the package on the official registry first: `npm view @vscode/vsce`
   - `npx @vscode/vsce package --allow-missing-repository`
   - The flag is needed only while `package.json` has no `repository` field.
4. Install the `.vsix` locally (`code --install-extension <file>.vsix`), open `test/sample.md`, and switch every preset in dark and light themes.

## 6. Publish

1. On the publisher page, choose **New extension**, then **Visual Studio Code**, and upload the `.vsix` [S1](#9-sources).
2. Wait for the listing to appear, then search for it in the VS Code Extensions panel.

## 7. Release an Update

1. Raise `version` in `package.json` (Major.Minor.Patch).
2. Add an entry to `CHANGELOG.md`.
3. Build and test (see [5. Build and Test](#5-build-and-test)).
4. On the publisher page, choose **Update** on the extension and upload the new `.vsix`.

## 8. Install and Switch Machines

### 8.1. Friend

1. Extensions panel: search **Markdown Preview Palettes**, then **Install**.
2. Settings: search **Markdown Preview Palettes** and pick a preset.

### 8.2. Mac with the Local Build

1. Uninstall the local build: `code --uninstall-extension local.markdown-preview-palettes`
2. Install the Marketplace version from the Extensions panel.
3. Both installed at once would apply the colours twice, so remove the local one first.

## 9. Sources

| ID | Supports | Evidence | Source | Status |
| --- | --- | --- | --- | --- |
| S1 | [1. Key Points](#1-key-points), [4. Create the Marketplace Publisher](#4-create-the-marketplace-publisher), [5. Build and Test](#5-build-and-test), [6. Publish](#6-publish) | No publishing fee mentioned; publisher created on the management page; `.vsix` upload on that page; publisher ID cannot change; names unique and permanently reserved | "Publishing Extensions", <https://code.visualstudio.com/api/working-with-extensions/publishing-extension>, read 2026-10-13 | Sourced |
| S2 | [2. Prerequisites](#2-prerequisites) | Ruff 0.16.8 released 2026-09-16 | PyPI, read 2026-10-13 | Sourced |

Gaps: the exact button names on the publisher page (**New extension**, **Update**) are not quoted in S1. They are Unconfirmed until the first upload; Sean Yang can confirm.

## 10. Changelog

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| 1.0.0 | 2026-10-13 | Created: setup, publisher, build, publish, update and install steps | Sean Yang asked for documented steps for the Linux machine |
