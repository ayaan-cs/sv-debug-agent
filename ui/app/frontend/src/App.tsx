import { useEffect, useState } from "react";
import { fetchSamples, fetchStatus, runDebug } from "./api";
import { EditorPanel } from "./components/EditorPanel";
import { ResultPanel } from "./components/ResultPanel";
import { Sidebar } from "./components/Sidebar";
import type { AppStatus, Sample } from "./types";

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

export default function App() {
  const [status, setStatus] = useState<AppStatus | null>(null);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [input, setInput] = useState(FALLBACK_SAMPLE);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [bootError, setBootError] = useState<string | null>(null);

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
            : "Could not reach the local API. Run start-api.ps1 first.",
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
      setError("Paste some SystemVerilog or an error first — or load a sample.");
      return;
    }

    setBusy(true);
    setError(null);
    try {
      const response = await runDebug(input);
      setResult(response.result);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Debug failed.");
    } finally {
      setBusy(false);
    }
  }

  function handleClear() {
    setInput("");
    setResult(null);
    setError(null);
  }

  function handleLoadSample(sample: Sample) {
    setInput(sample.content);
    setResult(null);
    setError(null);
  }

  return (
    <div className="app-shell">
      <Sidebar
        status={status}
        samples={samples}
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
            <div
              className={`mode-pill ${status.demo_mode ? "demo" : "live"}`}
            >
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

        <ResultPanel result={result} error={error} />
      </main>
    </div>
  );
}
