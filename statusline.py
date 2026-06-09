#!/usr/bin/env python3
__version__ = "1.0.0"

import argparse
import json
import os
import socket
import subprocess
import sys
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Claude Code status line")
    parser.add_argument("--user-host", action="store_true")
    parser.add_argument("--path", action="store_true")
    parser.add_argument("--model", action="store_true")
    parser.add_argument(
        "--context-full", action="store_true", help="bar + pct + tokens (shorthand)"
    )
    parser.add_argument("--context-bar", action="store_true")
    parser.add_argument("--context-pct", action="store_true")
    parser.add_argument("--tokens", action="store_true")
    parser.add_argument("--session-time", action="store_true")
    parser.add_argument("--date", action="store_true")
    parser.add_argument("--time", action="store_true")
    args = parser.parse_args()

    # --context-full is shorthand for all three context components
    if args.context_full:
        args.context_bar = args.context_pct = args.tokens = True

    # If no flags given, show everything
    show_all = not any(vars(args).values())

    def want(flag: bool) -> bool:
        return show_all or flag

    # --- Parse JSON from stdin ---
    data = json.loads(sys.stdin.read())

    cwd = data.get("cwd") or (data.get("workspace") or {}).get("current_dir", "")
    model = (data.get("model") or {}).get("display_name", "")
    ctx = data.get("context_window") or {}
    usage_pct = ctx.get("used_percentage") or data.get("usagePercent") or 0
    total_tokens = ctx.get("input_tokens") or data.get("totalTokens") or 0
    repo = (data.get("workspace") or {}).get("repo")
    session = data.get("session") or {}
    session_ms = session.get("duration_ms") or data.get("sessionDurationMs")

    home = os.path.expanduser("~")
    short_cwd = cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd

    # Truncate: replace first 2 non-empty path segments with ... when path is deep enough
    parts = [p for p in short_cwd.split("/") if p]
    if len(parts) > 2:
        short_cwd = ".../" + "/".join(parts[2:])

    # --- ANSI colors ---
    CYAN = "\033[0;36m"
    GREEN = "\033[0;32m"
    MAGENTA = "\033[0;35m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    # --- Left section ---
    left_parts = []

    if want(args.user_host):
        user = os.getlogin()
        host = socket.gethostname().split(".")[0]
        left_parts.append(f"{DIM}{user}@{host}{RESET}")

    if want(args.path):
        left_parts.append(f"{CYAN}{short_cwd}{RESET}")
        if repo:
            git_label = f"{repo['owner']}/{repo['name']}"
            branch = ""
            if cwd:
                try:
                    branch = subprocess.check_output(
                        [
                            "git",
                            "-C",
                            cwd,
                            "--no-optional-locks",
                            "branch",
                            "--show-current",
                        ],
                        stderr=subprocess.DEVNULL,
                        text=True,
                    ).strip()
                except Exception:
                    pass
            left_parts.append(f"{GREEN}{branch or git_label}{RESET}")

    # --- Context bar components ---
    usage_int = round(usage_pct)
    filled = usage_int * 20 // 100
    bar = "█" * filled + "░" * (20 - filled)

    if usage_pct < 70:
        ctx_color = "\033[38;5;82m"
    elif usage_pct < 85:
        ctx_color = "\033[38;5;226m"
    else:
        ctx_color = "\033[38;5;196m"

    if total_tokens > 1_000_000:
        token_display = f"{total_tokens / 1_000_000:.1f}M"
    elif total_tokens > 1_000:
        token_display = f"{total_tokens / 1_000:.1f}K"
    else:
        token_display = str(total_tokens)

    # --- Right section ---
    right_parts = []

    if want(args.model) and model:
        right_parts.append(f"{MAGENTA}{model}{RESET}")

    ctx_pieces = []
    if want(args.context_bar):
        ctx_pieces.append(f"{ctx_color}{bar}{RESET}")
    if want(args.context_pct):
        ctx_pieces.append(f"{ctx_color}{usage_int}%{RESET}")
    if want(args.tokens):
        ctx_pieces.append(f"{token_display} tokens")
    if ctx_pieces:
        right_parts.append(" │ ".join(ctx_pieces))

    if want(args.session_time) and session_ms is not None:
        total_s = int(session_ms) // 1000
        h, rem = divmod(total_s, 3600)
        m, s = divmod(rem, 60)
        session_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        right_parts.append(f"{DIM}session {session_str}{RESET}")

    now = datetime.now()
    if want(args.date):
        right_parts.append(f"{DIM}{now.strftime('%Y-%m-%d')}{RESET}")
    if want(args.time):
        right_parts.append(f"{DIM}{now.strftime('%H:%M:%S')}{RESET}")

    # --- Combine and output ---
    left = "  ".join(left_parts)
    right = "  ".join(right_parts)

    if left and right:
        print(f"{left}  |  {right}")
    else:
        print(left or right)


if __name__ == "__main__":
    main()
