"""Tests for the reusable container-image workflow."""

from pathlib import Path

from pyrig_containers.rig.configs.version_control.remote.workflows.container_image import (  # noqa: E501
    ContainerImageWorkflowConfigFile,
)


class TestContainerImageWorkflowConfigFile:
    """Test container-image building and publishing."""

    def test_build_image_tag(self) -> None:
        """Check the local image reference."""
        assert ContainerImageWorkflowConfigFile.I.build_image_tag() == ("image-tag")

    def test_concurrency_cancel_in_progress(self) -> None:
        """Check publishing is not cancelled by a subsequent call."""
        workflow = ContainerImageWorkflowConfigFile.I
        assert workflow.concurrency_cancel_in_progress() is False

    def test_container_image_tag_latest(self) -> None:
        """Test method."""
        assert (
            ContainerImageWorkflowConfigFile.I.container_image_tag_latest()
            == "ghcr.io/winipedia/pyrig-containers:latest"
        )

    def test_container_image_tag_version(self) -> None:
        """Test method."""
        assert (
            ContainerImageWorkflowConfigFile.I.container_image_tag_version()
            == 'ghcr.io/winipedia/pyrig-containers:"${VERSION}"'
        )

    def test_image_archive_path(self) -> None:
        """Check the archive path."""
        assert ContainerImageWorkflowConfigFile.I.image_archive_path() == Path(
            "image.tar",
        )

    def test_image_artifact_name(self) -> None:
        """Check the image artifact name."""
        assert ContainerImageWorkflowConfigFile.I.image_artifact_name() == "image"

    def test_insert_actor(self) -> None:
        """Test method."""
        workflow = ContainerImageWorkflowConfigFile.I
        assert workflow.insert_actor() == "${{ github.actor }}"

    def test_job_build(self) -> None:
        """Check the build is read-only and has no output plumbing."""
        workflow = ContainerImageWorkflowConfigFile.I
        job = workflow.job_build()
        timeout = 60
        assert job["job_id"] == "build"
        assert job["permissions"] == {"contents": "read"}
        assert job["timeout-minutes"] == timeout
        assert "outputs" not in job
        assert job["steps"] == workflow.steps_build()
        assert "environment" not in job
        assert "needs" not in job

    def test_job_publish(self) -> None:
        """Test method."""
        workflow = ContainerImageWorkflowConfigFile.I
        config = workflow.job_publish()
        timeout = 60
        assert config["job_id"] == "publish"
        assert config["environment"] == "container-image"
        assert config["timeout-minutes"] == timeout
        assert config["permissions"] == {
            "contents": "read",
            "packages": "write",
        }
        assert config["needs"] == ["build"]
        assert "if" not in config
        assert config["steps"] == workflow.steps_publish()

    def test_job_publish_needs(self) -> None:
        """Check publishing depends on the build."""
        workflow = ContainerImageWorkflowConfigFile.I
        assert workflow.job_publish_needs() == (workflow.job_build,)

    def test_jobs(self) -> None:
        """Test method."""
        workflow = ContainerImageWorkflowConfigFile.I
        assert workflow.jobs() == (workflow.job_build, workflow.job_publish)

    def test_permissions_job_build(self) -> None:
        """Check checkout is limited to read-only access."""
        assert ContainerImageWorkflowConfigFile.I.permissions_job_build() == {
            "contents": "read",
        }

    def test_permissions_job_publish(self) -> None:
        """Test method."""
        assert ContainerImageWorkflowConfigFile.I.permissions_job_publish() == {
            "contents": "read",
            "packages": "write",
        }

    def test_stem(self) -> None:
        """Check the workflow filename."""
        assert ContainerImageWorkflowConfigFile.I.stem() == "container-image"

    def test_step_build_image(self) -> None:
        """Test method."""
        step = ContainerImageWorkflowConfigFile.I.step_build_image()
        assert (
            step["run"]
            == r"""podman \
  build \
  --tag=image-tag \
  ."""
        )
        assert "env" not in step

    def test_step_download_image(self) -> None:
        """Check download restores the archive in the working directory."""
        step = ContainerImageWorkflowConfigFile.I.step_download_image()
        assert step["uses"].startswith("actions/download-artifact@")
        assert step["with"] == {"name": "image", "path": "."}

    def test_step_load_image(self) -> None:
        """Check the image archive is loaded."""
        assert ContainerImageWorkflowConfigFile.I.step_load_image()["run"] == (
            "podman load --input=image.tar"
        )

    def test_step_login_container_registry(self) -> None:
        """Test method."""
        step = ContainerImageWorkflowConfigFile.I.step_login_container_registry()
        assert (
            step["run"]
            == r'''podman \
  login \
  ghcr.io \
  --username="${ACTOR}" \
  --password="${TOKEN}"'''
        )

    def test_step_push_latest(self) -> None:
        """Test method."""
        workflow = ContainerImageWorkflowConfigFile.I
        step = workflow.step_push_latest()
        assert step["run"] == (
            """podman \\
  push \\
  image-tag \\
  ghcr.io/winipedia/pyrig-containers:latest"""
        )

    def test_step_push_version(self) -> None:
        """Test method."""
        step = ContainerImageWorkflowConfigFile.I.step_push_version()
        assert (
            step["run"]
            == r'''podman \
  push \
  image-tag \
  ghcr.io/winipedia/pyrig-containers:"${VERSION}"'''
        )
        assert step["env"] == {
            "VERSION": "${{ steps.extract-version.outputs.version }}",
        }

    def test_step_save_image(self) -> None:
        """Check the local image is saved without version extraction."""
        step = ContainerImageWorkflowConfigFile.I.step_save_image()
        assert (
            step["run"]
            == r"""podman \
  save \
  --output=image.tar \
  image-tag"""
        )
        assert "env" not in step

    def test_step_upload_image(self) -> None:
        """Check upload fails if the archive is missing."""
        step = ContainerImageWorkflowConfigFile.I.step_upload_image()
        assert step["uses"].startswith("actions/upload-artifact@")
        assert step["with"] == {
            "name": "image",
            "path": "image.tar",
            "if-no-files-found": "error",
        }

    def test_steps_build(self) -> None:
        """Check build and archiving precede artifact upload."""
        steps = ContainerImageWorkflowConfigFile.I.steps_build()
        assert [step["id"] for step in steps] == [
            "checkout-repository",
            "build-image",
            "save-image",
            "upload-image",
        ]

    def test_steps_publish(self) -> None:
        """Test method."""
        steps = ContainerImageWorkflowConfigFile.I.steps_publish()
        ids = [step["id"] for step in steps]
        assert ids == [
            "checkout-repository",
            "setup-package-manager",
            "extract-version",
            "download-image",
            "load-image",
            "login-container-registry",
            "push-version",
            "push-latest",
        ]

    def test_workflow_triggers(self) -> None:
        """Check the workflow accepts reusable calls without named secrets."""
        assert ContainerImageWorkflowConfigFile.I.workflow_triggers() == {
            "workflow_call": {},
        }
