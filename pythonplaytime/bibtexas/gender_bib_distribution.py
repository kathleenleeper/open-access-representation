from __future__ import division
from genderComputer import GenderComputer #import gendercomputer - more fully featured
import pprint as pp
import os
import bibtexparser as b #module for bibtexin'
from bibtexparser.bparser import BibTexParser #import to add customization
from bibtexparser.customization import *

gc = GenderComputer(os.path.abspath('./nameLists')) #make gendercomputer
women = 0
men = 0
uni = 0
notav = 0
auCount = 0
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
                auCount = auCount + 1
                gender = gc.resolveGender(j, None) #resolve gender, yay
                if gender == 'male':
                    men = men + 1
                elif gender == 'female':
                    women = women + 1
                elif gender == 'unisex':
                    uni = uni + 1
                else: 
                    notav = notav + 1
#'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
#calculate percents #hacks

percentMen = men/auCount*100
percentWomen = women/auCount*100
percentUni = uni/auCount*100
percentNotAv = notav/auCount*100
print 'author count total:', auCount
print 'women:', women,",", "%.2f" % percentWomen, '%'
print 'men:', men,",", "%.2f" %  percentMen, '%'
print 'unisex:', uni,",", "%.2f" %  percentUni, '%'
print 'unassigned:', notav,",", "%.2f" %  percentNotAv, '%'

