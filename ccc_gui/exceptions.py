# -*- coding: utf-8 -*-
""" The ccc-gui exception and error classes.
"""


class CccGuiException(Exception):
    """Root exception class.

    Only used as a base class for errors.
    This exception is never raised directly.
    """
    pass


class ModelValidationError(CccGuiException):
    """Model data validation failed."""
    pass
