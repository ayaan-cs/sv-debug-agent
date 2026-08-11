"""Shared sample inputs for the UI and offline tests."""

from __future__ import annotations

SAMPLES: list[dict[str, str]] = [
    {
        "id": "missing-reset",
        "title": "Missing reset (X risk)",
        "content": """\
module counter (
  input  logic clk,
  input  logic en,
  output logic [3:0] count
);
  always_ff @(posedge clk) begin
    if (en)
      count <= count + 1;
  end
endmodule""",
    },
    {
        "id": "old-always",
        "title": "Old-style always block",
        "content": """\
module toggle (
  input  wire clk,
  output reg  q
);
  always @(posedge clk) begin
    q <= ~q;
  end
endmodule""",
    },
    {
        "id": "syntax-error",
        "title": "Compiler syntax error",
        "content": """\
tb.v:12: syntax error
I give up.
error: Unable to elaborate top level modules""",
    },
    {
        "id": "x-log",
        "title": "X in simulation log",
        "content": """\
# time 0: reset=x data=x
# time 10: reset=0 data=x
# time 20: q=x (first unknown observed here)
# time 30: out=x""",
    },
]


def get_sample(sample_id: str) -> dict[str, str]:
    for sample in SAMPLES:
        if sample["id"] == sample_id:
            return sample
    raise KeyError(f"Unknown sample id: {sample_id}")
