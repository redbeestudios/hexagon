from typing import Callable

from rich.console import Console

from hexagon.support.printer.logger import Logger
from hexagon.support.printer.themes import load_theme

import gettext

theme = load_theme()

log = Logger(Console(color_system="auto" if theme.show_colors else None), theme)

gettext.bindtextdomain("hexagon", "locales")
gettext.textdomain("hexagon")
translator: Callable[[str], str] = gettext.gettext
