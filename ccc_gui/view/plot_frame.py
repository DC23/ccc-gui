# -*- coding: utf-8 -*-
"""
TK frame class that encapsulates the plot window.
"""

# Disable some pylint warnings caused by tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import
# pylint: disable=unused-import

import logging
from collections import namedtuple

import matplotlib
# global matplotlib options. Must be called before
# importing anything else from matplotlib
matplotlib.use('TkAgg')

import numpy as np
from matplotlib import style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2TkAgg,
)
from matplotlib.figure import Figure
from tkinter import (
    BooleanVar,
    StringVar,
    ttk,
)

from .utilities import recursive_grid_configure
from .plottable_result_def import PlottableResultDef


# pylint: disable=too-many-ancestors
class PlotFrame(ttk.Frame):

    """
    BioOpti plot frame. Encapsulates all the plotting functionality.

    Although this is a large class, there are just 2 key attributes that
    control the model outputs that can be viewed on the plot.
    The `__input_plot_items` list (initialised in `__init__`) determines
    the `sambuca_core.ForwardModelResults` items that can be plotted in
    Input Parameter mode. Similarly, the `__siop_plot_items` list
    (also initialised in `__init__`) determines the items that can be plotted
    in SIOP mode.

    Attributes:
        __current_plot_mode (PLOT_MODES): The current plot mode.
        __input_plot_items (list): The list of model outputs that can be plotted
            in 'input' mode.
        __siop_plot_items (list): The list of model outputs that can be plotted
            in 'siop' mode.
        __sensor_response_overlay_name (str): The selected sensor response
            function.
        __sensor_response_overlay_type (str): Selects the sensor response
            overlay type.
        __input_options (ttk.Frame): The parameter plot options frame.
        __siop_options (ttk.Frame): The siop plot options frame.
    """

    # Disabling the too-few-public-methods warning, as I find this small class
    # cleaner than named tuples or dictionaries for encapsulating both the
    # default values and the ability to hold user-values.
    # pylint: disable=too-few-public-methods
    class PlotOptions(object):

        """matplotlib specific options for PlotFrame."""

        def __init__(self,
                     width=5,
                     height=4,
                     legend_width_percentage=0.3,
                     legend_font_size=11,
                     _style=None,
                     dpi=100):
            """
            Args:
                width (int): Plot width.
                height (int): Plot height.
                legend_width_percentage (float): Percentage plot width
                    used for the legend.
                legend_font_size (int): Legend font size in points.
                _style (str): matplotlib style.
                dpi (int): Dots per inch.
            """

            self.width = width
            self.height = height
            self.legend_width_percentage = np.clip(legend_width_percentage, 0, 1)
            self.legend_font_size = legend_font_size
            self.style = _style
            self.dpi = dpi
            self.size = (width, height)
    # pylint: enable=too-few-public-methods

    # Define the plot modes, as a named tuple instance where the attributes have
    # the same value as their names.
    __plot_modes = ['PARAMETER', 'SIOP']
    __PlotModeType = namedtuple('__PlotModes', __plot_modes)
    PLOT_MODES = __PlotModeType(*__plot_modes)

    def set_plot_mode(self, plot_mode):
        """
        Sets the plot mode.

        Args:
            plot_mode (PLOT_MODES): the required plot mode.
        """

        assert plot_mode in PlotFrame.PLOT_MODES
        logging.getLogger(__name__).debug('Setting plot mode to %s', plot_mode)

        self.__current_plot_mode = plot_mode

        if plot_mode == self.PLOT_MODES.PARAMETER:
            self.__input_options.grid()
            self.__siop_options.grid_remove()

        elif plot_mode == self.PLOT_MODES.SIOP:
            self.__input_options.grid_remove()
            self.__siop_options.grid()

        self.__refresh_figure()

    def __init__(
            self,
            parent,
            model,
            plot_options=None,
            **kwargs):
        """
        Create a BioOpti plot frame.

        Args:
            parent (tk.frame): the parent tk window or frame.
            model (bioopti.Model): The bioopti data model.
            plot_options (PlotOptions): matplotlib specific options
                for the plot window.
        """

        logging.getLogger(__name__).debug('Initialising plotting')

        ttk.Frame.__init__(self, parent, **kwargs)

        if not plot_options:
            plot_options = PlotFrame.PlotOptions()

        self.__plot_options = plot_options
        self.__current_plot_mode = None
        self.__sensor_response_overlay_name = None
        self.__sensor_response_overlay_type = None
        # self.__siop_plot_mode = None

        self.__siop_plot_items = [
            PlottableResultDef('a', 'a', initial_value=True),
            PlottableResultDef('a Water', 'a_water'),
            PlottableResultDef('a Phyt', 'a_ph'),
            PlottableResultDef('a Phyt*', 'a_ph_star'),
            PlottableResultDef('a CDOM', 'a_cdom'),
            PlottableResultDef('a CDOM*', 'a_cdom_star'),
            PlottableResultDef('a NAP', 'a_nap'),
            PlottableResultDef('a NAP*', 'a_nap_star'),
            PlottableResultDef('bb', 'bb', initial_value=True),
            PlottableResultDef('bb water', 'bb_water'),
            PlottableResultDef('bb ph', 'bb_ph'),
            PlottableResultDef('bb ph*', 'bb_ph_star'),
            PlottableResultDef('bb nap', 'bb_nap'),
            PlottableResultDef('bb nap*', 'bb_nap_star'),
        ]

        # create the data-driven list of Input-mode plot items
        self.__input_plot_items = [
            PlottableResultDef('rrs', 'rrs', initial_value=True),
            PlottableResultDef('rrsdp', 'rrsdp'),
            PlottableResultDef('R(0-)', 'r_0_minus'),
            PlottableResultDef('Rdp(0-)', 'rdp_0_minus'),
            PlottableResultDef('Kd', 'kd'),
            PlottableResultDef('Kub', 'kub'),
            PlottableResultDef('Kuc', 'kuc'),
            ]

        self.__model = model
        self.__sensor_filters = model.sensor_filters

        plot_row = 4
        self.grid()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(plot_row, weight=5)

        # create the plot frame
        self.__init_plot(
            row=plot_row,
            toolbar_row=0,
            column=0)

        self.__init_plot_controls(row=1)

        # default to parameter mode
        self.set_plot_mode(self.PLOT_MODES.PARAMETER)

        self.__refresh_figure()

    def __init_plot(
            self,
            row=1,
            toolbar_row=0,
            column=0):
        """
        Initialise the embedded matplotlib canvas.

        Args:
            row (int): The tk grid row for the canvas widget.
            toolbar_row (int): The tk grid row for the canvas toolbar.
            column (int): The tk grid column for the canvas widget.
        """

        try:
            if self.__plot_options.style:
                logging.getLogger(__name__).debug(
                    "Applying plot style '%s'",
                    self.__plot_options.style)
                style.use(self.__plot_options.style)
        except AttributeError:
            logging.getLogger(__name__).warning(
                'matplotlib version %s does not support styles',
                matplotlib.__version__)
        except ValueError as error:
            logging.getLogger(__name__).warning(error)

        self.__figure = Figure(
            figsize=self.__plot_options.size,
            dpi=self.__plot_options.dpi)

        # create the plot canvas
        canvas = FigureCanvasTkAgg(self.__figure, master=self)
        canvas.get_tk_widget().config(highlightthickness=0)
        canvas.get_tk_widget().grid(
            row=row,
            column=column,
            sticky='NSEW')

        # the toolbar uses pack internally, so we have to put it into
        # an empty frame for it to work with grid
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(row=toolbar_row, column=column, sticky='NSEW')
        toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
        toolbar.update()

    def __init_plot_controls(self, row=2, column=0):
        """
        Initialises the plot control widgets.

        Args:
            row (int): the first row to use.
            column (int): the first column to use.
        """

        self.__input_options = self.__init_input_options_frame()
        self.__input_options.grid(row=row, column=column, sticky='NSEW')
        row += 1

        self.__siop_options = self.__init_siop_options_frame()
        self.__siop_options.grid(row=row, column=column, sticky='NSEW')

    def __create_checkbutton(self, parent, text, value=False):
        """
        Creates a Checkbutton.

        Args:
            parent (tk.frame): the Checkbutton parent.
            text (str): the checkbutton text.
            value (bool): the initial value of the Checkbutton.

        Returns (tuple):
            A tuple containing the bound BooleanVar and the Checkbutton.
        """

        def cb_changed():
            """ Checkbutton changed handler """
            logging.getLogger(__name__).debug(
                '%s value: %s',
                text,
                var.get())
            self.__refresh_figure()

        # TODO: Get the initial values from a saved state
        var = BooleanVar()
        var.set(value)
        check = ttk.Checkbutton(
            parent,
            text=text,
            command=cb_changed,
            variable=var,
            onvalue=True,
            offvalue=False)

        return var, check

    def __generate_plottable_item_controls(
            self,
            frame,
            plot_items,
            start_row=0,
            start_col=0,
            items_per_row=5):
        """ Generates the checkboxes for a list of plottable model results.

        Args:
            frame: The Tk frame.
            plot_items (list): The list of PlottableResultDef items.
            start_row (int): The first row index.
            start_col (int): The first column index.
            items_per_row (int): The number of items to place on a row.
        """

        row = start_row
        col = start_col
        last_col = start_col + items_per_row
        for plot_item in plot_items:
            plot_item.control, check = self.__create_checkbutton(
                frame,
                plot_item.display_name,
                value=plot_item.initial_value)
            check.grid(row=row, column=col, sticky='NW')
            col += 1
            if col >= last_col:
                col = start_col
                row += 1

    def __init_input_options_frame(self):
        """
        Initialises the parameter input options frame,
        used in parameter input mode.
        """

        # frame to hold the options together
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        # ----------------------------------------
        # frame for the plot item selection
        option_frame = ttk.LabelFrame(frame, text='Plot Items')
        option_frame.grid(row=0, column=0, sticky='NSEW')

        self.__generate_plottable_item_controls(
            option_frame,
            self.__input_plot_items,
            items_per_row=8)

        recursive_grid_configure(option_frame, padx=5, pady=5)

        # ----------------------------------------
        # create the overlay controls
        # wrap the overlay in a frame so they have different column indices to
        # the checkbuttons, and set the columnspan to a large enough number that
        # it will always span all the checkbuttons.
        overlay_frame = ttk.LabelFrame(frame, text='Overlay')
        overlay_frame.grid(row=1, column=0, columnspan=99, sticky='NSEW')

        def sensor_filter_overlay_changed(_=None):
            """ Overlay radio button changed handler """
            logging.getLogger(__name__).debug(
                'Selected Overlay: %s Type: %s',
                self.__sensor_response_overlay_name.get(),
                self.__sensor_response_overlay_type.get())
            self.__refresh_figure()

        row = 1
        col = 0

        # __sensor_response_overlay_type holds the overlay selection string
        self.__sensor_response_overlay_type = StringVar()
        # set the default overlay to none
        self.__sensor_response_overlay_type.set('none')

        radio = ttk.Radiobutton(
            overlay_frame,
            text='None',
            variable=self.__sensor_response_overlay_type,
            value='none',
            command=sensor_filter_overlay_changed)
        radio.grid(row=row, column=col, sticky='NW')
        col += 1

        radio = ttk.Radiobutton(
            overlay_frame,
            text='Response Function',
            variable=self.__sensor_response_overlay_type,
            value='response',
            command=sensor_filter_overlay_changed)
        radio.grid(row=row, column=col, sticky='NW')
        col += 1

        radio = ttk.Radiobutton(
            overlay_frame,
            text='Band Average',
            variable=self.__sensor_response_overlay_type,
            value='band_avg',
            command=sensor_filter_overlay_changed)
        radio.grid(row=row, column=col, sticky='NW')
        col += 1

        # Sensor filters
        filter_names = list(self.__sensor_filters.keys())
        filter_names.sort()
        self.__sensor_response_overlay_name = StringVar()
        self.__sensor_response_overlay_name.set(filter_names[0])
        combo = ttk.Combobox(
            overlay_frame,
            textvariable=self.__sensor_response_overlay_name)
        combo['values'] = filter_names
        combo.state(['readonly'])
        combo.bind('<<ComboboxSelected>>', sensor_filter_overlay_changed)
        combo.grid(row=row, column=col, sticky='NE')

        recursive_grid_configure(overlay_frame, padx=5, pady=5)

        return frame

    def __init_siop_options_frame(self):
        """Initialises the SIOP options frame, used in SIOP mode."""

        col = 0
        row = 0

        # frame to hold the options together
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        # ----------------------------------------
        # SIOP or IOP plot mode selection
        # DC 08-Dec-2015: Commenting out this section, as the new data-driven
        # code now allows all SIOPs and IOPs to be selected at the same time.
        # mode_frame = ttk.LabelFrame(frame, text='Select Plot Mode')
        # mode_frame.grid(row=0, column=0, sticky='NSEW')

        # def siop_mode_changed(_=None):
            # """ SIOP mode radio button changed handler """
            # logging.getLogger(__name__).debug(
                # 'SIOP Plot mode: %s',
                # self.__siop_plot_mode.get())
            # self.__refresh_figure()

        # # __siop_plot_mode holds the plot mode selection
        # self.__siop_plot_mode = StringVar()
        # self.__siop_plot_mode.set('siop')

        # radio = ttk.Radiobutton(
            # mode_frame,
            # text='SIOP',
            # variable=self.__siop_plot_mode,
            # value='siop',
            # command=siop_mode_changed)
        # radio.grid(row=row, column=col, sticky='NW')
        # col += 1

        # radio = ttk.Radiobutton(
            # mode_frame,
            # text='IOP',
            # variable=self.__siop_plot_mode,
            # value='iop',
            # command=siop_mode_changed)
        # radio.grid(row=row, column=col, sticky='NW')

        # recursive_grid_configure(mode_frame, padx=5, pady=5)

        # ----------------------------------------
        # frame for the plot item selection
        option_frame = ttk.LabelFrame(frame, text='Plot Items')
        option_frame.grid(row=1, column=0, sticky='NSEW')

        self.__generate_plottable_item_controls(
            option_frame,
            self.__siop_plot_items,
            items_per_row=8)

        recursive_grid_configure(option_frame, padx=5, pady=5)

        return frame

    def __refresh_overlay(self):
        """ Refreshes the sensor filter overlay. """

        overlay_type = self.__sensor_response_overlay_type.get()
        if overlay_type == 'response':
            filter_name = self.__sensor_response_overlay_name.get()
            filter_data = self.__sensor_filters[filter_name]
            band_centre_wavelengths = filter_data[0]
            sensor_filter = filter_data[1]
            num_bands = sensor_filter.shape[0]

            axes = self.__figure.add_subplot(111)
            for band in range(num_bands):
                band_data = sensor_filter[band, :]
                axes.plot(
                    band_centre_wavelengths,
                    band_data,
                    label='Filter Band {0}'.format(band))

                self.__expand_plot(
                    axes,
                    left=np.min(band_centre_wavelengths) - 50,
                    right=np.max(band_centre_wavelengths) + 50,
                    bottom=np.min(band_data),
                    top=np.max(band_data))

        elif overlay_type == 'band_avg':
            pass

    def __expand_plot(self, axes, left, right, top, bottom):
        """ Expands the plot limits to fit the given bounds.

        Args:
            axes: The matplotlib Axes to expand.
            left (float): the required left boundary.
            right (float): the required right boundary.
            top (float): the required top boundary.
            bottom (float): the required bottom boundary.
        """
        current_x = axes.get_xlim()
        current_y = axes.get_ylim()
        axes.set_xlim(min(left, current_x[0]), max(right, current_x[1]))
        axes.set_ylim(min(bottom, current_y[0]), max(top, current_y[1]))

    def __plot_spectra(self, x, y, label=''):
        """ Add a single spectra to the plot.

        Args:
            x (array-like): The x-axis values.
            y (array-like): The y-axis values.
            label (str): The optional label.
        """
        axes = self.__figure.add_subplot(111)
        axes.plot(x, y, label=label)
        self.__expand_plot(
            axes,
            left=np.min(x) - 50,
            right=np.max(x) + 50,
            bottom=np.min(y),
            top=np.max(y))

    def __refresh_result_plots(self):
        """ Refresh the model result plots.

            This method iterates the plottable item lists, and add each selected
            item to the current plot. Due to the data-driven implementation,
            you do not need to modify this function if new model outputs are
            added to the plot.
        """

        if self.__model.results:
            for i, result_set in enumerate(self.__model.results):

                # Get a dict from the namedtuple
                model_results = result_set.results._asdict()

                # Select the plottable items list to match the current mode
                plottable_items = self.__input_plot_items \
                    if self.__current_plot_mode == self.PLOT_MODES.PARAMETER \
                    else self.__siop_plot_items

                for plot_item in plottable_items:
                    if plot_item.control.get():
                        # Format the label with the result index
                        label = plot_item.display_name \
                            if i == 0 else \
                            '{0} - {1}'.format(plot_item.display_name, i)
                        self.__plot_spectra(
                            result_set.parameters.wavelengths,
                            model_results[plot_item.result_name],
                            label=label)

    def __refresh_figure(self):
        """ Updates the plot when the data or options have changed. """

        logging.getLogger(__name__).debug('Refreshing plot')
        self.__figure.clear()
        axes = self.__figure.add_subplot(111)
        self.__refresh_overlay()

        if self.__model.results:
            self.__refresh_result_plots()

            # make room for the legend, and place it to the right
            box = axes.get_position()
            axes.set_position([
                box.x0,
                box.y0,
                box.width * (1.0 - self.__plot_options.legend_width_percentage),
                box.height])
            axes.legend(
                ncol=2,
                prop={'size':self.__plot_options.legend_font_size},
                bbox_to_anchor=(1.0, 0.5),
                loc='center left')
            self.__figure.canvas.draw_idle()

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
        # We don't need to do this in the current implementation,
        # but it seems safer to assume that the model instance might change.
        self.__model = model
        self.__refresh_figure()

# pylint: enable=too-many-ancestors