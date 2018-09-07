# -*- coding: utf-8 -*-
"""
ccc-gui controller. Coordinates the model and view.
"""

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import

import logging
import os

from ..exceptions import ModelValidationError
from ..model import Model
from ..view import TkView


# The controller only needs a couple of public methods
# pylint: disable=too-few-public-methods
class Controller:
    """
    GUI controller class.

    Provides coordination between the model and the view.
    """

    def __init__(self, options):
        """
        Initialise the controller.

        Args:
            options: the program options.
        """

        logging.getLogger(__name__).debug('Initialising controller')
        self.__model = Model(options)
        # Ever more than one view? This could become a factory method.
        self.__view = TkView(options, self.__model)
        self.__attach_view_event_handlers()
        self.__skip_exit_confirmation = options.no_confirm_exit

    def run(self):
        """ Runs the controller. """
        logging.getLogger(__name__).debug('Running controller')

        # Issue an initial update request, so the plot will have something to
        # show when the program loads.
        self.__update_request_handler()
        self.__view.run()

    def __attach_view_event_handlers(self):
        """ Attaches event handlers to the view """

        self.__view.add_event_handler(
            self.__view.VIEW_EVENTS.CLOSE_REQUEST,
            self.__close_request_handler)

        self.__view.add_event_handler(
            self.__view.VIEW_EVENTS.UPDATE_REQUEST,
            self.__update_request_handler)

        self.__view.add_event_handler(
            self.__view.VIEW_EVENTS.SAVE_REQUEST,
            self.__save_request_handler)

    def __close_request_handler(self):
        """ view.CLOSE_REQUEST handler """

        if self.__skip_exit_confirmation or self.__view.yes_no_message(
                message='Exit ccc-gui?',
                title='Confirm Exit',
                icon='question'):
            logging.getLogger(__name__).debug('Controller: closing')
            return True
        else:
            logging.getLogger(__name__).debug('Controller: close cancelled')
            return False

    def __update_request_handler(self):
        """ view.UPDATE_REQUEST handler

        Updates the model data from the view.
        """

        self.__view.push_values_to_model(self.__model)

        try:
            self.__model.calculate()
        except ModelValidationError as error:
            logging.getLogger(__name__).warning(error)
            return False

        self.__view.pull_values_from_model(self.__model)
        return True

    def __save_request_handler(self):
        """ view.SAVE_REQUEST handler

        Saves the current model parameters and results.
        """

        try:
            path = self.__view.ask_save_as_filename()
            logging.getLogger(__name__).debug(path)
            self.__model.save(
                os.path.dirname(path),
                os.path.basename(path))
        except OSError as error:
            logging.getLogger(__name__).error(error)

        return True

# pylint: enable=too-few-public-methods
