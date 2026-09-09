"""Logger shared by the app, printing coloured output to the terminal."""
import logging

from rich.logging import RichHandler

LOG_LEVEL = logging.DEBUG

console_handler = RichHandler(rich_tracebacks=True, markup=True)
console_handler.setLevel(LOG_LEVEL)

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[console_handler],
    force=True
)

logger = logging.getLogger("orm-reference-api")
