from conexion_base_de_datos.conexion import PostgresSQLPool #llamamos a la conexión que realizamos en postgresql

class AuditoriaModel:
    def __init__(self):        
        self.pool = PostgresSQLPool() #Inicializamos el pool de la conexión necesario para ejecutar consultas sql.

    def get_auditorias(self):
        rv = self.pool.execute("SELECT * from auditorias")
        data = []
        content = {}
        for result in rv: #Recorremos todos los elementos dentro del resultado obtenido de laa consulta
            content = {
                'auditoria_id': result[0], 
                'user_id': result[1], 
                'fecha': result[2],
                'tweet_id' : result[3],
                'accion' : result[4],
            }
            data.append(content) #Añadimos el json creado para retornarlo en conjunto desde el end-point
            content = {}
        return data

if __name__ == "__main__":
    am = AuditoriaModel()