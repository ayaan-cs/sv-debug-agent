import type { AppStatus, DebugResponse, Sample } from "./types";

async function readError(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as { detail?: string };
    if (typeof data.detail === "string") return data.detail;
  } catch {
    /* ignore */
  }
  return res.statusText || "Request failed";
}

export async function fetchStatus(): Promise<AppStatus> {
  const res = await fetch("/api/status");
  if (!res.ok) throw new Error(await readError(res));
  return res.json();
}

export async function fetchSamples(): Promise<Sample[]> {
  const res = await fetch("/api/samples");
  if (!res.ok) throw new Error(await readError(res));
  return res.json();
}

export async function runDebug(input: string): Promise<DebugResponse> {
  const res = await fetch("/api/debug", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });
  if (!res.ok) throw new Error(await readError(res));
  return res.json();
}
