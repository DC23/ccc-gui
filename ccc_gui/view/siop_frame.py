# -*- coding: utf-8 -*-
"""
TK frame class that encapsulates the BioOpti SIOP data entry form.
"""

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import
# pylint: disable=too-many-ancestors

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
    VERTICAL,
    StringVar,
    ttk,
)

from .utilities import recursive_grid_configure


class SiopFrame(ttk.Frame):

    """
    BioOpti main SIOP entry form.
    """

    def __init__(self, parent, model, data_changed, **kwargs):
        """
        Initialise the SIOP input frame.

        Args:
            parent (tkinter.ttk.Frame): the parent frame.
            model (bioopti.Model): The bioopti data model.
            data_changed (function): A data-change callback function.
        """

        logging.getLogger(__name__).debug('Initialising SIOP frame')
        ttk.Frame.__init__(self, parent, **kwargs)

        self.__data_changed = data_changed
        self.columnconfigure(0, weight=1)
        self.__three_mode_text_width = 18
        self.__phyt_astar_spectra_items = ()

        # TODO: Region/site data loading is not implemented yet
        # frame = self.__init_regions()
        # frame.grid(row=0, column=0, sticky='NSWE')
        self.__regions = []
        self.__selected_region = None
        self.__sites = []
        self.__selected_site = None

        frame = self.__init_phytoplankton(model)
        frame.grid(row=1, column=0, sticky='NSWE')

        frame = self.__init_cdom(model)
        frame.grid(row=2, column=0, sticky='NSWE')

        frame = self.__init_nap(model)
        frame.grid(row=3, column=0, sticky='NSWE')

        recursive_grid_configure(self, padx=5, pady=5)

    def __init_regions(self):
        """
        Initialises the regions and sites frame.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        frame = ttk.LabelFrame(self, text='Regions and Sites')
        frame.columnconfigure(0, weight=1)

        row = 0
        col = 0

        # region
        def region_changed(_=None):
            """ region changed handler """
            logging.getLogger(__name__).debug(
                'Selected region: %s',
                self.__selected_region.get())
            self.__data_changed('region')

        # TODO: get regions from model
        self.__regions = ['Region 1', 'Region 2']
        self.__selected_region = StringVar()
        self.__selected_region.set(self.__regions[0])
        combo = ttk.Combobox(
            frame,
            textvariable=self.__selected_region)
        combo.state(['readonly'])
        combo['values'] = self.__regions
        combo.bind('<<ComboboxSelected>>', region_changed)
        combo.grid(row=row, column=col, sticky='NSWE')

        row += 1

        # site
        def site_changed(_=None):
            """ site changed handler """
            logging.getLogger(__name__).debug(
                'Selected site: %s',
                self.__selected_site.get())
            self.__data_changed('site')

        # TODO: get sites from model
        self.__sites = ['Site 1', 'Site 2']
        self.__selected_site = StringVar()
        self.__selected_site.set(self.__sites[0])
        combo = ttk.Combobox(
            frame,
            textvariable=self.__selected_site)
        combo.state(['readonly'])
        combo['values'] = self.__sites
        combo.bind('<<ComboboxSelected>>', site_changed)
        combo.grid(row=row, column=col, sticky='NSWE')

        recursive_grid_configure(frame, padx=5, pady=5)
        return frame

    def __init_phytoplankton(self, model):
        """
        Initialises the phytoplankton frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        frame = ttk.LabelFrame(self, text='Phytoplankton')
        frame.columnconfigure(1, weight=1)

        # row = 0
        # col = 0

        # # a* spectra
        # self.__init_a_ph_star_selection()

        # row += 1
        # col = 0

        # self.__phyt_bbstar_slope = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='bb* Slope',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['phyt_bbstar_slope'])
        # self.__phyt_bbstar_slope.grid(
        #     row=row,
        #     column=col,
        #     columnspan=3,
        #     sticky='NSWE')

        # row += 1

        # self.__phyt_bbstar_ref = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='bb* at lambda0x',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['phyt_bbstar_ref'])
        # self.__phyt_bbstar_ref.grid(
        #     row=row,
        #     column=col,
        #     columnspan=2,
        #     sticky='NSWE')

        return frame

    def __init_a_ph_star_selection(self):
        pass
         # TODO: reinstate this code, including the missing arguments from the
         # calling function if aphy* selection is implemented.
        # label_text = 'a* Spectra'
        # spectra_label = ttk.Label(
            # frame,
            # text=label_text,
            # width=len(label_text) + 3,
            # anchor='e')
        # spectra_label.grid(row=row, column=col, sticky='NW')

        # col += 1

        # # Using a treeview as there is not a styled list widget yet.
        # tree_padx = 5
        # tree_pady = 0
        # astar_spectra_view = ttk.Treeview(frame, show='tree')
        # astar_spectra_view.grid(row=row, column=col, sticky='NSWE')
        # astar_spectra_view.grid_configure(padx=(tree_padx, 0), pady=tree_pady)

        # def astar_spectra_selection_changed(_):
            # """ a* spectra selection changed event handler. """

            # self.__phyt_astar_spectra_items = astar_spectra_view.selection()
            # logging.getLogger(__name__).debug(
                # 'a* spectra selected: %s',
                # self.__phyt_astar_spectra_items)

        # astar_spectra_view.bind(
            # '<<TreeviewSelect>>',
            # astar_spectra_selection_changed)

        # # add a scrollbar. Tk makes this weird...
        # col += 1
        # scrollbar = ttk.Scrollbar(
            # frame,
            # orient=VERTICAL,
            # command=astar_spectra_view.yview)
        # scrollbar.grid(row=row, column=col, sticky='NSWE')
        # scrollbar.grid_configure(padx=(0, tree_padx), pady=tree_pady)
        # astar_spectra_view.configure(yscrollcommand=scrollbar.set)

        # recursive_grid_configure(frame, pady=5)

        # add the spectra
        # TODO: get a* spectra from model
        # astar_spectra = ['S_16D', 'S_17D', 'W_13J', 'Minimum Chips']
        # for index, spectra in enumerate(astar_spectra):
            # astar_spectra_view.insert('', index, spectra, text=spectra)

    def __init_cdom(self, model):
        """
        Initialises the CDOM frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        frame = ttk.LabelFrame(self, text='CDOM')
        frame.columnconfigure(0, weight=1)

        # row = 0
        # col = 0

        # self.__cdom_astar_slope = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='a* Slope',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['cdom_astar_slope'])
        # self.__cdom_astar_slope.grid(row=row, column=col, sticky='NSWE')

        # row += 1

        # self.__cdom_astar_ref = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='a* at lambda0-cdom',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['cdom_astar_ref'])
        # self.__cdom_astar_ref.grid(row=row, column=col, sticky='NSWE')

        return frame

    def __init_nap(self, model):
        """
        Initialises the NAP frame.

        Args:
            model (bioopti.Model): The bioopti data model.

        Returns:
            tkinter.ttk.Frame: The frame.
        """

        frame = ttk.LabelFrame(self, text='NAP')
        frame.columnconfigure(0, weight=1)

        # row = 0
        # col = 0

        # self.__nap_astar_slope = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='a* Slope',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['nap_astar_slope'])
        # self.__nap_astar_slope.grid(row=row, column=col, sticky='NSWE')

        # row += 1

        # self.__nap_astar_ref = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='a* at lambda0-nap',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['nap_astar_ref'])
        # self.__nap_astar_ref.grid(row=row, column=col, sticky='NSWE')

        # row += 1

        # self.__nap_bbstar_slope = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='bb* Slope',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['nap_bbstar_slope'])
        # self.__nap_bbstar_slope.grid(row=row, column=col, sticky='NSWE')

        # row += 1

        # self.__nap_bbstar_ref = ThreeModeRange(
        #     frame,
        #     self.__data_changed,
        #     text='bb* at lambda0x',
        #     text_width=self.__three_mode_text_width,
        #     bounded_value=model.bounded_values['nap_bbstar_ref'])
        # self.__nap_bbstar_ref.grid(row=row, column=col, sticky='NSWE')

        return frame

    def push_values_to_model(self, model):
        """ Pushes all modifiable values back into the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """
        # model.bounded_values['phyt_bbstar_slope']['values'] = \
        #     self.__phyt_bbstar_slope.values
        # model.bounded_values['phyt_bbstar_ref']['values'] = \
        #     self.__phyt_bbstar_ref.values
        # model.bounded_values['cdom_astar_slope']['values'] = \
        #     self.__cdom_astar_slope.values
        # model.bounded_values['cdom_astar_ref']['values'] = \
        #     self.__cdom_astar_ref.values
        # model.bounded_values['nap_astar_slope']['values'] = \
        #     self.__nap_astar_slope.values
        # model.bounded_values['nap_astar_ref']['values'] = \
        #     self.__nap_astar_ref.values
        # model.bounded_values['nap_bbstar_slope']['values'] = \
        #     self.__nap_bbstar_slope.values
        # model.bounded_values['nap_bbstar_ref']['values'] = \
        #     self.__nap_bbstar_ref.values
        pass

    def pull_values_from_model(self, model):
        """ Pulls all output values from the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """
        pass
