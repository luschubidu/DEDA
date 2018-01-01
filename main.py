import facebook
import re
import requests
import helps

#alt shift e for running code (snippets) in console
#newpi for statistical analysis

#http://facebook-sdk.readthedocs.io/en/latest/install.html

#https://stackoverflow.com/questions/34891784/how-to-get-all-of-the-facebook-graph-api-page-feed
#https://stackoverflow.com/questions/32838434/how-to-get-user-posts-through-facebook-sdk-python-api/32896364#32896364

#@TODO update token via https://developers.facebook.com/tools/explorer/145634995501895/
token = "EAACEdEose0cBAJoxpMMEOKyhZCzPCZCeMa5zZBvQ4PSy8wTIAeRXCmjURXTZBC4BTY8DJ5PWDjvNmKA2ZAFsIhT2QPoRJyeCXRPu8ANYcZCKgSMqArJThKkeRFdPlLzT71pzN2o4Dj3TFKYjWUqx5EGAaEqnFK5NTwiwg76az3qamrmp8sqkfehSyKWdRfIqjfPLt6ZCDCqZBgZDZD"

graph = facebook.GraphAPI(access_token=token, version="2.11")

parties=["CDU", "CSU (Christlich-Soziale Union)", "SPD", "Die Linke", "AfD", "BÜNDNIS 90/DIE GRÜNEN", "FDP"]

page_id = {}

for i in range(len(parties)):
   tmp = graph.search(type="page", q=parties[i])
   reg = re.compile("\\b"+parties[i]+"\\b")
   b = False
   j=0

   while not b and (j<10):
       if (re.search(reg, tmp["data"][j]["name"]) != "" and len(parties[i]) == len(tmp["data"][j]["name"])):

           if (parties[i]=="CSU (Christlich-Soziale Union)"):
               key = "CSU"
           elif (parties[i]=="BÜNDNIS 90/DIE GRÜNEN"):
               key="Grüne"
           elif (parties[i]=="Die Linke"):
               key="Linke"
           else:
               key = parties[i]

           page_id[key]=tmp["data"][j]["id"]
           b= True

       else:
           j =j+1



cdu_msg = helps.getAllMessagesOfAPage(graph, page_id["CDU"])
csu_msg = helps.getAllMessagesOfAPage(graph, page_id["CSU"])
spd_msg = helps.getAllMessagesOfAPage(graph, page_id["SPD"])
linke_msg = helps.getAllMessagesOfAPage(graph, page_id["Linke"])
fdp_msg = helps.getAllMessagesOfAPage(graph, page_id["FDP"])
afd_msg = helps.getAllMessagesOfAPage(graph, page_id["AfD"])
gruene_msg = helps.getAllMessagesOfAPage(graph, page_id["Grüne"])

print(cdu_msg)

#http://opensourceforu.com/2016/12/analysing-sentiments-nltk/


