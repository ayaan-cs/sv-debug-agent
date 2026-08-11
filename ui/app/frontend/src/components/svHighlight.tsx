import { Fragment, type ReactNode } from "react";

/**
 * Minimal SystemVerilog / Verilog tokenizer used by the editor's highlight
 * layer. Regex-based on purpose: zero extra dependencies, and it only has to
 * be good enough for the paste-and-debug workflow (code, compiler errors, logs).
 */

const KEYWORDS =
  "module|endmodule|package|endpackage|interface|endinterface|program|endprogram|" +
  "class|endclass|function|endfunction|task|endtask|generate|endgenerate|" +
  "begin|end|input|output|inout|ref|parameter|localparam|assign|initial|final|" +
  "always|always_ff|always_comb|always_latch|posedge|negedge|edge|wait|" +
  "typedef|const|static|automatic|virtual|extends|implements|import|export|" +
  "default|defparam|primitive|endprimitive|specify|endspecify|table|endtable|" +
  "fork|join|join_any|join_none|disable|assert|assume|cover|property|endproperty|" +
  "sequence|endsequence|covergroup|endgroup|randomize|constraint|new|this|super|" +
  "modport|clocking|endclocking|timeunit|timeprecision";

const CONTROL = "if|else|for|foreach|while|do|repeat|forever|case|casex|casez|endcase|break|continue|return|unique|priority|inside";

const TYPES =
  "logic|wire|reg|bit|byte|shortint|int|longint|integer|time|real|realtime|shortreal|" +
  "genvar|string|chandle|event|void|enum|struct|union|packed|tagged|signed|unsigned|" +
  "supply0|supply1|tri|triand|trior|wand|wor|uwire";

const RULES: Array<[RegExp, string]> = [
  [/^(\/\/[^\n]*|\/\*[\s\S]*?\*\/)/, "tok-comment"],
  [/^(#[^\n]*)/, "tok-comment"],
  [/^("(?:[^"\\\n]|\\.)*"?)/, "tok-string"],
  [/^(`[A-Za-z_]\w*)/, "tok-directive"],
  [/^(\$[A-Za-z_]\w*)/, "tok-system"],
  [/^(\d*'[sS]?[bBoOdDhH][0-9a-fA-FxXzZ?_]+)/, "tok-number"],
  [/^(\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?)/, "tok-number"],
  [new RegExp(`^(?:${CONTROL})\\b`), "tok-control"],
  [new RegExp(`^(?:${KEYWORDS})\\b`), "tok-keyword"],
  [new RegExp(`^(?:${TYPES})\\b`), "tok-type"],
  [/^([A-Za-z_]\w*)(?=\s*\()/, "tok-func"],
  [/^([A-Za-z_]\w*)/, ""],
  [/^(\s+)/, ""],
];

export function highlightSv(source: string): ReactNode[] {
  const out: ReactNode[] = [];
  let rest = source;
  let plain = "";
  let key = 0;

  const flush = () => {
    if (plain) {
      out.push(<Fragment key={`p${key++}`}>{plain}</Fragment>);
      plain = "";
    }
  };

  while (rest.length > 0) {
    let matched = false;

    for (const [re, cls] of RULES) {
      const m = re.exec(rest);
      if (!m || m[0].length === 0) continue;
      matched = true;
      if (cls) {
        flush();
        out.push(
          <span className={cls} key={`t${key++}`}>
            {m[0]}
          </span>,
        );
      } else {
        plain += m[0];
      }
      rest = rest.slice(m[0].length);
      break;
    }

    if (!matched) {
      plain += rest[0];
      rest = rest.slice(1);
    }
  }

  flush();
  return out;
}
