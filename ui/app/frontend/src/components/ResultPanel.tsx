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
      <div className="panel-titlebar">
        <span className="panel-title">OUTPUT</span>
        <span className="panel-subtitle">Debugging result</span>
      </div>

      <div className="result-scroll">
        {error ? <p className="result-error">{error}</p> : null}

        {result ? (
          <div className="result-body">
            <ReactMarkdown
              components={{
                pre: ({ children }) => <pre className="md-pre">{children}</pre>,
                code: ({ className, children, ...props }) => {
                  const isBlock = Boolean(className);
                  if (isBlock) {
                    return (
                      <code className={`md-code-block ${className ?? ""}`} {...props}>
                        {children}
                      </code>
                    );
                  }
                  return (
                    <code className="md-code-inline" {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {result}
            </ReactMarkdown>
          </div>
        ) : null}

        {alternatives.length > 0 ? (
          <div className="alt-list">
            <h3 className="alt-heading">Suggested alternative (Code B)</h3>
            <p className="alt-intro">
              Optional rewrite you can load into the editor and compare with your
              original input.
            </p>
            {alternatives.map((alt) => (
              <article key={alt.title} className="alt-card">
                <div className="alt-card-top">
                  <div>
                    <h4>{alt.title}</h4>
                    {alt.note ? <p className="alt-note">{alt.note}</p> : null}
                  </div>
                  <button
                    type="button"
                    className="btn btn-primary alt-apply"
                    onClick={() => onApplyAlternative(alt.code)}
                  >
                    Load into editor
                  </button>
                </div>
                <div className="alt-code-frame">
                  <div className="alt-code-label">alternative.sv</div>
                  <pre className="alt-code">
                    <code>{alt.code}</code>
                  </pre>
                </div>
              </article>
            ))}
          </div>
        ) : null}
      </div>
    </section>
  );
}
