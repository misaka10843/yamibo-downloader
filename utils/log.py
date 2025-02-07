import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"

logging.basicConfig(
    level="WARNING", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("rich")
