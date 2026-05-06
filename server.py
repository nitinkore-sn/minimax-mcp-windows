#!/usr/bin/env python3
# Author: Nitin Kore
# MiniMax M2.7 MCP server for Claude Desktop — routes coding tasks to MiniMax via SambaNova Cloud

import os
import httpx
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ["MINIMAX_API_KEY"]
BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.sambanova.ai/v1")
MODEL = os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7")

mcp = FastMCP("minimax")

ROUTING_RULES = """
ROUTING RULES — follow strictly, no exceptions:

ALWAYS call a MiniMax tool for:
- Writing, generating, or scaffolding any code
- Debugging or fixing code errors
- Reviewing or refactoring code
- Explaining what code does
- Writing tests, scripts, SQL, regex, shell commands
- Any task where the primary output is code

NEVER call MiniMax for (handle as Opus directly):
- Planning, roadmaps, task breakdowns
- Architecture and design decisions
- Tradeoff analysis or comparisons
- Research, summaries, documentation
- Anything where the primary output is prose/strategy
"""


@mcp.prompt()
def routing_instructions() -> str:
    """System-level routing rules for model delegation."""
    return ROUTING_RULES


@mcp.tool()
def minimax_generate_code(description: str, language: str = "Python", context: str = "") -> str:
    """
    ALWAYS call this when the user wants code written, generated, or scaffolded — any language.
    Do NOT answer coding requests yourself; delegate here every time.
    """
    ctx = f"\n\nExisting context:\n{context}" if context else ""
    prompt = f"Write {language} code for: {description}{ctx}\n\nReturn only the code with brief inline comments where non-obvious."
    return _call(prompt, system=f"You are an expert {language} developer. Return clean, production-ready code.")


@mcp.tool()
def minimax_debug_code(code: str, error: str = "", language: str = "") -> str:
    """
    ALWAYS call this when the user wants to fix a bug, an error, or broken code.
    Do NOT attempt to debug code yourself; delegate here every time.
    """
    err_hint = f"\n\nError message:\n{error}" if error else ""
    prompt = f"Find and fix the bug in this {language} code:{err_hint}\n\n```{language}\n{code}\n```\n\nReturn the fixed code and a one-line explanation of the fix."
    return _call(prompt, system="You are an expert debugger. Be precise and minimal — change only what is broken.")


@mcp.tool()
def minimax_code_review(code: str, language: str = "", instructions: str = "") -> str:
    """
    ALWAYS call this when the user wants code reviewed, refactored, or improved.
    Do NOT review code yourself; delegate here every time.
    """
    extra = f"\n\nFocus on: {instructions}" if instructions else ""
    prompt = f"Review this {language} code for bugs, issues, and improvements:\n\n```{language}\n{code}\n```{extra}"
    return _call(prompt, system="You are an expert code reviewer. Be concise and specific. Prioritize correctness, then clarity.")


@mcp.tool()
def minimax_explain_code(code: str, language: str = "") -> str:
    """
    ALWAYS call this when the user wants code explained or understood.
    Do NOT explain code yourself; delegate here every time.
    """
    prompt = f"Explain what this {language} code does, step by step:\n\n```{language}\n{code}\n```"
    return _call(prompt, system="Explain clearly and concisely. Focus on the 'why', not just the 'what'.")


@mcp.tool()
def minimax_write_tests(code: str, language: str = "Python", framework: str = "") -> str:
    """
    ALWAYS call this when the user wants tests written for their code.
    Do NOT write tests yourself; delegate here every time.
    """
    fw = f" using {framework}" if framework else ""
    prompt = f"Write thorough unit tests{fw} for this {language} code:\n\n```{language}\n{code}\n```"
    return _call(prompt, system=f"You are an expert in {language} testing. Cover happy path, edge cases, and error cases.")


def _call(prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    with httpx.Client(timeout=120) as client:
        resp = client.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": messages},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    mcp.run()
