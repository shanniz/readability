#!/usr/bin/env python

#from flask import Flask
#app = Flask(__name__)


import nltk
import re

from grammarStructure import GrammarStructure
from utilities import utilities
from shanDavReadability import Readability
##from userModel import UserModel
#from textProcess import TextProcessor






if __name__ == "__main__":
	
	userModelPath='profiles/user1/'
	testText = ['text1.txt', 'A grand plan.txt']
	text = open('texts/'+testText[1], 'r').read().lower()
	regexAlpha = re.compile('[^a-z.!]')
	text = regexAlpha.sub(' ', text) 
	text = re.sub(' +',' ', text)
	#learnerVocab = [line.rstrip('\n').lower() for line in open('profiles/user2/vocab.txt')]
	gs = GrammarStructure(''); 
	learnerVocab, learnerGrammmar=gs.loadUserProfileFromFile(userModelPath + 'vocabulary.json', userModelPath +'grammar.json');
	sentences = gs.getSentencesFromText(text.lower())
	posList, wordList = gs.getPOS_List(sentences) 
    #print nltk.pos_tag(utils.get_sentences(text)[0])
    #utils = utilities()
	rd = Readability(text, utilities())
	utils = utilities()
	familiarWords = utils.common_elements( rd.analyzedVars['words'], learnerVocab)
	difficultWords = utils.unfamiliarWords( rd.analyzedVars['words'], learnerVocab)
	familiarGrammar, unfamiliarGrammar = utils.common_grammar( posList, learnerGrammmar)
	#print 'This user is familiar with '   + str(len(familiarGrammar))   + ' grammar structure(s).'
	#rd.familiarTextWords = familiarWords
	#rd.setFamUnfamWords(familiarWords, difficultWords)
	rd.setLearnerVocabulary(learnerVocab, familiarWords, difficultWords)
	rd.setLearnerGrammar(learnerGrammmar, familiarGrammar, unfamiliarGrammar)
	print 'Summary\n'
	###rd.printTestStats()
    
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
	print '\nDav-Shan Text Difficulty Score (familiar vocabulary): ', rd.shanDav(True)
	print '\nDav-Shan Text Difficulty Score (familiar/unfamiliar vocab): ', rd.shanDav2(True)
	print '\nDav-Shan Text Difficulty Score (familiar grammar): ', rd.shanDav3(True)
	print ('\nThe learner is unfamiliar with following words in the text\n')
	print difficultWords
	print 'This user is unfamiliar with ' + str(len(unfamiliarGrammar)) + ' grammar structure(s)'
	print 'The unfamiliar structures are:'
	print unfamiliarGrammar

	#app.run()