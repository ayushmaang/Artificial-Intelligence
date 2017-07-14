import nltk
import matplotlib.pyplot as plt
import math

from nltk.corpus import inaugural

from nltk.corpus import brown

from nltk.corpus import wordnet as wn

import numpy as np

from nltk.book import text1,text2

from nltk import FreqDist



def ex7():
    list = (nltk.corpus.gutenberg.fileids())

    emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))

    for thing in list:
        emma = nltk.Text(nltk.corpus.gutenberg.words(thing))
        print(emma.concordance("however"))

def ex23():
    news_text = brown.words(categories='news')
    fdist = nltk.FreqDist(w.lower() for w in news_text)
    array = []
    count = 0
    for i in fdist:
        array.append(fdist.get(i))
        count+=1

    for i in range(len(array)):
        array[i] = math.log(array[i],math.e)


    array.sort()
    array.reverse()


    plt.plot(array)

    plt.ylabel('numbers')
    plt.show()

word_types = ["n","v","a","r"]


def ex27():
    for i in word_types:
        words = list()
        count = 0
        for x in wn.all_synsets(i):
            temp = x.name()
            cool = temp.split('.')[0]
            test = wn.synsets(cool,i)
            count+= len(wn.synsets(cool,i))
            words.append(x.name().split('.')[0])

        print(float(count)/float(len(words)))

def ex9():
    """Pick a pair of texts and study
    the differences between them, in terms of vocabulary,
    vocabulary richness, genre, etc.
    Can you find pairs
    of words which have quite different meanings across the two texts,
    such as monstrous in Moby Dick and in Sense and Sensibility?"""

    print("\nWord Diversity of Senmse and Sensibility by Jane Austen 1811: ",len(text2)/len(set(text2)))
    print("Word Diversity of Moby Dick by Herman Melville 1851: ",len(text1)/len(set(text1)))

    fdist1 = FreqDist([w.lower() for w in text1 if len(w) > 10])
    fdist2 = FreqDist([w.lower() for w in text2 if len(w) > 10])

    test = list(fdist1.items())
    temp = list((fdist2.items()))

    print("Text1")
    for i in test:
        if i[1] > 10:
            print(i[0],end=" ")
    print("\nText 2")
    for i in temp:
        if i[1] > 10:
            print(i[0],end=" ")



def ex12():
    """The CMU Pronouncing Dictionary contains multiple pronunciations for certain words.
    How many distinct words does it contain?
    What fraction of words in this dictionary have more than one possible pronunciation?"""
    total = nltk.corpus.cmudict.entries()
    cool = [i for i, pron in total]
    print("Distint Words")
    print(len(set(cool)))
    print("Fraction:")
    print((1- len(set(cool)) / len(cool)) * 100)


def ex15():
    """Write a program to find all words that occur at least three times in the Brown Corpus."""
    fdist = FreqDist(brown.words())
    print([w for w in set(fdist) if fdist[w] >= 3])

def ex18():
    """Write a program to print the 50 most frequent
    bigrams (pairs of adjacent words) of a text, omitting bigrams that contain stopwords."""

    stopwords = nltk.corpus.stopwords.words('english')
    bigrams = nltk.bigrams(nltk.corpus.brown.words(categories="news"))
    fdist = FreqDist([w for w in bigrams if w[0] not in stopwords and w[1] not in stopwords])

    print(list(fdist)[:50])

ex18()


