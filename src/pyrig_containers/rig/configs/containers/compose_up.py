"""Generate the Compose startup script."""

from pathlib import Path
from typing import override

from pyrig.core.subprocesses import Args
from pyrig.rig.configs.base.shell import ShellConfigFile

from pyrig_containers.rig.configs.containers.compose import ComposeConfigFile
from pyrig_containers.rig.tools.containers.engine import ContainerEngine


class ComposeUpConfigFile(ShellConfigFile):
    """Generate a script to start a locally built or published image."""

    @override
    def parent_path(self) -> Path:
        """Return the project root."""
        return Path()

    @override
    def script(self) -> str:
        """Return the image-source selection and Compose command."""
        return f"{self.compose_up_args().multiline()}\n"

    @override
    def stem(self) -> str:
        """Return the startup script filename stem."""
        return "compose-up"

    def compose_up_args(self) -> Args:
        """Return the arguments for the Compose up command."""
        return Args(
            "exec",
            *ContainerEngine.I.compose_up_files_args(
                '"${@:2}"',
                files=(
                    ComposeConfigFile.I.path(),
                    ComposeConfigFile.I.override_file('"${1}"'),
                ),
            ),
        )
