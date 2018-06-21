import configparser
import logging
import os
import sys

config_path = '../../config/config.ini'

from pymongo import MongoClient

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(config_path)

    atlas_user = config['mongodb']['atlas_user']
    atlas_pass = config['mongodb']['atlas_pass']

    # mongodb+srv://admin:<PASSWORD>@teslabot-b6ciq.mongodb.net/test?retryWrites=true
    atlas_uri = 'mongodb+srv://' + atlas_user + ':' + atlas_pass + '@teslabot-b6ciq.mongodb.net/test?retryWrites=true'
    logger.debug('atlas_uri: ' + atlas_uri)

    db = MongoClient(atlas_uri)['test_db']

    collection = db['test_collection']

    insert_result = collection.insert_one({'text': 'Hello, world!'})
    logger.debug('insert_result.inserted_id: ' + str(insert_result.inserted_id))
