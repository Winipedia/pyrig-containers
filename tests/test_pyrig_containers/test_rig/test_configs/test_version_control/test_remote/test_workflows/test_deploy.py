"""Tests for the container-image deployment workflow call."""

from pyrig_containers.rig.configs.version_control.remote.workflows.deploy import (
    DeployWorkflowConfigFile,
)


class TestDeployWorkflowConfigFile:
    """Test container-image workflow integration."""

    def test_job_container_image(self) -> None:
        """Check the workflow reference and forwarded permissions."""
        job = DeployWorkflowConfigFile.I.job_container_image()
        assert job["job_id"] == "container-image"
        assert job["uses"] == "$/.github/workflows/container-image.yml"
        assert job["permissions"] == {"contents": "read", "packages": "write"}
        assert "secrets" not in job
        assert "runs-on" not in job
        assert "environment" not in job
        assert "steps" not in job

    def test_jobs(self) -> None:
        """Check the container-image call is included alongside base jobs."""
        workflow = DeployWorkflowConfigFile.I
        assert workflow.job_container_image in workflow.jobs()
