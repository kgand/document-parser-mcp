"""
System-related utility functions.
"""

import uuid
from typing import Optional


def get_available_memory() -> float:
    """
    Get available system memory in GB.

    Returns:
        Available memory in GB
    """
    try:
        import psutil

        memory = psutil.virtual_memory()
        return memory.available / (1024**3)
    except ImportError:
        # Return conservative estimate if psutil not available
        return 4.0


def is_mlx_available() -> bool:
    """
    Check if MLX is available on the system.

    Returns:
        True if MLX is available, False otherwise
    """
    try:
        import mlx

        return True
    except ImportError:
        return False


def generate_unique_id(prefix: Optional[str] = None) -> str:
    """
    Generate a unique identifier.

    Args:
        prefix: Optional prefix for the ID

    Returns:
        Unique identifier string
    """
    unique_id = str(uuid.uuid4())[:8]

    if prefix:
        return f"{prefix}_{unique_id}"

    return unique_id


def get_system_info() -> dict:
    """
    Get system information for diagnostics.

    Returns:
        Dictionary with system information
    """
    import platform
    import sys

    info = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "mlx_available": is_mlx_available(),
        "available_memory_gb": get_available_memory(),
    }

    return info
