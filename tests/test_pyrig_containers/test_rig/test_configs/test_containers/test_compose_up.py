"""Test module."""

from pathlib import Path
from uuid import uuid4

import pytest
from pyrig.core.subprocesses import Args

from pyrig_containers.rig.configs.containers.compose_up import ComposeUpConfigFile


@pytest.mark.parametrize(
    ("mode", "extra_flags", "cleanup_flags", "expected_logs", "not_expected_logs"),
    [
        (
            "pull",
            (),
            (),
            "Trying to pull ghcr.io/winipedia/pyrig-containers:latest",
            "STEP 1/",
        ),
        (
            "build",
            ("--build",),
            ("--rmi=local",),
            "STEP 1/",
            "Trying to pull ghcr.io/winipedia/pyrig-containers:latest",
        ),
    ],
)
def test_execute_compose_up(  # noqa: PLR0913
    mode: str,
    extra_flags: tuple[str, ...],
    cleanup_flags: tuple[str, ...],
    expected_logs: str,
    not_expected_logs: str,
    *,
    on_linux: bool,
) -> None:
    """Check that the script pulls or builds the app image."""
    if not on_linux:
        return
    usage_exit_code = 2
    project = f"pyrigtest{uuid4().hex}"
    env = f"COMPOSE_PROJECT_NAME={project}"
    args = Args(
        "env",
        env,
        "bash",
        "compose-up.sh",
        mode,
        "--exit-code-from=app",
        *extra_flags,
    )
    result = args.run(check=False)
    Args(
        "env",
        env,
        "uvx",
        "--from=podman-compose",
        "podman",
        "compose",
        "--file=compose.yml",
        f"--file=compose.{mode}.yml",
        "down",
        *cleanup_flags,
    ).run()
    logs = result.stdout + result.stderr
    assert result.returncode == usage_exit_code
    assert "A pyrig plugin to integrate containers." in logs
    assert expected_logs in logs, logs
    assert not_expected_logs not in logs, logs


class TestComposeUpConfigFile:
    """Test class."""

    def test_compose_up_args(self) -> None:
        """Test method."""
        assert tuple(ComposeUpConfigFile.I.compose_up_args()) == (
            "exec",
            "podman",
            "compose",
            "--file=compose.yml",
            '--file=compose."${1}".yml',
            "up",
            '"${@:2}"',
        )

    def test_parent_path(self) -> None:
        """Test method."""
        assert ComposeUpConfigFile.I.parent_path() == Path()

    def test_script(self) -> None:
        """Test method."""
        assert (
            ComposeUpConfigFile.I.script()
            == r"""exec \
  podman \
  compose \
  --file=compose.yml \
  --file=compose."${1}".yml \
  up \
  "${@:2}"
"""
        )

    def test_stem(self) -> None:
        """Test method."""
        assert ComposeUpConfigFile.I.stem() == "compose-up"
