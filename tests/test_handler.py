import os
from unittest import TestCase

import boto3
from moto import mock_rds2

from value_objects.rds_constants import RDS


class Test(TestCase):
    @staticmethod
    def init_mock_rds():
        os.environ['REGIONS'] = 'sa-east-1'

        client_sa = boto3.client('rds', region_name='sa-east-1')
        client_sa.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_1')
        client_sa.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_2')
        client_sa.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_3')
        client_sa.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_4')
        client_sa.stop_db_instance(DBInstanceIdentifier='my_database_4')

        client_us = boto3.client('rds', region_name='us-east-1')
        client_us.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_1')
        client_us.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_2')
        client_us.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_3')
        client_us.create_db_instance(Engine='mysql', DBInstanceClass='db.m2.small',
                                     DBInstanceIdentifier='my_database_4')
        return client_sa, client_us

    @mock_rds2
    def test_stop_instances(self):
        client_sa, client_us = Test.init_mock_rds()

        from lambda_handler import lambda_handler

        response = lambda_handler({
            'action': 'stop'
        }, None)

        self.assertEqual(200, response.get('statusCode'))

        for i in range(1, 4):
            instance_sa = client_sa.describe_db_instances(DBInstanceIdentifier=f'my_database_{i}')
            self.assertEqual("stopped", instance_sa.get(RDS.INSTANCES)[0].get(RDS.STATUS))

            instance_us = client_us.describe_db_instances(DBInstanceIdentifier=f'my_database_{i}')
            self.assertEqual("available", instance_us.get(RDS.INSTANCES)[0].get(RDS.STATUS))

    @mock_rds2
    def test_start_instances(self):
        client_sa, client_us = Test.init_mock_rds()

        from lambda_handler import lambda_handler

        response = lambda_handler({
            'action': 'start'
        }, None)

        self.assertEqual(200, response.get('statusCode'))

        for i in range(1, 4):
            instance_sa = client_sa.describe_db_instances(DBInstanceIdentifier=f'my_database_{i}')
            self.assertEqual("available", instance_sa.get(RDS.INSTANCES)[0].get(RDS.STATUS))

            instance_us = client_us.describe_db_instances(DBInstanceIdentifier=f'my_database_{i}')
            self.assertEqual("available", instance_us.get(RDS.INSTANCES)[0].get(RDS.STATUS))
