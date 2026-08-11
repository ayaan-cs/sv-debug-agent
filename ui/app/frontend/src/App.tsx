import { useEffect, useState } from "react";
import { fetchSamples, fetchStatus, runDebug } from "./api";
import { EditorPanel } from "./components/EditorPanel";
import { ResultPanel } from "./components/ResultPanel";
import { Sidebar } from "./components/Sidebar";
import { BugIcon, FilesIcon, ThemeIcon } from "./components/icons";
import type { Alternative, AppStatus, Sample } from "./types";

type Theme = "dark" | "light";

const THEME_KEY = "sv-debug-theme";
const INPUT_KEY = "sv-debug-editor-input";
const INPUT_MAX_STORED = 200_000;
const FILE_NAME = "debug.sv";

function readStoredTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY);
  return stored === "light" ? "light" : "dark";
}

function readStoredInput(): string {
  return localStorage.getItem(INPUT_KEY) ?? "";
}

function persistInput(value: string): void {
  try {
    localStorage.setItem(
      INPUT_KEY,
      value.length > INPUT_MAX_STORED ? value.slice(0, INPUT_MAX_STORED) : value,
    );
  } catch {
    // Ignore quota / private-mode failures; editing still works in-memory.
  }
}

export default function App() {
  const [theme, setTheme] = useState<Theme>(() => readStoredTheme());
  const [status, setStatus] = useState<AppStatus | null>(null);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [activeSampleId, setActiveSampleId] = useState<string | null>(null);
  const [input, setInput] = useState(() => readStoredInput());
  const [result, setResult] = useState<string | null>(null);
  const [alternatives, setAlternatives] = useState<Alternative[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [bootError, setBootError] = useState<string | null>(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  useEffect(() => {
    persistInput(input);
  }, [input]);

  useEffect(() => {
    let cancelled = false;

    async function boot() {
      try {
        const [nextStatus, nextSamples] = await Promise.all([
          fetchStatus(),
          fetchSamples(),
        ]);
        if (cancelled) return;
        setStatus(nextStatus);
        setSamples(nextSamples);
        setBootError(null);
      } catch (err) {
        if (cancelled) return;
        setBootError(
          err instanceof Error
            ? err.message
            : "Could not reach the local API. Run ui/app/start-api.ps1 first.",
        );
      }
    }

    void boot();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleDebug() {
    if (!input.trim()) {
      setResult(null);
      setAlternatives([]);
      setError("Paste some SystemVerilog or an error first — or load a sample.");
      return;
    }

    setBusy(true);
    setError(null);
    try {
      const response = await runDebug(input);
      setResult(response.result);
      setAlternatives(response.alternatives ?? []);
    } catch (err) {
      setResult(null);
      setAlternatives([]);
      setError(err instanceof Error ? err.message : "Debug failed.");
    } finally {
      setBusy(false);
    }
  }

  function handleClear() {
    setInput("");
    setResult(null);
    setAlternatives([]);
    setError(null);
    setActiveSampleId(null);
  }

  function handleLoadSample(sample: Sample) {
    setInput(sample.content);
    setResult(null);
    setAlternatives([]);
    setError(null);
    setActiveSampleId(sample.id);
  }

  function handleApplyAlternative(code: string) {
    setInput(code);
    setError(null);
    setActiveSampleId(null);
  }

  const modeLabel = status
    ? status.demo_mode
      ? "Demo · offline helpers"
      : status.has_api_key
        ? "Live · Gemini"
        : "Live · no API key"
    : "Connecting…";

  return (
    <div className="app-shell">
      <div className="titlebar">
        <div className="titlebar-left">
          <span className="titlebar-mark">SV</span>
          <span className="titlebar-title">
            {FILE_NAME} — {status?.app_name ?? "SV Debug Agent"}
          </span>
        </div>
        <div />
        <div className="titlebar-right">
          <button
            type="button"
            className="icon-btn"
            onClick={() => setTheme((c) => (c === "dark" ? "light" : "dark"))}
            aria-label={`Switch to ${theme === "dark" ? "Light+" : "Dark+"} theme`}
            title={`Switch to ${theme === "dark" ? "Light+" : "Dark+"} theme`}
          >
            <ThemeIcon />
          </button>
        </div>
      </div>

      <div className="workbench">
        <nav className="activitybar" aria-label="Activity bar">
          <button type="button" className="activity-item is-active" aria-label="Explorer" title="Explorer">
            <FilesIcon />
          </button>
          <button type="button" className="activity-item" aria-label="Run and debug" title="Run and debug">
            <BugIcon />
          </button>
          <span className="activitybar-spacer" />
          <button
            type="button"
            className="activity-item"
            onClick={() => setTheme((c) => (c === "dark" ? "light" : "dark"))}
            aria-label="Toggle theme"
            title="Toggle theme"
          >
            <ThemeIcon />
          </button>
        </nav>

        <Sidebar
          status={status}
          samples={samples}
          activeSampleId={activeSampleId}
          onLoadSample={handleLoadSample}
        />

        <main className="main">
          <EditorPanel
            value={input}
            busy={busy}
            fileName={FILE_NAME}
            onChange={setInput}
            onDebug={() => void handleDebug()}
            onClear={handleClear}
          />

          {bootError ? (
            <p className="boot-error" role="alert">
              {bootError}
            </p>
          ) : null}

          <ResultPanel
            result={result}
            error={error}
            busy={busy}
            alternatives={alternatives}
            onApplyAlternative={handleApplyAlternative}
          />
        </main>
      </div>

      <footer className="statusbar">
        <span className="status-item">
          <span className="status-dot" />
          {modeLabel}
        </span>
        <span className="status-item">{busy ? "Analyzing…" : "Ready"}</span>
        <div className="status-right">
          <span className="status-item">Spaces: 2</span>
          <span className="status-item">UTF-8</span>
          <span className="status-item">LF</span>
          <span className="status-item">SystemVerilog</span>
          <button
            type="button"
            className="status-item"
            onClick={() => setTheme((c) => (c === "dark" ? "light" : "dark"))}
          >
            {theme === "dark" ? "Dark+" : "Light+"}
          </button>
        </div>
      </footer>
    </div>
  );
}
