import base64
import logging
import multiprocessing
import os
from cmath import log10

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger("dev")
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)


class CensusData:
    """Class to parse and display the distribution of an input column of numbers,
    to verify if the data confirms to the Bernoff's law.
    """
    NUMBER_OF_COLUMNS = 6
    COL_OF_INTEREST = "7_2009"

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.parse_done = False

    def parse(self, write_to_db=False):
        """Parses the input Census data file and populates a pandas dataframe.

        Returns:
            Boolean: True if parsed without errors.
        """
        n = 0
        self.good_data = []
        self.bad_data = []

        single_line = []
        header_columns = []
        with open(self.file_to_read) as file:
            for line in file:
                n = n + 1
                if n == 1:
                    header_columns = line.split("\t")
                    if(len(header_columns) != self.NUMBER_OF_COLUMNS):
                        return False
                    continue

                single_line = line.split("\t")

                if len(single_line) == self.NUMBER_OF_COLUMNS:
                    self.good_data.append(single_line)
                else:
                    self.bad_data.append(single_line)

                single_line = []

        self.dataframe = pd.DataFrame(self.good_data, columns=header_columns)

        # Persist in an in memory data store
        # Not fully implemented/tested.
        if(write_to_db):
            import sqlite3

            conn = sqlite3.connect('test_database')
            c = conn.cursor()
            table_string = ""
            for index in range(self.NUMBER_OF_COLUMNS-1):
                table_string += "\"" + header_columns[index]+"\"" + " text,"
            table_string += "\"" + \
                header_columns[self.NUMBER_OF_COLUMNS-1]+"\""+" text"
            table_string = "CREATE TABLE IF NOT EXISTS " + \
                os.path.basename(self.file_to_read)+" ("+table_string+")"
            print(table_string)
            c.execute(table_string)
            conn.commit()

            c.execute('''  
                SELECT * FROM ''' + os.path.basename(self.file_to_read)
                      )

            for row in c.fetchall():
                print(row)

        self.parse_done = True
        return self.parse_done

    def extractCounts(self):
        """Builds a dictionary of counts for each of the 1 through 9, most significant
        digits of the column being analysed.
        """
        population_values = self.dataframe[self.COL_OF_INTEREST]
        self.counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for item in population_values:
            for index in range(0, 1):
                self.counts[int(item[index])] = self.counts.get(
                    int(item[index]), 0) + 1

    def is_following_bernofs_law(self):
        """Return True if ~80% of the given values are closer than a euclidean
        distance of .05"""

        x_digits = list(self.counts.keys())
        y_frequency = list(self.counts.values())

        n_parsed_records = len(self.good_data)
        y_frequency = [
            frequency_count / n_parsed_records for frequency_count in y_frequency
        ]

        y_frequency_2 = []
        for digit in x_digits:
            y_frequency_2.append(log10(1 + (1 / digit)))

        distances = []
        threshold_counts = {True: 0, False: 0}
        for index in range(0, 9):
            distances.append(abs(y_frequency_2[index] - y_frequency[index]))
            within_threshold = abs(
                y_frequency_2[index] - y_frequency[index]) < 0.05
            threshold_counts[within_threshold] = (
                threshold_counts.get(within_threshold, 0) + 1
            )
        """
        # Return true if there are at least 7 instances (out of 9) where the
        # distribution is close to the logarithmic distribution pre-computed in y_frequency_2
        """
        return threshold_counts[False] < 3, distances

    @staticmethod
    def generate_html(embed_plot=False, follows_benfords_law=False):
        """Generates a HTML doc with the Bernof's plot embeded in it and a string
        indicating if the dataset follows Bernof's law.

        Args:
            embed_plot (bool, optional): If true, embeds the plot in the document. Defaults to False.
            follows_benfords_law (bool, optional): Summarizes the conformity of
            the input data to Bernof's law, based on the value of this parameter. Defaults to False.
        """
        pre = """
            <!doctype html>
                <html>
                    <head>
                        <title>Benford's law Demo</title>
                    </head>
                    <body>
                        <h3>Benford's Law</h3>
                        <p><em>Benford's law</em>, also known as the Newcomb-Benford law, 
                        the law of anomalous numbers, or the first-digit law, is an observation 
                        that in many real-life sets of numerical data, the leading digit is 
                        likely to be small. In sets that obey the law, the number 1 appears as 
                        the leading significant digit about 30% of the time, while 9 appears as 
                        the leading significant digit less than 5% of the time. </p>
                        <a href="https://en.wikipedia.org/wiki/Benford%27s_law"> -- Wikipedia Reference</a>
                        <p>1. Select a TAB delimited file that contains a column of integer values under 
                        the column heading <em>7_2009</em></p>
                        <p>2. Select Plot to display the frequency distribution of the most 
                        significant digits in the <em>7_2009</em> column.</p>

                        <form method="POST" action="" enctype="multipart/form-data">
                            <p><input type="file" name="file"></p>
                            <p><input type="submit" value="Plot"></p>
                        </form>
        """
        post = """
                    </body >
                </html>
                """

        file = open("templates/index.html", "w")
        file.writelines(pre)

        if embed_plot:
            data_uri = base64.b64encode(
                open("plot.png", "rb").read()).decode("utf-8")
            img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
            file.writelines(img_tag)

            result_tag = '<p>The given dataset does NOT follow Benford\'s Law.</p>'
            if(follows_benfords_law):
                result_tag = '<p>The given dataset follows Benford\'s Law.</p>'
            file.writelines(result_tag)

        file.writelines(post)
        file.close()

    def do_plot(self, x_digits, y_frequency, y_frequency_2):
        """1. Generate a plot and save it to a file. 
           2. Generate the HTML with the plot embedded in it.

        Args:
            x_digits (_type_): list of digits 1 through 9
            y_frequency (_type_): Percentage occurrences of each digit in the parsed data.
            y_frequency_2 (_type_): Percentage occurrences of each digit in a reference
            dataset that shows the Bernof's distribution.
        """
        plt.figure(figsize=(10, 5))
        plt.bar(x_digits, y_frequency, color="green", width=0.5)
        plt.plot(x_digits, y_frequency_2, color="red")
        plt.xlabel("Digits [1 to 9]")
        plt.ylabel("Frequency [%]")
        plt.title("Most Significant Digit distribution")
        plt.legend(['Benford\'s Law', os.path.basename(self.file_to_read)])
        plt.savefig("plot.png")
        self.generate_html(True, self.is_following_bernofs_law())

    def generate_plot(self):
        """Build two series; First one is the distribution of digit occurrences
        Second one is a reference distribution that follows Bernof's theory.
        """
        if self.parse_done is False:
            if(self.parse()):
                self.extractCounts()
            else:
                return

        x_digits = list(self.counts.keys())
        y_frequency = list(self.counts.values())
        n_parsed_records = len(self.good_data)
        y_frequency = [
            frequency_count / n_parsed_records for frequency_count in y_frequency
        ]

        y_frequency_2 = []
        for digit in x_digits:
            y_frequency_2.append(log10(1 + (1 / digit)))

        job_for_another_core = multiprocessing.Process(
            target=self.do_plot, args=(x_digits, y_frequency, y_frequency_2))
        job_for_another_core.start()
