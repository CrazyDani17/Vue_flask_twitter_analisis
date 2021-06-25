from flask import Flask
from flask_cors import CORS, cross_origin # para que no genere errores de CORS al hacer peticiones

from controladores.usuario_blueprint import user_blueprint
from controladores.tweet_blueprint import tweet_blueprint
from controladores.auditoria_blueprint import auditoria_blueprint
from controladores.estadistica_blueprint import estadistica_blueprint
    
app = Flask(__name__)

app.register_blueprint(user_blueprint)
app.register_blueprint(tweet_blueprint)
app.register_blueprint(auditoria_blueprint)
app.register_blueprint(estadistica_blueprint)

cors = CORS(app)

#Especificamos el puerto y el host donde se desplegara el API REST (Flask Backend)
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port='5000')