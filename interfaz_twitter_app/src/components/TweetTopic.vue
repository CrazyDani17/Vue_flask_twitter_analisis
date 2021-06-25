<script>
import SideBar from './SideBar'
export default{   
    components: {
        SideBar
    },    
    data(){ 
        return {
            fields_tweets: ['tweet', 'puntaje', 'calificacion', { key: 'twitter_username', label: 'Usuario' }, { key: 'twitter_user_location', label: 'Ubicación' }, 'hashtags'],
            tweets:[],
            newTopic:{"user_id": this.$session.get("user_id")},
            show: true,
            show_loading: false,
            dismissSecs: 5,
            dismissCountDown: 0,
            mostrar_data: false,
            showDismissibleAlert: false
        }
    },
    methods:{
        search(e){
            e.preventDefault();
            this.$http.post ("http://127.0.0.1:5000/search_by_topic", this.newTopic)
                .then(res => {
                console.log(res.body);
                if(res.body){
                    this.showAlert();
                    this.mostrar_tweets(res.body);
                    this.show_loading = false;
                }
            });
        },
        onReset(event) {
            event.preventDefault()
            // Reset our form values
            this.newTopic.topic = ''
            // Trick to reset/clear native browser form validation state
            this.show = false
            this.$nextTick(() => {
                this.show = true
            })
        },
        mostrar_tweets(rbody){
            this.tweets = rbody
            this.mostrar_data = true
        },
        countDownChanged(dismissCountDown) {
            this.dismissCountDown = dismissCountDown
        },
        showAlert() {
            this.dismissCountDown = this.dismissSecs
        }
    },
}
</script>

<template>
<div class='topics'>
    <b-img align: center src="https://cdn.discordapp.com/attachments/823595523097100348/853765066277126164/loguito_final_sinfondo.png" width="250" height="250"></b-img>
    <div align="justify">
        <SideBar/>
    </div>
    <h2>Buscar tweets por tema:</h2>

    <b-alert
      :show="dismissCountDown"
      dismissible
      variant="success"
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >
      Felicidades encontraste los siguientes tweets {{ dismissCountDown }} ...
    </b-alert>

    <ul>
        <b-table v-if="mostrar_data" striped hover :items="tweets" :fields="fields_tweets"></b-table>
    </ul>



    
    <b-overlay :show="show_loading" rounded="sm" style="max-width: 320px; position: absolute;left:38%;">
        <b-card 
        header="Ingresa un tema a buscar" :aria-hidden="show_loading ? 'true' : null" 
        border-variant="dark" 
        header-bg-variant="dark"
        header-border-variant="dark"
        header-text-variant="white"
        align="center"
        class="text-center">
            <b-form @submit='search' @reset="onReset" v-if="show">
                <b-form-input
                type='text' 
                v-model='newTopic.topic'
                placeholder='Tema'
                required
            ></b-form-input><br>
            <b-button type="submit" variant="primary" @click="show_loading = !show_loading"><b-icon icon="search" aria-hidden="true"></b-icon> Buscar</b-button>
            <b-button type="reset" variant="danger">Limpiar</b-button>
        </b-form>
        </b-card>
    </b-overlay>
  </div>
</template>