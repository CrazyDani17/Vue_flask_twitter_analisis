<template>
  <div>
    <b-button v-if="show_button" pill variant="outline-primary" style="position: absolute;left:3%;top: 5%;" v-b-toggle.sidebar-variant>Menú</b-button>
    <b-dropdown  right v-if="show_button" pill variant="outline-primary" style="position: absolute;left:88%;top: 5%;">
        <template #button-content>
            <b-icon icon="file-person" aria-hidden="true"></b-icon> {{ msg }}
        </template>
        <b-dropdown-item-button>
            <b-icon icon="pencil-square" aria-hidden="true"></b-icon>
            Mi perfil
        </b-dropdown-item-button>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item-button variant="danger" @click="logout">
            <b-icon icon="trash-fill" aria-hidden="true"></b-icon>
            Cerrar sesión
        </b-dropdown-item-button>
    </b-dropdown>
    <b-sidebar id="sidebar-variant" title="Menú" bg-variant="light" text-variant="blue" backdrop shadow width="auto">
      <template #default="{ hide }">
      <div class="px-3 py-2">
        <nav class="mb-3">
            <b-nav vertical>
              <b-nav-item router-link to="/" @click="hide">
                <b-icon icon="house" aria-hidden="true"></b-icon> Inicio
              </b-nav-item>
              <b-nav-item router-link to="administrar_usuarios" @click="hide">
                <b-icon icon="file-person" aria-hidden="true"></b-icon> Administrar Usuarios
              </b-nav-item>
              <b-nav-item router-link to="tweets" @click="hide">
                <b-icon icon="twitter" aria-hidden="true"></b-icon> Tweets
              </b-nav-item>
              <b-nav-item router-link to="buscar_tweets" @click="hide">
                <b-icon icon="search" aria-hidden="true"></b-icon> Búsqueda de tweets
              </b-nav-item>
              <b-nav-item router-link to="estadisticas" @click="hide">
                <b-icon icon="graph-up" aria-hidden="true"></b-icon> Revisar estadísticas
              </b-nav-item>
            </b-nav>
          </nav>
        <b-img src="https://cdn.discordapp.com/attachments/823595523097100348/850257330041257984/laptweet.png" fluid thumbnail width="200%"></b-img>
      </div>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  data () {
    return {
      msg: this.$session.get("username"),
      show_button: true
    }
  },
  methods: {
    logout() {
      this.$session.destroy()
      this.$router.push('/user/login')
      this.show_button = false
    },
  },
  created(){
      this.msg = this.$session.get("username"),
      this.show_button = true
  }
}
</script>

