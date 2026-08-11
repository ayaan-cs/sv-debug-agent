# Claude Design prompt

Copy everything below the line into Claude Design.

---

Design a polished desktop-productivity UI for **SV Debug Agent**, a local app that helps FPGA / SystemVerilog engineers debug HDL, compiler errors, and simulation logs.

## Product context
- This is a **local developer tool**, not a marketing site.
- Users paste SystemVerilog source, Icarus/Verilator errors, or sim logs, then click **Debug**.
- The app has **Demo mode** (offline helpers, no API key) and **Live mode** (Gemini).
- Keep the interaction model simple: load sample → edit paste → Debug → read result.

## Existing skeleton to respect
Work from this structure in `ui/app/frontend` (do not invent a different IA):

- Left **sidebar**
  - Brand: SV Debug Agent
  - Sample buttons (Missing reset, Old-style always, Compiler syntax error, X in simulation log)
  - Mode explanation
  - Short tips
- Main workspace
  - Strong brand mark
  - One headline: “Debug SystemVerilog faster”
  - One short supporting sentence
  - Mode pill (Demo / Live)
  - Large monospace paste/editor
  - Primary **Debug** + secondary **Clear**
  - Result panel below

Technical mapping (keep classnames / component roles if possible):
- `.app-shell`, `.sidebar`, `.main`, `.hero`, `.brand`, `.editor`, `.actions`, `.result-panel`
- Components: `Sidebar`, `EditorPanel`, `ResultPanel`
- App code lives under `ui/app/`; legacy Streamlit is under `ui/legacy/` and should not be redesigned here.

## Design goals
- Feel like a focused **engineering workstation**, not a SaaS landing page.
- Brand-first: “SV Debug Agent” should dominate the first view more than the headline.
- One clear composition in the first viewport: brand, headline, one sentence, mode pill, editor, actions.
- Excellent readability for long code/logs.
- Fast to understand for a first-time user with no docs open.

## Visual direction
- Cool slate workspace with a restrained teal accent (`#0f766e` family is fine to evolve).
- Dark monospace editor for HDL/logs; light surrounding chrome.
- Expressive but professional typography (avoid Inter/Roboto/Arial/system defaults).
- Subtle atmospheric background (soft gradient/wash), not flat white and not neon/glow cyberpunk.
- Prefer structure and hierarchy over cards. Avoid card grids, pill clusters, stats, and marketing badges.
- No purple-gradient AI cliché look. No cream + terracotta newspaper look. No emoji decoration.

## UX details to design
1. Empty / first-run state with a sample already loaded.
2. Loading/analyzing state on Debug.
3. Success result state with scannable diagnosis.
4. Error state (API down, empty input, missing key).
5. Demo vs Live mode distinction that is obvious but calm.
6. Responsive behavior: sidebar stacks above main under ~860px.
7. Keyboard-friendly affordances (visible focus, clear primary action).

## Deliverables
- High-fidelity UI for the main screen in desktop width (~1280–1440).
- Compact/mobile or narrow layout variant.
- Component notes for: sample list buttons, mode pill, editor, Debug/Clear, result panel.
- Suggest font pairing, spacing scale, and tokenized colors that can drop into the existing React/CSS skeleton.
- Keep copy concise and practical; do not add extra marketing sections.

## Constraints
- Do **not** redesign the product into a multi-page dashboard.
- Do **not** add auth, settings pages, charts, or file trees unless as a subtle future affordance.
- Preserve the paste-and-debug workflow as the single primary job.
