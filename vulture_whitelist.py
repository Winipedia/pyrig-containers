"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.string_ import StringConfigFile
from pyrig.rig.tools.base.tool import Tool

from pyrig_containers.rig.configs.container_file import ContainerfileConfigFile
from pyrig_containers.rig.tools.containers.engine import ContainerEngine
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry

_CONFIG_FILE_OVERRIDES = (
    ConfigFile.extension,
    ConfigFile.extension_separator,
    ConfigFile.parent_path,
    ConfigFile.stem,
    StringConfigFile.content,
)
_CONFIG_FILES = (ContainerfileConfigFile,)
_TOOLS = (
    ContainerEngine,
    ContainerRegistry,
)
_TOOLS_OVERRIDES = (
    Tool.dev_dependencies,
    Tool.group,
    Tool.link_url,
    Tool.name,
)
