"""Package manager wrapper.

Wraps PackageManager commands and information.
"""

from pyrig.rig.tools.package_manager import PackageManager as BasePackageManager


class PackageManager(BasePackageManager):
    """You can override methods from the base class to customize behavior."""

    def container_image(self) -> tuple[str, str, str]:
        """Return the container image coordinates for copying uv.

        Used when generating a ``Containerfile`` to add a
        ``COPY --from=<image> <src> <dst>`` directive that installs uv
        into the container image.

        Returns:
            Tuple of (image_name, path_in_source_image, path_in_target_image).
        """
        return "ghcr.io/astral-sh/uv:latest", "/uv", "/usr/local/bin/uv"
