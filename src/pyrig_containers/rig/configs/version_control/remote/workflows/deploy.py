"""Extension of the deploy workflow that builds and pushes a container image.

Runs after a release and tags the image with both the release version and
`latest`.
"""

from typing import Any

from pyrig.rig.configs.version_control.remote.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)

from pyrig_containers.rig.tools.containers.engine import ContainerEngine
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """Deploy workflow that adds a job to build and push a container image to GHCR."""

    def jobs(self) -> dict[str, Any]:
        """Add the container image publish job to the base jobs.

        Returns:
            Dict combining the base jobs with the container image job.
        """
        return {
            **super().jobs(),
            **self.job_container_image(),
        }

    def job_container_image(self) -> dict[str, Any]:
        """Build the job that builds and pushes the container image to GHCR.

        Requests `packages: write` permission at the job level, required to
        push to GHCR.

        Returns:
            Dict mapping the derived job ID to its configuration.
        """
        return self.job(
            self.job_container_image,
            permissions={
                **self.permission_contents(),
                **self.permission_packages(write=True),
            },
            steps=self.steps_container_image(),
        )

    def steps_container_image(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the publish-container-image job.

        Returns:
            Ordered list of step dicts: core setup, log in to the registry,
            build the image, then push the versioned tag and the latest tag.
        """
        return [
            *self.steps_core_setup(),
            self.step_login_container_registry(),
            self.step_extract_version(),
            self.step_build_container_image(),
            self.step_push_container_image_version(),
            self.step_push_container_image_latest(),
        ]

    def step_login_container_registry(self) -> dict[str, Any]:
        """Build a step that logs podman in to the container registry.

        Authenticates as the workflow actor, using the automatic
        `GITHUB_TOKEN` secret as the password.

        Returns:
            Step that runs `podman login` against the registry.
        """
        actor_var, token_var = "ACTOR", "TOKEN"
        return self.step(
            self.step_login_container_registry,
            run=ContainerEngine.I.login_args(
                registry=ContainerRegistry.I.host(),
                username=self.insert_parameter_expansion(actor_var),
                password=self.insert_parameter_expansion(token_var),
            ).multiline(),
            env={
                actor_var: self.insert_actor(),
                token_var: self.insert_github_token(),
            },
        )

    def step_build_container_image(self) -> dict[str, Any]:
        """Build a step that builds the container image.

        Tags the built image with both the versioned tag and the `latest` tag.

        Returns:
            Step that runs `podman build`.
        """
        return self.step(
            self.step_build_container_image,
            run=ContainerEngine.I.build_args(
                tags=(
                    self.container_image_tag_version(),
                    self.container_image_tag_latest(),
                ),
            ).multiline(),
            env={
                self.version_var(): self.insert_output_version(),
            },
        )

    def step_push_container_image_version(self) -> dict[str, Any]:
        """Build a step that pushes the versioned image tag to the registry.

        Returns:
            Step that runs `podman push` for the versioned tag.
        """
        return self.step(
            self.step_push_container_image_version,
            run=ContainerEngine.I.push_args(
                tag=self.container_image_tag_version(),
            ).multiline(),
            env={
                self.version_var(): self.insert_output_version(),
            },
        )

    def step_push_container_image_latest(self) -> dict[str, Any]:
        """Build a step that pushes the `latest` image tag to the registry.

        Returns:
            Step that runs `podman push` for the `latest` tag.
        """
        return self.step(
            self.step_push_container_image_latest,
            run=str(ContainerEngine.I.push_args(tag=self.container_image_tag_latest())),
        )

    def container_image_tag_version(self) -> str:
        """Build the project's image reference tagged with the project version.

        Returns:
            Image reference tagged with the bare project version.
        """
        return ContainerRegistry.I.image_tag(self.insert_version_expansion())

    def container_image_tag_latest(self) -> str:
        """Build the project's image reference tagged `latest`."""
        return ContainerRegistry.I.image_tag("latest")

    def insert_actor(self) -> str:
        """Return the expression that resolves to the workflow actor.

        Returns:
            GitHub Actions expression for `github.actor`.
        """
        return self.insert_expression("github.actor")
