from typing import Any, List, Optional
from hash_quad import *
import string

class Concordance:

    def __init__(self) -> None:
        """ Starting size of hash table should be 191: self.concordance_table = HashTable(191) """
        self.stop_table: Optional[HashTable] = None          # hash table for stop words
        self.concordance_table: HashTable = HashTable(191)              # hash table for concordance

    def load_stop_table(self, filename: str) -> None:
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.stop_table = HashTable(191)
        try:
            with open(filename, 'r') as dataf:
                datalines = dataf.readlines()
        except:
            raise FileNotFoundError
        filtered = []
        for j in range(0, len(datalines)):
            x = datalines[j].replace('\n', '')
            filtered.append(x)
        for i in range(0, len(filtered)):
            self.stop_table.insert(filtered[i], [i])




    def load_concordance_table(self, filename: str) -> None:
        """ Read words from input text file (filename) and insert them into the concordance hash table, 
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)

        Process of adding new line numbers for a word (key) in the concordance:
            If word is in table, get current value (list of line numbers), append new line number, insert (key, value)
            If word is not in table, insert (key, value), where value is a Python List with the line number
        If file does not exist, raise FileNotFoundError """
        try:
            with open(filename, 'r') as dataf:
                datalines = dataf.readlines()
        except:
            raise FileNotFoundError
        bad = []
        datalines_temp = datalines
        for i in range(0, len(datalines)):
            for j in datalines[i]:
                if j.isupper():
                    datalines_temp[i] = datalines_temp[i].replace(j, j.lower())
                if j in string.digits or (j in string.punctuation and j != '-') or j == '\n':
                    datalines_temp[i] = datalines_temp[i].replace(j, '')
                if j == '-':
                    datalines_temp[i] = datalines_temp[i].replace(j, ' ')
            counting = ' '.join(datalines_temp)
            counting = counting.split()
            for k in counting:
                if self.stop_table.in_table(k) == True and k not in bad:
                    bad.append(k)
            final = [' '.join([a for a in datalines2.split() if not a in bad]) for datalines2 in datalines_temp[i].split()]
            for m in range(0, len(final)):
                if final[m] != '':
                    if self.concordance_table.in_table(final[m]) == True:
                        temp = self.concordance_table.get_value(final[m])
                        if (i + 1) not in temp:
                            new_val = temp.append(i + 1)
                    else:
                        self.concordance_table.insert(final[m], [i + 1])

    def write_concordance(self, filename: str) -> None:
        """ Write the concordance entries to the output file(filename)
        See sample output files for format. """
        keys = self.concordance_table.get_all_keys()
        keys.sort()
        with open(filename, 'w') as outall:
            for q in range(0, len(keys) - 1):
                values = ''
                for ok in self.concordance_table.get_value(keys[q]):
                    values = values + str(ok) + ' '
                outall.write(str(keys[q] + ': ' + str(values)) + '\n')
            values2 = ''
            for oki in self.concordance_table.get_value(keys[len(keys)-1]):
                values2 = values2 + str(oki) + ' '
            outall.write(str(keys[len(keys)-1]) + ': ' + str(values2))

