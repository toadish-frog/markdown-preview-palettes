// Markdown Preview Palettes
// Adds a hidden marker naming the chosen preset to every rendered preview.
// media/preview.css reads the marker and applies that preset's colours.
'use strict';

const vscode = require('vscode');

const SECTION = 'markdownPreviewPalettes';
const PRESETS = new Set(['teal', 'plum', 'crimson', 'golden', 'mono', 'default']);
const FALLBACK = 'teal';

function currentPreset() {
  const value = vscode.workspace.getConfiguration(SECTION).get('preset', FALLBACK);
  // Only known preset names ever reach the HTML
  return PRESETS.has(value) ? value : FALLBACK;
}

function presetPlugin(md) {
  // Add a placeholder token once per parse. It is rendered fresh on every render,
  // so a settings change shows after a refresh even when VS Code reuses cached tokens.
  md.core.ruler.push('mpp_preset', (state) => {
    if (!state.inlineMode) {
      state.tokens.unshift(new state.Token('mpp_preset', '', 0));
    }
  });
  md.renderer.rules.mpp_preset = () => {
    const preset = currentPreset();
    return preset === 'default' ? '' : `<span class="mpp-preset" data-preset="${preset}" hidden></span>`;
  };
}

function activate(context) {
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((event) => {
      if (event.affectsConfiguration(`${SECTION}.preset`)) {
        vscode.commands.executeCommand('markdown.preview.refresh');
      }
    })
  );
  return {
    extendMarkdownIt(md) {
      return md.use(presetPlugin);
    },
  };
}

function deactivate() {}

module.exports = { activate, deactivate };
