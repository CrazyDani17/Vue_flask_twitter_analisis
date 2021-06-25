from conexion_base_de_datos.conexion import conn

class EstadisticaModel:
    def __init__(self):
        self.cursor = conn.cursor()

    def get_temas(self):
        self.cursor.execute("SELECT tema from tweets")  
        rv = self.cursor.fetchall()
        content = {}
        temas = []
        data = [{
                    'value' : None,
                    'text' : 'Por favor selecciona un tema',
                }] #Para fijar el primer valor por defecto del select
        for result in rv:
            if result[0] not in temas and result[0] != None: #Filtramos para que no se repita el tema
                temas.append(result[0])
                content = {
                    'value' : result[0],
                    'text' : result[0]
                }
                data.append(content)
        return data
    def get_estadistica_general(self): #Para obtener los puntos a graficar en el boxplot inicial (general)
        self.cursor.execute("SELECT negativos, neutros, positivos from tweets")
        rv = self.cursor.fetchall()
        content = {}
        negativos = []
        neutros = []
        positivos = []
        for result in rv: #Se aplican estos filtros por si los puntos negativos son 0 o nulos para que no
                          # no se vean reflejados en el gráfico estadístico
            if result[0] != None:
                for negativo in result[0]:
                    if negativo > 0:
                        negativos.append(negativo)
            if result[1] != None:
                for neutro in result [1]:
                    if neutro > 0:
                        neutros.append(neutro)
            if result[2] != None:
                for positivo in result [2]:
                    if positivo > 0:
                        positivos.append(positivo)
        content = {
                'negativos' : negativos,
                'neutros' : neutros,
                'positivos' : positivos
            }
        return content
    
    def get_estadistica_por_tema(self, tema): #Obtener puntos del boxplot con filtro por tema
        params = {'tema' : tema}
        self.cursor.execute("""SELECT negativos, neutros, positivos from tweets where tema=%(tema)s""", params)
        rv = self.cursor.fetchall()
        content = {}
        negativos = []
        neutros = []
        positivos = []
        for result in rv:
            if result[0] != None:
                for negativo in result[0]:
                    if negativo > 0:
                        negativos.append(negativo)
            if result[1] != None:
                for neutro in result [1]:
                    if neutro > 0:
                        neutros.append(neutro)
            if result[2] != None:
                for positivo in result [2]:
                    if positivo > 0:
                        positivos.append(positivo)
        content = {
                'negativos' : negativos,
                'neutros' : neutros,
                'positivos' : positivos
            }
        return content

if __name__ == "__main__":    
    em = EstadisticaModel()