# -*- coding: utf-8 -*-
""" Main model class """

import logging

# import car_cost_calculator  # for the version number

# from ..exceptions import ModelValidationError


# pylint: disable=too-few-public-methods
class Model():
    """ Main data model class
    """

    def __init__(self, options):
        """
        Initialise the model.

        Args:
            options: the program options.
        """
        assert options
        # TODO: add cost model object
        self.__hack = None
        log = logging.getLogger(__name__)
        log.info('Initialising model')

    def calculate(self):
        """ Calculates the model.
        """
        logger = logging.getLogger(__name__)
        logger.debug('Model calculating...')
        self.__hack = None

# pylint: enable=too-few-public-methods
