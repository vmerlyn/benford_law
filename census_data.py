import spacy

nlp = spacy.load("en_core_web_lg")

import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

class CensusData:

    good_data = []
    bad_data = []

    NCOL = 6

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read

    def parse(self):
        n = 0

        single_line = []
        with open(self.file_to_read) as file:
            for line in file:
                n = n + 1
                
                text = nlp(line.rstrip())

                if(n == 1):
                    continue
                    
                for ent in text.ents:
                    single_line.append(ent.text)
                
                if(len(single_line) == self.NCOL):
                    self.good_data.append(single_line)
                else:
                    self.bad_data.append(single_line)

                single_line = []
        
