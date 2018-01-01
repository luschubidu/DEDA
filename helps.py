import requests
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


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
