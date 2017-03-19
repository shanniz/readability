
import json


##Usage:
##obj = Struct(**dictionaryObj)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)



class helpers:
    @staticmethod
    def read_JSON(dataFile = 'readabilityConfig.json'):
        with open(dataFile) as json_data:
            data = json.load(json_data)
        return data

    @staticmethod
    def save_JSON(data, dataFile):
        with open(dataFile, 'w') as fp:
            json.dump(data, fp)
        return True