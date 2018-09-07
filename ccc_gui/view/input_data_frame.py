# -*- coding: utf-8 -*-
"""
TK frame class that encapsulates the main data entry form.
"""

# Disable some pylint warnings caused by tkinter
# pylint: disable=too-many-ancestors

import logging
from tkinter import (
    VERTICAL,
    ttk,
)

from .utilities import recursive_grid_configure


class InputDataFrame(ttk.Frame):

    """
    main parameter entry form.
    """

    def __init__(self, parent, model, data_changed, **kwargs):
        """
        Initialise the parameter data input frame.

        Args:
            parent (tkinter.ttk.Frame): the parent frame.
            model (ccc-gui.Model): The data model.
            data_changed (function): A data-change callback function.
        """

        logging.getLogger(__name__).debug('Initialising parameter input frame')
        ttk.Frame.__init__(self, parent, **kwargs)

        self.__data_changed = data_changed
        self.columnconfigure(0, weight=1)
        self.__three_mode_text_width = 12

        concentrations_frame = self.__init_concentrations(model)
        concentrations_frame.grid(row=0, column=0, sticky='NSWE')

        substrate_frame = self.__init_substrates(model)
        substrate_frame.grid(row=1, column=0, sticky='NSWE')

        other_params_frame = self.__init_other_parameters(model)
        other_params_frame.grid(row=2, column=0, sticky='NSWE')

        recursive_grid_configure(self, padx=5, pady=5)

    def __init_concentrations(self, model):
        """
        Initialises the concentrations frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        concentrations_frame = ttk.LabelFrame(self, text='Concentrations')
        concentrations_frame.columnconfigure(0, weight=1)

        row = 0
        col = 0

        self.__chlorophyl = ThreeModeRange(
            concentrations_frame,
            self.__data_changed,
            text='Chlorophyl',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['chlorophyl'])
        self.__chlorophyl.grid(row=row, column=col, sticky='NSWE')

        row += 1

        self.__cdom = ThreeModeRange(
            concentrations_frame,
            self.__data_changed,
            text='CDOM',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['cdom'])
        self.__cdom.grid(row=row, column=col, sticky='NSWE')

        row += 1

        self.__nap = ThreeModeRange(
            concentrations_frame,
            self.__data_changed,
            text='NAP',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['nap'])
        self.__nap.grid(row=row, column=col, sticky='NSWE')

        return concentrations_frame

    def __init_substrates(self, model):
        """
        Initialises the substrates frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        substrate_frame = ttk.LabelFrame(self, text='Substrates')
        substrate_frame.columnconfigure(0, weight=1)

        row = 0
        col = 0

        # Reflectance substrates
        # Using a treeview as there is not a styled list widget yet.
        tree_padx = 5
        tree_pady = 0
        self.__substrates = ttk.Treeview(substrate_frame, show='tree')
        self.__substrates.grid(row=row, column=col, sticky='NSWE')
        self.__substrates.grid_configure(padx=(tree_padx, 0), pady=tree_pady)
        self.__substrates.bind(
            '<<TreeviewSelect>>',
            self.__substrate_selection_changed)

        # add a scrollbar. Tk makes this weird...
        col += 1
        scrollbar = ttk.Scrollbar(
            substrate_frame,
            orient=VERTICAL,
            command=self.__substrates.yview)
        scrollbar.grid(row=row, column=col, sticky='NSWE')
        scrollbar.grid_configure(padx=(0, tree_padx), pady=tree_pady)
        self.__substrates.configure(yscrollcommand=scrollbar.set)

        recursive_grid_configure(substrate_frame, pady=5)

        # add the substrates
        sorted_substrates = list(model.substrates.keys())
        sorted_substrates.sort()
        for index, substrate in enumerate(sorted_substrates):
            self.__substrates.insert('', index, substrate, text=substrate)

        # select the first substrate
        self.__substrates.selection_set(sorted_substrates[0])

        row += 1
        col = 0

        # substrate fraction
        self.__substrate_fraction = ThreeModeRange(
            substrate_frame,
            self.__data_changed,
            text='Fraction',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['substrate_fraction'])
        self.__substrate_fraction.grid(
            row=row,
            column=col,
            columnspan=2,
            sticky='NSWE')
        row += 1

        # 3 mode depth
        self.__depth = ThreeModeRange(
            substrate_frame,
            self.__data_changed,
            text='Depth',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['substrate_depth'])
        self.__depth.grid(row=row, column=col, columnspan=2, sticky='NSWE')
        # self.__depth.grid_configure(pady=5)

        return substrate_frame

    def __init_other_parameters(self, model):
        """
        Initialises the concentrations frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        frame = ttk.LabelFrame(self, text='Other Parameters')
        frame.columnconfigure(0, weight=1)

        row = 0
        col = 0

        self.__solar_zenith = ThreeModeRange(
            frame,
            self.__data_changed,
            text='Solar Zenith',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['solar_zenith'])
        self.__solar_zenith.grid(row=row, column=col, sticky='NSWE')
        # TODO: solar zenith is not working in the model, so disabling control
        self.__solar_zenith.disable()

        row += 1

        self.__q_factor = ThreeModeRange(
            frame,
            self.__data_changed,
            text='Q Factor',
            text_width=self.__three_mode_text_width,
            bounded_value=model.bounded_values['q_factor'])
        self.__q_factor.grid(row=row, column=col, sticky='NSWE')

        return frame

    def __substrate_selection_changed(self, _):
        """ Substrate selection changed event handler. """

        items = self.__substrates.selection()

        # limit the number of substrates to 2
        if len(items) > 2:
            self.__substrates.selection_set(items[:2])

        logging.getLogger(__name__).debug('Substrates selected: %s', items)

        if len(items) <= 2:
            self.__data_changed('substrates')

    def push_values_to_model(self, model):
        """ Pushes all modifiable values back into the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """

        model.bounded_values['chlorophyl']['values'] = self.__chlorophyl.values
        model.bounded_values['cdom']['values'] = self.__cdom.values
        model.bounded_values['nap']['values'] = self.__nap.values
        model.bounded_values['substrate_fraction']['values'] = \
            self.__substrate_fraction.values
        model.bounded_values['substrate_depth']['values'] = self.__depth.values
        model.bounded_values['solar_zenith']['values'] = \
            self.__solar_zenith.values
        model.bounded_values['q_factor']['values'] = self.__q_factor.values

        model.selected_substrates = self.__substrates.selection()

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
