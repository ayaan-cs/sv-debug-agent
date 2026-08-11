import Editor from "@monaco-editor/react";

type EditorPanelProps = {
  value: string;
  busy: boolean;
  theme: "dark" | "light";
  onChange: (value: string) => void;
  onDebug: () => void;
  onClear: () => void;
};

export function EditorPanel({
  value,
  busy,
  theme,
  onChange,
  onDebug,
  onClear,
}: EditorPanelProps) {
  return (
    <section className="editor-panel" aria-label="Debug input">
      <div className="editor-toolbar">
        <span className="editor-tab">debug.sv</span>
        <span className="editor-lang">SystemVerilog</span>
      </div>
      {busy ? <div className="analyzing-banner">Analyzing…</div> : null}
      <div className={`monaco-wrap${busy ? " is-busy" : ""}`}>
        <Editor
          height="380px"
          language="systemverilog"
          theme={theme === "dark" ? "vs-dark" : "light"}
          value={value}
          onChange={(next) => onChange(next ?? "")}
          options={{
            readOnly: busy,
            fontFamily: "Consolas, 'Courier New', monospace",
            fontSize: 14,
            lineHeight: 22,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            wordWrap: "on",
            automaticLayout: true,
            tabSize: 2,
            renderLineHighlight: "line",
            padding: { top: 12, bottom: 12 },
            scrollbar: {
              verticalScrollbarSize: 10,
              horizontalScrollbarSize: 10,
            },
          }}
        />
      </div>
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
