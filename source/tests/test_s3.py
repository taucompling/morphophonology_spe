import pickle
from tests.my_test_case import MyTestCase
from utils.s3 import S3


class TestS3(MyTestCase):
    def setUp(self):
        self.s3 = S3()

    def test_save_str(self):
        key = 'tests/file_from_string.txt'
        string = "wow"
        self.s3.upload_string(string, key)

        downloaded = self.s3.download_string(key)
        print(downloaded)
        assert downloaded == string
        self.s3.delete_file(key)

    def test_save_pickle(self):
        dummy_obj = {'hello': 'world', 'wow': 'wow!'}
        obj_s = pickle.dumps(dummy_obj)
        key = 'tests/file_from_pickle.obj'
        self.s3.upload_object(obj_s, key)

        retrieved_obj = pickle.loads(self.s3.get_file_to_bytes(key))
        print(retrieved_obj)
        assert retrieved_obj == dummy_obj

        self.s3.delete_file(key)

    def test_file_exists(self):
        key = 'tests/test_exists.txt'
        self.s3.upload_string('hello', key)
        assert self.s3.file_exists(key)
        self.s3.delete_file(key)
        assert not self.s3.file_exists(key)

    def test_join_paths(self):
        paths = ['/hello/', 'world', '/wow', '//wow//']
        print(self.s3.join_paths(*paths))