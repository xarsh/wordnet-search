# encoding: utf-8
import MeCab
from wordnet_search import WordnetSearch

result = []

m = MeCab.Tagger("-Ochasen")
m.parse('')

node = m.parseToNode("小説の中だけの世界").next
w = WordnetSearch(["天気", "健康", "産品", "もの", "時", "催し物"])

while node.next:
    result.append(w.getTopic(node.surface))
    node = node.next

print(result)
