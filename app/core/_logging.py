import logging
from datetime import date

from rich.logging import RichHandler

logging.basicConfig(
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f"logs/{date.today()}.log", mode="a"),
        RichHandler(rich_tracebacks=True),
    ],
)

logger = logging.getLogger("flaccy")

logging.getLogger("main.orm_sqlite.model").setLevel(logging.WARNING)
