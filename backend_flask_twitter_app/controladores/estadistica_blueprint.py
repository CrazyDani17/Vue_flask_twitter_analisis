from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify

from flask_cors import CORS, cross_origin # para que no genere errores de CORS al hacer peticiones

from modelos.estadistica_modelo import EstadisticaModel

estadistica_blueprint = Blueprint('estadistica_blueprint', __name__)

model = EstadisticaModel()

@estadistica_blueprint.route('/estadisticas', methods=['POST','GET'])
@cross_origin() # new decorator
def estadisticas():
    return jsonify(model.get_estadistica_general())

@estadistica_blueprint.route('/estadisticas/tema/<topic>', methods=['POST','GET'])
@cross_origin() # new decorator
def estadisticas_tema(topic):
    return jsonify(model.get_estadistica_por_tema(str(topic)))

@estadistica_blueprint.route('/estadisticas/temas', methods=['POST','GET'])
@cross_origin() # new decorator
def estadisticas_temas():
    return jsonify(model.get_temas())