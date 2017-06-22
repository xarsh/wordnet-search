# encoding: utf-8
from sense_loader import SenseLoader
from word_loader import WordLoader
from synlink_loader import SynlinkLoader

class WordnetSearch:
    def __init__(self, categories):
        self.categories = categories
        self.candidates = []

    def find_synlinks_recursively(self, sense):
        if sense is None:
            # print()
            return

        with SynlinkLoader() as synlink_loader, WordLoader() as word_loader, SenseLoader() as sense_loader:
            word = word_loader.load_word_with_wordid(sense.wordid).lemma
            synlink = synlink_loader.load_synlinks_with_sense_and_link(sense)
            # print(f"{word} ", end='')
            if (word in self.categories):
                self.candidates.append(word)
            if not synlink:
                # print()
                return
            sense = sense_loader.load_sense_with_synset(synlink[0].synset2)

        self.find_synlinks_recursively(sense)

    def getTopic(self, word):
        self.candidates = []
        with WordLoader() as word_loader, SenseLoader() as sense_loader:
            words = word_loader.load_words_with_lemma(word)

            if not words:
                return

            for sense in sense_loader.load_senses_with_synset(words[0]):
                self.find_synlinks_recursively(sense)

        return list(set(self.candidates)) # uniq
