# -*- coding: utf-8 -*-
""" Main Tk view for BioOpti """

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
from collections import namedtuple

from tkinter import (
    BooleanVar,
    filedialog,
    Menu,
    messagebox,
    Tk,
    ttk,
)

from .input_data_frame import InputDataFrame
from .plot_frame import PlotFrame
from .session_frame import SessionFrame
from .siop_frame import SiopFrame
# from ..model import Model

class TkView(object):

    """ Main Tk view.

    Attributes:
        VIEW_EVENTS (namedtuple): View events used to communicate with
            a controller.
        __controller_event_handlers (dict): Dictionary of registered
            controller event handlers.
        __root: The root Tk window.
        __input_data_notebook (ttk.Notebook): Notebook used to hold the input
            parameter frames.
        __plot_frame (PlotFrame): The plot frame.
        __plot_mode (dictionary): Maps the tab names to a plot mode.
        __live_update (BooleanVar): Determines whether the plot will update on
            every view data change, or only when the Update button is pressed.
    """

    # Define the View events
    __view_event_names = ['CLOSE_REQUEST', 'UPDATE_REQUEST', 'SAVE_REQUEST']
    __ViewEventType = namedtuple('__EventType', __view_event_names)
    VIEW_EVENTS = __ViewEventType(*__view_event_names)

    def __init__(self, options, model):
        """
        Initialise the TkView.

        Args:
            options (argparse.Namespace): the program options.
            model (bioopti.Model): The bioopti data model.
        """
        logging.getLogger(__name__).debug('Building Tk GUI')

        # initialise the event handler dictionary
        def __null_event_handler():
            """ Default event handler """
            return True

        self.__controller_event_handlers = {event: __null_event_handler
                                            for event in self.VIEW_EVENTS}

        self.__plot_mode = {}

        # create the root window, with resizeable first column and row
        self.__root = Tk()
        self.__root.title('BioOpti')
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        default_padding = '5'

        self.__init_main_menu()

        sizegrip = ttk.Sizegrip(self.__root)
        sizegrip.grid(row=999, column=0, sticky='SE', padx=0, pady=0)

        # ----------------------------------------
        # create a styled frame to contain everything else
        # and add it to the resizeable row 0 and column 0
        main_frame = ttk.Frame(self.__root, padding=default_padding)
        main_frame.grid(column=0, row=0, sticky='NWES')
        main_frame.columnconfigure(1, weight=1)  # the plot window is resizeable
        main_frame.rowconfigure(0, weight=1)

        # ----------------------------------------
        # Left-hand side of the window: Notebook, Update Plot button

        # create the notebook (tab control) for the Input and SIOP panels
        self.__input_data_notebook = ttk.Notebook(main_frame)
        self.__input_data_notebook.grid(
            column=0,
            # span 2 columns, so that the update and live-update controls can
            # go side by side
            columnspan=2,
            row=0,
            sticky='NW')

        # create the input frame, and add it to the notebook
        self.__input_data_frame = InputDataFrame(
            self.__input_data_notebook,
            model,
            self.__data_changed_handler,
            padding=default_padding)
        tab_name = 'Input'
        self.__input_data_notebook.add(self.__input_data_frame, text=tab_name)
        self.__plot_mode[tab_name] = PlotFrame.PLOT_MODES.PARAMETER

        # create the SIOP frame and add it to the notebook
        self.__siop_frame = SiopFrame(
            self.__input_data_notebook,
            model,
            self.__data_changed_handler,
            padding=default_padding)
        tab_name = 'SIOP'
        self.__input_data_notebook.add(self.__siop_frame, text=tab_name)
        self.__plot_mode[tab_name] = PlotFrame.PLOT_MODES.SIOP

        # create the session saving frame and add it to the notebook
        self.__session_frame = SessionFrame(
            self.__input_data_notebook,
            self.__data_changed_handler,
            options,
            padding=default_padding)
        tab_name = 'Sessions'
        self.__input_data_notebook.add(self.__session_frame, text=tab_name)

        # create the update plot button and add it below the notebook
        update_plot_button = ttk.Button(
            main_frame,
            command=self.__notify_update_request,
            text='Update')
        update_plot_button.grid(column=0, row=1, sticky='NW')
        update_plot_button.grid_configure(
            padx=(0, default_padding),
            pady=default_padding)

        # Create the live-update checkbutton
        self.__live_update = BooleanVar()
        self.__live_update.set(True)

        def live_update_changed():
            logging.getLogger(__name__).debug(
                'live update changed: %s', self.__live_update.get())

            # If the live-update has just been turned on, then force an immediate
            # update by faking a data change event.
            if self.__live_update.get():
                self.__data_changed_handler()

        check = ttk.Checkbutton(
            main_frame,
            text='Live Updates',
            command=live_update_changed,
            variable=self.__live_update,
            onvalue=True,
            offvalue=False)
        check.grid(column=1, row=1, sticky='NW')
        check.grid_configure(padx=(0, default_padding), pady=default_padding)

        # create the save results button
        save_button = ttk.Button(
            main_frame,
            command=self.__notify_save_request,
            text='Save')
        save_button.grid(column=0, row=2, sticky='NW')
        save_button.grid_configure(
            padx=(0, default_padding),
            pady=default_padding)

        # ----------------------------------------
        # Right-hand side of the window: the plot control
        self.__plot_frame = PlotFrame(
            main_frame,
            model,
            plot_options=PlotFrame.PlotOptions(
                width=options.plot_width,
                height=options.plot_height,
                legend_width_percentage=options.plot_legend_width,
                legend_font_size=options.plot_legend_font_size,
                _style=options.plot_style,
                dpi=options.plot_dpi),
            borderwidth=1,
            relief='groove',
            padding=default_padding)
        self.__plot_frame.grid(
            row=0,
            rowspan=99,  # Span all possible rows on the left-hand side
            column=3,
            sticky='NSEW')

        # add a bit of space around the major window elements
        self.__input_data_notebook.grid_configure(padx=(0, 3), pady=2)
        self.__plot_frame.grid_configure(padx=(3, 0), pady=2)

        # update the root window so it can calculate the optimal window size
        self.__root.update()
        # now set the minsize to be the optimal size
        self.__root.minsize(
            self.__root.winfo_width(),
            self.__root.winfo_height())

        self.__install_tk_event_handlers()
        self.__init_keyboard_bindings()

        # due to the order of widget creation, there is no tab changed event
        # sent for the initial selected tab. Now that all the controls are
        # created, we can let the plot frame know which tab is selected.
        self.__notify_tab_changed(
            self.__input_data_notebook.tab(
                self.__input_data_notebook.select(),
                'text'))

    def __notify_tab_changed(self, tab_name):
        """
        Notifies observers that the selected tab has changed.

        Args:
            tab_name (str): Name of the selected tab.
        """

        logging.getLogger(__name__).debug(
            'Notebook Tab Changed. Current tab: %s',
            tab_name)

        # at present, only the plot frame needs to know about tab changes
        try:
            self.__plot_frame.set_plot_mode(self.__plot_mode[tab_name])
        except KeyError:
            pass  # Ignore the missing key for tabs the plot doesn't care about

    def __init_keyboard_bindings(self):
        """
        Initialises the keyboard event bindings.
        """

        self.__root.bind(
            '<Control-x>',
            self.__close_request_handler)

    # disable unused argument warnings. I don't use the variable args,
    # but I need them defined so this same handler functions work in
    # different contexts. In some uses, Tkinter passes no arguments,
    # but in others it passes an event argument.
    # pylint: disable=unused-argument
    def __close_request_handler(self, *args, **kwargs):
        """ Close request handler.

        Proxies the Tk exit events to View events seen by the controller, with
        the controller having a right of veto.
        """

        handler = self.__controller_event_handlers[
            self.VIEW_EVENTS.CLOSE_REQUEST]

        if handler():
            self.__root.quit()
            self.__root.destroy()

    def __notify_update_request(self, *args, **kwargs):
        """ Triggers an update request.

        Sends an update request to the controller.
        """

        handler = self.__controller_event_handlers[
            self.VIEW_EVENTS.UPDATE_REQUEST]
        handler()

    def __notify_save_request(self, *args, **kwargs):
        """ Triggers a save request.

        Sends a save request to the controller.
        """

        handler = self.__controller_event_handlers[
            self.VIEW_EVENTS.SAVE_REQUEST]
        handler()

    def __install_tk_event_handlers(self):
        """ Binds to Tk events, so we can trigger our own view events. """

        self.__root.wm_protocol(
            'WM_DELETE_WINDOW',
            self.__close_request_handler)

        def notebook_tab_changed(_):
            """ Notebook tab changed event handler """

            tab_window_id = self.__input_data_notebook.select()
            tab_name = self.__input_data_notebook.tab(tab_window_id, 'text')
            self.__notify_tab_changed(tab_name)

        self.__input_data_notebook.bind(
            '<<NotebookTabChanged>>',
            notebook_tab_changed)

    def __init_main_menu(self):
        """ Creates the main application menu. """

        # disable the default "tear-off" menu, then create the application menu
        self.__root.option_add('*tearOff', False)

        # create the top level menu
        main_menu = Menu(self.__root)
        self.__root['menu'] = main_menu

        # file menu
        menu_file = Menu(main_menu)

        menu_file.add_command(
            label='Save Current Results',
            command=self.__notify_save_request)

        menu_file.add_command(
            label='Exit',
            command=self.__close_request_handler)

        main_menu.add_cascade(menu=menu_file, label='File')

        # help menu
        menu_help = Menu(main_menu)
        main_menu.add_cascade(menu=menu_help, label='Help')

        # TODO: special handling for platform-specific system menus

    def run(self):
        """
        Execute the Tk main loop for the view.
        """

        logging.getLogger(__name__).debug('Entering GUI event loop')
        self.__root.mainloop()

    def add_event_handler(self, event, handler):
        """
        Register an event handler for a defined view event.

        The current implementation only supports a single event handler for
        any event, so setting an event more than once will override the previous
        handler.

        In all cases, returning False from a handler will prevent further action
        from occuring, such as cancelling a window close request.

        Args:
            event (VIEW_EVENTS): The specified event.
            handler (function): The handler function.
        """

        try:
            self.__controller_event_handlers[event] = handler
        except KeyError as key_error:
            logging.getLogger(__name__).error(
                "View event '%s' is not defined",
                key_error.args[0])

    @staticmethod
    def ask_save_as_filename():
        """
        Creates a user dialog that requests a filename.

        Returns:
            The selected filename.
        """

        return filedialog.asksaveasfilename()

    @staticmethod
    def yes_no_message(message, title=None, icon='question'):
        """
        Creates a user dialog requiring a yes/no response.

        Args:
            message (str): The message.
            title (str): Dialog title.
            icon (str): String identifying a valid Tk icon. Options are:
                'question', 'info', 'error', 'warning'.

        Returns:
            True for yes, False for no.
        """

        result = messagebox.askyesno(
            message=message,
            title=title,
            icon=icon)
        logging.getLogger(__name__).debug('messagebox result: %s', result)
        return result

    def __data_changed_handler(self, description=''):
        """ Handler function called by child views when some of their data
        changes.

        Args:
            description (str): A short text description of the changed data.
        """
        try:
            if self.__live_update.get():
                self.__notify_update_request()
        except:
            pass

    def push_values_to_model(self, model):
        """ Pushes all modifiable values back into the model.

        Args:
            model (bioopti.Model): The bioopti data model.
        """

        self.__input_data_frame.push_values_to_model(model)
        self.__siop_frame.push_values_to_model(model)
        self.__session_frame.push_values_to_model(model)
        self.__plot_frame.push_values_to_model(model)

    def pull_values_from_model(self, model):
        """ Pulls all output values from the model, and triggers a plot refresh.

        Args:
            model (bioopti.Model): The bioopti data model.
        """

        self.__input_data_frame.pull_values_from_model(model)
        self.__siop_frame.pull_values_from_model(model)
        self.__session_frame.pull_values_from_model(model)
        self.__plot_frame.pull_values_from_model(model)
