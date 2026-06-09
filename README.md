# claude-p10k

A [Claude Code](https://claude.ai/code) status line script inspired
by [Powerlevel10k](https://github.com/romkatv/powerlevel10k). Shows context usage, model, working directory, git branch,
and time in a clean, configurable bar.

## Preview

```
user@hostname  .../Projects/repo  main  |  Sonnet 4.6  ████████░░░░░░░░░░░░ │ 42% │ 84.0K tokens  2026-06-08  14:23:01
```

## Requirements

- Python 3.7+
- Claude Code with status line support

## Installation

1. Clone the repo:

   ```sh
   git clone https://github.com/after2400/claude-p10k.git ~/.claude/claude-p10k
   ```

2. Add to `~/.claude/settings.json`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "python3 ~/.claude/claude-p10k/statusline.py",
       "refreshInterval": 5,
       "padding": 1
     }
   }
   ```

## Segments

| Flag             | Description                                               |
| ---------------- | --------------------------------------------------------- |
| `--user-host`    | `user@hostname`                                           |
| `--path`         | Current directory (truncated - top 2 levels) + git branch |
| `--model`        | Active Claude model                                       |
| `--context-full` | Context bar + percentage + token count (shorthand)        |
| `--context-bar`  | Visual block progress bar (20 chars)                      |
| `--context-pct`  | Context usage percentage                                  |
| `--tokens`       | Token count (e.g. `84.0K tokens`)                         |
| `--session-time` | Elapsed session duration                                  |
| `--date`         | Current date (`YYYY-MM-DD`)                               |
| `--time`         | Current time (`HH:MM:SS`)                                 |

With no flags, all segments are shown. Pass flags to show only specific segments:

```sh
python3 statusline.py --model --context-full --time
```

## Context bar colors

- Green — under 70%
- Yellow — 70–85%
- Red — over 85%

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setup, code style, and submitting changes.
