import pickle
from tests.my_test_case import MyTestCase
import boto3


class TestDynamodb(MyTestCase):
    def setUp(self):
        self.table = boto3.resource('dynamodb').Table('spe_simulations')

    def test_update(self):
        response = self.table.update_item(
            Key={'simulation_id': 'test'},
            UpdateExpression='SET island_0_best_incoming_fitness = :val1',
            ExpressionAttributeValues={
                ':val1': -1
            }
        )
        print(response)

    def test_get_item(self):
        response = self.table.get_item(Key={'simulation_id': 'test'}, ProjectionExpression='island_0_best_incoming_fitness')
        print(response['Item'])