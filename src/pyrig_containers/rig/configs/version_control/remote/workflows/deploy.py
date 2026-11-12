"""Extend deployment with the reusable container-image workflow."""

from collections.abc import Callable
from typing import Any, override

from pyrig.rig.configs.version_control.remote.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)

from pyrig_containers.rig.configs.version_control.remote.workflows.container_image import (  # noqa: E501
    ContainerImageWorkflowConfigFile,
)


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """Include container-image publishing in the deployment workflow."""

    @override
    def jobs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the base deployment jobs and the container-image workflow call."""
        return (*super().jobs(), self.job_container_image)

    def job_container_image(self) -> dict[str, Any]:
        """Call the reusable container-image workflow."""
        return self.job_workflow_call(
            self.job_container_image,
            workflow=ContainerImageWorkflowConfigFile,
        )
