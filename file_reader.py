# coding: utf-8

import unittest

class FileReadTest(unittest.TestCase):
    def test_read_file(self):
        reader = FileReader()
        text = reader.read_file("./data/test.txt")
        self.assertEqual(text, "hoge\nfuga")

class FileReader:
    def read_file(self,path):
        text=""
        with open(path,'r') as f:
            text = f.read()
        return text
