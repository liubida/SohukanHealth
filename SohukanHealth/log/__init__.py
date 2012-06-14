import logging
import os

logger = logging.getLogger()
handler = logging.FileHandler('../../sohukan.log')

logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

#logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 's3.log').replace('\\', '/'))