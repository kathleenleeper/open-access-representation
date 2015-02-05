#import codecs
#from gender_detector import GenderDetector #import genderMalev mdul

from genderComputer import GenderComputer #import gendercomputer - more fully featured
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
    data = b.load(bibtex_file, parser = parser)

print(data.entries[10])

#for i in  data.entries:

for i in data.entries:
    items  = i.iteritems()
    for k, v in items:
        if k == 'author':
            for j in v:
                au = ', '.join(reversed(j.split(', ', 1))) #convert from last, first to first, last
                print au
               # print j
        
