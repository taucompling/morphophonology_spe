from tests.my_test_case import MyTestCase
from configuration import Configuration

configurations = Configuration()
from FAdo.fa import sConcat
from FAdo.reex import *
#from yappy_parser import Yappy

class TestFado(MyTestCase):

    def setUp(self):
        pass


    def test_dfa(self):
        r2 = str2regexp("(k+s+t)(Y)*", no_table=0).toDFA()
        self.write_to_dot_to_file(r2, "r2")



