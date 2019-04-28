# coding: utf-8
import os
import unittest
from slackclient import SlackClient 

class SlackBotTest(unittest.TestCase):
    def test_post_message(self):
        bot=SlackBot()
        bot.post_message("Hello")

if __name__=="__main__":
    unittest.main()
