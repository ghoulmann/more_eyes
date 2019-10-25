import spacy
from spacy_readability import Readability
from string import punctuation
import syllables

'''
def process(text):
    nlp = spacy.load('en_core_web_sm') 
    nlp.add_pipe(Readability(), last=True)
    return nlp(text)
'''
class NLP():
    def __init__(self, text):
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe(Readability(), last=True)
        self.doc = self.nlp(text)
        self.readability = self.readability_indexes()
        self.word_tokens = self.tokenize_words(self.doc)
        self.polysyllables = self.get_polysyllables(self.word_tokens[1])
    def readability_indexes(self):
        self.readability_scores = {}
        self.readability_scores['ari'] = self.doc._.automated_readability_index
        self.readability_scores['coleman_liau_index'] = self.doc._.coleman_liau_index
        self.readability_scores['dale_chall'] = self.doc._.dale_chall
        self.readability_scores['flesch_kincaid_grade'] = self.doc._.flesch_kincaid_grade_level
        self.readability_scores['flesch_kincaid_re'] = self.doc._.flesch_kincaid_reading_ease
        self.readability_scores['forcast'] = self.doc._.forcast
        return self.readability_scores
    def tokenize_words(self, document):
        self.spacy_word_tokens = [t.text for t in document]
        self.no_punct_word_tokens = []
        for w in self.spacy_word_tokens:
            for p in punctuation:
                w = w.replace(p, "").replace("\n", "")
            self.no_punct_word_tokens.append(w.lower())
        return (self.spacy_word_tokens, self.no_punct_word_tokens)
    def get_polysyllables(self, some_list):
        self.polysyllables = []
        for w in some_list: 
            if syllables.estimate(w) > 3: 
                self.polysyllables.append(w)

                    
                

        return self.polysyllables




    