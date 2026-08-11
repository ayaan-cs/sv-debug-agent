"""Demo-mode alternative code suggestions (no Gemini required)."""

from __future__ import annotations

from .classifiers import looks_like_compiler_issue, looks_like_source, looks_like_x_issue
from .helpers import check_common_lint_patterns

Alternative = dict[str, str]  # title, code, note


MISSING_RESET_ALT = """\
module counter (
  input  logic clk,
  input  logic reset,   // active-high reset
  input  logic en,
  output logic [3:0] count
);
  always_ff @(posedge clk) begin
    if (reset)
      count <= '0;
    else if (en)
      count <= count + 1;
  end
endmodule"""


OLD_ALWAYS_ALT = """\
module toggle (
  input  logic clk,
  input  logic reset,
  output logic q
);
  always_ff @(posedge clk) begin
    if (reset)
      q <= 1'b0;
    else
      q <= ~q;
  end
endmodule"""


SYNTAX_HINT_ALT = """\
// Checklist for "syntax error" near a line in Icarus:
// 1) Look at the line *above* the reported line for a missing ';'
// 2) Check begin/end balance
// 3) Confirm every module ends with endmodule

module example;
  initial begin
    $display("hello");
  end
endmodule"""


X_LOG_ALT = """\
module reg_with_reset (
  input  logic clk,
  input  logic reset_n,  // active-low reset
  input  logic d,
  output logic q
);
  always_ff @(posedge clk or negedge reset_n) begin
    if (!reset_n)
      q <= 1'b0;         // initialize so q is not 'x' after reset
    else
      q <= d;
  end
endmodule"""


def suggest_alternatives(user_input: str) -> list[Alternative]:
    """Return demo alternative snippets for common issues in the pasted input."""
    text = user_input.strip()
    lint = check_common_lint_patterns(text)
    alts: list[Alternative] = []

    if "always_ff" in text and "reset" not in text.lower():
        alts.append(
            {
                "title": "Add an explicit reset path",
                "note": (
                    "Your always_ff block never initializes count, so simulation "
                    "can start at 'x' and propagate. Alternative Code B adds reset."
                ),
                "code": MISSING_RESET_ALT,
            }
        )

    if "always @" in text:
        alts.append(
            {
                "title": "Prefer always_ff with reset",
                "note": (
                    "Old-style always @ is easy to get wrong. Alternative Code B uses "
                    "always_ff plus a reset so q is defined from time 0."
                ),
                "code": OLD_ALWAYS_ALT,
            }
        )

    if looks_like_compiler_issue(text) and not looks_like_source(text):
        alts.append(
            {
                "title": "Minimal syntax-clean skeleton",
                "note": (
                    "Compiler messages often point near the real typo. Alternative Code B "
                    "is a tiny known-good template plus a checklist while you fix the file."
                ),
                "code": SYNTAX_HINT_ALT,
            }
        )

    if looks_like_x_issue(text) and not any(
        a["title"].startswith("Add an explicit") for a in alts
    ):
        alts.append(
            {
                "title": "Initialize registers on reset",
                "note": (
                    "If the first 'x' appears on a flop output, initialize it on reset "
                    "(Code B) so unknowns do not spread through the design."
                ),
                "code": X_LOG_ALT,
            }
        )

    if not alts and looks_like_source(text) and "No obvious issues" in lint:
        return []

    return alts


def format_alternatives_markdown(alternatives: list[Alternative]) -> str:
    if not alternatives:
        return ""

    parts = [
        "### Suggested alternative code",
        "",
        "After the diagnosis above, here is an optional **Code B** style rewrite you could try:",
        "",
    ]
    for idx, alt in enumerate(alternatives, start=1):
        parts.append(f"#### Alternative {idx}: {alt['title']}")
        parts.append(alt["note"])
        parts.append("")
        parts.append("```systemverilog")
        parts.append(alt["code"].rstrip())
        parts.append("```")
        parts.append("")
    return "\n".join(parts)
