# coding: utf-8
import os
import unittest
from slackclient import SlackClient 

class SlackBotTest(unittest.TestCase):
    def test_post_message(self):
        bot=SlackBot()
        bot.post_message("Hello")
        
    def test_markov_chain(self):
        bot=SlackBot()
        text="今日は晴れです\n" \
             "今日は雨です\n" \
             "今日は雨だね\n" \
             "今日は雨です"
        message=bot.markov_chain(text)
        self.assertEqual(message, "今日は雨です")

class SlackBot:
    def __init__(self):
        self.slack_token=os.environ["SLACK_API_TOKEN"]
        self.sc=SlackClient(self.slack_token)

    def post_message(self,message):
        self.sc.api_call(
            "chat.postMessage",
            channel="sandbox",
            text=message
        )

if __name__=="__main__":
    unittest.main()
