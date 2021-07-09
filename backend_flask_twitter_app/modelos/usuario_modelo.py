from conexion_base_de_datos.conexion import PostgresSQLPool

class UserModel:
    def __init__(self):        
        self.cursor = PostgresSQLPool()

    def user_login(self, user_name, password):
        params = {
            'user_name' : user_name,
            'password' : password
        }
        query = """SELECT user_id from users where user_name = %(user_name)s and password = %(password)s"""
        user_id = self.cursor.execute(query, params)
        #Realizamos la verificación solo obteniendo un único dato de la consulta
        #Si en user_id está presente con los datos solicitados, entonces concede el acceso
        if user_id:
            data = {
                'user_id': user_id[0][0],
                'estado' : "True",
            }
        else: #De lo contrario lo rechaza
            data = {
                'user_id': None,
                'estado' : "False",
            }
        return data

    def get_user(self, id):
        params = {'id' : id}    
        rv = self.cursor.execute("SELECT * from users where user_id=%(id)s", params)
        data = []
        content = {}
        for result in rv:
            content = {
                'user_id': result[5], 
                'user_name': result[0], 
                'password': result[1],
                'nombre_completo' : result[2],
                'email' : result[3],
                'tipo_de_usuario' : result[4],
            }
            data.append(content)
            content = {}
        return data

    def get_users(self):
        rv = self.cursor.execute("SELECT * from users")  
        data = []
        content = {}
        for result in rv:
            content = {
                'user_id': result[5], 
                'user_name': result[0],
                'password': result[1],
                'nombre_completo' : result[2],
                'email' : result[3],
                'tipo_de_usuario' : result[4],
            }
            data.append(content)
            content = {}
        return data

    def create_user(self, user_name, password, nombre_completo, email, tipo_de_usuario):
        params = {
            'user_name' : user_name,
            'password' : password,
            'nombre_completo' : nombre_completo,
            'email' : email,
            'tipo_de_usuario' : tipo_de_usuario
        }
        query = """insert into users (user_name, password, nombre_completo, email, tipo_de_usuario) 
         values (%(user_name)s, %(password)s, %(nombre_completo)s, %(email)s, %(tipo_de_usuario)s) RETURNING user_id"""    
        rv = self.cursor.execute(query, params, commit=True)
        id_of_new_row = rv[0]

        data = {
            'user_id': id_of_new_row,
            'user_name': params['user_name'],
            'password': params['password'],
            'nombre_completo': params['nombre_completo'],
            'email': params['email'],
            'tipo_de_usuario': params['tipo_de_usuario']
        }
        return data

    def delete_user(self, id):
        params = {'id' : id}      
        query = """delete from users where user_id = %(id)s RETURNING user_id"""    
        rv = self.cursor.execute(query, params, commit=True)

        user_id = rv[0]
        if user_id:
            data = {
                'user_id': user_id,
                'eliminado' : "True",
            }
        else:
            data = {
                'user_id': id,
                'eliminado' : "False",
            }
        return data

    def update_user(self, id, user_name, password, nombre_completo, email, tipo_de_usuario):
        params = {
            'user_id' : id,
            'user_name' : user_name,
            'password' : password,
            'nombre_completo' : nombre_completo,
            'email' : email,
            'tipo_de_usuario' : tipo_de_usuario
        }
        query = """UPDATE users SET user_name = %(user_name)s, password = %(password)s, nombre_completo = %(nombre_completo)s, email = %(email)s, tipo_de_usuario = %(tipo_de_usuario)s WHERE user_id = %(user_id)s"""    
        rv = self.cursor.execute(query, params, commit=True)
        data = {
            'user_id': id,
            'user_name': params['user_name'],
            'password': params['password'],
            'nombre_completo': params['nombre_completo'],
            'email': params['email'],
            'tipo_de_usuario': params['tipo_de_usuario']
        }
        return data

if __name__ == "__main__":
    um = UserModel()