"""GitHub Actions workflow for deploying.

Provides the ``DeployWorkflowConfigFile`` class, which generates the
``.github/workflows/deploy.yml`` workflow file. This workflow is the final
step in the automated CI/CD pipeline and runs after a successful release.

This plugin extends the base deploy workflow with a ``container-image`` job that
builds the project's Containerfile with podman and pushes the resulting container
image to the GitHub Container Registry (GHCR).
"""

from typing import Any

from pyrig.rig.configs.base.config_file import ConfigDict
from pyrig.rig.configs.remote_version_control.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)

from pyrig_containers.rig.tools.containers.engine import ContainerEngine
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """Deploy workflow that adds a build-and-push-image-to-GHCR job after release."""

    def jobs(self) -> ConfigDict:
        """Get the jobs for the deploy workflow.

        Combines the base jobs with the container image publish job.

        Returns:
            Dict combining the base jobs with the container image job.
        """
        return {
            **super().jobs(),
            **self.job_container_image(),
        }

    def job_container_image(self) -> ConfigDict:
        """Build the job that builds and pushes the container image to GHCR.

        Requests ``packages: write`` permission (required to push to GHCR) at
        the job level. The job runs only when the triggering workflow run
        succeeded. Steps are provided by :meth:`steps_container_image`.

        Returns:
            Dict mapping the derived job ID to its configuration.
        """
        return self.job(
            job_func=self.job_container_image,
            permissions={"packages": "write"},
            steps=self.steps_container_image(),
            if_condition=self.if_workflow_run_is_success(),
        )

    def steps_container_image(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the publish-container-image job.

        Combines core setup (checkout and package manager) with podman
        installation, registry login, image build, and image push steps.

        Returns:
            Ordered list of step dicts: core setup, install podman, log in to
            GHCR, build the image, push the versioned tag, push the latest tag.
        """
        return [
            *self.steps_core_setup(),
            self.step_install_container_engine(),
            self.step_login_container_registry(),
            self.step_build_image(),
            self.step_push_image_version(),
            self.step_push_image_latest(),
        ]

    def step_install_container_engine(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that installs podman on the runner.

        Uses ``redhat-actions/podman-install`` so the build and push steps have
        a guaranteed podman installation regardless of the runner image.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step using ``redhat-actions/podman-install@main``.
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

        Authenticates with GHCR using the ``github.actor`` as the username and
        the automatic ``GITHUB_TOKEN`` secret as the password.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman login`` against GHCR.
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

    def step_build_image(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that builds the container image.

        Builds the ``Containerfile`` in the build context (the project root,
        discovered automatically by podman) and tags the resulting image with
        both the versioned tag (``:<version>``) and ``:latest``.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman build``.
        """
        return self.step(
            step_func=self.step_build_image,
            run=str(
                ContainerEngine.I.build_args(
                    tags=(self.image_tag_version(), self.image_tag_latest()),
                )
            ),
            step=step,
        )

    def step_push_image_version(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that pushes the versioned image tag to GHCR.

        Pushes the ``:<version>`` tag built by :meth:`step_build_image`.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman push`` for the versioned tag.
        """
        return self.step(
            step_func=self.step_push_image_version,
            run=str(ContainerEngine.I.push_args(tag=self.image_tag_version())),
            step=step,
        )

    def step_push_image_latest(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that pushes the ``:latest`` image tag to GHCR.

        Pushes the ``:latest`` tag built by :meth:`step_build_image`.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman push`` for the ``:latest`` tag.
        """
        return self.step(
            step_func=self.step_push_image_latest,
            run=str(ContainerEngine.I.push_args(tag=self.image_tag_latest())),
            step=step,
        )

    def image_tag_version(self) -> str:
        """Build the versioned image reference.

        Tags the image with the bare project version, resolved at workflow
        execution time via :meth:`insert_version` (``$(uv version --short)``).
        Container image tags use the bare version, with no leading ``v`` prefix
        (e.g. ``1.2.3``).

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>:<version>``.
        """
        return ContainerRegistry.I.image_tag(self.insert_version())

    def image_tag_latest(self) -> str:
        """Build the ``:latest`` image reference.

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>:latest``.
        """
        return ContainerRegistry.I.image_tag("latest")

    def insert_actor(self) -> str:
        """Get the expression that resolves to the workflow actor.

        Returns:
            GitHub Actions expression for ``github.actor``.
        """
        return self.insert_var("github.actor")
