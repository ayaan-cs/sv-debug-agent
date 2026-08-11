import { useState } from "react";
import type { AppStatus, Sample } from "../types";
import { ChevronIcon, SvFileIcon } from "./icons";

type SidebarProps = {
  status: AppStatus | null;
  samples: Sample[];
  activeSampleId: string | null;
  onLoadSample: (sample: Sample) => void;
};

type SectionProps = {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
};

function Section({ title, children, defaultOpen = true }: SectionProps) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section className="sidebar-section">
      <button
        type="button"
        className="sidebar-section-header"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        <ChevronIcon className="sidebar-chevron" />
        {title}
      </button>
      {open ? <div className="sidebar-section-body">{children}</div> : null}
    </section>
  );
}

export function Sidebar({
  status,
  samples,
  activeSampleId,
  onLoadSample,
}: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Workspace controls">
      <h2 className="sidebar-title">Explorer</h2>

      <Section title="Samples" defaultOpen={false}>
        <div className="sample-list">
          {samples.map((sample) => (
            <button
              key={sample.id}
              type="button"
              className={`sample-button${sample.id === activeSampleId ? " is-active" : ""}`}
              aria-current={sample.id === activeSampleId ? "true" : undefined}
              onClick={() => onLoadSample(sample)}
              title={sample.title}
            >
              <SvFileIcon className="sample-icon" />
              <span className="sample-name">{sample.title}</span>
            </button>
          ))}
          {samples.length === 0 ? (
            <p className="sidebar-copy">No samples loaded — start the local API.</p>
          ) : null}
        </div>
      </Section>

      <Section title="Mode" defaultOpen={false}>
        <div className="mode-rows">
          <p className="mode-row">
            <span className="mode-key">DEMO_MODE</span>
            <span className="mode-val">{status ? String(status.demo_mode) : "…"}</span>
          </p>
          <p className="mode-row">
            <span className="mode-key">GEMINI_API_KEY</span>
            <span className="mode-val">
              {status ? (status.has_api_key ? "set" : "missing") : "…"}
            </span>
          </p>
        </div>
        <p className="sidebar-copy">
          {status?.demo_mode
            ? "Demo mode diagnoses offline with the built-in helpers. Nothing leaves this machine."
            : status?.has_api_key
              ? "Live mode sends your input to Gemini using the key in .env."
              : "No API key found. Add GEMINI_API_KEY to .env, or set DEMO_MODE=true."}
        </p>
      </Section>

      <Section title="Tips" defaultOpen={false}>
        <ul className="tip-list">
          <li>
            <span>
              Start from the first unknown <code>x</code> in a sim log.
            </span>
          </li>
          <li>
            <span>Keep a few lines of context around compiler errors.</span>
          </li>
          <li>
            <span>Source plus the error together works best.</span>
          </li>
        </ul>
      </Section>
    </aside>
  );
}
