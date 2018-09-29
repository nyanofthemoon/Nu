import logging
from logging.config import fileConfig

fileConfig('./nu/configs/logging.ini')
logger = logging.getLogger()
