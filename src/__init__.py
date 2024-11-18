"""
MkDocs SQL Plugin
---------------

A MkDocs plugin for executing and displaying SQL queries in your documentation.
"""

from .plugin import SQLPlugin
from .version import __version__, get_version

__all__ = ['SQLPlugin', '__version__', 'get_version']
