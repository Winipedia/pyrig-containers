# pyrig-containers

<!-- security -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/deploy.yml)
<!-- code-quality -->
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/pyrig-containers/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-containers)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- tooling -->
[![ContainerEngine](https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6)](https://podman.io)
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-containers?style=social)](https://github.com/Winipedia/pyrig-containers)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- documentation -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://www.mkdocs.org)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-black?style=for-the-badge&logo=github&logoColor=white)](https://Winipedia.github.io/pyrig-containers)
<!-- project-info -->
[![ContainerRegistry](https://img.shields.io/badge/GHCR-Container_Image-black?logo=github&logoColor=white)](https://github.com/Winipedia/pyrig-containers/pkgs/container/pyrig-containers)
[![PackageIndex](https://img.shields.io/pypi/v/pyrig-containers?logo=pypi&logoColor=white)](https://pypi.org/project/pyrig-containers)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/pyrig-containers)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/pyrig-containers)](https://github.com/Winipedia/pyrig-containers/blob/main/LICENSE)

---

> A pyrig plugin to integrate containers.

---

## Overview

pyrig-containers is a [pyrig](https://github.com/Winipedia/pyrig) plugin that adds
container support to a pyrig-managed Python project. Installed as a development
dependency, it plugs into pyrig's config-generation and tooling system, so the
files and CI steps needed to build and publish a container image are scaffolded,
validated, and kept in sync automatically — the same way as the rest of your
project.

## What it adds

- **A production-ready Containerfile** — generated at the project root from a slim
  Python base image, using uv for dependency installation, a non-root runtime
  user, and a layer order tuned for build-cache reuse.
- **Container tooling in the rig** — a Podman-based container engine and the
  GitHub Container Registry (GHCR) are registered as first-class tools, each
  contributing a Markdown badge to the README.
- **Automated image publishing** — the deploy workflow gains a job that, after a
  successful release, builds the image and pushes it to GHCR tagged with both the
  released version and `latest`.

## Requirements

pyrig-containers builds on pyrig and follows its conventions. Functionality is
guaranteed only for the container engine wrapped by the plugin's tool class —
Podman in this project. Images are built with Podman and published to GHCR
using the repository's built-in GitHub token, so there are no extra registry
credentials to configure.

## Documentation

Full documentation, including the auto-generated API reference, is available at
the [project documentation site](https://Winipedia.github.io/pyrig-containers).
