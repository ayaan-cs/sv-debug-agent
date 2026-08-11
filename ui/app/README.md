# App UI (desktop + React)

Current UI for SV Debug Agent.

- `frontend/` — React + Vite shell (use with Claude Design)
- `backend/` — thin FastAPI wrapper around root `sv_agent.py`
- `desktop_app.py` — native desktop window (pywebview)
- `CLAUDE_DESIGN_PROMPT.md` — prompt for design polish

## Desktop app

From this folder:

```powershell
.\start-desktop.ps1
```

## Browser / design mode

```powershell
.\start-api.ps1
.\start-ui.ps1
```

Then open http://localhost:5173
