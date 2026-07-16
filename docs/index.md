# Home

<!-- project-status -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-containers/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-containers/actions/workflows/deploy.yml)
[![ProjectTester](https://codecov.io/gh/Winipedia/pyrig-containers/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-containers)
<!-- code-quality -->
[![ByteOrderMarkerFormatter](https://img.shields.io/badge/BOM-fix--byte--order--marker-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![CaseConflictChecker](https://img.shields.io/badge/case--conflict-check--case--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![EndOfFileFormatter](https://img.shields.io/badge/EOF-end--of--file--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![EndOfLineFormatter](https://img.shields.io/badge/EOL-mixed--line--ending-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONFormatter](https://img.shields.io/badge/JSON-pretty--format--json-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONLinter](https://img.shields.io/badge/JSON-check--json-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![LargeFileChecker](https://img.shields.io/badge/large--files-check--added--large--files-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![MarkdownLinter](https://img.shields.io/badge/Markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![MergeConflictChecker](https://img.shields.io/badge/merge--conflict-check--merge--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![ModuleTestNamingChecker](https://img.shields.io/badge/test--naming-name--tests--test-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![ShellFormatter](https://img.shields.io/badge/shell-shfmt-orange)](https://github.com/mvdan/sh)
[![ShellLinter](https://img.shields.io/badge/shell-shellcheck-blue)](https://github.com/koalaman/shellcheck)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TOMLLinter](https://img.shields.io/badge/TOML-tombi-blueviolet)](https://github.com/tombi-toml/tombi)
[![TrailingWhitespaceFormatter](https://img.shields.io/badge/whitespace-trailing--whitespace--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![YAMLLinter](https://img.shields.io/badge/YAML-ryl-red)](https://github.com/owenlamont/ryl)
<!-- tooling -->
[![ContainerEngine](https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6)](https://podman.io)
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-containers?style=social)](https://github.com/Winipedia/pyrig-containers)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
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

pyrig-containers integrates containers into a pyrig-managed project through three
pieces: generation of a `Containerfile`, container tooling registered in the rig,
and an automated step that publishes the image to the GitHub Container Registry
(GHCR) on release. This page describes each piece; see the API Reference for the
generated, code-level documentation.

```bash
uv add pyrig-containers --dev
uv run pyrig sync
```

If you want to locally build images or do other container actions you will need
to install podman locally as well.

## Components

### Containerfile generation

`ContainerfileConfigFile` generates a `Containerfile` at the project root. It starts
from a slim Python base image matching the project's supported Python version,
installs `uv` from its official image, and copies project metadata and the lock
file before the source tree to maximise build-cache reuse. The image runs as a
non-root `appuser` (UID 1000) and installs only non-development dependencies.
Functionality is guaranteed for Podman, the container engine the plugin wraps.

### Container engine

`ContainerEngine` wraps Podman. It provides the command arguments used to
authenticate with a registry, to build and tag an image from the
Containerfile, and to push an individual tag. It contributes a Podman
badge to the project's README.

### Container registry

`ContainerRegistry` models the GitHub Container Registry. It owns the registry host
(`ghcr.io`), composes the project's lowercased image name
(`ghcr.io/<owner>/<project>`, since GHCR requires lowercase names), and builds
tagged image references from it. It contributes a GHCR badge to the
project's README.

### Deploy workflow

The deploy workflow is extended with a `container-image` job. After a successful
release it installs Podman, logs in to GHCR using the workflow actor and the
automatic `GITHUB_TOKEN`, builds the image from the Containerfile, and pushes it
under two tags: the released version (`:<version>`) and `:latest`.

## API Reference

For class- and method-level details, see the [API](api.md) Reference, which is generated
automatically from the source.
