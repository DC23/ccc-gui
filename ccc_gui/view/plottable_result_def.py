# -*- coding: utf-8 -*-
"""
Utility class for binding a display name, a model result, and a Tk checkbox.
"""

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# pylint: disable=too-many-ancestors
# Disabling the too-few-public-methods warning, as I find this small class
# cleaner than named tuples or dictionaries
# pylint: disable=too-few-public-methods
class PlottableResultDef(object):
    """ This class is used to define a plottable result, by binding
    a display name, a Tk checkbox, and a named model result.

    Attributes:
        display_name (str): The name as displayed in the GUI.
        result_name (str): The Sambuca model result name.
        control: The Tk checkbox control used to control display.
        initial_value (bool): The initial check-state of the Tk control.
    """

    def __init__(self,
                 display_name,
                 result_name,
                 control=None,
                 initial_value=False):
        """
        Args:
            display_name (str): The name as displayed in the GUI.
            result_name (str): The plottable model result.
            control: The Tk checkbox control used to control display.
            initial_value: The initial check-state of the Tk control.
        """
        self.display_name = display_name
        self.result_name = result_name
        self.control = control
        self.initial_value = initial_value

# pylint: enable=too-few-public-methods
