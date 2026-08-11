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
    <aside className="sidebar" aria-label="Explorer">
      <div className="sidebar-header">
        <span>EXPLORER</span>
        <button
          type="button"
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          {theme === "dark" ? "Light+" : "Dark+"}
        </button>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-title">SAMPLES</div>
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
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-title">MODE</div>
        {status?.demo_mode ? (
          <p className="sidebar-copy">
            Demo mode · offline helpers (no API key)
          </p>
        ) : status?.has_api_key ? (
          <p className="sidebar-copy">Live Gemini mode</p>
        ) : (
          <p className="sidebar-copy">No API key · set DEMO_MODE=true</p>
        )}
      </div>

      <div className="sidebar-section sidebar-tips">
        <div className="sidebar-section-title">TIPS</div>
        <p className="sidebar-tip">Start from the first unknown X in a sim log.</p>
        <p className="sidebar-tip">Keep context around compiler errors.</p>
        <p className="sidebar-tip">Source + error together works best.</p>
      </div>
    </aside>
  );
}
