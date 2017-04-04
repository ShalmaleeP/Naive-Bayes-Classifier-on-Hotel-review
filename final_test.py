from __future__ import division
from collections import defaultdict
import math
import sys
import re

f1 = open("nbmodel.txt", "r")
f = f1.read()
lines = f.splitlines()
f1.close()

pp = float(lines[0].split(" ")[3])
pn = float(lines[1].split(" ")[3])
pd = float(lines[2].split(" ")[3])
pt = float(lines[3].split(" ")[3])

prob_pos = defaultdict(float)
prob_neg = defaultdict(float)
prob_dec = defaultdict(float)
prob_tru = defaultdict(float)

for line in lines[5:]:
    cont = line.split(" ")
    word = cont[0]
    dictname = cont[2]
    val = cont[4]
    if (dictname == "positive"):
        prob_pos[word] = float(val)
    if (dictname == "negative"):
        prob_neg[word] = float(val)
    if (dictname == "deceptive"):
        prob_dec[word] = float(val)
    if (dictname == "truthful"):
        prob_tru[word] = float(val)

file = open("test.txt", 'r')
data = file.read()
test = data.splitlines()
file.close()

d = defaultdict(list)
idlist = [];
for testline in test:
    cont = testline.split(" ")
    id = cont[0]
    idlist.append(id)
    line = testline.lower()
    wordsinsen = []
    for j in cont[1:]:
        # j = re.sub(r'[^\w\s]', '', j)
        wordsinsen.append(j)

    for i in wordsinsen[1:]:
        d[id].append(i)

result = defaultdict(list)

outfile = open("nboutput.txt", "w+")
op = []
for eachid in d:
    scorep = math.log(pp)
    scoren = math.log(pn)
    scored = math.log(pd)
    scoret = math.log(pt)
    # print eachid
    for current_word in d[eachid]:
        if current_word in prob_pos:
            scorep += math.log(prob_pos[current_word])
        if current_word in prob_pos:
            scoren += math.log(prob_neg[current_word])
        if current_word in prob_pos:
            scored += math.log(prob_dec[current_word])
        if current_word in prob_pos:
            scoret += math.log(prob_tru[current_word])
    if (scorep > scoren):
        result[eachid].append("positive")
        class1 = "positive"
    else:
        result[eachid].append("negative")
        class1 = "negative"
    if (scored > scoret):
        result[eachid].append("deceptive\n")
        class2 = "deceptive"
    else:
        result[eachid].append("truthful\n")
        class2 = "truthful"
    towrite = eachid + " " + class2 + " " + class1
    outfile.write("%s\n" % towrite)

outfile.close()