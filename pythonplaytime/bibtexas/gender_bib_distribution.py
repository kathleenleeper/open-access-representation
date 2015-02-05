from genderComputer import GenderComputer #import gendercomputer - more fully featured
import pprint as pp
import os
import bibtexparser as b #module for bibtexin'

from bibtexparser.bparser import BibTexParser #import to add customization
from bibtexparser.customization import *

gc = GenderComputer(os.path.abspath('./nameLists')) #make gendercomputer
bib = 'CriticalOpenNeuro.bib' #bring that bib file in

with open(bib) as bibtex_file:
    parser = BibTexParser()
    parser.customization = author #parse author fields as individuals
    data = b.load(bibtex_file, parser = parser)


for i in data.entries:
    items  = i.iteritems()
    for k, v in items:
        if k == 'author':
            for j in v:
                gender = gc.resolveGender(j, None) #resolve gender, yay
                print j, gender
