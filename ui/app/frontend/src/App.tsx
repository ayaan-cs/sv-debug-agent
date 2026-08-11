import { useEffect, useState } from "react";
import { fetchSamples, fetchStatus, runDebug } from "./api";
import { EditorPanel } from "./components/EditorPanel";
import { ResultPanel } from "./components/ResultPanel";
import { Sidebar } from "./components/Sidebar";
import type { Alternative, AppStatus, Sample } from "./types";

type Theme = "dark" | "light";

const THEME_KEY = "sv-debug-theme";

const FALLBACK_SAMPLE = `module counter (
  input  logic clk,
  input  logic en,
  output logic [3:0] count
);
  always_ff @(posedge clk) begin
    if (en)
      count <= count + 1;
  end
endmodule`;

function readStoredTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY);
  return stored === "light" ? "light" : "dark";
}

export default function App() {
  const [theme, setTheme] = useState<Theme>(() => readStoredTheme());
  const [status, setStatus] = useState<AppStatus | null>(null);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [input, setInput] = useState(FALLBACK_SAMPLE);
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
        if (nextSamples[0]) setInput(nextSamples[0].content);
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
  }

  function handleLoadSample(sample: Sample) {
    setInput(sample.content);
    setResult(null);
    setAlternatives([]);
    setError(null);
  }

  function handleApplyAlternative(code: string) {
    setInput(code);
    setError(null);
  }

  return (
    <div className="app-shell">
      <Sidebar
        status={status}
        samples={samples}
        theme={theme}
        onToggleTheme={() =>
          setTheme((current) => (current === "dark" ? "light" : "dark"))
        }
        onLoadSample={handleLoadSample}
      />

      <main className="main">
        <header className="hero">
          <p className="brand">SV Debug Agent</p>
          <h1>Debug SystemVerilog faster</h1>
          <p className="lede">
            Paste HDL, a compiler error, or a sim log. Get a concrete
            explanation of what is wrong and how to fix it.
          </p>
          {status ? (
            <div className={`mode-pill ${status.demo_mode ? "demo" : "live"}`}>
              {status.demo_mode
                ? "Demo mode · offline helpers"
                : "Live mode · Gemini"}
            </div>
          ) : null}
        </header>

        {bootError ? (
          <p className="boot-error" role="alert">
            {bootError}
          </p>
        ) : null}

        <EditorPanel
          value={input}
          busy={busy}
          onChange={setInput}
          onDebug={() => void handleDebug()}
          onClear={handleClear}
        />

        <ResultPanel
          result={result}
          error={error}
          alternatives={alternatives}
          onApplyAlternative={handleApplyAlternative}
        />
      </main>
    </div>
  );
}
