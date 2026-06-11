"""module."""

from pyrig.rig.configs.remote_version_control.workflows.deploy import (
    DeployWorkflowConfigFile,
)


class TestDeployWorkflowConfigFile:
    """Test class."""

    def test_jobs(self) -> None:
        """Test method."""
        jobs = DeployWorkflowConfigFile.I.jobs()
        # base documentation job is preserved and the container image job is added
        assert "documentation" in jobs
        assert "container-image" in jobs

    def test_job_container_image(self) -> None:
        """Test method."""
        job = DeployWorkflowConfigFile.I.job_container_image()
        assert set(job) == {"container-image"}
        config = job["container-image"]
        assert config["permissions"] == {"packages": "write"}
        assert config["if"] == DeployWorkflowConfigFile.I.if_workflow_run_is_success()
        assert config["steps"] == DeployWorkflowConfigFile.I.steps_container_image()

    def test_steps_container_image(self) -> None:
        """Test method."""
        steps = DeployWorkflowConfigFile.I.steps_container_image()
        ids = [step["id"] for step in steps]
        assert ids == [
            "checkout-repository",
            "setup-package-manager",
            "install-container-engine",
            "login-container-registry",
            "build-container-image",
            "push-container-image-version",
            "push-container-image-latest",
        ]

    def test_step_install_container_engine(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_install_container_engine()
        assert step["uses"] == "redhat-actions/podman-install@main"

    def test_step_login_container_registry(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_login_container_registry()
        assert step["run"] == (
            "podman login ghcr.io "
            "--username ${{ github.actor }} "
            "--password ${{ secrets.GITHUB_TOKEN }}"
        )

    def test_step_build_container_image(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_build_container_image()
        version = DeployWorkflowConfigFile.I.container_image_tag_version()
        latest = DeployWorkflowConfigFile.I.container_image_tag_latest()
        assert step["run"] == f"podman build --tag {version} --tag {latest} ."

    def test_step_push_container_image_version(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_push_container_image_version()
        assert step["run"] == (
            f"podman push {DeployWorkflowConfigFile.I.container_image_tag_version()}"
        )

    def test_step_push_container_image_latest(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_push_container_image_latest()
        assert step["run"] == (
            f"podman push {DeployWorkflowConfigFile.I.container_image_tag_latest()}"
        )

    def test_container_image_tag_version(self) -> None:
        """Test method."""
        assert (
            DeployWorkflowConfigFile.I.container_image_tag_version()
            == "ghcr.io/winipedia/pyrig-containers:$(uv version --short)"
        )

    def test_container_image_tag_latest(self) -> None:
        """Test method."""
        assert (
            DeployWorkflowConfigFile.I.container_image_tag_latest()
            == "ghcr.io/winipedia/pyrig-containers:latest"
        )

    def test_insert_actor(self) -> None:
        """Test method."""
        assert DeployWorkflowConfigFile.I.insert_actor() == "${{ github.actor }}"
