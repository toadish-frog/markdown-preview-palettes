# Shortcuts for the same checks CI runs. Ruff, Node and npx are needed only for the targets that use them.
PY ?= python3

.PHONY: css check test test-py test-js lint format package all

css:         ## Regenerate media/preview.css and run the contrast check
	$(PY) scripts/build.py css

check:       ## Contrast check only
	$(PY) scripts/build.py check

test-py:
	$(PY) -m unittest discover -s test -v

test-js:
	node --test test/extension.test.js

test: test-py test-js

lint:        ## Formatting and lint checks (no changes made)
	ruff format --check .
	ruff check .
	npx --yes markdownlint-cli2@0.23.3 "**/*.md" "#dist" "#private" "#node_modules"
	node --check extension.js

format:      ## Apply Python formatting
	ruff format .

package:     ## Build dist/*.vsix
	$(PY) scripts/build.py package

all: lint test package
