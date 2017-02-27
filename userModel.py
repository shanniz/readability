"""
utility functions for breaking down a given block of text
into it's component syntactic parts.
"""

import nltk
import syllables_en

from nltk.tokenize import RegexpTokenizer

from grammarStructure import GrammarStructure

TOKENIZER = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
SPECIAL_CHARS = ['.', ',', '!', '?']


class UserModel:
    vacabModel = {}
    grammarModel = {}
    def __init__(self, vocabModelPath, graModelPath):
        #init user
        self.vacabModelPath = vocabModPath
        self.grammarModelPath = graModelPath


    def loadModel(self, list1, list2):
        return list(set(list1) & set(list2))

    def saveModel(self, list1, list2):
        return list(set(list1)-set(list2))

    def getSentences(self, text):
        return get_sentences(text)

    

#text = 'Shan is driving an electric car. This is a declaration about Shan. A Hiker is climbing a huge mountain.'

gs = GrammarStructure('')

userModelPath='profiles/user3/'

testText = ['text1.txt', 'A grand plan.txt', 'Jane with Mom.txt']
text = gs.getTextFromFile('texts/'+testText[2])
sentences = gs.getSentencesFromText(text.lower())

posList, wordList = gs.getPOS_List(sentences) 
gs.updateVocabularyKnowledge(wordList, userModelPath + 'vocabulary.json')
gs.updateGrammarKnowledge(posList, userModelPath + 'grammar.json')
