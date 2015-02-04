#import codecs
#from gender_detector import GenderDetector #import genderMalev mdule
#from genderComputer import GenderComputer #import gendercomputer - more fully featured
#import csv
#import re # regular expression searching

import os

import bibtexparser as b #module for bibtexin'
from b.bparsers import BibTexParser #import to add customizations

b = 'CriticalOpenNeuro.bib' #bring that bib file in

parser = BibTexParser()


with open(b) as bibfile:
    bib = bparse.load(bibfile)
