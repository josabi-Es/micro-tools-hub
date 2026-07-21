# 🧰 micro-tools-hub

![CI](https://github.com/josabi-Es/micro-tools-hub/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/josabi-Es/micro-tools-hub/actions/workflows/cd-image.yml/badge.svg)

<img src="https://skillicons.dev/icons?i=python,fastapi,docker,git,githubactions&theme=light" />

A personal hub of small backend APIs. Each mini-app is a self-contained FastAPI service, scaffolded from the same [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template, tested and linted the same way, and shipped to Docker Hub the same way — no shared runtime, no coordination between apps, no manual release step.

Browse `apps/` to see what tools exist and pull the image you need.

## 🔁 How a change ships

<svg width="100%" viewBox="0 0 920 210" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowTeal" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#00ffc8"/>
    </marker>
    <marker id="arrowRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#ff5470"/>
    </marker>
  </defs>

  <rect width="920" height="210" rx="16" fill="#0b0f14"/>
  <text x="460" y="24" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" fill="#e6f6f1" opacity=".8">micro-tools-hub · CI/CD flow</text>

  <path id="pathFail" d="M256,120 Q154,40 52,120" fill="none" stroke="#ff5470" stroke-width="1.5" marker-end="url(#arrowRed)"/>
  <circle r="3" fill="#ff5470"><animateMotion dur="1.8s" repeatCount="indefinite"><mpath href="#pathFail"/></animateMotion></circle>
  <text x="154" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#ff5470">&lt; test failed</text>

  <path id="pathA" d="M82,120 L226,120" stroke="#00ffc8" stroke-width="1.5" marker-end="url(#arrowTeal)"/>
  <circle r="3" fill="#00ffc8"><animateMotion dur="1.8s" repeatCount="indefinite"><mpath href="#pathA"/></animateMotion></circle>
  <text x="154" y="138" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#00ffc8">push to dev</text>

  <path id="pathB" d="M286,120 L430,120" stroke="#00ffc8" stroke-width="1.5" marker-end="url(#arrowTeal)"/>
  <circle r="3" fill="#00ffc8"><animateMotion dur="1.8s" begin=".4s" repeatCount="indefinite"><mpath href="#pathB"/></animateMotion></circle>
  <text x="358" y="102" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#00ffc8">merge into main</text>

  <path id="pathC" d="M490,120 L634,120" stroke="#00ffc8" stroke-width="1.5" marker-end="url(#arrowTeal)"/>
  <circle r="3" fill="#00ffc8"><animateMotion dur="1.8s" begin=".8s" repeatCount="indefinite"><mpath href="#pathC"/></animateMotion></circle>
  <text x="562" y="102" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#00ffc8">build and push</text>

  <path id="pathD" d="M838,110 L694,110" stroke="#ff5470" stroke-width="1.5" marker-end="url(#arrowRed)"/>
  <circle r="3" fill="#ff5470"><animateMotion dur="1.8s" repeatCount="indefinite"><mpath href="#pathD"/></animateMotion></circle>
  <text x="766" y="95" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#ff5470">&lt; check latest</text>

  <path id="pathE" d="M694,130 L838,130" stroke="#00ffc8" stroke-width="1.5" marker-end="url(#arrowTeal)"/>
  <circle r="3" fill="#00ffc8"><animateMotion dur="1.8s" begin=".4s" repeatCount="indefinite"><mpath href="#pathE"/></animateMotion></circle>
  <text x="766" y="148" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#00ffc8">pull image &gt;</text>

  <circle cx="52" cy="120" r="30" fill="rgba(0,255,200,0.08)" stroke="#00ffc8" stroke-width="1.5"/>
  <text x="52" y="128" text-anchor="middle" font-size="24">👤</text>
  <text x="52" y="168" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#e6f6f1">User</text>

  <circle cx="256" cy="120" r="30" fill="rgba(0,255,200,0.08)" stroke="#00ffc8" stroke-width="1.5" stroke-dasharray="4 3"/>
  <image href="https://skillicons.dev/icons?i=githubactions" x="236" y="100" width="40" height="40"/>
  <text x="256" y="168" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#e6f6f1">GitHub Actions CI</text>

  <circle cx="460" cy="120" r="30" fill="rgba(0,255,200,0.08)" stroke="#00ffc8" stroke-width="1.5"/>
  <image href="https://skillicons.dev/icons?i=githubactions" x="440" y="100" width="40" height="40"/>
  <text x="460" y="168" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#e6f6f1">Git Actions CD</text>

  <circle cx="664" cy="120" r="30" fill="rgba(0,255,200,0.08)" stroke="#00ffc8" stroke-width="1.5"/>
  <image href="https://skillicons.dev/icons?i=docker" x="644" y="100" width="40" height="40"/>
  <text x="664" y="168" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#e6f6f1">Docker Hub</text>

  <circle cx="868" cy="120" r="30" fill="rgba(0,255,200,0.08)" stroke="#00ffc8" stroke-width="1.5"/>
  <text x="868" y="128" text-anchor="middle" font-size="24">🌍</text>
  <text x="868" y="168" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#e6f6f1">External App</text>
</svg>

- Write commits with a [Conventional Commit](https://www.conventionalcommits.org/) prefix (`fix`, `feat`, `feat!`) — that's the only signal the pipeline needs.
- Open the PR into `main`: CI lints and tests the apps you touched, then bumps their `version` in `manifest.json` automatically (patch/minor/major from your commits — see `versioning/`).
- Merge: the image is built, checked for size, and pushed to Docker Hub tagged `latest` and with that exact version. That's the whole release loop.


## 📁 Structure

```
apps/
  template/        # cookiecutter scaffold for a new mini-app (not a real app)
  <app-name>/       # one folder per mini-app, all structured the same way
    main.py
    manifest.json   # name, version, docker_repo, endpoint, tags
    Dockerfile
    pyproject.toml
    tests/
versioning/          # auto-bumps each app's version from its commits (see above)
spec/                 # planning docs (constitution + feature specs)
```

## ➕ Add a new app

```bash
cd apps
uvx cookiecutter ./template
```

Fill in the generated `manifest.json`, write your endpoint logic in `main.py`, then open a PR to `dev`. See [`docs/colaboration.md`](docs/colaboration.md) for the full contributor workflow.

## 🌿 Branching

Work happens on `dev`; `main` reflects what's been released. See `spec/constitution/` for the full rationale and `spec/features/` for what's planned per version.
