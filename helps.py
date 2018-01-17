import requests
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd
import itertools

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
    singlewords = ""

    for i in range(len(msg)):
        singlewords = singlewords + msg[i]

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(singlewords)

    stopWords = set(stopwords.words('german'))

    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)

    print(wordsFiltered)

    return wordsFiltered

def getTestData():
    neg = pd.read_csv("C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\SentiWS_v1.8c\\SentiWS_v1.8c_Negative.txt",
                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])
    negativedata = prepareSentimentData(neg)

    pos = pd.read_csv("C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\SentiWS_v1.8c\\SentiWS_v1.8c_Positive.txt",
                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])
    positivedata = prepareSentimentData(pos)

    result = positivedata.append(negativedata, ignore_index=True)

    return result

def prepareSentimentData(data):
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



