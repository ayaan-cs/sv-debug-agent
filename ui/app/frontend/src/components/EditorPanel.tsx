import { useEffect, useMemo, useRef, useState } from "react";
import { highlightSv } from "./svHighlight";
import { PlayIcon, CloseIcon, SplitIcon } from "./icons";

type EditorPanelProps = {
  value: string;
  busy: boolean;
  fileName: string;
  onChange: (value: string) => void;
  onDebug: () => void;
  onClear: () => void;
};

export function EditorPanel({
  value,
  busy,
  fileName,
  onChange,
  onDebug,
  onClear,
}: EditorPanelProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const highlightRef = useRef<HTMLPreElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);
  const [caret, setCaret] = useState({ line: 1, col: 1 });

  const lines = useMemo(() => value.split("\n"), [value]);
  const gutter = useMemo(
    () => Array.from({ length: Math.max(lines.length, 24) }, (_, i) => i + 1),
    [lines.length],
  );
  const highlighted = useMemo(() => highlightSv(value), [value]);

  function syncScroll() {
    const ta = textareaRef.current;
    if (!ta) return;
    if (highlightRef.current) {
      highlightRef.current.scrollTop = ta.scrollTop;
      highlightRef.current.scrollLeft = ta.scrollLeft;
    }
    if (gutterRef.current) gutterRef.current.scrollTop = ta.scrollTop;
  }

  function syncCaret() {
    const ta = textareaRef.current;
    if (!ta) return;
    const upto = ta.value.slice(0, ta.selectionStart).split("\n");
    setCaret({ line: upto.length, col: (upto[upto.length - 1]?.length ?? 0) + 1 });
  }

  useEffect(() => {
    syncScroll();
  }, [value]);

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      onDebug();
      return;
    }
    if (event.key === "Tab") {
      event.preventDefault();
      const ta = event.currentTarget;
      const { selectionStart: s, selectionEnd: e } = ta;
      const next = `${value.slice(0, s)}  ${value.slice(e)}`;
      onChange(next);
      requestAnimationFrame(() => {
        ta.selectionStart = ta.selectionEnd = s + 2;
      });
    }
  }

  return (
    <>
      <div className="tabbar">
        <div className="tab is-active">
          <span className="tab-dirty" aria-hidden="true" />
          {fileName}
        </div>
        <div className="tabbar-actions">
          <button
            type="button"
            className="btn btn-primary"
            onClick={onDebug}
            disabled={busy}
            title="Run debug (Ctrl/Cmd + Enter)"
          >
            {busy ? <span className="spinner" aria-hidden="true" /> : <PlayIcon />}
            {busy ? "Analyzing…" : "Debug"}
            <span className="btn-kbd">⌃⏎</span>
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClear}
            disabled={busy}
            title="Clear editor"
          >
            <CloseIcon />
            Clear
          </button>
          <button type="button" className="icon-btn" title="Split editor" aria-label="Split editor">
            <SplitIcon />
          </button>
        </div>
      </div>

      <div className="breadcrumbs">
        <span>sv-debug-agent</span>
        <span className="sep">›</span>
        <span>scratch</span>
        <span className="sep">›</span>
        <span>{fileName}</span>
        <span className="crumb-count">
          Ln {caret.line}, Col {caret.col} · {lines.length} lines · {value.length} chars
        </span>
      </div>

      <section className="editor-panel" aria-label="Debug input">
        {busy ? (
          <div className="editor-progress" aria-hidden="true">
            <span />
          </div>
        ) : null}

        <div className="editor-gutter" ref={gutterRef} aria-hidden="true">
          {gutter.map((n) => (
            <div key={n} style={n === caret.line ? { color: "var(--gutter-ink-active)" } : undefined}>
              {n}
            </div>
          ))}
        </div>

        <div className="editor-scroll">
          <pre className="editor-highlight" ref={highlightRef} aria-hidden="true">
            {highlighted}
            {"\n"}
          </pre>
          <textarea
            id="debug-input"
            className="editor"
            ref={textareaRef}
            value={value}
            onChange={(event) => onChange(event.target.value)}
            onScroll={syncScroll}
            onKeyUp={syncCaret}
            onClick={syncCaret}
            onSelect={syncCaret}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            disabled={busy}
            aria-label="SystemVerilog source, compiler error, or simulation log"
          />
          {value.length === 0 ? (
            <p className="editor-placeholder">
              module … / error: … / # time 20: q=x
            </p>
          ) : null}
        </div>
      </section>
    </>
  );
}
