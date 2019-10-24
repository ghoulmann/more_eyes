import spacy
from spacy_readability import Readability
from string import punctuation

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
        spacy_word_tokens =  [t.text for t in document]
        no_punct_word_tokens = []
        for w in spacy_word_tokens:
            for p in punctuation:
                if p in w:
                    if w == p:
                        pass
                    elif p in w:
                        w.replace(p, "")
                        no_punct_word_tokens.append(w)
                    else:
                        pass
                else:
                    no_punct_word_tokens.append(w)
                    
                

        return (spacy_word_tokens, no_punct_word_tokens)




    