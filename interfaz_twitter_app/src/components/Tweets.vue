<script>
import SideBar from './SideBar'
export default{   
    components: {
        SideBar
    },    
    data(){ 
        return {
            fields: ['tweet', 'puntaje', 'calificacion', { key: 'twitter_username', label: 'Usuario' }, { key: 'twitter_user_location', label: 'Ubicación' }, 'hashtags', { key: 'actions', label: 'Acciones' }],
            tweets:[],
            newTweet:{}
        }
    },
    methods:{
        addTweet(e){
            e.preventDefault();
            this.tweets.push(this.newTweet);
            this.newTweet = {};
        },
        deleteTweet(tweet){
            this.tweets.splice(this.tweets.indexOf(tweet),1);
            this.$http.post ("http://192.168.0.120:5000/delete_tweet/"+ tweet["tweet_id"])
                .then(res => {
                console.log(res.body);
            });
        }
    },
    created(){ // call when component is created
		this.$http.get ('http://192.168.0.120:5000/tweets')
		.then(res => this.tweets = res.body);
	}
}
</script>

<template>
<div class='tweets' align="justify">
<div align="justify">
    <SideBar/>
</div>
<b-img align: center src="https://cdn.discordapp.com/attachments/823595523097100348/853765066277126164/loguito_final_sinfondo.png" width="250" height="250"></b-img>
<b-navbar type="light" variant="light">
    <b-navbar-nav class="ml-auto">
        <b-button pill variant="outline-primary" router-link to="historial"> Historial </b-button>
</b-navbar-nav>
</b-navbar>
<ul>
<b-table responsive striped hover :items="tweets" :fields="fields">
    <template #cell(actions)="tweet">
        <div>
        <b-button-group>
        <b-button variant="outline-primary">
            <b-icon icon="pencil-square" aria-hidden="true"></b-icon>
        </b-button>
        <b-button variant="outline-danger" @click="deleteTweet(tweet.item)">
            <b-icon icon="trash-fill" aria-hidden="true"></b-icon>
        </b-button>
        </b-button-group>
    </div>
    </template>
</b-table>
</ul>
</div>
</template>