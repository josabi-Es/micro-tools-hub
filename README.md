# micro-tools-hub

A personal hub of small backend APIs. Each one is a tiny FastAPI service in its own container, built and pushed to Docker Hub automatically. Browse `apps/` to see what tools exist and pull the image you need, no shared setup required.

## Structure

```
apps/
  template/        # cookiecutter scaffold for a new mini-app (not a real app)
  <app-name>/       # one folder per mini-app, all structured the same way
    main.py
    manifest.json   # name, version, docker_repo, endpoint, tags
    Dockerfile
    pyproject.toml
    tests/
spec/                 # planning docs (constitution + feature specs)
```

## Add a new app

```bash
cd apps
uvx cookiecutter ./template
```

Fill in the generated `manifest.json`, write your endpoint logic in `main.py`, then open a PR to `dev`.

## Use an existing app

Look up the app under `apps/`, then:

```bash
docker pull salillas/<app-name>
docker run -p 8000:8000 salillas/<app-name>
```

## Publishing to Docker Hub

Publishing is automatic, not manual. On every PR into `main` that touches an app, CI bumps that app's `version` in `manifest.json` from the Conventional Commit types in the PR (`fix`→patch, `feat`→minor, see `versioning/`). Once merged, `cd-image.yml` builds and pushes the image to Docker Hub tagged `latest` and with that version.

No registry, no shared runtime, no coordination between apps. The image on Docker Hub *is* the deployment: merge → build → push → every consumer that pulls `latest` gets the new version, that's the whole release loop.

## Branching

Work happens on `dev`; `main` reflects what's been released. See `spec/constitution/` for the full rationale and `spec/features/` for what's planned per version.
