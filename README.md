# SV Debug Agent

Local app that helps debug SystemVerilog source, compiler errors, and simulation logs.

**Layout**
- `sv_agent.py` — all debugging logic (unchanged core)
- `samples.py` — shared sample inputs
- `ui/app/` — current desktop + React UI
- `ui/legacy/` — Streamlit UI

## Desktop app (recommended)

```powershell
pip install -r requirements.txt
copy .env.example .env
.\ui\app\start-desktop.ps1
```

## Browser / design mode

```powershell
.\ui\app\start-api.ps1
.\ui\app\start-ui.ps1
```

UI: http://localhost:5173

## Legacy Streamlit UI

```powershell
.\ui\legacy\start.ps1
```

## Live Gemini mode

```env
DEMO_MODE=false
GEMINI_API_KEY=your_real_key_here
```

## Design polish

Use `ui/app/CLAUDE_DESIGN_PROMPT.md` with Claude Design. Keep `sv_agent.py` unchanged.
