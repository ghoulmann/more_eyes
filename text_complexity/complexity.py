import textstat

class Readability():
    def __init__(self, text):
        self.readability_scores(text)
        self.statistics(text)
    def readability_scores(self, text):
        self.ari = textstat.automated_readability_index(text)
        self.flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        self.coleman_liau_index = textstat.coleman_liau_index(text)
        self.dale_chall_readability_score = textstat.dale_chall_readability_score(text)
        self.flesch_reading_ease = textstat.flesch_reading_ease(text)
        self.gunning_fog = textstat.gunning_fog(text)
        self.linsear_write_formula = textstat.linsear_write_formula(text)
        self.lix = textstat.lix(text)
        self.rix = textstat.rix(text)
        self.smog_index = textstat.smog_index(text)
        self.text_standard = textstat.text_standard(text)
    def statistics(self, text):
        self.asl = textstat.avg_sentence_length(text)
        self.avg_sentence_per_word = textstat.avg_sentence_per_word(text)
        self.avg_syllables_per_word = textstat.avg_syllables_per_word(text)
        self.difficult_words = textstat.difficult_words(text)
        self.lexicon_count = textstat.lexicon_count(text)
        self.polysyllable_count = textstat.polysyllabcount(text)
        self.sentence_count = textstat.sentence_count(text)
