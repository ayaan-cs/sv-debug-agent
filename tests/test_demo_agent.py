"""Offline tests — never call Gemini or require an API key."""

from __future__ import annotations

import os

import pytest

from sv_debug.config import demo_mode_enabled, has_api_key
from sv_debug.demo import (
    demo_debug_systemverilog,
    looks_like_compiler_issue,
    looks_like_source,
    looks_like_x_issue,
)
from sv_debug.helpers import check_common_lint_patterns
from sv_debug.pipeline import debug_systemverilog
from sv_debug.samples import SAMPLES, get_sample


@pytest.fixture(autouse=True)
def force_demo_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep contributors safe: tests never use a real Gemini key."""
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    # Ensure config reloads env after monkeypatch
    import sv_debug.config as config

    monkeypatch.setattr(config, "_ENV_LOADED", True)


def test_demo_mode_forced() -> None:
    assert demo_mode_enabled() is True
    assert has_api_key() is False


def test_missing_reset_lint() -> None:
    sample = get_sample("missing-reset")
    result = check_common_lint_patterns(sample["content"])
    assert "always_ff" in result
    assert "reset" in result.lower()


def test_old_always_lint() -> None:
    sample = get_sample("old-always")
    result = check_common_lint_patterns(sample["content"])
    assert "always @" in result or "old-style" in result.lower()


def test_clean_source_has_no_issue_noise() -> None:
    source = """\
module ok (
  input  logic clk,
  input  logic reset,
  output logic q
);
  always_ff @(posedge clk or posedge reset) begin
    if (reset) q <= 0;
    else q <= ~q;
  end
endmodule"""
    result = check_common_lint_patterns(source)
    assert "No obvious issues" in result


@pytest.mark.parametrize(
    ("sample_id", "expect_tokens"),
    [
        ("missing-reset", ["Demo mode", "Quick lint check", "reset"]),
        ("old-always", ["Demo mode", "always"]),
        ("syntax-error", ["Demo mode", "Compiler", "syntax error"]),
        ("x-log", ["Demo mode", "X-propagation"]),
    ],
)
def test_demo_pipeline_on_samples(sample_id: str, expect_tokens: list[str]) -> None:
    sample = get_sample(sample_id)
    result = debug_systemverilog(sample["content"])
    for token in expect_tokens:
        assert token.lower() in result.lower()


def test_all_samples_have_required_fields() -> None:
    assert len(SAMPLES) >= 4
    ids = set()
    for sample in SAMPLES:
        assert sample["id"]
        assert sample["title"]
        assert sample["content"].strip()
        ids.add(sample["id"])
    assert len(ids) == len(SAMPLES)


def test_classifier_helpers() -> None:
    assert looks_like_compiler_issue("tb.v:12: syntax error")
    assert looks_like_x_issue("# time 20: q=x (first unknown observed here)")
    assert looks_like_source("module foo; endmodule")


def test_demo_function_matches_pipeline() -> None:
    text = get_sample("syntax-error")["content"]
    assert "Gemini" not in demo_debug_systemverilog(text) or "without calling Gemini" in demo_debug_systemverilog(text)
    # Pipeline must stay in demo path under forced env
    assert os.getenv("DEMO_MODE") == "true"
    assert "Demo mode" in debug_systemverilog(text)
