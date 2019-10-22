import spacy
from spacy_readability import Readability

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
        self.Doc = self.nlp(text)
        self.readability = self.readability_indexes()
    def readability_indexes(self):
        self.readability_scores = {}
        self.readability_scores['ari'] = self.Doc._.automated_readability_index
        self.readability_scores['coleman_liau_index'] = self.Doc._.coleman_liau_index
        self.readability_scores['dale_chall'] = self.Doc._.dale_chall
        self.readability_scores['flesch_kincaid_grade'] = self.Doc._.flesch_kincaid_grade_level
        self.readability_scores['flesch_kincaid_re'] = self.Doc._.flesch_kincaid_reading_ease
        self.readability_scores['forcast'] = self.Doc._.forcast
        return self.readability_scores




    