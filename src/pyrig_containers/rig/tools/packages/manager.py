"""Container-specific conventions for the project's package manager."""

from pyrig.rig.tools.packages.manager import PackageManager as BasePackageManager


class PackageManager(BasePackageManager):
    """You can override methods from the base class to customize behavior."""

    def container_image(self) -> tuple[str, str, str]:
        """Return the image and paths for copying uv into a container image.

        Returns:
            Tuple of `(image, path_in_source_image, path_in_target_image)`.
        """
        return "ghcr.io/astral-sh/uv:latest", "/uv", "/usr/local/bin/uv"
