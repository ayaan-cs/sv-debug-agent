import ReactMarkdown from "react-markdown";
import type { Alternative } from "../types";

type ResultPanelProps = {
  result: string | null;
  error: string | null;
  alternatives: Alternative[];
  onApplyAlternative: (code: string) => void;
};

export function ResultPanel({
  result,
  error,
  alternatives,
  onApplyAlternative,
}: ResultPanelProps) {
  if (!result && !error && alternatives.length === 0) return null;

  return (
    <section className="result-panel" aria-live="polite">
      <h2 className="result-title">Debugging result</h2>
      {error ? <p className="result-error">{error}</p> : null}
      {result ? (
        <div className="result-body">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
      ) : null}

      {alternatives.length > 0 ? (
        <div className="alt-list">
          <h3 className="alt-heading">Try an alternative (Code B)</h3>
          {alternatives.map((alt) => (
            <article key={alt.title} className="alt-card">
              <div className="alt-card-top">
                <h4>{alt.title}</h4>
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
      ) : null}
    </section>
  );
}
