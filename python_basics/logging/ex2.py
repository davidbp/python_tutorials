import logging

logging.basicConfig(level=logging.INFO)

logging.warning('Warning: check this!')  # will be printed because `logging.basicConfig(level=logging.INFO)`
logging.info('Information logged')  # will be printed
