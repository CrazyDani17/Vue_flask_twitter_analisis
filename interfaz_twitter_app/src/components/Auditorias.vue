<script>
//Se importa el Menu desplegable
import SideBar from './SideBar'
export default{   
    components: {
        SideBar
    },   
    data(){ 
        return {//la data la podemos utilizar luego ateponiendo al nombre "this."
            //Estas son todas las columnas que tendrá la tabla
            fields: ['auditoria_id', 'accion', 'fecha', 'tweet_id','user_id'],
            auditorias:[],
        }
    },
    created(){ // Este método es llamado cuando este es creado, por ello llamamos a  toda la data inicial
		this.$http.get ('http://192.168.0.120:5000/auditorias') //llamamos al end-point por el método get
		.then(res => this.auditorias = res.body);
	}
}
</script>

<template>
<div class='auditorias'>
<!--- Llamamos al componente SideBar para el Menú lateral desplegable --->
<div align="justify">
<SideBar/>
</div>
<!--- La imagen del logo --->
<b-img align: center src="https://cdn.discordapp.com/attachments/823595523097100348/853765066277126164/loguito_final_sinfondo.png" width="250" height="250"></b-img>
<ul>
<!--- Tabla que presenta todos los elementos (auditorias) de la base de datos --->
<b-table responsive striped hover :items="auditorias" :fields="fields">
</b-table>
</ul>
</div>
</template>