import json
import logging
import os
from pprint import pprint
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

json_file = '../../resources/polo_data.json'
json_file_formatted = '../../resources/polo_data_formatted.json'


if __name__ == '__main__':
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        pprint(json_data)

        with open(json_file_formatted, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, sort_keys=True, ensure_ascii=False)

        logger.info('Done.')

    except Exception as e:
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal')
