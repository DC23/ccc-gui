# -*- coding: utf-8 -*-
""" Main model class """


# standard library imports
import logging

# third-party library imports
import car_cost_calculator  # for the version number

# local package imports
# from ..exceptions import ModelValidationError


# pylint: disable=too-few-public-methods
class Model(object):
    """ Main data model class
    """

    def __init__(self):
        """
        Initialise the model.
        """
        log = logging.getLogger(__name__)
        log.info('Initialising model')

    def calculate(self):
        """ Calculates the model.
        """
        logger = logging.getLogger(__name__)
        logger.debug('Model calculating...')

# pylint: enable=too-few-public-methods
