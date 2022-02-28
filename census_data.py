import logging
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

class CensusData:
    def __init__(self, file_to_read):
        self.file_to_read = file_to_read

    def process(self):
        n = 0

        single_line = []
        all_lines = []
        with open(self.file_to_read) as file:
            for line in file:
                n = n + 1
                
                #text = nlp(line.rstrip())
                text="."

                if(n == 1):
                    continue
                    
                #for ent in text.ents:
                #    single_line.append(ent.text)
                all_lines.append(single_line)
                single_line = []
        
        return all_lines