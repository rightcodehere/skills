#!/usr/bin/env python3
"""Human-in-the-loop reproduction loop.
Copy this file, edit the steps below, and run it.
The agent runs the script; the user follows prompts in their terminal.

Usage:
    python hitl-loop.template.py

Two helpers:
    step("<instruction>")          -> show instruction, wait for Enter
    capture("<question>")          -> show question, read response, return it

At the end, captured values are printed as KEY=VALUE for the agent to parse.
"""


def step(instruction: str) -> None:
    print(f"\n>>> {instruction}")
    input("    [Enter when done] ")


def capture(question: str) -> str:
    print(f"\n>>> {question}")
    return input("    > ")


# --- edit below ---------------------------------------------------------

step("Open the app at http://localhost:3000 and sign in.")

errored = capture("Click the 'Export' button. Did it throw an error? (y/n)")

error_msg = capture("Paste the error message (or 'none'):")

# --- edit above ---------------------------------------------------------

print("\n--- Captured ---")
print(f"ERRORED={errored}")
print(f"ERROR_MSG={error_msg}")
