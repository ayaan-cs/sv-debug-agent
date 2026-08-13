# SV Debug Agent

Local desktop app that helps debug SystemVerilog source, compiler errors, and simulation logs.

Demo mode works without a Gemini API key — contributors do not need (and should not commit) API tokens.

## Project layout

| Path | Purpose |
|------|---------|
| `sv_debug/` | Debugging logic (helpers, demo mode, Gemini path, samples, CLI) |
| `tests/` | Offline sample tests (no API key required) |
| `ui/app/` | Desktop + React UI (recommended) |
| `legacy/` | Exact upstream `master` snapshot (`app.py` + `sv_agent.py`) |

## Quick start

```powershell
pip install -r requirements.txt
copy .env.example .env
.\ui\app\start-desktop.ps1
```

This opens **SV Debug Agent** in a native window. The first launch builds the frontend automatically.

### Optional: browser UI

```powershell
.\ui\app\start-api.ps1
.\ui\app\start-ui.ps1
```

Then open http://localhost:5173

### Optional: upstream master snapshot

Original Streamlit UI + agent from upstream `master`:

```powershell
.\legacy\start.ps1
```

### Optional: CLI

```powershell
python -m sv_debug
```

Paste input, then type `END` on its own line.

## Configuration

Edit `.env` (from `.env.example`):

```env
# Offline helpers (no API key needed) — recommended for contributors
DEMO_MODE=true
GEMINI_API_KEY=your_gemini_api_key_here
```

Keep `DEMO_MODE=true` unless you are testing your own Gemini key locally. Never commit a real key.

For live Gemini on your machine only:

1. Get a key from https://aistudio.google.com/apikey
2. Set:

```env
DEMO_MODE=false
GEMINI_API_KEY=your_real_key_here
```

## Tests (no API key)

```powershell
pip install -r requirements.txt
pytest
```

These cover helper lint checks, sample inputs, and the offline demo pipeline.

## Usage

1. Load a sample from the sidebar, or paste HDL / an error / a sim log
2. Click **Debug**
3. Use the theme toggle for dark (default) or light mode

## Contributing safely

Useful contributions that do **not** require the maintainer’s API tokens:

- Improve demo helpers / SystemVerilog pattern checks in `sv_debug/helpers.py`
- Add samples in `sv_debug/samples.py` and matching tests in `tests/`
- Improve the desktop/React UI under `ui/app/frontend/` (teal-branded shell in `App.tsx` + `index.css`)
- Docs / README clarity

Keep `.env` local. Prefer demo-mode tests so CI and reviewers never need secrets.
Never commit API keys, `node_modules/`, or `ui/app/frontend/dist/`.

### Suggested local checklist

```powershell
pytest
cd ui\app\frontend
npm run build
```

Run the desktop app with `DEMO_MODE=true` before opening a PR.

Shared test branch on the upstream repo (does not merge to `master`): `test_ui`.
