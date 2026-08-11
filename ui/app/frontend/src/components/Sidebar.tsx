import type { AppStatus, Sample } from "../types";

type SidebarProps = {
  status: AppStatus | null;
  samples: Sample[];
  onLoadSample: (sample: Sample) => void;
};

export function Sidebar({ status, samples, onLoadSample }: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Workspace controls">
      <div className="sidebar-brand">SV Debug Agent</div>

      <section className="sidebar-section">
        <h2 className="sidebar-label">Try a sample</h2>
        <p className="sidebar-copy">Load an example, then press Debug.</p>
        <div className="sample-list">
          {samples.map((sample) => (
            <button
              key={sample.id}
              type="button"
              className="sample-button"
              onClick={() => onLoadSample(sample)}
            >
              {sample.title}
            </button>
          ))}
        </div>
      </section>

      <section className="sidebar-section">
        <h2 className="sidebar-label">Mode</h2>
        {status?.demo_mode ? (
          <>
            <p className="sidebar-copy">
              Demo mode is on. Diagnosis runs offline with built-in helpers — no
              API key required.
            </p>
            <p className="sidebar-copy">
              For Gemini later: set DEMO_MODE=false and add GEMINI_API_KEY in
              your .env file.
            </p>
          </>
        ) : status?.has_api_key ? (
          <p className="sidebar-copy">
            Live Gemini mode is active using your API key.
          </p>
        ) : (
          <p className="sidebar-copy">
            No API key found. Add GEMINI_API_KEY to .env, or set DEMO_MODE=true.
          </p>
        )}
      </section>

      <section className="sidebar-section">
        <h2 className="sidebar-label">Tips</h2>
        <p className="sidebar-tip">Start from the first unknown X in a sim log.</p>
        <p className="sidebar-tip">
          Keep a few lines of context around compiler errors.
        </p>
        <p className="sidebar-tip">Source plus the error together works best.</p>
      </section>
    </aside>
  );
}
