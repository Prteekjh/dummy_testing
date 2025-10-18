#!/usr/bin/env python3
"""Simple terminal chat client for OpenAI's GPT-4o model."""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Dict

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "The 'openai' package is required. Install it with 'pip install openai'."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive terminal chat client for the GPT-4o model."
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="Model name to use (default: gpt-4o).",
    )
    parser.add_argument(
        "--system",
        default=None,
        help="Optional system prompt that primes the assistant.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature between 0 and 2 (default: 0.7).",
    )
    return parser.parse_args()


def ensure_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Missing OPENAI_API_KEY environment variable. "
            "Set it to your OpenAI API key before running this script."
        )


def main() -> None:
    args = parse_args()
    ensure_api_key()
    client = OpenAI()

    messages: List[Dict[str, str]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})

    print("GPT-4o terminal chat. Type 'exit' or press Ctrl-D to quit.\n")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            print()  # newline for clean exit
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting…")
            break

        if not user_input.strip():
            continue

        if user_input.strip().lower() in {"exit", "quit"}:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            stream = client.chat.completions.create(
                model=args.model,
                messages=messages,
                temperature=args.temperature,
                stream=True,
            )
        except Exception as exc:  # pragma: no cover - runtime dependent
            print(f"Error querying OpenAI: {exc}", file=sys.stderr)
            messages.pop()  # remove the last user message so it can be retried
            continue

        assistant_response_parts: List[str] = []
        print("Assistant: ", end="", flush=True)
        for chunk in stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                assistant_response_parts.append(content)
                print(content, end="", flush=True)
        print()

        assistant_message = "".join(assistant_response_parts)
        messages.append({"role": "assistant", "content": assistant_message})

    print("Goodbye!")


if __name__ == "__main__":
    main()
