"""Version information."""

import os
from importlib.metadata import version, PackageNotFoundError

# First try to get version from environment variable (used during build)
__version__ = os.environ.get("MKDOCS_SQL_VERSION")

if not __version__:
    try:
        # Try to get version from installed package
        __version__ = version("mkdocs_sql")
    except PackageNotFoundError:
        # Fallback to default version
        __version__ = "0.3.0"

def get_version():
    """Return package version."""
    return __version__
