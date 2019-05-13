# coding: utf-8

import unittest

class FileReadTest(unittest.TestCase):
    def test_read_file(self):
        reader = FileReader("./data/kf1")
