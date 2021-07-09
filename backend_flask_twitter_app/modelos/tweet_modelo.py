from conexion_base_de_datos.conexion import PostgresSQLPool
from tweepy_api.tweepy_api import api
import tweepy #Incluimos la api de Tweepy para obtener los tweets de Twiiter.
import nltk #Incluimos esta para la calificación de Tweets con NLP
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize
import json
import copy

tweet_content_structure = {
                'tweet_id': '',
                'tweet': '',
                'twitter_username': '',
                'twitter_user_location': '',
                'hashtags': '',
                'user_id': '',
                "negativo" : '',
                "neutro" : '',
                "positivo" : '',
                "negativos" : '',
                "neutros" : '',
                "positivos" : '',
                "puntaje" : '',
                "promedios" : '',
                "calificacion" : '',
                "tema" : ''
            }

def agregar_datos_tweet(tweet, twiitter_username, twitter_user_location, hashtags):
    tweet_content_structure['tweet'] = tweet
    tweet_content_structure['twiitter_username'] = twiitter_username
    tweet_content_structure['twitter_user_location'] = twitter_user_location
    tweet_content_structure['hashtags'] = hashtags

def agregar_datos_singulares(user_id, negativo, neutro,positivo):
    tweet_content_structure['user_id'] = user_id
    tweet_content_structure['negativo'] = negativo
    tweet_content_structure['neutro'] = neutro
    tweet_content_structure['positivo'] = positivo
def agregar_datos_plurales(negativos, neutros, positivos, promedios):
    tweet_content_structure['negativos'] = negativos
    tweet_content_structure['neutros'] = neutros
    tweet_content_structure['positivos'] = positivos
    tweet_content_structure['promedios'] = promedios
def agregar_clasificacion(puntaje,calificacion,tema):
    tweet_content_structure['puntaje'] = puntaje
    tweet_content_structure['calificacion'] = calificacion
    tweet_content_structure['tema'] = tema

def setear_tweet_id(id):
        tweet_content_structure['tweet_id'] = id

def get_hashtags(hashtags):
    hashtag_text = ""
    for hashtag in hashtags:
        hashtag_text = hashtag_text + hashtag['text'] + ", "
    hashtag_text = hashtag_text[:-2]
    return hashtag_text
        

class TweetModel:
    def __init__(self):        
        self.pool = PostgresSQLPool()
    
    def clasificacion_tweet(self,tweet):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(tweet) #separamos el texto del tweet por oraciones
        analizador = SentimentIntensityAnalyzer()
        negativos = []
        neutros = []
        positivos = []
        promedios = []
        scores = analizador.polarity_scores(tweet) #Analizamos el tweet completo
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
        
        return negativo, neutro, positivo, negativos, neutros, positivos, promedios, promedio, calificacion


    def search_tweet_by_topic(self, topic, user_id): #Busqueda de Tweets por tema gracias a tweeepy
        params = { 'topic' : topic,'user_id' : user_id } #El id es necesario para las auditorias
        tweets_extraidos = []
        for tweet in tweepy.Cursor(api.search, q=params['topic'], tweet_mode="extended").items(3):
            hashtag_text = get_hashtags(tweet._json['entities']['hashtags'])  #Almacenamos los hastags
            
            calificaciones = self.clasificacion_tweet(tweet._json['full_text']) #Clasificación de tweets con nltk

            agregar_datos_tweet(tweet._json['full_text'], tweet._json['user']['name'], tweet._json['user']['location'], hashtag_text)
            agregar_datos_singulares(params['user_id'], calificaciones[0], calificaciones[1], calificaciones[2])
            agregar_datos_plurales(calificaciones[3], calificaciones[4], calificaciones[5], calificaciones[6])
            agregar_clasificacion(calificaciones[7], calificaciones[8], params['topic'])
             
            query = """insert into tweets (tweet, twitter_username, twitter_user_location,hashtags, user_id, negativo, neutro, positivo, negativos, neutros, positivos, puntaje, promedios, calificacion, tema) 
             values (%(tweet)s, %(twitter_username)s, %(twitter_user_location)s, %(hashtags)s, %(user_id)s, %(negativo)s, %(neutro)s, %(positivo)s, %(negativos)s, %(neutros)s, %(positivos)s, %(puntaje)s, %(promedios)s, %(calificacion)s, %(tema)s) RETURNING tweet_id"""
            rv = self.pool.execute(query, tweet_content_structure, commit=True) #Luego realizamos la inserción del tweet ya clasificado
            id_of_new_row =  rv[0] #id recibido de la consulta al realizar la inserción

            setear_tweet_id(id_of_new_row)

            content = copy.deepcopy(tweet_content_structure)

            tweets_extraidos.append(content) #Todo esto se realiza por cada tweet obtenido de tweepy
        return tweets_extraidos

    def get_tweet(self, id):
        params = {'id' : id}    
        rv = self.pool.execute("SELECT * from tweets where tweet_id=%(id)s", params)
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
        rv = self.pool.execute("SELECT * from tweets")
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
            'tweet_id': '',
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
        rv = self.pool.execute(query, params, commit=True)
        params['tweet_id'] = rv[0]
        return params

    def delete_tweet(self, id):
        params = {'id' : id}
        query = """delete from tweets where tweet_id = %(id)s RETURNING tweet_id"""    
        rv = self.pool.execute(query, params, commit=True)

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
        rv = self.pool.execute(query, params, commit=True)
        return params

if __name__ == "__main__":    
    tm = TweetModel()