#*******************************************************************************
# Author:      Zeeshan Ahmed Nizamani
# Created:     2017, Jan 19
# Desciption:
#              Python script to process the grammar structure from the text.
#              The program identifies POS tags in sentences from the grammar
#              POS tagging is achieved using NLTK library
#              The final goal is to compare the grammar structure of the given text with the learners profile.
#********************************************************************************/

#import pickle
import nltk
import re
from nltk import word_tokenize
import json
#from pattern.en import tag

####tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

###text = 'Shan is driving an electric car. This is a declaration about Shan. A Hiker is climbing a huge mountain.'

class GrammarStructure:
    text = {}
    """docstring for GrammarStructure"""
    def __init__(self, txt):
        #super(GrammarStructure, self).__init__()
        self.text = txt

    def getSentencesFromText(self, txt):
        #####return tokenizer.tokenize(txt, realign_boundaries=True)
        return nltk.sent_tokenize(txt)

    def get_POS_JSON(self, sentence):
        tagsList = [el[1] for el in (tuple(x) for x in word_tags)]
        wordList = [el[0] for el in (tuple(x) for x in word_tags)]
        wordTags = {}
        for i in range(len(wordList)):
            wordTags[wordList[i]] = tagsList[i]

    def getSentencePOS(self, sentence):
        words = word_tokenize(sentence)
        word_tags = nltk.pos_tag(words)
        #word_tags = st.tag(sentence.split())
        tagsList = [el[1] for el in (tuple(x) for x in word_tags)]
        return tagsList, word_tags

    def getPOS_List(self, sentences):
        sentPOS_List = []
        wordTags_List = []
        for sentence in sentences:

            tagsOnly, word_tags = self.getSentencePOS(sentence)
            #print (word_tags)
            sentPOS_List.append(tagsOnly)    
            wordTags_List.append(word_tags)

        return sentPOS_List, wordTags_List

    def getTextFromFile(self, filePath):
        text1 = open(filePath, 'r').read().lower()
        regexAlpha = re.compile('[^a-z.!]')
        text1 = regexAlpha.sub(' ', text1) 
        text1 = re.sub(' +',' ', text1)
        return text1


    def getUniqueWordDict(self, wordLists):
        wDict = {}
        for wList in wordLists:
            #print wList
            for wordPair in wList:
                wDict[str(wordPair[0])] = str(wordPair[1])
                #break

        return wDict

    #merge new learned vocabulary with the original vocabulary
    def mergeDictionaries(self, dict1, dict2):
        dictMerged = dict(dict1.items() + dict2.items())
        return dictMerged

    #to merge new grammar knowledge with the original knowledge
    def mergeGrammarList(self, list1, list2):
        mList=[]
        #return list(set(list1 + list2))
        for l in list1:
            if l not in mList:
                mList.append(l)
        
        for l in list2:
            if l not in mList:
                mList.append(l)

        return mList

    #Read the original vocabulary so as to merge with any new vocabulary knowledge to update the knowledge
    def updateVocabularyKnowledge(self, wordList, vocabularyPath):
        originalVocabulary = {}
        with open(vocabularyPath) as data_file:
            wordsData = data_file.read()
            if len(wordsData)>0:     
                originalVocabulary = json.loads(wordsData)
        newVocab = self.getUniqueWordDict( wordList)
        newVocab = self.mergeDictionaries(newVocab, originalVocabulary)       
        with open(vocabularyPath, 'wb') as outfile:
            json.dump(newVocab, outfile)

        return 0

    #Read the original grammar so as to merge with any new grammar knowledge to update the knowledge
    def updateGrammarKnowledge(self, posList, grammarPath):
        originalGrammarKnowledge={}
        with open(grammarPath) as data_file:
            grammarData = data_file.read()
            if len(grammarData)>0:    
                #originalGrammarKnowledge = json.load(grammarData)
                originalGrammarKnowledge = json.loads(grammarData)
        newGrammarKnowledge = self.mergeGrammarList(originalGrammarKnowledge, posList)

        with open(grammarPath, 'wb') as outfile:
            json.dump(newGrammarKnowledge, outfile)

        return 0

    def patternPOS_Tag(self,txt):
        tagged_result = tag(txt)

    def loadUserProfileFromFile(self, vocabPath, grammarPath):
        learnerVocab = [line.rstrip('\n').lower() for line in open(vocabPath)]
        d=json.loads(learnerVocab[0])
        learnerVocab=[k for k in d]

        learnerGrammar = [line.rstrip('\n') for line in open(grammarPath)]
        learnerGrammar=json.loads(learnerGrammar[0])
        return learnerVocab, learnerGrammar


'''
gs = GrammarStructure('')
###txt = gs.getTextFromFile('texts/text1.txt')
sentences = gs.getSentencesFromText(text.lower())
posList, wordList = gs.getPOS_List(sentences) 
gs.updateVocabularyKnowledge(wordList, 'profiles/user1/vocabulary.json')
gs.updateGrammarKnowledge(posList, 'profiles/user1/grammar.json')
'''




####nltk.batch_pos_tag([['this', 'is', 'batch', 'tag', 'test'], ['nltk', 'is', 'text', 'analysis', 'tool']])

#POS help/documentation
##nltk.help.upenn_tagset('RB')
#, or a regular expression, e.g., 
##nltk.help.upenn_brown_tagset('NN.*')


'''with open('profiles/user1/grammar.json') as data_file:    
    originalGrammarKnowledge = json.load(data_file)
newGrammarKnowledge = gs.mergeGrammarList(originalGrammarKnowledge, posList)
#print newGrammarKnowledge

with open('profiles/user1/grammar.json', 'wb') as outfile:
    json.dump(newGrammarKnowledge, outfile)
'''

'''
with open('profiles/user1/vocabulary.json') as data_file:    
    originalVocabulary = json.load(data_file)

jsonVocab = gs.getUniqueWordDict( wordList)
newVocab = gs.mergeDictionaries(jsonVocab, originalVocabulary)
with open('profiles/user1/vocabulary.json', 'wb') as outfile:
    json.dump(jsonVocab, outfile)
'''

'''with open('posSentences', 'wb') as fp:
    pickle.dump(posList, fp)

print "\n standford POS \n"

itemlist = []
with open ('posSentences', 'rb') as fp:
    itemlist = pickle.load(fp)

#print itemlist
for pos in itemlist:
    print pos
'''