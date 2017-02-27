"""
utility functions for breaking down a given block of text
into it's component syntactic parts.
"""

import nltk

from nltk.tokenize import RegexpTokenizer
import syllables_en

TOKENIZER = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
SPECIAL_CHARS = ['.', ',', '!', '?']


class utilities:
    #def __init__(self):
    #   print ('init untils')

    def common_elements(self, list1, list2):
        return list(set(list1) & set(list2))

    def unfamiliarWords(self, list1, list2):
        return list(set(list1)-set(list2))

    def common_grammar(self, textGrammar, learnedGrammar):
    	familiar=[]; unFamiliar = []
    	for txtGram in textGrammar:
    		if txtGram in learnedGrammar:
    			familiar.append(txtGram)
    		else:
    			unFamiliar.append(txtGram)
    	return familiar, unFamiliar
    	

    def getSentences(self, text):
        return get_sentences(text)

    def normalizeScore(self, score):
        max = 10
        min = 1
        normalizedScore = score if score<=10 else (score-min)/(max-min)
        return normalizedScore
    

    def get_char_count(self, words):
        characters = 0
        for word in words:
            characters += len(word.decode("utf-8"))
        return characters
        
    def get_words(self, text=''):
        words = []
        words = TOKENIZER.tokenize(text)
        filtered_words = []
        for word in words:
            if word in SPECIAL_CHARS or word == " ":
                pass
            else:
                new_word = word.replace(",","").replace(".","")
                new_word = new_word.replace("!","").replace("?","")
                filtered_words.append(new_word)
        return filtered_words

    def get_sentences(self, text=''):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(text)
        return sentences

    def count_syllables(self, words):
        syllableCount = 0
        for word in words:
            syllableCount += syllables_en.count(word)
        return syllableCount

    #This method must be enhanced. At the moment it only
    #considers the number of syllables in a word.
    #This often results in that too many complex words are detected.
    def count_complex_words(self, text=''):
        words = self.get_words(text)
        sentences = self.get_sentences(text)
        complex_words = 0
        found = False
        cur_word = []
        
        for word in words:          
            cur_word.append(word)
            if self.count_syllables(cur_word)>= 3:
                
                #Checking proper nouns. If a word starts with a capital letter
                #and is NOT at the beginning of a sentence we don't add it
                #as a complex word.
                if not(word[0].isupper()):
                    complex_words += 1
                else:
                    for sentence in sentences:
                        if str(sentence).startswith(word):
                            found = True
                            break
                    if found: 
                        complex_words += 1
                        found = False
                    
            cur_word.remove(word)
        return complex_words

