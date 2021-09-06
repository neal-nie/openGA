# -*- coding: UTF-8 -*-
"""
openGA is open source genetic algorithm framework
"""
from .version import __version__
import logging

logger = logging.getLogger("openGA")

# set up log record to write into file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(filename)-15s[line:%(lineno)-5d]-%(name)-12s-%(levelname)-8s: %(message)s',
                    filename="record.log",
                    filemode="w",
                    datefmt='%m-%d %H:%M')

# set up log record to show in console
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.WARNING)
logger.addHandler(console)

# set level for log file
# logger.setLevel(logging.ERROR)


__all__ = [
    "__version__",
]
