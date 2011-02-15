import sys
import logging

class SimpleLogger:
    def __init__(self, filename):
        logging.basicConfig(filename=filename,level=logging.DEBUG)
        sys.stdout = self
        sys.stderr = self
    def write(self, string):
        logging.debug(string.strip())

