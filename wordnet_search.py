# encoding: utf-8
from sense_loader import SenseLoader
from word_loader import WordLoader
from synlink_loader import SynlinkLoader

class WordnetSearch:
    def set_categories(self, categories):
        self.categories = categories

    def find_synlinks_recursively(self, senses, link, lang='jpn', _depth=0):
        if senses is None:
            return

        with SynlinkLoader() as synlink_loader, WordLoader() as word_loader, SenseLoader() as sense_loader:
            word = word_loader.load_word_with_wordid(senses.wordid).lemma
            synlink = synlink_loader.load_synlinks_with_sense_and_link(senses, link)
            print(f"{word} ", end='')
            if (word in self.categories):
                self.candidates.append(word)
            if not synlink:
                return
            sense = sense_loader.load_sense_with_synset(synlink[0].synset2)

        self.find_synlinks_recursively(sense, link)

    def get_topics(self, word):
        self.candidates = []
        with WordLoader() as word_loader, SenseLoader() as sense_loader:
            words = word_loader.load_words_with_lemma(word)

            if not words:
                return

            for sense in sense_loader.load_senses_with_synset(words[0]):
                self.find_synlinks_recursively(sense, 'hype')

        return list(set(self.candidates)) # uniq

    def get_hypos(self, word):
        self.hypos = []
        with SynlinkLoader() as synlink_loader, WordLoader() as word_loader, SenseLoader() as sense_loader:
            words = word_loader.load_words_with_lemma(word)

            if not words:
                return

            for sense in sense_loader.load_senses_with_synset(words[0]):
                for synlink in synlink_loader.load_synlinks_with_sense_and_link(sense, 'hypo'):
                    hypo = sense_loader.load_sense_with_synset(synlink.synset2)
                    if hypo:
                        self.hypos.append(word_loader.load_word_with_wordid(hypo.wordid).lemma)

        return self.hypos # uniq