<template>
  <div class="hello">
    <div align="justify">
      <SideBar/>
      <b-img align: center src="https://cdn.discordapp.com/attachments/823595523097100348/853765066277126164/loguito_final_sinfondo.png" width="250" height="250"></b-img>
    </div>
    <h1>{{ msg }}</h1>
    <h4>Ingresa al menú principal</h4>
  </div>
</template>

<script>
import SideBar from './SideBar'
export default {
  name: 'HelloWorld',
  components: {
    SideBar
  },
  data () {
    return {
      msg: 'Bienvenido'
    }
  },
  created(){
    if(this.$session.exists() == false){
      this.$router.push('/user/login')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h4 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
