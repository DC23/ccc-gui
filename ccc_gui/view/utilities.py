# -*- coding: utf-8 -*-
"""
Utility functions for the views.

These are not in the ccc-gui.utility module as they are specific to the View.
"""

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import
# pylint: disable=too-many-ancestors

import logging
from tkinter import TclError

def recursive_grid_configure(parent, **kwargs):
    """
    Utility function for applying uniform grid_configure options to all
    children of a frame.

    Args:
        parent (tk.widget): The parent widget.
        **kwargs: any keyword args supported by grid_configure
    """

    for child in parent.winfo_children():
        child.grid_configure(**kwargs)

def recursive_set_state(parent, state):
    """
    Utility function for recursively setting state on a widget and all
    children.

    Args:
        parent: the parent tkinter widget
        state: a valid tkinter widget state string
    """

    if state == 'enabled':
        state = '!disabled'

    try:
        parent.state([state])
    except TclError:
        logging.getLogger(__name__).debug(
            'Widget %s does not support configure',
            type(parent))

    for child in parent.winfo_children():
        recursive_set_state(child, state=state)
