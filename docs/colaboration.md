# Contributing

Want to add a mini-app to this hub? Here's the flow.

## 1. Fork and branch

Fork this repo, then create a branch for your app off `dev`:

```bash
git checkout -b feat/add-<app-name> dev
```

## 2. Scaffold with cookiecutter

Don't hand-write the folder structure — generate it:

```bash
cd apps
uvx cookiecutter ./template
```

Fill in `manifest.json`, write your endpoint logic in `main.py`, keep `models/` (Pydantic) and `utils/` for anything beyond a one-liner.

## 3. Make sure it's green before opening a PR

```bash
cd apps/<app-name>
uvx ruff check .
uvx ruff format --check .
uv run pytest -v
```

Same checks run in CI — if they fail there, the PR can't merge.

## 4. Commit messages: this is not optional

Every commit touching your app **must** use a [Conventional Commits](https://www.conventionalcommits.org/) prefix, because CI reads it to bump your app's version automatically:

| Prefix | Meaning | Version bump |
|---|---|---|
| `fix: ...` | bug fix | patch (`0.1.0` → `0.1.1`) |
| `feat: ...` | new feature | minor (`0.1.0` → `0.2.0`) |
| `feat!: ...` or `BREAKING CHANGE:` in the body | breaking change | major, but only once the app is already past `1.0.0` |
| `chore:`, `docs:`, `refactor:`, `test:` | no user-facing change | no bump |

Get the prefix right — it's the only signal the pipeline has.

## 5. Open the Pull Request — into `dev`, not `main`

Open the PR against `dev`. CI (ruff + tests) must pass before it can be merged. Keep your PR scoped to your own `apps/<app-name>/` folder — don't touch other apps or shared files (`.github/`, `versioning/`, root `pyproject.toml`) unless that's the point of the PR.

## 6. Review and merge

Only the maintainer merges PRs and only the maintainer's merge to `main` triggers a Docker Hub publish — external contributors never get write access or touch secrets. Once merged, your app's image is built and pushed automatically, versioned from the commits you wrote in step 4.
