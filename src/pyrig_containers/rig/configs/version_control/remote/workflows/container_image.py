"""Reusable workflow that builds and pushes a container image.

Runs after a release and tags the image with both the release version and
`latest`.
"""

from collections.abc import Callable
from pathlib import Path
from types import MethodType
from typing import Any, override

from pyrig.rig.configs.base.workflow import WorkflowConfigFile

from pyrig_containers.rig.tools.containers.engine import ContainerEngine
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class ContainerImageWorkflowConfigFile(WorkflowConfigFile):
    """Build and publish a container image to GHCR."""

    @override
    def concurrency_cancel_in_progress(self) -> bool:
        """Return `False`; image publishing must not be cancelled."""
        return False

    @override
    def jobs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the image build and publish jobs."""
        return (self.job_build, self.job_publish)

    @override
    def workflow_triggers(self) -> dict[str, Any]:
        """Return a reusable-workflow trigger."""
        return self.on_workflow_call()

    @override
    def stem(self) -> str:
        """Return the workflow file stem, `container-image`."""
        return "container-image"

    def job_publish(self) -> dict[str, Any]:
        """Load and publish the built image after environment approval."""
        return self.job(
            self.job_publish,
            needs=self.job_publish_needs(),
            environment=self.stem(),
            permissions=self.job_publish_permissions(),
            steps=self.steps_publish(),
            timeout_minutes=60,
        )

    def job_publish_needs(self) -> tuple[MethodType, ...]:
        """Return the image build prerequisite."""
        return (self.job_build,)

    def job_publish_permissions(self) -> dict[str, str]:
        """Return checkout access for version extraction and registry write access."""
        return {
            **self.permission_contents(),
            **self.permission("packages", write=True),
        }

    def steps_publish(self) -> list[dict[str, Any]]:
        """Prepare the version and image, then authenticate and push both tags."""
        return [
            *self.steps_core_setup(),
            self.step_extract_version(),
            self.step_download_image(),
            self.step_load_image(),
            self.step_login_container_registry(),
            self.step_push_version(),
            self.step_push_latest(),
        ]

    def job_build(self) -> dict[str, Any]:
        """Build and upload a single image archive."""
        return self.job(
            self.job_build,
            permissions=self.job_build_permissions(),
            steps=self.steps_build(),
            timeout_minutes=60,
        )

    def step_download_image(self) -> dict[str, Any]:
        """Download the image archive into its expected directory."""
        return self.step_download_artifact(
            self.step_download_image,
            name=self.image_artifact_name(),
            path=self.image_archive_path().parent,
        )

    def step_load_image(self) -> dict[str, Any]:
        """Load the image archive and restore its local tag."""
        return self.step(
            self.step_load_image,
            run=str(
                ContainerEngine.I.load_args(
                    input_=self.image_archive_path().as_posix(),
                ),
            ),
        )

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

    def step_push_latest(self) -> dict[str, Any]:
        """Build a step that pushes the `latest` image tag to the registry.

        Returns:
            Step that runs `podman push` for the `latest` tag.
        """
        return self.step(
            self.step_push_latest,
            run=ContainerEngine.I.push_args(
                self.container_image_tag_latest(),
                tag=self.build_image_tag(),
            ).multiline(),
        )

    def step_push_version(self) -> dict[str, Any]:
        """Build a step that pushes the versioned image tag to the registry.

        Returns:
            Step that runs `podman push` for the versioned tag.
        """
        return self.step(
            self.step_push_version,
            run=ContainerEngine.I.push_args(
                self.container_image_tag_version(),
                tag=self.build_image_tag(),
            ).multiline(),
            env={
                self.version_var(): self.insert_output_version(),
            },
        )

    def container_image_tag_latest(self) -> str:
        """Build the project's image reference tagged `latest`."""
        return ContainerRegistry.I.image_tag("latest")

    def container_image_tag_version(self) -> str:
        """Build the project's image reference tagged with the project version.

        Returns:
            Image reference tagged with the bare project version.
        """
        return ContainerRegistry.I.image_tag(self.insert_version_expansion())

    def insert_actor(self) -> str:
        """Return the expression that resolves to the workflow actor.

        Returns:
            GitHub Actions expression for `github.actor`.
        """
        return self.insert_expression("github.actor")

    def job_build_permissions(self) -> dict[str, str]:
        """Return read-only repository access for checkout."""
        return self.permission_contents()

    def steps_build(self) -> list[dict[str, Any]]:
        """Check out the project, build the image, and upload its archive."""
        return [
            self.step_checkout_repository(),
            self.step_build_image(),
            self.step_save_image(),
            self.step_upload_image(),
        ]

    def step_build_image(self) -> dict[str, Any]:
        """Build a step that builds the container image.

        Uses a local tag to identify the image across the archive handoff.

        Returns:
            Step that runs `podman build`.
        """
        return self.step(
            self.step_build_image,
            run=ContainerEngine.I.build_args(
                tags=(self.build_image_tag(),),
            ).multiline(),
        )

    def step_save_image(self) -> dict[str, Any]:
        """Save the locally tagged image to a portable archive."""
        return self.step(
            self.step_save_image,
            run=ContainerEngine.I.save_args(
                image=self.build_image_tag(),
                output=self.image_archive_path().as_posix(),
            ).multiline(),
        )

    def step_upload_image(self) -> dict[str, Any]:
        """Upload the image archive for the publish job."""
        return self.step_upload_artifact(
            self.step_upload_image,
            name=self.image_artifact_name(),
            path=self.image_archive_path(),
        )

    def build_image_tag(self) -> str:
        """Return the local image tag shared by build and publish."""
        return "image-tag"

    def image_archive_path(self) -> Path:
        """Return the image archive path shared by build and publish."""
        return Path("image.tar")

    def image_artifact_name(self) -> str:
        """Return the artifact name used to transfer the image."""
        return "image"
