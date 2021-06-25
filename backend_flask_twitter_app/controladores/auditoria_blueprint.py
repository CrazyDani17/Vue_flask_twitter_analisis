from flask import Flask
from flask import Blueprint #Para los controlladores
from flask import request #Para obtener información recibida en el end-point
from flask import jsonify #Para retornar información del end-point a un cliente de consumo

from flask_cors import CORS, cross_origin #Para que no genere errores de CORS al hacer peticiones

from modelos.auditoria_modelo import AuditoriaModel #Importamos el modelo necesario para ingresar a la funciones 

auditoria_blueprint = Blueprint('auditoria_blueprint', __name__)

model = AuditoriaModel()

@auditoria_blueprint.route('/auditorias', methods=['POST','GET']) #Indicamos la ruta y método
@cross_origin() # new decorator
def auditorias():
    return jsonify(model.get_auditorias()) #Indicamos la función