import os

from services.rds_service import RDSService

regions = os.getenv('REGIONS').split(',')

services = [
    RDSService(regions),
]


def lambda_handler(event, context):
    action = event.get('action', 'undefined')

    if action == 'start':
        for service in services:
            service.start_instances()
    elif action == 'stop':
        for service in services:
            service.stop_instances()
    else:
        print('Action unknown:', action)

    return {
        "statusCode": 200
    }
