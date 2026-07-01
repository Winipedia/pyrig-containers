"""Extension of the deploy workflow that publishes a container image to GHCR."""

from typing import Any

from pyrig.rig.configs.version_control.remote.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)

from pyrig_containers.rig.tools.containers.engine import ContainerEngine
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """Deploy workflow that adds a build-and-push-image-to-GHCR job after release."""

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
            job_func=self.job_container_image,
            permissions={"packages": "write"},
            steps=self.steps_container_image(),
        )

    def steps_container_image(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the publish-container-image job.

        Returns:
            Ordered list of step dicts: core setup, install the container
            engine, log in to the registry, build the image, then push the
            versioned tag and the latest tag.
        """
        return [
            *self.steps_core_setup(),
            self.step_install_container_engine(),
            self.step_login_container_registry(),
            self.step_build_container_image(),
            self.step_push_container_image_version(),
            self.step_push_container_image_latest(),
        ]

    def step_install_container_engine(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that installs podman on the runner.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step using `redhat-actions/podman-install@main`.
        """
        return self.step(
            step_func=self.step_install_container_engine,
            uses="redhat-actions/podman-install@main",
            step=step,
        )

    def step_login_container_registry(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that logs podman in to the container registry.

        Authenticates as the workflow actor, using the automatic
        `GITHUB_TOKEN` secret as the password.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs `podman login` against the registry.
        """
        return self.step(
            step_func=self.step_login_container_registry,
            run=str(
                ContainerEngine.I.login_args(
                    registry=ContainerRegistry.I.host(),
                    username=self.insert_actor(),
                    password=self.insert_github_token(),
                )
            ),
            step=step,
        )

    def step_build_container_image(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that builds the container image.

        Tags the built image with both the versioned tag and the `latest` tag.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs `podman build`.
        """
        return self.step(
            step_func=self.step_build_container_image,
            run=str(
                ContainerEngine.I.build_args(
                    tags=(
                        self.container_image_tag_version(),
                        self.container_image_tag_latest(),
                    ),
                )
            ),
            step=step,
        )

    def step_push_container_image_version(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that pushes the versioned image tag to the registry.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs `podman push` for the versioned tag.
        """
        return self.step(
            step_func=self.step_push_container_image_version,
            run=str(
                ContainerEngine.I.push_args(tag=self.container_image_tag_version())
            ),
            step=step,
        )

    def step_push_container_image_latest(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that pushes the `latest` image tag to the registry.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs `podman push` for the `latest` tag.
        """
        return self.step(
            step_func=self.step_push_container_image_latest,
            run=str(ContainerEngine.I.push_args(tag=self.container_image_tag_latest())),
            step=step,
        )

    def container_image_tag_version(self) -> str:
        """Build the project's image reference tagged with the project version.

        The version is a shell substitution expression resolved when the
        workflow runs, not the literal version at generation time.

        Returns:
            Image reference tagged with the bare project version.
        """
        return ContainerRegistry.I.image_tag(self.shell_insert_version())

    def container_image_tag_latest(self) -> str:
        """Build the project's image reference tagged `latest`."""
        return ContainerRegistry.I.image_tag("latest")

    def insert_actor(self) -> str:
        """Get the expression that resolves to the workflow actor.

        Returns:
            GitHub Actions expression for `github.actor`.
        """
        return self.insert_expression("github.actor")
