"""
Three-Component Memory System package.

This package re-exports the core implementation from the existing
top-level module (src/__init__.py) so that imports of the form

    from three_component_memory import MemorySystem

work correctly in both local usage and CI without changing the
original module layout.
"""

from importlib import import_module

# The root implementation lives in the flat module implemented by
# src/__init__.py. When src/ is on sys.path, that module is named
# "__init__", so we simply import and re-export from there.
_base = import_module("__init__")

MemorySystem = _base.MemorySystem
get_memory_system = _base.get_memory_system
quick_start = _base.quick_start

__version__ = getattr(_base, "__version__", "0.0.0")
__author__ = getattr(_base, "__author__", "")
__email__ = getattr(_base, "__email__", "")

__all__ = [
    "MemorySystem",
    "get_memory_system",
    "quick_start",
    "__version__",
    "__author__",
    "__email__",
]

