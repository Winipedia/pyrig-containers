"""GitHub Actions workflow for deploying.

Provides the ``DeployWorkflowConfigFile`` class, which generates the
``.github/workflows/deploy.yml`` workflow file. This workflow is the final
step in the automated CI/CD pipeline and runs after a successful release.

This plugin extends the base deploy workflow with an ``image`` job that builds
the project's Containerfile with podman and pushes the resulting container image
to the GitHub Container Registry (GHCR).
"""

from typing import Any

from pyrig.rig.configs.base.config_file import ConfigDict
from pyrig.rig.configs.remote_version_control.workflows.deploy import (
    DeployWorkflowConfigFile as BaseDeployWorkflowConfigFile,
)
from pyrig.rig.tools.package_manager import PackageManager
from pyrig.rig.tools.version_control.version_controller import VersionController

from pyrig_containers.rig.configs.container_file import ContainerfileConfigFile
from pyrig_containers.rig.tools.container_engine import ContainerEngine


class DeployWorkflowConfigFile(BaseDeployWorkflowConfigFile):
    """Deploy workflow that adds a build-and-push-image-to-GHCR job after release."""

    def jobs(self) -> ConfigDict:
        """Get the jobs for the deploy workflow.

        Combines the base jobs with the container image publish job.

        Returns:
            Dict combining the base jobs with the image job.
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
                    self.container_registry(),
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
        """Build a step that builds the container image from the Containerfile.

        Builds the project's Containerfile and tags the resulting image with
        both the versioned tag (``:v<version>``) and ``:latest``.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman build``.
        """
        return self.step(
            step_func=self.step_build_image,
            run=str(
                ContainerEngine.I.build_args(
                    self.image_tag_version(),
                    self.image_tag_latest(),
                    containerfile=ContainerfileConfigFile.I.path().as_posix(),
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

        Pushes the ``:v<version>`` tag built by :meth:`step_build_image`.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs ``podman push`` for the versioned tag.
        """
        return self.step(
            step_func=self.step_push_image_version,
            run=str(ContainerEngine.I.push_args(self.image_tag_version())),
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
            run=str(ContainerEngine.I.push_args(self.image_tag_latest())),
            step=step,
        )

    def image_tag_version(self) -> str:
        """Build the versioned image reference.

        Resolves the project version at workflow execution time via
        :meth:`insert_version` (``v$(uv version --short)``).

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>:v<version>``.
        """
        return f"{self.image_name()}:{self.insert_version()}"

    def image_tag_latest(self) -> str:
        """Build the ``:latest`` image reference.

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>:latest``.
        """
        return f"{self.image_name()}:latest"

    def image_name(self) -> str:
        """Build the fully qualified image name without a tag.

        Combines the registry host with the repository owner and project name.

        Returns:
            Image name in the form ``ghcr.io/<owner>/<project>``.
        """
        owner = VersionController.I.repo_owner()
        project = PackageManager.I.project_name()
        return f"{self.container_registry()}/{owner}/{project}"

    def container_registry(self) -> str:
        """Get the container registry host to publish to.

        Returns:
            ``"ghcr.io"`` (the GitHub Container Registry).
        """
        return "ghcr.io"

    def insert_actor(self) -> str:
        """Get the expression that resolves to the workflow actor.

        Returns:
            GitHub Actions expression for ``github.actor``.
        """
        return self.insert_var("github.actor")
