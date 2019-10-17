from database import *
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import re
from timeit import default_timer as timer
from nltk.stem import PorterStemmer
import time
from greek_stemmer import GreekStemmer
timestr = time.strftime("%Y%m%d-%H%M%S")
#https://pythonprogramming.net/lemmatizing-nltk-tutorial/
#https://medium.com/@pemagrg/pre-processing-text-in-python-ad13ea544dae
start = timer()
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
    nltk.download('all')
    return data6

def remove_punctuation(text):
    '''a function for removing punctuation'''
    # replacing the punctuations with no space,
    # which in effect deletes the punctuation marks
    translator = str.maketrans('', '', string.punctuation)
    # return the text stripped of punctuation marks
    return text.translate(translator)

def porterstemmer(words):
    ps = PorterStemmer()
    for word in words:
        print(word + ":" + ps.stem(word))
    return
def plot(filtered_sentence):
    freq = nltk.FreqDist(filtered_sentence)
    value=[]
    for key, val in freq.items():
        value.append(str(key) + ':' + str(val))
    freq.plot(50, cumulative=False)
    return value


def matrix(results):
    end = timer()
    lr = (len(set(results)) / len(results) )*100
    count_distinct = len(set(results))
    count_words_total = len(results)
    print("count_distinct", count_distinct)
    print("Measure of the lexical richness of the text.Number of distinct words",
          lr, "%")
    print("Total words", count_words_total)
    total_time = end - start
    print("time:", total_time)
    return lr , count_distinct , count_words_total , total_time

def stopw(word,stop_words):
    filtered_sentence = []
    for w in word:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

def savetofile(value,lr , count_distinct , count_words_total,total_time):
    with open(str(timestr ) + '.text', 'a+') as filehandle:
        filehandle.write('Measure of the lexical richness of the text.Number of distinct words %s\n' % str(lr))
        filehandle.write('Total words %s\n' % str(count_words_total))
        filehandle.write('count_distinct %s\n' % str(count_distinct))
        filehandle.write('total_time %s\n' % str(total_time))
        filehandle.close()
    with open(str(timestr ) + '.text', 'a+', encoding="utf-8") as filehandle:
        for listitem in value:
            filehandle.write('%s\n' % listitem)
    filehandle.close()

def count_punctuation_f(lr , count_distinct , count_words_total):
    with open(str(timestr) + '.text', 'w+') as filehandle:
        filehandle.write('Punctuation Measure of the lexical richness of the text.Number of distinct words %s\n' % str(lr))
        filehandle.write('Punctuation Total words %s\n' % str(count_words_total))
        filehandle.write('Punctuation count_distinct %s\n' % str(count_distinct))
        filehandle.close()

def calculatepunctuation(p_lr,p_count_distinct,p_count_words_total , p_total_time , lr,count_distinct,count_words_total , total_time):
    plr = p_lr - lr
    pcount_distinct = int(count_distinct) - int(p_count_distinct)
    pcount_words_total = int(count_words_total) - int(p_count_words_total)
    ptotal_time = int(total_time) - int(p_total_time)
    print("Measure of the lexical richness of the text.Number of distinct words" ,plr)
    print("count_distinct",pcount_distinct)
    print("Total words" ,pcount_words_total)
    print("Time took",ptotal_time , "s")
    with open(str(timestr ) + '.text', 'a+') as filehandle:
        filehandle.write('difference between Measure of the lexical richness of the text.Number of distinct words %s\n' % str(plr))
        filehandle.write('difference between Total words %s\n' % str(pcount_words_total))
        filehandle.write('difference between count_distinct %s\n' % str(pcount_distinct))
        filehandle.write('difference between total_time %s\n' % str(ptotal_time))
        filehandle.close()



def spacy_sent_tokenize(data6):
    with open('sentence' + str(timestr) + '.text', 'a+',encoding="utf-8" ) as filehandle:

        for doc in data6:
            print('Original Article: %s' % (doc))
            filehandle.write('Original Article: %s\n' % (doc))
            sentences = re.split('(\.|!|\?)', str(doc))
            for i, s in enumerate(sentences):
                print('-->Sentence %d: %s' % (i, s))
                filehandle.write('-->Sentence %d: %s\n' % (i, s))
data6 =dataprocessing(data)
#data6 = remove_punctuation(data6)

print("--------------------------------------------------calculate punctuation--------------------")
count_punctuation =remove_punctuation(data6)
sent_tokenize(count_punctuation,"greek")
count_punctuation = word_tokenize(count_punctuation)
stop_words = set(stopwords.words('english'))
count_punctuation = stopw(count_punctuation,stop_words)
p_lr,p_count_distinct,p_count_words_total , p_total_time = matrix(count_punctuation)
count_punctuation_f(p_lr,p_count_distinct,p_count_words_total)
print("--------------------------------------------------calculate punctuation--------------------")

print("--------------------------------------------------count total------------------------------")
sent_tokenize(data6,"greek")
word = word_tokenize(data6)
#word = porterstemmer(word)
stop_words = set(stopwords.words('english'))
filtered_sentence = stopw(word,stop_words)
lr,count_distinct,count_words_total , total_time = matrix(filtered_sentence)
value =plot(word)
savetofile(value,lr,count_distinct,count_words_total,total_time)
print("--------------------------------------------------punctuation count------------------------")
calculatepunctuation(p_lr,p_count_distinct,p_count_words_total , p_total_time , lr,count_distinct,count_words_total , total_time)
result_sent_tokenize = spacy_sent_tokenize(data)


