"""
We use the objectstore to get the latest and greatest of the mks dump
"""

import os

# import datetime
# from dateutil import parser
from objectstore import get_connection
from objectstore import databasedumps

assert os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD')

ENV = os.getenv('ENVIRONMENT', 'ACCEPTANCE')

OBJECTSTORE = dict(
    VERSION='2.0',
    AUTHURL='https://identity.stack.cloudvps.com/v2.0',
    TENANT_NAME='BGE000081_Handelsregister',
    TENANT_ID='0efc828b88584759893253f563b35f9b',
    USER=os.getenv('OBJECTSTORE_USER', 'handelsregister'),
    PASSWORD=os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD'),
    REGION_NAME='NL',
)


handelsregister = get_connection(OBJECTSTORE)

dump = open('/tmp/backups/database.dump', 'rb')


databasedumps.run(handelsregister)
