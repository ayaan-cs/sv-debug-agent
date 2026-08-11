# SV Debug Agent

A Streamlit app that helps debug SystemVerilog source, compiler errors, and simulation logs.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env   # Windows: copy .env.example .env
streamlit run app.py
```

Open http://localhost:8501

## Demo mode (no API key)

By default, if `GEMINI_API_KEY` is missing or still a placeholder, the app runs in **demo mode**. It uses the same local helper tools (X-propagation, compiler errors, lint patterns) without calling Gemini.

In `.env`:

```env
DEMO_MODE=true
GEMINI_API_KEY=your_gemini_api_key_here
```

## Live Gemini mode

1. Get a key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Put it in `.env` and turn demo mode off:

```env
DEMO_MODE=false
GEMINI_API_KEY=your_real_key_here
```

## Usage tips

- Load a sample from the sidebar to try the flow quickly
- Paste the **first** `'x'` in a sim log — later unknowns are often just fallout
- Include a few lines of context around compiler errors
