# encoding: utf-8
import MeCab
from wordnet_search import WordnetSearch

result = []

m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
m.parse('')

node = m.parseToNode("線路と鉄道は別の概念だ").next
w = WordnetSearch()

# w.set_categories(["天気", "健康", "産品", "もの", "時", "催し物"])

while node.next:
    result.append(w.get_hypos(node.surface))
    # result.append(w.get_topics(node.surface))
    node = node.next

print(result)
