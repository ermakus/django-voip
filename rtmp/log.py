import sys
import logging

class SimpleLogger:
    def __init__(self, filename):
        logging.basicConfig(filename=filename,level=logging.DEBUG)
        sys.stdout = self
        sys.stderr = self
    def write(self, string):
        msg = string.strip()
        if len(msg) > 0:
            logging.debug(string.rstrip())

