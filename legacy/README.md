# Legacy snapshot

Exact copies of `app.py` and `sv_agent.py` from upstream `master`
(`miguelse3rd2006-hue/sv-debug-agent`).

This preserves the original Streamlit UI + Gemini agent. It is separate from
the modern desktop app (`ui/app`) and the packaged agent (`sv_debug/`).

## Run

From the repo root:

```powershell
.\legacy\start.ps1
```

Or:

```powershell
cd legacy
pip install -r requirements.txt
streamlit run app.py
```

Requires a Gemini API key in the environment (`GEMINI_API_KEY` / `GOOGLE_API_KEY`),
same as the original master branch.
