import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import type { Alternative } from "../types";
import { ErrorIcon, SvFileIcon } from "./icons";

type ResultPanelProps = {
  result: string | null;
  error: string | null;
  busy: boolean;
  alternatives: Alternative[];
  onApplyAlternative: (code: string) => void;
};

type PanelTab = "diagnosis" | "alternatives";

const PANEL_HEIGHT_KEY = "sv-debug-panel-height";
const DEFAULT_HEIGHT = 280;
const MIN_HEIGHT = 120;

function readStoredHeight(): number {
  const raw = localStorage.getItem(PANEL_HEIGHT_KEY);
  const n = raw ? Number(raw) : NaN;
  return Number.isFinite(n) && n >= MIN_HEIGHT ? n : DEFAULT_HEIGHT;
}

function clampHeight(next: number): number {
  const max = Math.max(MIN_HEIGHT + 40, Math.floor(window.innerHeight * 0.7));
  return Math.min(max, Math.max(MIN_HEIGHT, Math.round(next)));
}

export function ResultPanel({
  result,
  error,
  busy,
  alternatives,
  onApplyAlternative,
}: ResultPanelProps) {
  const [tab, setTab] = useState<PanelTab>("diagnosis");
  const [height, setHeight] = useState(() => readStoredHeight());
  const [dragging, setDragging] = useState(false);
  const dragStartY = useRef(0);
  const dragStartHeight = useRef(0);
  const hasContent = Boolean(result) || Boolean(error) || alternatives.length > 0;
  const problems = useMemo(() => (error ? 1 : 0), [error]);

  useEffect(() => {
    localStorage.setItem(PANEL_HEIGHT_KEY, String(height));
  }, [height]);

  useEffect(() => {
    if (!dragging) return;

    function onMove(event: PointerEvent) {
      const delta = dragStartY.current - event.clientY;
      setHeight(clampHeight(dragStartHeight.current + delta));
    }

    function onUp() {
      setDragging(false);
    }

    document.body.classList.add("is-panel-resizing");
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
    window.addEventListener("pointercancel", onUp);

    return () => {
      document.body.classList.remove("is-panel-resizing");
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
    };
  }, [dragging]);

  if (!hasContent && !busy) return null;

  const showAlternatives = tab === "alternatives" && alternatives.length > 0;

  function startResize(event: React.PointerEvent<HTMLDivElement>) {
    event.preventDefault();
    dragStartY.current = event.clientY;
    dragStartHeight.current = height;
    setDragging(true);
  }

  return (
    <section
      className={`result-panel${dragging ? " is-resizing" : ""}`}
      style={{ height }}
      aria-live="polite"
    >
      <div
        className={`panel-sash${dragging ? " is-active" : ""}`}
        role="separator"
        aria-orientation="horizontal"
        aria-label="Resize diagnosis panel"
        aria-valuenow={height}
        aria-valuemin={MIN_HEIGHT}
        tabIndex={0}
        onPointerDown={startResize}
        onKeyDown={(event) => {
          if (event.key === "ArrowUp") {
            event.preventDefault();
            setHeight((h) => clampHeight(h + 24));
          } else if (event.key === "ArrowDown") {
            event.preventDefault();
            setHeight((h) => clampHeight(h - 24));
          }
        }}
      />

      <div className="panel-tabs" role="tablist" aria-label="Debug output">
        <button
          type="button"
          role="tab"
          aria-selected={tab === "diagnosis"}
          className={`panel-tab${tab === "diagnosis" ? " is-active" : ""}`}
          onClick={() => setTab("diagnosis")}
        >
          Diagnosis
          {problems > 0 ? <span className="count">{problems}</span> : null}
        </button>
        {alternatives.length > 0 ? (
          <button
            type="button"
            role="tab"
            aria-selected={tab === "alternatives"}
            className={`panel-tab${tab === "alternatives" ? " is-active" : ""}`}
            onClick={() => setTab("alternatives")}
          >
            Code B
            <span className="count">{alternatives.length}</span>
          </button>
        ) : null}
      </div>

      <div className="panel-scroll">
        {showAlternatives ? (
          <div className="alt-list">
            <h3 className="alt-heading">Alternative implementations</h3>
            {alternatives.map((alt) => (
              <article key={alt.title} className="alt-card">
                <div className="alt-card-top">
                  <h4>
                    <SvFileIcon />
                    {alt.title}
                  </h4>
                  <button
                    type="button"
                    className="btn btn-secondary alt-apply"
                    onClick={() => onApplyAlternative(alt.code)}
                  >
                    Load into editor
                  </button>
                </div>
                {alt.note ? <p className="alt-note">{alt.note}</p> : null}
                <pre className="alt-code">
                  <code>{alt.code}</code>
                </pre>
              </article>
            ))}
          </div>
        ) : (
          <>
            {error ? (
              <p className="result-error" role="alert">
                <ErrorIcon />
                <span>{error}</span>
              </p>
            ) : null}
            {busy && !result ? (
              <p className="result-body" style={{ color: "var(--ink-dim)" }}>
                Analyzing input…
              </p>
            ) : null}
            {result ? (
              <div className="result-body">
                <ReactMarkdown>{result}</ReactMarkdown>
              </div>
            ) : null}
          </>
        )}
      </div>
    </section>
  );
}
