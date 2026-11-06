// Unit tests for extension.js with a stubbed VS Code API and a minimal markdown-it stand-in.
// Run: node --test test/extension.test.js   (Node 18+, no packages needed)
'use strict';

const test = require('node:test');
const assert = require('node:assert');
const Module = require('node:module');

// ---------- Stub the 'vscode' module ----------
let configValue;
let configListener;
const executed = [];
const vscodeStub = {
  workspace: {
    getConfiguration: () => ({ get: (_key, fallback) => (configValue === undefined ? fallback : configValue) }),
    onDidChangeConfiguration: (listener) => {
      configListener = listener;
      return { dispose() {} };
    },
  },
  commands: {
    executeCommand: (command) => {
      executed.push(command);
      return Promise.resolve();
    },
  },
};
const originalLoad = Module._load;
Module._load = function (request, ...rest) {
  return request === 'vscode' ? vscodeStub : originalLoad.call(this, request, ...rest);
};
const extension = require('../extension.js');

// ---------- Minimal markdown-it stand-in ----------
function Token(type, tag, nesting) {
  this.type = type;
  this.tag = tag;
  this.nesting = nesting;
  this.attrs = null;
}
Token.prototype.attrJoin = function (name, value) {
  this.attrs = this.attrs || [];
  const found = this.attrs.find((attr) => attr[0] === name);
  if (found) found[1] += ` ${value}`;
  else this.attrs.push([name, value]);
};
Token.prototype.attrGet = function (name) {
  const found = (this.attrs || []).find((attr) => attr[0] === name);
  return found ? found[1] : null;
};

// Token list for a quote whose first paragraph holds the given inline children
function quote(...children) {
  const inline = new Token('inline', '', 0);
  inline.children = children.map(([type, content]) => Object.assign(new Token(type, '', 0), { content }));
  return [new Token('blockquote_open', 'blockquote', 1), new Token('paragraph_open', 'p', 1), inline];
}

function fakeMarkdownIt() {
  const coreRules = [];
  const md = {
    core: { ruler: { push: (_name, rule) => coreRules.push(rule) } },
    renderer: { rules: {} },
    use(plugin) {
      plugin(md);
      return md;
    },
  };
  // Parse = run core rules over a fake token list; render = run the custom rule for our token
  md.parse = (inlineMode = false, tokens = [new Token('paragraph_open', 'p', 1)]) => {
    const state = { inlineMode, tokens, Token };
    coreRules.forEach((rule) => rule(state));
    return state.tokens;
  };
  md.render = (tokens) =>
    tokens.map((t, i) => (md.renderer.rules[t.type] ? md.renderer.rules[t.type](tokens, i) : '')).join('');
  return md;
}

const context = { subscriptions: [] };
const api = extension.activate(context);
const md = api.extendMarkdownIt(fakeMarkdownIt());

// ---------- Tests ----------
test('adds the preset marker for the configured preset', () => {
  configValue = 'crimson';
  assert.strictEqual(md.render(md.parse()), '<span class="mpp-preset" data-preset="crimson" hidden></span>');
});

test('uses teal when nothing is configured', () => {
  configValue = undefined;
  assert.match(md.render(md.parse()), /data-preset="teal"/);
});

test('"default" renders no marker, so no colours apply', () => {
  configValue = 'default';
  assert.strictEqual(md.render(md.parse()), '');
});

test('unknown or unsafe values fall back to teal and never reach the HTML', () => {
  configValue = '"><script>alert(1)</script>';
  const html = md.render(md.parse());
  assert.match(html, /data-preset="teal"/);
  assert.doesNotMatch(html, /script/);
});

test('marker is rendered fresh, so a setting change applies to cached tokens', () => {
  const tokens = md.parse();
  configValue = 'golden';
  assert.match(md.render(tokens), /data-preset="golden"/);
  configValue = 'mono';
  assert.match(md.render(tokens), /data-preset="mono"/);
});

test('inline-only parses get no marker', () => {
  assert.ok(md.parse(true).every((t) => t.type !== 'mpp_preset'));
});

test('alert quotes get a callout class and a hidden-able marker', () => {
  for (const [marker, kind] of [['[!NOTE]', 'note'], ['[!info]', 'note'], ['[!TIP]', 'tip'], ['[!Warning]', 'warning']]) {
    const tokens = md.parse(false, quote(['text', marker], ['softbreak', ''], ['text', 'Body']));
    const blockquote = tokens.find((t) => t.type === 'blockquote_open');
    assert.strictEqual(blockquote.attrGet('class'), `mpp-alert mpp-alert-${kind}`);
    const inline = tokens.find((t) => t.type === 'inline');
    assert.strictEqual(inline.children[0].type, 'mpp_alert_marker');
    assert.strictEqual(md.render(inline.children), `<span class="mpp-alert-marker">${marker}</span>`);
    assert.strictEqual(tokens.find((t) => t.type === 'paragraph_open').attrGet('class'), null);
  }
});

test('a marker alone in its paragraph marks that paragraph as title-only', () => {
  const tokens = md.parse(false, quote(['text', '[!TIP]']));
  assert.strictEqual(tokens.find((t) => t.type === 'paragraph_open').attrGet('class'), 'mpp-alert-title-only');
});

test('other quotes and markers are left unchanged', () => {
  const cases = [
    quote(['text', '[!IMPORTANT]'], ['softbreak', ''], ['text', 'Body']),
    quote(['text', '[!NOTE] text on the same line']),
    quote(['text', 'Plain quote with [!TIP] inside']),
    quote(['text', '[!TIP]'], ['code_inline', 'x']),
  ];
  for (const tokens of cases) {
    md.parse(false, tokens);
    assert.strictEqual(tokens.find((t) => t.type === 'blockquote_open').attrGet('class'), null);
    assert.strictEqual(tokens.find((t) => t.type === 'inline').children[0].type, 'text');
  }
});

test('the alert marker never renders text other than the four names', () => {
  const marker = Object.assign(new Token('mpp_alert_marker', 'span', 0), { info: '<img src=x onerror=alert(1)>' });
  assert.strictEqual(md.render([marker]), '');
});

test('changing the preset setting refreshes the preview; other settings do not', () => {
  executed.length = 0;
  configListener({ affectsConfiguration: (key) => key === 'editor.fontSize' });
  assert.deepStrictEqual(executed, []);
  configListener({ affectsConfiguration: (key) => key === 'markdownPreviewPalettes.preset' });
  assert.deepStrictEqual(executed, ['markdown.preview.refresh']);
  assert.strictEqual(context.subscriptions.length, 1);
});
