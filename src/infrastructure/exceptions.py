"""Compatibility re-exports; canonical definitions live in application.exceptions."""

from application.exceptions.exceptions import (
    InvalidEtherscanResponseStatus,
    ModelLoadingError,
)

__all__ = ["InvalidEtherscanResponseStatus", "ModelLoadingError"]
