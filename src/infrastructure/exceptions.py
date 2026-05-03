class InfrastructureError(Exception):
    """Wrapper for a base exception"""


class InvalidEtherscanResponseStatus(InfrastructureError):
    """Raised when we've got '0' instead of '1' in the status field in response from etherscan."""


class ModelLoadingError(InfrastructureError):
    """ """
