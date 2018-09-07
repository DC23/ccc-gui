# -*- coding: utf-8 -*-
""" GUI entry point.
"""

# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=wildcard-import

import logging
import logging.config
import configargparse

from .controller import Controller

__version__ = '0.1.0'


def __get_options():
    """Parses the CLI options"""

    parser = configargparse.ArgParser(default_config_files=['./ccc_gui.cfg'])

    # General options
    parser.add(
        '-c',
        '--config',
        required=False,
        is_config_file=True,
        default='ccc_gui.cfg',
        metavar='FILE',
        help='CCC GUI configuration file.')

    parser.add(
        '-lc',
        '--logging-config',
        required=False,
        default='bioopti_logging.cfg',
        metavar='FILE',
        help='Logging configuration file.')

    parser.add(
        '-nce',
        '--no-confirm-exit',
        required=False,
        default=False,
        action='store_true',
        help='Disables the exit confirmation dialog.')

    # Plot options
    parser.add(
        '-ps',
        '--plot-style',
        required=False,
        default=None,
        help='''Matplotlib style to use. Values are grayscale, fivethirtyeight,
            ggplot, bmh, dark_background, or any other styles supported by matplotlib.
            The default value of None will use the default matplotlib style.''')

    parser.add(
        '-pw',
        '--plot-width',
        required=False,
        type=int,
        default=5,
        help='Specifies the width of the embedded plot.')

    parser.add(
        '-ph',
        '--plot-height',
        required=False,
        type=int,
        default=4,
        help='Specifies the height of the embedded plot.')

    parser.add(
        '-plw',
        '--plot-legend-width',
        required=False,
        type=float,
        default=0.25,
        help='''Specifies the percentage of the plot width that will be used
        for the legend.''')

    parser.add(
        '-plfs',
        '--plot_legend_font_size',
        required=False,
        type=int,
        default=11,
        help='Specifies the plot legend font size in points')

    parser.add(
        '-pd',
        '--plot-dpi',
        required=False,
        type=int,
        default=100,
        help='Plot DPI.')

    parser.add(
        '-pm',
        '--plot-max-plots',
        required=False,
        type=int,
        default=30,
        help='The maximum number of plots that can be generated at once.')

    return parser.parse_args()


def __init_logging(logging_config_file):
    """
    Initialises logging.

    Args:
        logging_config_file (str): The logging configuration file.
    """

    logging.config.fileConfig(logging_config_file)
    logging.getLogger(__name__).debug('Logging online')


def main():
    """
    Main entry point for the bioopti application.
    """

    options = __get_options()
    __init_logging(options.logging_config)

    logging.getLogger(__name__).info('ccc-gui version %s', __version__)

    # Disabling the broad exception warning as catching
    # everything is *exactly* the intent here.
    # pylint: disable=broad-except
    try:
        controller = Controller(options)
        controller.run()
    except Exception as exception:
        logging.getLogger(__name__).error(exception, exc_info=True)
    # pylint: enable=broad-except
