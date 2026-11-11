// Markdown Preview Palettes
// Adds a hidden marker naming the chosen preset to every rendered preview.
// media/preview.css reads the marker and applies that preset's colours.
'use strict';

const vscode = require('vscode');

const SECTION = 'markdownPreviewPalettes';
const PRESETS = new Set(['teal', 'plum', 'crimson', 'golden', 'mono', 'phosphor', 'parchment', 'azure', 'ember', 'folio', 'onyx', 'graphite', 'default']);
const FALLBACK = 'teal';

function currentPreset() {
  const value = vscode.workspace.getConfiguration(SECTION).get('preset', FALLBACK);
  // Only known preset names ever reach the HTML
  return PRESETS.has(value) ? value : FALLBACK;
}

// GitHub alert markers that get a callout box; [!INFO] shares the note style.
// Only the class names are added: presets without callout colours show these as ordinary quotes.
const ALERT_MARKER = /^\[!(NOTE|INFO|TIP|WARNING)\]$/i;
const ALERT_KINDS = { NOTE: 'note', INFO: 'note', TIP: 'tip', WARNING: 'warning' };

function markAlerts(state) {
  const tokens = state.tokens;
  for (let i = 0; i + 2 < tokens.length; i++) {
    const [quote, paragraph, inline] = [tokens[i], tokens[i + 1], tokens[i + 2]];
    if (quote.type !== 'blockquote_open' || paragraph.type !== 'paragraph_open' || inline.type !== 'inline') {
      continue;
    }
    const first = inline.children && inline.children[0];
    const next = inline.children && inline.children[1];
    const match = first && first.type === 'text' && ALERT_MARKER.exec(first.content.trim());
    // The marker must stand alone on the quote's first line
    if (!match || (next && next.type !== 'softbreak' && next.type !== 'hardbreak')) {
      continue;
    }
    quote.attrJoin('class', `mpp-alert mpp-alert-${ALERT_KINDS[match[1].toUpperCase()]}`);
    const marker = new state.Token('mpp_alert_marker', 'span', 0);
    marker.info = match[1]; // one of the four fixed names above (any letter case), never other text
    inline.children[0] = marker;
    if (inline.children.length === 1) {
      paragraph.attrJoin('class', 'mpp-alert-title-only');
    }
  }
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
  md.core.ruler.push('mpp_alerts', markAlerts);
  md.renderer.rules.mpp_alert_marker = (tokens, idx) => {
    const name = tokens[idx].info;
    return ALERT_KINDS[String(name).toUpperCase()] ? `<span class="mpp-alert-marker">[!${name}]</span>` : '';
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
