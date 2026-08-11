import type { AppStatus, Sample } from "../types";

type SidebarProps = {
  status: AppStatus | null;
  samples: Sample[];
  theme: "dark" | "light";
  onToggleTheme: () => void;
  onLoadSample: (sample: Sample) => void;
};

export function Sidebar({
  status,
  samples,
  theme,
  onToggleTheme,
  onLoadSample,
}: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Workspace controls">
      <div className="sidebar-top">
        <div className="sidebar-brand">SV Debug Agent</div>
        <button
          type="button"
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          {theme === "dark" ? "Light" : "Dark"}
        </button>
      </div>

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
          <p className="sidebar-copy">
            Demo mode runs offline with built-in helpers. No API key required.
            Set DEMO_MODE=false and GEMINI_API_KEY in .env for Gemini.
          </p>
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
