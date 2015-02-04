#import codecs
#from gender_detector import GenderDetector #import genderMalev mdule
#from genderComputer import GenderComputer #import gendercomputer - more fully featured
#import csv
#import re # regular expression searching
import pprint as pp
import os

import bibtexparser as b #module for bibtexin'
from bibtexparser.bparser import BibTexParser #import to add customization
from bibtexparser.customization import *

bib = 'CriticalOpenNeuro.bib' #bring that bib file in

with open(bib) as bibtex_file:
    parser = BibTexParser()
    parser.customization = author #parse author fields as individuals
    bib_database = b.load(bibtex_file, parser = parser)


