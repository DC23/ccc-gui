# -*- coding: utf-8 -*-
"""
TK frame class that encapsulates the main data entry form.
"""

# Disable some pylint warnings caused by tkinter
# pylint: disable=too-many-ancestors

import logging
from tkinter import (
    HORIZONTAL,
    VERTICAL,
    ttk,
    NE,
    NW,
    NSEW,
    DoubleVar,
    StringVar,
)

from .utilities import recursive_grid_configure


class SingleCarFrame(ttk.Frame):
    """
    Tk frame for a single car examination
    """

    def __init__(self, parent, model, data_changed, **kwargs):
        """
        Initialise the frame.

        Args:
            parent (tkinter.ttk.Frame): the parent frame.
            model (ccc-gui.Model): The data model.
            data_changed (function): A data-change callback function.
        """

        logging.getLogger(__name__).debug('Initialising parameter input frame')
        ttk.Frame.__init__(self, parent, **kwargs)

        self.__data_changed = data_changed
        self.columnconfigure(0, weight=1)

        controls = self.__init_controls(model)
        controls.grid(row=0, column=0, sticky='NSWE')

        recursive_grid_configure(self, padx=5, pady=5)

    def __init_controls(self, model):
        """
        Initialises the concentrations frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        control_frame = ttk.LabelFrame(self)
        control_frame.columnconfigure(0, weight=1)

        row = 0
        col = 0
        self.__purchase_price_var = DoubleVar()
        self.__purchase_price = ttk.Scale(
            control_frame,
            from_=0,
            to=100000,
            variable=self.__purchase_price_var,
            orient=HORIZONTAL,
            length=250,
            command=self.__data_changed)
        self.__purchase_price_var.set(30000)
        self.__purchase_price.grid(row=row, column=col, sticky='NSWE')
        row += 1

        return control_frame

    def push_values_to_model(self, model):
        """ Pushes all modifiable values back into the model.

        Args:
            model (ccc-gui.Model): The data model.
        """
        logging.getLogger(__name__).debug('price %s', self.__purchase_price_var.get())

        # model.bounded_values['chlorophyl']['values'] = self.__chlorophyl.values
        # model.bounded_values['cdom']['values'] = self.__cdom.values
        # model.bounded_values['nap']['values'] = self.__nap.values
        # model.bounded_values['substrate_fraction']['values'] = \
        #     self.__substrate_fraction.values
        # model.bounded_values['substrate_depth']['values'] = self.__depth.values
        # model.bounded_values['solar_zenith']['values'] = \
        #     self.__solar_zenith.values
        # model.bounded_values['q_factor']['values'] = self.__q_factor.values

        # model.selected_substrates = self.__substrates.selection()

    def pull_values_from_model(self, model):
        """ Pulls all output values from the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """

        # In this first version, there is nothing that needs to be updated.
        # I assume that there is nothing else changing the parameter values.
        # This may not be a safe assumption long-term (eg: validation might
        # change things), but it gets me closer to v1.0

        # substrate names are loaded during initialisation,
        # and are assumed to be unchanging
        pass
