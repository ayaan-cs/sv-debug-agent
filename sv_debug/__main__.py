"""CLI: python -m sv_debug"""

from __future__ import annotations

from .pipeline import debug_systemverilog


def main() -> None:
    print("Paste simulator output, compiler error, or SystemVerilog source below.")
    print("(Type END on its own line when finished.)")
    print("")

    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    result = debug_systemverilog("\n".join(lines))
    print("\n=== DEBUGGING RESULT ===\n")
    print(result)


if __name__ == "__main__":
    main()
