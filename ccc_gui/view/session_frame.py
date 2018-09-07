# -*- coding: utf-8 -*-
""" Session saving frame """

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

import logging

from tkinter import (
    ttk,
)


# pylint: disable=too-many-ancestors
class SessionFrame(ttk.Frame):

    """
    BioOpti session frame.

    Manages the UI for saving and loading session settings.

    Attributes:

    """

    def __init__(self, parent, data_changed, options, **kwargs):
        """
        Initialise the Session frame.

        Args:
            parent (tkinter.ttk.Frame): the parent frame.
            data_changed (function): A data-change callback function.
            options: the program options.
        """

        logging.getLogger(__name__).debug('Initialising Session frame')
        assert options
        self.__data_changed = data_changed
        ttk.Frame.__init__(self, parent, **kwargs)

    def push_values_to_model(self, model):
        """ Pushes all modifiable values back into the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """
        pass

    def pull_values_from_model(self, model):
        """ Pulls all output values from the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """
        pass
