type ResultPanelProps = {
  result: string | null;
  error: string | null;
};

export function ResultPanel({ result, error }: ResultPanelProps) {
  if (!result && !error) return null;

  return (
    <section className="result-panel" aria-live="polite">
      <h2 className="result-title">Debugging result</h2>
      {error ? <p className="result-error">{error}</p> : null}
      {result ? <pre className="result-body">{result}</pre> : null}
    </section>
  );
}
