# -*- coding: utf-8 -*-
"""
TK frame class that encapsulates the plot window.
"""

# Disable some pylint warnings caused by tkinter
# pylint: disable=C0413, C0103

import logging
from collections import namedtuple
from tkinter import (
    BooleanVar,
    StringVar,
    ttk,
)

import numpy as np
import matplotlib
# global matplotlib options. Must be called before
# importing anything else from matplotlib
matplotlib.use('TkAgg')

from matplotlib import style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2TkAgg,
)
from matplotlib.figure import Figure, SubplotParams

from .utilities import recursive_grid_configure
from .plottable_result_def import PlottableResultDef


# pylint: disable=too-many-ancestors
class PlotFrame(ttk.Frame):

    """
    ccc-gui plot frame. Encapsulates all the plotting functionality.

    Attributes:
        __current_plot_mode (PLOT_MODES): The current plot mode.
        __single_car_plot_items (list): The list of model outputs that can 
            be plotted in 'SINGLE_CAR' mode.
        __multi_car_plot_items (list): The list of model outputs that can be 
            plotted in 'MULTI_CAR' mode.
        __single_car_options (ttk.Frame): The single-car options frame.
        __multi_car_options (ttk.Frame): The multi-car options frame.
    """

    # Disabling the too-few-public-methods warning, as I find this small class
    # cleaner than named tuples or dictionaries for encapsulating both the
    # default values and the ability to hold user-values.
    # pylint: disable=too-few-public-methods
    class PlotOptions():
        """ matplotlib specific options for PlotFrame."""

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
    __plot_modes = ['SINGLE_CAR', 'MULTI_CAR']
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

        if plot_mode == self.PLOT_MODES.SINGLE_CAR:
            self.__single_car_options.grid()
            self.__multi_car_options.grid_remove()

        elif plot_mode == self.PLOT_MODES.MULTI_CAR:
            self.__single_car_options.grid_remove()
            self.__multi_car_options.grid()

        self.__refresh_figure()

    def __init__(
            self,
            parent,
            model,
            plot_options=None,
            **kwargs):
        """
        Create a plot frame.

        Args:
            parent (tk.frame): the parent tk window or frame.
            model (ccc-gui.Model): The data model.
            plot_options (PlotOptions): matplotlib specific options
                for the plot window.
        """
        logging.getLogger(__name__).debug('Initialising plotting')
        ttk.Frame.__init__(self, parent, **kwargs)

        if not plot_options:
            plot_options = PlotFrame.PlotOptions()

        self.__plot_options = plot_options
        self.__current_plot_mode = None

        self.__multi_car_plot_items = [
            PlottableResultDef('a', 'a', initial_value=True),
            PlottableResultDef('a Water', 'a_water'),
            PlottableResultDef('a Phyt', 'a_ph'),
            PlottableResultDef('a Phyt*', 'a_ph_star'),
            PlottableResultDef('a CDOM', 'a_cdom'),
            PlottableResultDef('a CDOM*', 'a_cdom_star'),
            PlottableResultDef('a NAP', 'a_nap'),
            PlottableResultDef('a NAP*', 'a_nap_star'),
        ]

        # create the data-driven list of Input-mode plot items
        self.__single_car_plot_items = [
            PlottableResultDef('rrs', 'rrs', initial_value=True),
            PlottableResultDef('rrsdp', 'rrsdp'),
            PlottableResultDef('R(0-)', 'r_0_minus'),
            PlottableResultDef('Rdp(0-)', 'rdp_0_minus'),
            PlottableResultDef('Kd', 'kd'),
            PlottableResultDef('Kub', 'kub'),
            PlottableResultDef('Kuc', 'kuc'),
            ]

        self.__model = model

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
        self.set_plot_mode(self.PLOT_MODES.SINGLE_CAR)

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
            dpi=self.__plot_options.dpi,
            subplotpars=SubplotParams(left=0.05, right=0.95, top=0.95, bottom=0.05))

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

        self.__single_car_options = self.__init_single_car_options_frame()
        self.__single_car_options.grid(row=row, column=column, sticky='NSEW')
        row += 1

        self.__multi_car_options = self.__init_multi_car_options_frame()
        self.__multi_car_options.grid(row=row, column=column, sticky='NSEW')

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

    def __init_single_car_options_frame(self):
        """
        Initialises the single-car mode options frame
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
            self.__single_car_plot_items,
            items_per_row=8)

        recursive_grid_configure(option_frame, padx=5, pady=5)
        return frame

    def __init_multi_car_options_frame(self):
        """Initialises the multi-car options frame """
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        # ----------------------------------------
        # frame for the plot item selection
        option_frame = ttk.LabelFrame(frame, text='Plot Items')
        option_frame.grid(row=1, column=0, sticky='NSEW')

        self.__generate_plottable_item_controls(
            option_frame,
            self.__multi_car_plot_items,
            items_per_row=8)

        recursive_grid_configure(option_frame, padx=5, pady=5)
        return frame

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
                plottable_items = self.__single_car_plot_items \
                    if self.__current_plot_mode == self.PLOT_MODES.SINGLE_CAR \
                    else self.__multi_car_plot_items

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

        # if self.__model.results:
        # TODO: enable plots
        if False:
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
            model (ccc-gui.Model): The data model.
        """
        pass

    def pull_values_from_model(self, model):
        """ Pulls all output values from the model.

        Args:
            model (ccc-gui.Model): The data model.
        """
        # We don't need to do this in the current implementation,
        # but it seems safer to assume that the model instance might change.
        self.__model = model
        self.__refresh_figure()

# pylint: enable=too-many-ancestors
