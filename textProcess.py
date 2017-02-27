"""
Text processing class
"""

import re

class TextProcessor:
    text = {}
    
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

    
