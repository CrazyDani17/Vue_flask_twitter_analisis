<script>
//Se importa el Menu desplegable
import SideBar from './SideBar'
export default{   
    components: {
        SideBar
    },
    data(){ //la data la podemos utilizar luego ateponiendo al nombre "this."
        return {
            //Estas son todas las columnas que tendrá la tabla
            fields: ['user_name', 'nombre_completo', 'email', 'tipo_de_usuario',{ key: 'actions', label: 'Acciones' }],
            users:[],
        }
    },
    methods:{
        deleteUser(user){
            //Los console log son simplemente para imprimir valores en la consola del navegador
            console.log("eliminando");
            //Splice es necesario para eliminarlo de la tabla dimámica de vue
            this.users.splice(this.users.indexOf(user),1);
            //llama al end-point para la eliminación del usuario desde el backend
            this.$http.post ("http://192.168.0.120/delete_user/"+ user["user_id"])
                .then(res => {
                console.log(res.body);
            });
        }
    },
    created(){ // Este método es llamado cuando este es creado, por ello llamamos a  toda la data inicial
		this.$http.get ('http://192.168.0.120:5000/users') //llamamos al end-point por el método get
		.then(res => this.users = res.body);
	}
}
</script>

<template>
<div class='users'>
<!--- Llamamos al componente SideBar para el Menú lateral desplegable --->
<div align="justify">
<SideBar/>
</div>
<!--- La imagen del logo --->
<b-img align: center src="https://cdn.discordapp.com/attachments/823595523097100348/853765066277126164/loguito_final_sinfondo.png" width="250" height="250"></b-img>
<!--- Botón para dirigirte al fomulario agregar nuevo usuario --->
<b-button pill variant="outline-primary" style="position: absolute;left:87%;top: 35%;" router-link to="crear_usuario">Añadir Usuario</b-button>    
<ul>
<!--- Tabla que presenta todos los elementos (usuarios) de la base de datos --->
<b-table striped hover :items="users" :fields="fields">
    <!--- Por cada fila de usuario --->
    <template #cell(actions)="user">
        <div>
        <!--- Añadimos los botones de editar y eliminar --->
        <b-button-group>
        <b-button variant="outline-primary">
            <b-icon icon="pencil-square" aria-hidden="true"></b-icon>
        </b-button>
        <b-button variant="outline-danger" @click="deleteUser(user.item)">
            <b-icon icon="trash-fill" aria-hidden="true"></b-icon>
        </b-button>   
        </b-button-group>
    </div>
    </template>
</b-table>

</ul>
</div>
</template>