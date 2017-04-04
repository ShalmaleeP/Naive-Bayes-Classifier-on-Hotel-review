from __future__ import division
from collections import defaultdict
import sys
import re

file = open("train-text.txt", 'r')
f = file.read()
lines = f.splitlines()
d = defaultdict(list)
wordcount = defaultdict(int)
vocab = []
identifierset = []
stoplist = ['the', 'for', 'had', 'and', 'to', 'a', 'i', 'was', 'in', 'of', 'you', 'is', 'it', 'at', 'my', 'that',
            'with', 'they', 'on', 'our', 'be', 'as', 'there', 'an', 'or', 'this']

for i in lines:
    id = i.split(" ")[0]
    identifierset.append(id)
    i = i.lower();
    words = i.split(" ");
    wordsinsen = []
    for j in words:
        # j = re.sub(r'[^\w\s]', '', j)
        wordsinsen.append(j)

    for i in range(1, len(wordsinsen)):
        if (wordcount[wordsinsen[i]] == 0 and wordsinsen[i] not in stoplist):
            vocab.append(wordsinsen[i])
        if (wordsinsen[i] not in stoplist):
            wordcount[wordsinsen[i]] = wordcount[wordsinsen[i]] + 1
            d[id].append(wordsinsen[i])
file.close()

import operator

sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1))

file = open("train-labels.txt", 'r')
f = file.read()
lines = f.splitlines()
file.close()

positive = set()
negative = set()
deceptive = set()
truthful = set()

for line in lines:
    single = line.split()
    id = single[0]
    if (single[1] == "deceptive"):
        deceptive.add(id)
    if (single[2] == "negative"):
        negative.add(id)
    if (single[1] == "truthful"):
        truthful.add(id)
    if (single[2] == "positive"):
        positive.add(id)

dictpositive = defaultdict(int)
dictnegative = defaultdict(int)
dictdeceptive = defaultdict(int)
dicttruthful = defaultdict(int)

for identifier in positive:
    for item in d[identifier]:
        dictpositive[item] += 1

for identifier in negative:
    for item in d[identifier]:
        dictnegative[item] += 1

for identifier in deceptive:
    for item in d[identifier]:
        dictdeceptive[item] += 1

for identifier in truthful:
    for item in d[identifier]:
        dicttruthful[item] += 1

N = len(identifierset)
f1 = open('nbmodel.txt', 'w+')

prior1 = float(len(positive) / N)
prior2 = float(len(negative) / N)
prior3 = float(len(deceptive) / N)
prior4 = float(len(truthful) / N)

f1.write("Prior for positive %f\n" % prior1)
f1.write("Prior for negative %f\n" % prior2)
f1.write("Prior for deceptive %f\n" % prior3)
f1.write("Prior for truthful %f\n" % prior4)

# For positive
sumofwordsinpd = sum(dictpositive.values())
probpos = defaultdict(float)
for word in vocab:
    probpos[word] = (dictpositive[word] + 1) / (sumofwordsinpd + len(vocab))
    f1.write("%s | positive = %f \n" % (word, probpos[word]))

# For negative
sumofwordsinpt = sum(dictnegative.values())
probneg = defaultdict(float)
for word in vocab:
    probneg[word] = (dictnegative[word] + 1) / (sumofwordsinpt + len(vocab))
    f1.write("%s | negative = %f \n" % (word, probneg[word]))

# For deceptive
sumofwordsinnd = sum(dictdeceptive.values())
probdec = defaultdict(float)
for word in vocab:
    probdec[word] = (dictdeceptive[word] + 1) / (sumofwordsinnd + len(vocab))
    f1.write("%s | deceptive = %f \n" % (word, probdec[word]))

# For truthful
sumofwordsinnt = sum(dicttruthful.values())
probtru = defaultdict(float)
for word in vocab:
    probtru[word] = (dicttruthful[word] + 1) / (sumofwordsinnt + len(vocab))
    f1.write("%s | truthful = %f \n" % (word, probtru[word]))

f1.close()

