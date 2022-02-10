from typing import Callable

from services.resource_service import ResourceService
import boto3

from value_objects.rds_constants import RDS


class RDSService(ResourceService):

    def start_instances(self) -> None:
        self.__for_instances(self.__start)

    def stop_instances(self) -> None:
        self.__for_instances(self.__stop)

    def __for_instances(self, function: Callable):
        for region in self.regions:
            try:
                self.client = boto3.client(RDS.CLIENT_NAME, region_name=region)
            except Exception as e:
                print("Cannot instantiate client in region", region, e)
                continue

            pages = self.client.get_paginator(RDS.DESCRIBE_INSTANCES_COMMAND) \
                        .paginate(PaginationConfig={RDS.PAGE_SIZE: 30})

            for page in pages:
                for instance in page.get(RDS.INSTANCES):
                    identifier = instance.get(RDS.IDENTIFIER)
                    function(
                        status=instance.get(RDS.STATUS),
                        identifier=identifier
                    )

    def __start(self, status: str, identifier: str):
        if status != 'stopped':
            print(f'Instance "{identifier}" cannot be started. Current status: {status}')
            return
        self.client.start_db_instance(DBInstanceIdentifier=identifier)
        print('Instance started:', identifier)

    def __stop(self, status: str, identifier: str):
        if status != 'available':
            print(f'Instance "{identifier}" cannot be stopped. Current status: {status}')
            return
        self.client.stop_db_instance(DBInstanceIdentifier=identifier)
        print('Instance stopped:', identifier)
