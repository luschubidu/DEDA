import requests
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd
import itertools
import re

def getAllMessagesOfAPage(graph, page_id):
    page = graph.get_object(id=page_id, fields="posts")
    messages = []
    str_msg = "message"
    i = 0

    for i in range(len(page["posts"]["data"])):
        if str_msg in page["posts"]["data"][i]:
            messages.append(page["posts"]["data"][i]["message"])

    i = 0
    next_page = page["posts"]["paging"]["next"]

    while (len(messages) < 100):
        try:
            data = requests.get(next_page).json()

            for i in range(len(data["data"])):
                if str_msg in data["data"][i]:
                    messages.append(data["data"][i]["message"])

                next_page = data["paging"]["next"]

        except KeyError:
            print("Can't find 'next' key -- no additional page")
            break

    return messages

def cleanWordList(msg):
    # split messages in  sentences (before dot no www, and no number & after month
    sen = list()

    for message in msg:
        message = str(message)

        index = list().clear()
        i = -1
        b = True

        while b:
            i = message.find(".", i+1)

            if i==-1:
                b = False
            elif message[i-1]!="w" or not message[i-1].isdigit() and message[i+2:message.find(" ", i+2)] not in ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]:
                index.append(i)

        a = 0
        for idx in index:
            tmp = message[a:idx]
            a = idx
            sen.append(tmp)

    r = list()

    for elem in sen:
        messageFiltered = removeStopWords(elem)
        r.append(messageFiltered)

    return r

def removeStopWords(msg):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(msg)

    stopWords = set(stopwords.words('german'))

    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)

    return wordsFiltered

def getTestDataDict():
    neg = pd.read_csv("C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\SentiWS_v1.8c\\SentiWS_v1.8c_Negative.txt",
                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])
    negativedata = prepareSentimentDict(neg)

    pos = pd.read_csv("C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\SentiWS_v1.8c\\SentiWS_v1.8c_Positive.txt",
                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])
    positivedata = prepareSentimentDict(pos)

    result = positivedata.append(negativedata, ignore_index=True)

    return result

def prepareSentimentDict(data):
    combinedwords = data["wordplustype"]
    wordlist = list()
    wordtype = list()

    for combination in combinedwords:
        comb = str(combination)
        word = comb[:comb.find("|")]
        ty = comb[comb.find("|") + 1:]

        wordlist.append(word)
        wordtype.append(ty)

    tmp = pd.DataFrame(
        {"word" : wordlist,
         "type" : wordtype,
         "polarity" : data["polarity"],
         "sim" : data["sim"]}
    )

    tmp2 = tmp

    for index, row in tmp.iterrows():
        rsim = row["sim"]
        simwords = str(rsim).split(",")

        if("nan" not in str(simwords)):
            pol = list(itertools.repeat(row["polarity"],simwords.__len__()))
            t = list(itertools.repeat(row["type"],simwords.__len__()))

            tmp3 = pd.DataFrame(
                {"polarity" : pol,
                 "type" : t,
                 "word" : simwords
                 }
            )

            tmp2 = tmp2.append(tmp3, ignore_index=True)

    del tmp2["sim"]
    tmp2 = tmp2[["word", "type", "polarity"]]

    return tmp2

def getTestDataSentences():
    data = pd.read_csv("C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\mlsa\\layer2.phrases.majority.txt",
                       sep="\t", header=None, names=["sentence_ID", "phrase", "type_of_phrase"])

    phrases = data.phrase
    phrase = list()
    polarity = list()

    for index, row in phrases.iteritems():
        r = str(row)
        ph = r[:r.__len__()-1]
        pol = r[r.__len__()-1:]

        #+ = pos, - = neg, 0 = neutral, # = bipolar (both negative and positive)
        if pol == "+":
            pol = 1
        elif pol == "-":
            pol = 0
        elif pol == "0":
            pol = 2
        elif pol == "#":
            pol = 3

        ph = removeStopWords(ph)

        tmp = ""

        for elem in ph:
            tmp = tmp + elem + " "

        tmp = tmp[:tmp.__len__()-1]

        phrase.append(tmp)
        polarity.append(pol)

    testdata = pd.DataFrame({
        "phrase" : phrase,
        "polarity" : polarity,
    })

    return testdata



    #TODO 1. split column phrase into phrase and polarity (=last character in the elemenet)
    #TODO 2. remove brackets and other additional characters (only sentence left) with regex or tokenization with Vector?
    #TODO 3. prepare dataframe only with phrases and polarity




