from conexion_base_de_datos.conexion import PostgresSQLPool
from tweepy_api.tweepy_api import api
import tweepy #Incluimos la api de Tweepy para obtener los tweets de Twiiter.
import nltk #Incluimos esta para la calificación de Tweets con NLP
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

class TweetModel:
    def __init__(self):        
        self.cursor = PostgresSQLPool()

    def search_tweet_by_topic(self, topic, user_id): #Busqueda de Tweets por tema gracias a tweeepy
        params = {
            'topic' : topic,
            'user_id' : user_id #El id es necesario para las auditorias
        }

        tweets_extraidos = []
        for tweet in tweepy.Cursor(api.search, q=params['topic'], tweet_mode="extended").items(3):
            hashtag_text = ""
            hashtags = tweet._json['entities']['hashtags']
            #Almacenamos los hastags
            for hashtag in hashtags:
                hashtag_text = hashtag_text + hashtag['text'] + ", "
            hashtag_text = hashtag_text[:-2]
            
            #Clasificación de tweets con nltk
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            sentences = tokenizer.tokenize(tweet._json['full_text']) #separamos el texto del tweet por oraciones
            analizador = SentimentIntensityAnalyzer()
            negativos = []
            neutros = []
            positivos = []
            promedios = []
            scores = analizador.polarity_scores(tweet._json['full_text']) #Analizamos el tweet completo
            negativo = scores['neg']
            neutro = scores['neu']
            positivo = scores['pos']
            promedio = scores['compound'] #Promedio va de -1 a 1 indicando si se inclina más a uno de los sentimientos
            calificacion = ""

            for sentence in sentences:
                scores = analizador.polarity_scores(sentence) #clasitifamos las oracines de los tweets
                negativos.append(scores['neg'])
                neutros.append(scores['neu'])
                positivos.append(scores['pos'])
                promedios.append(scores['compound'])
            n_oraciones = len(sentences)
            
            if  promedio <= -0.5:
                calificacion = "negativo"
            elif promedio > -0.5 and promedio < 0.5:
                calificacion = "neutro"
            else:
                calificacion = "positivo"

            #Luego realizamos la inserción del tweet ya clasificado
            query_params = {
                "tweet" :  tweet._json['full_text'],
                "twitter_username" : tweet._json['user']['name'],
                "twitter_user_location" : tweet._json['user']['location'],
                "hashtags" : hashtag_text,
                "user_id" : params['user_id'],
                "negativo" : negativo,
                "neutro" : neutro,
                "positivo" : positivo,
                "negativos" : negativos,
                "neutros" : neutros,
                "positivos" : positivos,
                "puntaje" : promedio,
                "promedios" : promedios,
                "calificacion" : calificacion,
                "tema" : params['topic']
            }
            query = """insert into tweets (tweet, twitter_username, twitter_user_location,hashtags, user_id, negativo, neutro, positivo, negativos, neutros, positivos, puntaje, promedios, calificacion, tema) 
             values (%(tweet)s, %(twitter_username)s, %(twitter_user_location)s, %(hashtags)s, %(user_id)s, %(negativo)s, %(neutro)s, %(positivo)s, %(negativos)s, %(neutros)s, %(positivos)s, %(puntaje)s, %(promedios)s, %(calificacion)s, %(tema)s) RETURNING tweet_id"""
            rv = self.cursor.execute(query, query_params, commit=True)
            id_of_new_row =  rv[0]#id recibido de la consulta al realizar la inserción
            content = {
                'tweet_id': id_of_new_row,
                'tweet': query_params['tweet'],
                'twitter_username': query_params['twitter_username'],
                'twitter_user_location': query_params['twitter_user_location'],
                'hashtags': query_params['hashtags'],
                'user_id': query_params['user_id'],
                "negativo" : query_params['negativo'],
                "neutro" : query_params['neutro'],
                "positivo" : query_params['positivo'],
                "negativos" : query_params['negativos'],
                "neutros" : query_params['neutros'],
                "positivos" : query_params['positivos'],
                "puntaje" : query_params['puntaje'],
                "promedios" : query_params['promedios'],
                "calificacion" : query_params['calificacion'],
                "tema" : query_params['tema']
            }
            tweets_extraidos.append(content)
            #Todo esto se realiza por cada tweet obtenido de tweepy

        return tweets_extraidos

    def get_tweet(self, id):
        params = {'id' : id}    
        rv = self.cursor.execute("SELECT * from tweets where tweet_id=%(id)s", params)
        data = []
        content = {}
        for result in rv:
            content = {
                'tweet' : result[0],
                'puntaje' : result[1],
                'calificacion' : result[2],
                'twitter_username' : result[3],
                'twitter_user_location' : result[4],
                'hashtags' : result[5],
                'user_id' : result[6]

            }
            data.append(content)
            content = {}
        return data

    def get_tweets(self):
        rv = self.cursor.execute("SELECT * from tweets")
        data = []
        content = {}
        for result in rv:
            content = {'tweet_id': result[0], 'tweet': result[1], 'puntaje': result[2],
                   'calificacion': result[3], 'twitter_username': result[4],
                   'twitter_user_location': result[5], 'hashtags': result[6],
                   'user_id': result[7]}
            data.append(content)
            content = {}
        return data

    def create_tweet(self, tweet, puntaje, calificacion, twitter_username, twitter_user_location, hashtags, user_id):
        params = {
            'tweet' : tweet,
            'puntaje' : puntaje,
            'calificacion' : calificacion,
            'twitter_username' : twitter_username,
            'twitter_user_location' : twitter_user_location,
            'hashtags' : hashtags,
            'user_id' : user_id

        }
        query = """insert into tweets (tweet, puntaje, calificacion, twitter_username,twitter_user_location,hashtags,user_id) 
         values (%(tweet)s, %(puntaje)s, %(calificacion)s, %(twitter_username)s, %(twitter_user_location)s
        , %(hashtags)s, %(user_id)s) RETURNING tweet_id"""    
        rv = self.cursor.execute(query, params, commit=True)
        id_of_new_row = rv[0]

        data = {
            'tweet_id': id_of_new_row,
            'tweet': params['tweet'],
            'puntaje': params['puntaje'],
            'calificacion': params['calificacion'],
            'twitter_username': params['twitter_username'],
            'twitter_user_location': params['twitter_user_location'],
            'hashtags': params['hashtags'],
            'user_id': params['user_id']

        }
        return data

    def delete_tweet(self, id):
        params = {'id' : id}      
        query = """delete from tweets where tweet_id = %(id)s RETURNING tweet_id"""    
        rv = self.cursor.execute(query, params, commit=True)

        tweet_id = rv[0]
        if tweet_id:
            data = {
                'tweet_id': tweet_id,
                'eliminado' : "True",
            }
        else:
            data = {
                'tweet_id': id,
                'eliminado' : "False",
            }
        return data

    def update_tweet(self, id, tweet, puntaje, calificacion, twitter_username, twitter_user_location, hashtags, user_id):
        params = {
            'tweet_id' : id,
            'tweet' : tweet,
            'puntaje' : puntaje,
            'calificacion' : calificacion,
            'twitter_username' : twitter_username,
            'twitter_user_location' : twitter_user_location,
            'hashtags' : hashtags,
            'user_id': user_id
        }
        query = """UPDATE tweets SET tweet = %(tweet)s, puntaje = %(puntaje)s, calificacion = %(calificacion)s, twitter_username = %(twitter_username)s, twitter_user_location = %(twitter_user_location)s, hashtags = %(hashtags)s, user_id = %(user_id)s WHERE tweet_id = %(tweet_id)s"""    
        rv = self.cursor.execute(query, params, commit=True)

        data = {
            'tweet_id': id,
            'tweet': params['tweet'],
            'puntaje': params['puntaje'],
            'calificacion': params['calificacion'],
            'twitter_username': params['twitter_username'],
            'twitter_user_location': params['twitter_user_location'],
            'hashtags': params['hashtags'],
            'user_id': params['user_id']
        }
        return data

if __name__ == "__main__":    
    tm = TweetModel()