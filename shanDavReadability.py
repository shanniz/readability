#!/usr/bin/env python

import math
import nltk
import re
###import json

from grammarStructure import GrammarStructure
from utilities import utilities
##from userModel import UserModel
#from textProcess import TextProcessor


#Text Features:
#idioms, phrases, pronunciation, 

#Profile Features:
#


class Readability:
    analyzedVars = {}
    utils = {}
    
    #user profile features
    learnerVocabulary = []
    familiarTextWords = []
    unfamiliarTextWords = []
    learnerGrammar = []
    familiarTextGrammar = []
    unfamiliarTextGrammar = []

    def __init__(self, text, util):
        self.utils = util
        self.analyze_text(text)
        

    def setLearnerVocabulary(self, learnedWords, famWords, unfamWords):
    	self.learnerVocabulary = learnedWords
        self.familiarTextWords = famWords; self.unfamiliarTextWords = unfamWords
    	
    #words in the text that learner knows and doesnt know
    #def setFamUnfamWords(self, famWords, unfamWords):
	#	self.familiarTextWords = famWords; self.unfamiliarTextWords = unfamWords

    def setLearnerGrammar(self, learnedGrammar, famGrammar, unfamGrammar):
        self.learnerGrammar = learnedGrammar
        self.familiarTextGrammar = famGrammar; self.unfamiliarTextGrammar = unfamGrammar


	#grammar structures in the text that learner knows and doesnt know
    #def setFamUnfamGrammar(self, famGrammar, unfamGrammar):
    #    self.familiarTextGrammar = famGrammar
    #    self.unfamiliarTextGrammar = unfamGrammar
		

    def analyze_text(self, text):
        words = self.utils.get_words(text)
        char_count = self.utils.get_char_count(words)
        word_count = len(words)
        sentence_count = len(self.utils.get_sentences(text))
        syllable_count = self.utils.count_syllables(words)
        complexwords_count = self.utils.count_complex_words(text)
        
        avg_words_p_sentence = word_count / sentence_count

		#Text Features
        self.analyzedVars = {
            'words': words,
            'char_cnt': float(char_count),
            'word_cnt': float(word_count),
            'sentence_cnt': float(sentence_count),
            'syllable_cnt': float(syllable_count),
            'complex_word_cnt': float(complexwords_count),
            'avg_words_p_sentence': float(avg_words_p_sentence)
        }

    def ARI(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 4.71 * (
    self.analyzedVars[
        'char_cnt'] / self.analyzedVars[
            'word_cnt']) + 0.5 * (
                self.analyzedVars['word_cnt'] / self.analyzedVars['sentence_cnt']) - 21.43
        return score

    def FleschReadingEase(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 206.835 - (1.015 * (self.analyzedVars['avg_words_p_sentence'])) - (
                84.6 * (self.analyzedVars['syllable_cnt'] / self.analyzedVars['word_cnt']))
        return round(score, 4)

    def FleschKincaidGradeLevel(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 0.39 * (self.analyzedVars['avg_words_p_sentence']) + 11.8 * (
                self.analyzedVars['syllable_cnt'] / self.analyzedVars['word_cnt']) - 15.59
        return round(score, 4)

    def GunningFogIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = 0.4 * ((self.analyzedVars['avg_words_p_sentence']) + (
                100 * (self.analyzedVars['complex_word_cnt'] / self.analyzedVars['word_cnt'])))
        return round(score, 4)

    def SMOGIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (
    math.sqrt(self.analyzedVars['complex_word_cnt'] * (30 / self.analyzedVars['sentence_cnt'])) + 3)
        return score

    def ColemanLiauIndex(self):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (5.89 * (self.analyzedVars['char_cnt'] / self.analyzedVars['word_cnt'])) - (
                30 * (self.analyzedVars['sentence_cnt'] / self.analyzedVars['word_cnt'])) - 15.8
        return round(score, 4)

    def LIX(self):
        longwords = 0.0
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            for word in self.analyzedVars['words']:
                if len(word) >= 7:
                    longwords += 1.0
            score = self.analyzedVars['word_cnt'] / self.analyzedVars[
                'sentence_cnt'] + float(100 * longwords) / self.analyzedVars['word_cnt']
        return score

    def RIX(self):
        longwords = 0.0
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            for word in self.analyzedVars['words']:
                if len(word) >= 7:
                    longwords += 1.0
            score = longwords / self.analyzedVars['sentence_cnt']
        return score



    def printTestStats(self):
    	print 'text Statistics\n'
    	print 'char_cnt ', self.analyzedVars['char_cnt']
    	print 'word_cnt ', self.analyzedVars['word_cnt']
    	print 'sentence_cnt ', self.analyzedVars['sentence_cnt']
    	print 'syllable_cnt ', self.analyzedVars['syllable_cnt']
    	print 'complex_word_cnt ', self.analyzedVars['complex_word_cnt']
    	print 'avg_words_p_sentence ', self.analyzedVars['avg_words_p_sentence']


    def shanDav(self, retDifficulty):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10) + self.analyzedVars['syllable_cnt']/ self.analyzedVars['word_cnt'] 
            #math.sqrt(self.analyzedVars['complex_word_cnt'] * (30 / self.analyzedVars['avg_words_p_sentence'])) + 3) + 
            #(len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10)
        
        if retDifficulty == True:
            return 10-score

        return score


    def shanDav2(self, retDifficulty):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10) + self.analyzedVars['syllable_cnt']/ self.analyzedVars['word_cnt'] 
            #math.sqrt(self.analyzedVars['complex_word_cnt'] * (30 / self.analyzedVars['avg_words_p_sentence'])) + 3) + 
            #(len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10)
            
        if retDifficulty == True:
            return 10-score

        return score


    #familiar grammar
    def shanDav3(self, retDifficulty):
        score = 0.0
        if self.analyzedVars['word_cnt'] > 0.0:
            score = (len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10) 
            + (len(self.familiarTextGrammar) / self.analyzedVars['sentence_cnt'] * 10) 
            + self.analyzedVars['syllable_cnt']/ self.analyzedVars['word_cnt'] 
            #math.sqrt(self.analyzedVars['complex_word_cnt'] * (30 / self.analyzedVars['avg_words_p_sentence'])) + 3) + 
            #(len(self.familiarTextWords) / self.analyzedVars['word_cnt'] * 10)
            
        if retDifficulty == True:
            return 10-score

        return score


'''
if __name__ == "__main__":
	
	testText = ['text1.txt', 'A grand plan.txt']
	text = open('texts/'+testText[0], 'r').read().lower()

	regexAlpha = re.compile('[^a-z.!]')
	text = regexAlpha.sub(' ', text) 
	text = re.sub(' +',' ', text)
	#learnerVocab = [line.rstrip('\n').lower() for line in open('profiles/user2/vocab.txt')]

	gs = GrammarStructure(''); learnerVocab, learnerGrammmar=gs.loadUserProfileFromFile('profiles/user1/vocabulary.json', 'profiles/user1/grammar.json');
    #print (type(learnerVocab))
	sentences = gs.getSentencesFromText(text.lower())
	posList, wordList = gs.getPOS_List(sentences) 
	#print posList
	
	#print type(learnerVocab)
    #utils = utilities()
	#print nltk.pos_tag(utils.get_sentences(text)[0])

    #utils = utilities()
	rd = Readability(text, utilities())
	utils = utilities()

	print (len( nltk.sent_tokenize(text)) );print type(learnerVocab[0]); print type(learnerGrammmar[0]); 

	familiarWords = utils.common_elements( rd.analyzedVars['words'], learnerVocab)
	difficultWords = utils.unfamiliarWords( rd.analyzedVars['words'], learnerVocab); #familiarGrammar = utils.common_elements( posList, learnerGrammmar); unfamiliarGrammar = utils.unfamiliarWords(posList, learnerGrammmar)

	#rd.familiarTextWords = familiarWords
	rd.setFamUnfamWords(familiarWords, difficultWords)
	###rd.setFamUnfamGrammar(familiarGrammar, unfamiliarGrammar)
	
	###rd.setLearnerVocabulary(learnerVocab)

	print 'Summary\n'
	rd.printTestStats()
	
    #return rd.shanDav()
	#print '"%s"\n' % text
	#print 'ARI: ', rd.ARI()
	#print 'FleschReadingEase: ', rd.FleschReadingEase()
	#print 'FleschKincaidGradeLevel: ', rd.FleschKincaidGradeLevel()
	#print 'GunningFogIndex: ', rd.GunningFogIndex()
	#print 'SMOG Readability Index: ', rd.SMOGIndex()
	#print 'ColemanLiauIndex: ', rd.ColemanLiauIndex()
	#print 'LIX: ', rd.LIX()
	#print 'RIX: ', rd.RIX()
	#print ('RIX: ', rd.RIX())
	
	print '\nDav-Shan Text Difficulty Score: ', rd.shanDav()

	print ('\nThe learner is unfamiliar with following words in the text\n')
	print difficultWords
'''
