# -*- coding: utf-8 -*-
#Modules GOOGLE
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json
import csv  


#Ensemble des données pour la connexion sur l'API de Youtube DATA V3
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "SECRET CODE"
developer_key="API KEY"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Pour se connecter à l'API 
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=developer_key)

#Liste Stat Comparées
Chaines=['TastyNetwork','MonstercatMedia']
ID=[]
Nombre_View=[]
Nombre_Subs=[]
Nombre_Video=[]

#Requête à l'API
for k in Chaines:
    #Requête pour les infos générales des chaines
    #statistics --> nbre de views + nbre de subs + nbre de vidéo publiés
    #brandingSettings --> titre de la chaine, keyword, description, familyfriendly
    #topicDetails --> catégorisation YT
    request = youtube.channels().list(
        part="statistics,brandingSettings,topicDetails",
        forUsername=k)
    response = request.execute()
    with open('Infos_Genérales_'+k+'.json','w', encoding='utf-8') as output:
        json.dump(response, output)
    
    #Variable pour tableau comparatif chaine générales
    nb_view=response['items'][0]['statistics']['viewCount']
    Nombre_View.append(nb_view)
    nb_subs=response['items'][0]['statistics']['subscriberCount']
    Nombre_Subs.append(nb_subs)
    nb_video=response['items'][0]['statistics']['videoCount']
    Nombre_Video.append(nb_video)

#Tableau comparatif Stats
with open('Stats_Comparee.csv', 'w', encoding='utf-8') as output:
    data=csv.writer(output, lineterminator='\n')
    data.writerow(['Chaine', 'Nombre de video', 'Nombre de vues', 'Nombre de subs'])
    data.writerows(zip(Chaines, Nombre_Video, Nombre_View, Nombre_Subs))