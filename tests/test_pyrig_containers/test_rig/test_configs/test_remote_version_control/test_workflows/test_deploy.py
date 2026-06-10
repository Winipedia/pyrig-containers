"""module."""

from pyrig_containers.rig.configs.remote_version_control.workflows.deploy import (
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
            "build-image",
            "push-image-version",
            "push-image-latest",
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

    def test_step_build_image(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_build_image()
        assert step["run"] == (
            "podman build --file Containerfile "
            f"--tag {DeployWorkflowConfigFile.I.image_tag_version()} "
            f"--tag {DeployWorkflowConfigFile.I.image_tag_latest()} ."
        )

    def test_step_push_image_version(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_push_image_version()
        assert step["run"] == (
            f"podman push {DeployWorkflowConfigFile.I.image_tag_version()}"
        )

    def test_step_push_image_latest(self) -> None:
        """Test method."""
        step = DeployWorkflowConfigFile.I.step_push_image_latest()
        assert step["run"] == (
            f"podman push {DeployWorkflowConfigFile.I.image_tag_latest()}"
        )

    def test_container_registry(self) -> None:
        """Test method."""
        assert DeployWorkflowConfigFile.I.container_registry() == "ghcr.io"

    def test_image_name(self) -> None:
        """Test method."""
        assert (
            DeployWorkflowConfigFile.I.image_name()
            == "ghcr.io/winipedia/pyrig-containers"
        )

    def test_image_tag_version(self) -> None:
        """Test method."""
        version = DeployWorkflowConfigFile.I.insert_version()
        assert (
            DeployWorkflowConfigFile.I.image_tag_version()
            == f"ghcr.io/winipedia/pyrig-containers:{version}"
        )

    def test_image_tag_latest(self) -> None:
        """Test method."""
        assert (
            DeployWorkflowConfigFile.I.image_tag_latest()
            == "ghcr.io/winipedia/pyrig-containers:latest"
        )

    def test_insert_actor(self) -> None:
        """Test method."""
        assert DeployWorkflowConfigFile.I.insert_actor() == "${{ github.actor }}"
