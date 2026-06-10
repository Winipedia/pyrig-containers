"""GitHub Actions workflow for deploying.

Provides the ``DeployWorkflowConfigFile`` class, which generates the
``.github/workflows/deploy.yml`` workflow file. This workflow is the final
step in the automated CI/CD pipeline and runs after a successful release.
"""

from pyrig.rig.configs.remote_version_control.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """You can override methods from the base class to customize behavior."""
