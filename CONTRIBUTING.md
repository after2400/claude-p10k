# Contributing

Thanks for your interest in contributing to claude-p10k!

## Dev setup

1. Fork and clone the repo
2. Install pre-commit hooks:
   ```sh
   pip install pre-commit
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

## Making changes

- Branch from `main` using a descriptive name: `feat/my-feature`, `fix/broken-segment`
- Keep changes focused — one concern per PR
- Update the README if you add or change a segment flag

## Code style

- **Python** (`statusline.py`) — formatted and linted with [Ruff](https://docs.astral.sh/ruff/)
- **Everything else** — formatted with [Prettier](https://prettier.io/)

To check locally before pushing:

```sh
ruff check statusline.py
ruff format --check statusline.py
npx prettier --check .
```

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

feat(statusline): add vim mode indicator
fix(ci): correct fetch-depth for commitlint
docs: update segment flag table
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Valid scopes** (optional): `statusline`, `ci`, `docs`, `config`

Commit messages and PR titles are enforced automatically via GitHub Actions.

## Submitting a PR

1. Ensure all CI checks pass
2. Write a clear PR title following Conventional Commits
3. Describe what changed and why in the PR body
