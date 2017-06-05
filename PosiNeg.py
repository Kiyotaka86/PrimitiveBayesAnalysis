#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 18:58:29 2017

@author: Kio
"""
import mpmath
import math

#to read test file by review
def txtline(name):
    postes = open(name, 'r')
    postes = postes.read()
    postes = postes.lower()
    postes = postes.replace('.', '')
    postes = postes.replace('&#8217;', '')
    postes = postes.replace('\'', '')
    postes = postes.replace('?', '')
    postes = postes.replace('/', '')
    postes = postes.replace('!', '')
    postes = postes.replace(',', '')
    postes = postes.split('\n')
    
    return postes

#process whole training txt files
def txtsp (name):
    postes = open(name, 'r')
    postes = postes.read()
    postes = postes.lower()
    postes = postes.replace('.', '')
    postes = postes.replace('&#8217;', '')
    postes = postes.replace('\'', '')
    postes = postes.replace('?', '')
    postes = postes.replace('/', '')
    postes = postes.replace('!', '')
    postes = postes.replace(',', '')
    postes = postes.split(' ')

# I was attempting combine two words if negative adverb and adjective together 
#    neglist = ['not', 'dont', 'doesnt', 'didnt', 'wasnt', 'werent', 'arent', 'amnt', 'isnt']
#    adjlist = ['good','awesome', 'descent', 'better', 'hilarious', 'funny', 'interesting']
#
#    for w in range(1, len(postes)):
#        if postes[w] in adjlist:
#            if postes[w-1] in neglist:
#                newst =  postes[w -1] + postes[w]
#                postes[w] = newst
#                del postes[w-1]

    return postes


def word_count(text):
    wcount = {}

    for w in text:
        if len(w) > 0:
            if not w in wcount:
                wcount[w] = 1
            else:
                wcount[w]+=1
    return wcount


posi2 = txtsp('train-pos.txt')
posidic = word_count(txtsp('train-pos.txt'))

nega2 = txtsp('train-neg.txt')
negadic = word_count(txtsp('train-neg.txt'))


#calculate the probability of word shows up
poswratio = {}

for w in posidic:
    poswratio[w] = round((0.5 + posidic[w]) / (1.0 + len(posi2)), 15)
    
             
negwratio = {}

for w in negadic:
    negwratio[w] = round((0.5 + negadic[w])/(1.0 + len(nega2)), 15)

    
dicw ={}
for w in poswratio:
    if w in negwratio:
        dicw.setdefault(w, [])
        dicw[w].append(poswratio[w])
        dicw[w].append(negwratio[w])

#read either positive or negative test case
postes = txtline('test-pos.txt')

#the number of positive and negative reviews 
prolis = {"pos":0, "neg":0, "Neither":0}

for w in range(0, len(postes)):
    pos = 0.0
    neg = 0.0
    testline = postes[w].split(' ')
    for a in testline:
        if a in dicw:
            pos = pos + math.log(poswratio[a])
            neg = neg + math.log(negwratio[a])  
#it weirdly did not work well. I would like to talk about it with you
#        else:
#            pos = pos + math.log((1.0) - (poswratio[a]))
#            neg = neg + math.log((1.0) - (negwratio[a]))
    positive =  mpmath.exp(pos)
    negative =  mpmath.exp(neg)
# increment the dict according to the result
    if (positive/(positive+negative)) > 0.5:
        prolis["pos"]+=1
    elif (positive/(positive+negative)) < 0.5:
        prolis['neg']+=1
    else:
        prolis['Neither']+=1


print len(postes)
print prolis

    