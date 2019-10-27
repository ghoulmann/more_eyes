import spacy
from spacy_readability import Readability
from spacy.matcher import Matcher
from string import punctuation
import syllables

#from big_phoney import BigPhoney

class NLP():
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(Readability(), last=True)
    matcher = Matcher(nlp.vocab)
    def __init__(self, text):
        
        #self.nlp.add_pipe(Readability(), last=True)
        self.doc = self.nlp(text)
        self.readability = self.readability_indexes()
        self.word_tokens = self.tokenize_words(self.doc)
        
        self.sents = list(self.doc.sents)
        self.polysyllables = self.get_polysyllables(self.word_tokens[1])
        self.nominalized_words = self.get_nominalized(self.word_tokens[1])
        self.pos = self.get_pos(self.doc)
        self.prepositional_phrases = self.get_pps(self.doc)
        self.passive_phrases = self.get_passive_phrases(self.doc)
        self.get_pronouns(self.doc)
        self.get_weak_verbs(self.doc)
        self.sentence_count = len(self.sents)
        self.statistics()
        self.word_count = len(self.word_tokens[1])
        #self.lexicon_count = len(self.lexicon)
    def readability_indexes(self):
        readability_scores = {}
        readability_scores['ari'] = self.doc._.automated_readability_index
        readability_scores['coleman_liau_index'] = self.doc._.coleman_liau_index
        readability_scores['dale_chall'] = self.doc._.dale_chall
        readability_scores['flesch_kincaid_grade'] = self.doc._.flesch_kincaid_grade_level
        readability_scores['flesch_kincaid_re'] = self.doc._.flesch_kincaid_reading_ease
        readability_scores['forcast'] = self.doc._.forcast
        readability_scores['smog'] = self.doc._.smog
        return readability_scores
    
    def tokenize_words(self, document):
        spacy_word_tokens = [t.text for t in document]
        no_punct_word_tokens = []
        for w in spacy_word_tokens:
            for p in punctuation:
                w = w.replace(p, "").replace("\n", "").replace("", '')
            no_punct_word_tokens.append(w.lower())
        no_punct_word_tokens.remove('')
        return (spacy_word_tokens, no_punct_word_tokens)
    def get_polysyllables(self, some_list):
        polysyllables = []
        for w in some_list: 
            if syllables.estimate(w) > 3: 
                polysyllables.append(w)
        return polysyllables
    # def get_polysyllables2(self, doc):
    #     phoney = BigPhoney()
    #     self.total_syllables = phoney.count_syllables(self.doc.text)
    #     self.polys = []
    #     for token in doc:
    #         if phoney.count_syllables(token.text) > 3:
    #             self.polys.append(token.text)
    #         else:
    #             pass
    def get_nominalized(self, list):
        nominalized_words = {}
        nominalized_words['-tion words'] = []
        
        for word in list:
            if word.endswith("tion"):
                nominalized_words['-tion words'].append(word)
            
            else:
                pass
        return nominalized_words
    def get_pos(self, nlp_doc):
        parts_of_speech = {}
        parts_of_speech['gerunds'] = []
        parts_of_speech['adjectives'] = []
        parts_of_speech['adverbs'] = []
        parts_of_speech['prepositions'] = []
        for token in nlp_doc:
            if token.tag_ == "VBG":
                parts_of_speech['gerunds'].append(token.text)
            elif token.pos_ == "ADJ":
                parts_of_speech['adjectives'].append(token.text)
            elif token.pos_ == "ADV":
                parts_of_speech['adverbs'].append(token.text)
            
            else:
                pass
        return parts_of_speech

    def get_pps(self, doc):
        #Function to get prepositions from a parsed document.
        pps = []
        for token in doc:
            if token.pos_ == 'ADP':
                pp = ' '.join([tok.orth_ for tok in token.subtree])
                pps.append(pp)
        return pps

    def get_passive_phrases(self, doc):
        self.passive_sents = []
        passive_phrases = []
        passive_rule = [{'DEP': 'nsubjpass'},
        {'DEP':'aux','OP':'*'},
        {'DEP':'auxpass'},
        {'TAG':'VBN'}
        ] 
        self.matcher.add('passive', None, passive_rule)
        sents = list(doc.sents)
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            string_id = doc.vocab.strings[match_id]
            span = doc[start:end]
            passive_phrases.append(span.text)
        for s in self.sents:
            for p in passive_phrases:
                if p in s.text:
                    self.passive_sents.append(s.text)
        #return passive_phrases
    def get_weak_verbs(self, doc):
        self.weak_verbs = {}
        self.weak_verbs['to be'] = []
        self.weak_verbs['auxiliary'] = []
        for token in doc:
            if token.lemma_ == "be":
                self.weak_verbs['to be'].append(token.text)
            elif token.pos_ == 'AUX':
                self.weak_verbs['auxiliary'].append(token.text)
            else:
                pass
    def get_pronouns(self, doc):
        self.personal_pronouns = {}
        self.personal_pronouns['first person pronouns'] = []
        self.personal_pronouns['second person pronouns'] = []
        self.pronouns = []
        for token in doc:
            if token.tag_ == 'PRP' or token.tag_ == "PRP$":
                if token.text.lower() in ['i', 'me', 'mine', 'my', 'myself']:
                    self.personal_pronouns['first person pronouns'].append(token.text)
                elif token.text.lower() in ['you', 'your', 'yours', 'yourself']:
                    self.personal_pronouns['second person pronouns'].append(token.text)
                
                
                else:
                    pass
            elif token.pos_ == "PRON":
                    self.pronouns.append(token.text.lower())
            else:
                pass
    def statistics(self):
        self.statistics = {}
        self.statistics['per sentence'] = {} # rate per sentence
        self.statistics['per sentence'].update({'preposition rate':len(self.prepositional_phrases)/self.sentence_count})
        self.statistics['per sentence'].update({'be rate':len(self.weak_verbs['to be'])/self.sentence_count})   
        self.statistics['per sentence'].update({'passive rate':len(self.passive_sents)/self.sentence_count})
        self.statistics['percent of sentences'] = {}
        self.statistics['percent of sentences'].update({'prepositions':self.statistics['per sentence']['preposition rate'] * 100})
        self.statistics['percent of sentences'].update({'to be':self.statistics['per sentence']['be rate'] * 100})
        self.statistics['percent of sentences'].update({'passives':self.statistics['per sentence']['passive rate'] * 100})
        self.statistics['ratios'] = {}
        self.statistics['ratios'].update({'adverbs to adjectives':len(self.pos['adverbs'])/len(self.pos['adjectives'])})
        