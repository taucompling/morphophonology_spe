from io import BytesIO
from os import getenv
import boto3
from botocore.errorfactory import ClientError


class S3:
    def __init__(self, bucket_name='spe-simulations'):
        aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
        if not aws_access_key_id or not aws_secret_access_key:
            raise EnvironmentError("Must set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")

        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(self.bucket_name)

    def upload_file(self, key, local_file_path):
        with open(local_file_path, 'rb') as f:
            return self.upload_from_byte_object(f, key)

    def upload_from_byte_object(self, byte_object, key):
        return self.bucket.put_object(Key=key, Body=byte_object)

    def upload_string(self, string, key):
        encoded_str = string.encode('utf-8')
        return self.upload_object(encoded_str, key)

    def upload_object(self, bytes, key):
        return self.get_object(key).put(Body=bytes)

    def download_string(self, key):
        return self.get_file_to_bytes(key).decode('utf-8')

    def get_file_to_bytes(self, key):
        return self.get_object(key).get()['Body'].read()

    def download_file(self, key, local_file_path):
        return self.get_object(key).download_file(local_file_path)

    def delete_file(self, key):
        return self.get_object(key).delete()

    def file_exists(self, key):
        object_ = self.get_object(key)
        try:
            object_.load()
            return True
        except ClientError:
            return False

    def get_object(self, key):
        return self.s3.Object(self.bucket_name, key)

    @staticmethod
    def join_paths(*paths):
        path = ''
        for p in paths:
            path += '{}/'.format(p.strip('/'))
        return path
