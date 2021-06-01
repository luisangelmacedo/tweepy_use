import tweepy       #Modulo de la API de Twitter
import datetime     #Modulo de fechas
import os           #Modulo del Sistema Operativo
from datetime import date 

consumerKey = "yourConsumerKeyHere"
consumerSecret = "yourConsumerSecretHere"
accessKey = "yourAccesKeyHere"
accessSecret = "yourAccessSecretHere"

#Menu
def choosingMenu():
    os.system("cls")
    print("+----------------------------------------------+")
    print("|               TweepyAPIFunctions             |")
    print("+----------------------------------------------+")
    print("| 1. Obtener tweets de un timeline             |")
    print("| 2. Obtener tweets por busqueda               |")
    print("| 3. Obtener tweets por interaccion            |")
    print("| 4. Salir                                     |")
    print("+----------------------------------------------+")
    option = input("| Select an option: ")
    
    if option == "1":
        print("+----------------------------------------------+")
        userName = input("| Username: ")
        print("+----------------------------------------------+")
        getTimeLine(userName)
        
    elif option == "2":
        print("+----------------------------------------------+")
        word = input("| Word: ")
        tweetLimit = input("| Quantity: ")
        print("+----------------------------------------------+")
        getTrends(word, int(tweetLimit))
    
    elif option == "3":
        print("+----------------------------------------------+")
        tweetId = input("| Tweet Id: ")
        tweetLimit = int(input("| Quantity: "))
        print("+----------------------------------------------+")
        getResponses(tweetId, tweetLimit)
        
    elif option == "4":
        exit()
        
    else:
        choosingMenu()
        
def getTimeLine(userName):
    #Este método solo tiene permitido descargar máximo los ultimos 3240 tweets del usuario
    #Especificar aquí durante las pruebas un número entre 200 y 3240
    tweetLimit = 3240
    
    #autorizar twitter, inicializar tweepy
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    
    #inicializar una list to para almacenar los Tweets descargados por tweepy
    allTweets = []    
    newTweets = api.user_timeline(screen_name = userName, count = 200, tweet_mode = "extended") #Modo extendido para obtener 280 carac. excep. RT
    allTweets.extend(newTweets)
    oldest = allTweets[-1].id - 1
    
    while len(newTweets) > 0 and len(allTweets) <= tweetLimit:
        newTweets = api.user_timeline(screen_name = userName, count = 200, include_rts = False, max_id = oldest, tweet_mode = "extended")
        allTweets.extend(newTweets)
        oldest = allTweets[-1].id - 1
    
    today = date.today()
    outTweets = [(tweet.id_str, tweet.coordinates, tweet.in_reply_to_screen_name, tweet.created_at, tweet.full_text.replace('\n', ' '), tweet.retweet_count, tweet.favorite_count) for tweet in allTweets]
    dump = open(f"{today.day}{today.month}{today.year}-{userName}.lam", "a", encoding="utf-8")
    
    for result in outTweets:
        line = "¦".join(map(str,result)) #Separador ¦ para el archivo exportado
        dump.write(line + "\n")
    
    print(f"| {len(allTweets)} tweets descargados")
    dump.close()
 
def getTrends(word, tweetLimit):
    #autorizar twitter, inicializar tweepy
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    
    #inicializar una list to para almacenar los Tweets descargados por tweepy
    allTweets = []
    counter = 0
    cleanTweets = []
    
    while counter <= tweetLimit:
        today = date.today()
        dump = open(f"{today.day}{today.month}{today.year}-{userName}.lam", "a", encoding="utf-8")
        
        if not counter: #Para obtener la primera tanda de 100 tweets
            newTweets = api.search(q = word+" -filter:retweet", count = 100, tweet_mode = "extended")
            allTweets.extend(newTweets)
            oldest = allTweets[-1].id - 1
            
        else: #Para anexar los siguientes tweets sin perder la primera tanda
            newTweets = api.search(q = word, count = 100, max_id = oldest, tweet_mode = "extended")
            allTweets.extend(newTweets)
            oldest = allTweets[-1].id - 1     
        
        for cnt in newTweets:
            if str(cnt.full_text.replace('\n', ' ')) in cleanTweets:
                pass
                
            else:
                cleanTweets.insert(counter, str(cnt.full_text.replace('\n', ' '))) #Guardamos los tweets para validar repetidos
                line = f"{cnt.id_str}¦{cnt.coordinates}¦{cnt.in_reply_to_screen_name}¦{cnt.created_at}¦{cnt.full_text}¦{cnt.retweet_count}¦{cnt.favorite_count}"
                dump.write(line + "\n")
                counter = counter + 1
    
    print(f"| {tweetLimit} tweets descargados")

def getResponses(tweetId, tweetLimit):
    #autorizar twitter, inicializar tweepy
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    
    #inicializar una list to para almacenar los Tweets descargados por tweepy
    allTweets = []
    counter = 0
    cleanTweets = []
    
    while counter <= tweetLimit:
        today = date.today()
        dump = open(f"{today.day}{today.month}{today.year}-{tweetId}.lam", "a", encoding="utf-8")
        
        if not counter: #Para obtener la primera tanda de 100 tweets
            newTweets = api.search(q = "conversation_id:"+str(tweetId), count = 100, tweet_mode = "extended")
            allTweets.extend(newTweets)
            oldest = allTweets[-1].id - 1
            
        else: #Para anexar los siguientes tweets sin perder la primera tanda
            newTweets = api.search(q = word, count = 100, max_id = oldest, tweet_mode = "extended")
            allTweets.extend(newTweets)
            oldest = allTweets[-1].id - 1     
        
        for cnt in newTweets:
            if str(cnt.full_text.replace('\n', ' ')) in cleanTweets:
                pass
                
            else:
                cleanTweets.insert(counter, str(cnt.full_text.replace('\n', ' '))) #Guardamos los tweets para validar repetidos
                line = f"{cnt.id_str}¦{cnt.coordinates}¦{cnt.in_reply_to_screen_name}¦{cnt.created_at}¦{cnt.full_text}¦{cnt.retweet_count}¦{cnt.favorite_count}"
                dump.write(line + "\n")
                counter = counter + 1
    
    print(f"| {len(cleanTweets)} tweets descargados")
    
choosingMenu()