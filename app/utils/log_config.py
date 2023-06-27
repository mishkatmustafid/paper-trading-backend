"""
Logging configuration module
"""

from uvicorn.config import LOGGING_CONFIG
from uvicorn.logging import ColourizedFormatter

log_config = LOGGING_CONFIG

# Log format
log_config["formatters"]["access"][
    "fmt"
] = "%(asctime)s.%(msecs)d | %(levelname)-8s | %(name)s:%(filename)s:%(lineno)d - %(message)s"
log_config["formatters"]["default"][
    "fmt"
] = "%(asctime)s.%(msecs)d | %(levelname)-8s | %(name)s:%(filename)s:%(lineno)d - %(message)s"

# Date format
date_fmt = "%Y-%m-%d:%H:%M:%S"
log_config["formatters"]["default"]["datefmt"] = date_fmt
log_config["formatters"]["access"]["datefmt"] = date_fmt

console_formatter = ColourizedFormatter(
    "{asctime} {levelprefix} : {message}", style="{", use_colors=True
)
