import locale
import logging
from datetime import date

from rich.logging import RichHandler

if locale.getpreferredencoding().upper() != "UTF-8":
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

l, encoding = locale.getlocale()

logging.basicConfig(
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f"logs/{date.today()}.log", mode="a", encoding=encoding),
        RichHandler(rich_tracebacks=True),
    ],
)

logger = logging.getLogger("flaccy")

logging.getLogger("main.orm_sqlite.model").setLevel(logging.WARNING)
