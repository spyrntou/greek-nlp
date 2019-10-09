from database import *
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import re
from timeit import default_timer as timer
from nltk.stem import PorterStemmer


#https://medium.com/@pemagrg/pre-processing-text-in-python-ad13ea544dae
start = timer()
import time
job_cat_list = []
query = "select meta_value from meta_terms where meta_key like 'description'"
data=database.main(query)


def dataprocessing(data):
    data = str(data)
    s2 = re.sub(r'<.*?>','',data)
    data6 = s2.replace("\\r", " ")
    data6 = data6.replace("\\xa0", "; ")
    data6 = data6.replace("\\r\\n", " ")
    data6 = data6.replace("\\r\\r", " ")
    data6 = data6.replace("\\n\\xa0", "; ")
    data6 = data6.replace("\\n\\n", " ")
    data6 = data6.replace("\\n", " ")
    nltk.download('all-corpora')
    return data6

def remove_punctuation(text):
    '''a function for removing punctuation'''
    # replacing the punctuations with no space,
    # which in effect deletes the punctuation marks
    translator = str.maketrans('', '', string.punctuation)
    # return the text stripped of punctuation marks
    return text.translate(translator)

def porterstemmer(word):
    ps = PorterStemmer()
    for word in words:
        print(word + ":" + ps.stem(word))
    return
def plot(filtered_sentence):
    freq = nltk.FreqDist(filtered_sentence)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))
    freq.plot(50, cumulative=False)


def matrix(results):
    end = timer()
    lr = len(set(results)) / len(results)
    count_distinct = len(set(results))
    count_words_total = len(results)
    print("count_distinct", count_distinct)
    print("measure of the lexical richness of the text. The next example shows us that the number of distinct words",
          lr * 100, "%")
    print("Total words", count_words_total)
    print("time:", end - start)



data6 =dataprocessing(data)
data6 = remove_punctuation(data6)
sent_tokenize(data6,"greek")
words = word_tokenize(data6)
#words = porterstemmer(words)
stop_words = set(stopwords.words('greek'))
filtered_sentence = []
for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)
matrix(filtered_sentence)
plot(filtered_sentence)
