# App UI

Recommended UI for SV Debug Agent.

| Path | Purpose |
|------|---------|
| `frontend/` | React + Vite UI |
| `backend/` | FastAPI wrapper around root `sv_agent.py` |
| `desktop_app.py` | Native desktop window (pywebview) |

## Run

Desktop:

```powershell
.\start-desktop.ps1
```

Browser:

```powershell
.\start-api.ps1
.\start-ui.ps1
```

Open http://localhost:5173
