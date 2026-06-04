class ApplicationError(Exception):
    """Wrapper for a base exception"""


class InvalidEtherscanResponseStatus(ApplicationError):
    """Raised when we've got '0' instead of '1' in the status field in response from etherscan."""


class ModelLoadingError(ApplicationError):
    """ """


class BuildFeaturesError(ApplicationError):
    """"""


class AnalysisRequestFailed(ApplicationError):
    """ """


class InvalidPublishingMethodSelected(ApplicationError):
    """Raises when selected publish instead of publish many."""
