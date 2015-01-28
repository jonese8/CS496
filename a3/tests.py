import unittest

class restTestCase(unittest.TestCase):

  def setUp(self):
    #setUp
    someVal = 1

  def tearDown(self):
    #stuff to close
    someVal = 0

  def test_dummy(self):
    m = self.app.get('/')
    n = 1 + 1
    assert n == 2