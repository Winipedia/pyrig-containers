# pyrig-containers

<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/deploy.yml)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/pyrig-containers/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-containers)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- code-quality -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityLinter](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- tooling -->
[![ContainerEngine](https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6)](https://podman.io)
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-containers?style=social)](https://github.com/Winipedia/pyrig-containers)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![ContainerRegistry](https://img.shields.io/badge/GHCR-Container_Image-black?logo=github&logoColor=white)](https://github.com/Winipedia/pyrig-containers/pkgs/container/pyrig-containers)
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/pyrig-containers)
[![PackageIndex](https://img.shields.io/pypi/v/pyrig-containers?logo=pypi&logoColor=white)](https://pypi.org/project/pyrig-containers)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/pyrig-containers)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/pyrig-containers)](https://github.com/Winipedia/pyrig-containers/blob/main/LICENSE)

---

> A pyrig plugin to integrate containers.

---

## Overview

pyrig-containers is a [pyrig](https://github.com/Winipedia/pyrig) plugin that
packages your project as a container image and publishes it on every release.

## What it adds

- **Containerfile** — a ready-to-use `Containerfile` generated at the project
  root.
- **Container tooling** — wrappers for the container engine (Podman) and the
  GitHub Container Registry, each contributing a badge.
- **Automatic publishing** — a deploy step that builds the image and pushes it
  to the registry after a successful release.

## Usage

```bash
uv add pyrig-containers --dev
uv run pyrig sync
```

Building images locally requires Podman to be installed.

## Documentation

Full documentation, including the auto-generated API reference, is available on
the [documentation site](https://Winipedia.github.io/pyrig-containers).
