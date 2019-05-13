# coding: utf-8
import os
from collections import defaultdict, Counter
import random
import unittest
import re

from slackclient import SlackClient
import MeCab
from file_reader import FileReader

class SlackBotTest(unittest.TestCase):
    def test_post_message(self):
        bot=SlackBot()
        # bot.post_message("Hello")

    def test_markov_chain(self):
        bot=SlackBot()
        text="今日は晴れです"
        message=bot.markov_chain(text)
        self.assertEqual(message, "今日は晴れです")

    def test_markov_chain_texts(self):
        bot = SlackBot()
        text = "今日は晴れです\n" \
               "今日は雨です\n" \
               "今日は雨だね\n" \
               "今日は雨です"
        message = bot.markov_chain(text)
        self.assertEqual(message, "今日は雨です")

    def test_serval_markov_chain(self):
        bot=SlackBot()
        reader = FileReader()
        texts=[]
        r = re.compile(r"サーバル\n(.+?\n)*\n")
        for i in range(12):
            text=reader.read_file("./data/kf{}.txt".format(i+1))
            texts.extend(r.findall(text))
        message=bot.markov_chain(''.join(texts))
        # bot.post_message(message)



class SlackBot:
    def __init__(self):
        self.slack_token=os.environ["SLACK_API_TOKEN"]
        self.sc=SlackClient(self.slack_token)

    def post_message(self,message):
        self.sc.api_call(
            "chat.postMessage",
            channel="sandbox",
            text=message,
        )

    def markov_chain(self,texts):
        N=3
        mecab = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        begin="__BEGIN__"
        end="__END__"
        model=defaultdict(Counter)
        begin_sentences=[]
        for text in texts.split('\n'):
            words = list(mecab.parse(text).split(' '))
            words.insert(0, begin)
            words.append(end)
            words.remove('\n')
            for i in range(len(words)-N+1):
                state=tuple(words[i:i+N])
                next=tuple(words[i+1:i+N+1])
                model[state][next]+=1
                # __BEGIN__が含まれるときは、最初の文を選ぶためのリストに入れる
                if i == 0:
                    if state not in begin_sentences:
                        begin_sentences.append(state)
        state = random.choice(begin_sentences)
        out = list(state)
        for i in range(20):
            # 最も可能性が高い遷移先
            state=model[state].most_common(1)[0][0]
            out.extend(state[-1])
            if state[-1]==end:
                break
        text = ''.join(out).lstrip(begin).rstrip(end)
        return text

if __name__=="__main__":
    unittest.main(exit=False)
