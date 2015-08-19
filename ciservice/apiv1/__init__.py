import logging

RESULT_TYPE = 'result_type'
RESULT_FILE = 'file'
RESULT_MEMORY = 'memory'

logging.basicConfig(format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
                    level=logging.DEBUG)
finders = {}