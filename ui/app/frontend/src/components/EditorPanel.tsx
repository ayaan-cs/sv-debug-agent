type EditorPanelProps = {
  value: string;
  busy: boolean;
  onChange: (value: string) => void;
  onDebug: () => void;
  onClear: () => void;
};

export function EditorPanel({
  value,
  busy,
  onChange,
  onDebug,
  onClear,
}: EditorPanelProps) {
  return (
    <section className="editor-panel" aria-label="Debug input">
      <label className="editor-label" htmlFor="debug-input">
        Paste code, compiler error, or sim log
      </label>
      {busy ? <div className="analyzing-banner">Analyzing…</div> : null}
      <textarea
        id="debug-input"
        className={`editor${busy ? " is-busy" : ""}`}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="module … / error: … / # time 20: q=x"
        spellCheck={false}
        disabled={busy}
      />
      <div className="actions">
        <button
          type="button"
          className="btn btn-primary"
          onClick={onDebug}
          disabled={busy}
        >
          {busy ? "Analyzing…" : "Debug"}
        </button>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onClear}
          disabled={busy}
        >
          Clear
        </button>
      </div>
    </section>
  );
}
