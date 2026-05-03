class DomainValidationError(Exception):
    """Base domain exception"""


class InvalidEthereumLength(DomainValidationError):
    """Raised when wallet address longer/shorter than 42 chars."""


class InvalidEthereumAddressPrefix(DomainValidationError):
    """Raised when address prefix is not correct"""


class InvalidRiskScore(DomainValidationError):
    """ """


class UnsupportedCorrelationIdFormat(DomainValidationError):
    """ """


class InvalidRiskLevel(DomainValidationError):
    """ """
