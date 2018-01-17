import facebook
import re
import helps

#@TODO update token via https://developers.facebook.com/tools/explorer/145634995501895/
token = "EAACEdEose0cBAJoCYeT177IuDLtHJdLIGxIjKZCsvKpF8yfA1puhlZAUBztmVi0mfhsE3imv35epXDAZA5BsdSvkufowhFVB1wHYPJMM4WkwZBtkgCEfdgZBaLJm1l5qkEeEEMdZCJzw6fdTgo4MtTtZAARSZBI6ZA7ArMKT9fU8nzCmmGvNGvadHOl6gxtm5ZA3JsKzkZCaSKD9QZDZD"

graph = facebook.GraphAPI(access_token=token, version="2.11")

#@TODO try to search for "Gruene" instead of "Grüne" since encoding could cause problems
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


#@TODO maybe use one nested dict for all messages?
cdu_msg = helps.getAllMessagesOfAPage(graph, page_id["CDU"])
csu_msg = helps.getAllMessagesOfAPage(graph, page_id["CSU"])
spd_msg = helps.getAllMessagesOfAPage(graph, page_id["SPD"])
linke_msg = helps.getAllMessagesOfAPage(graph, page_id["Linke"])
fdp_msg = helps.getAllMessagesOfAPage(graph, page_id["FDP"])
afd_msg = helps.getAllMessagesOfAPage(graph, page_id["AfD"])
gruene_msg = helps.getAllMessagesOfAPage(graph, page_id["Grüne"])


#@TODO do sentimental analysis
testdata = helps.getTestData()
print(testdata.head())

cdu = helps.cleanWordList(cdu_msg)

#make pos / neg to 0 ad 1
#types of words?

#Dataframe bilden mit Partei und Score, die trainieren um herauszufinden, wie wahrscheinlich es ist, dass die nächste Nachricht pos / neg ist?