from marshmallow.exceptions import ValidationError


class ObjectDoesNotExist(Exception):
    """Exception if not found results"""
    pass


class CommunicationError(Exception):
    """Exception for diferents problem with communications."""
    pass


__all__ = ('ValidationError', 'ObjectDoesNotExist', 'CommunicationError')
