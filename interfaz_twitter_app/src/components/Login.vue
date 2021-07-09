<script>
export default {
    data(){ 
        return {
            user:{}
        }
    },
    methods: {
        login(e) {
          e.preventDefault();
            this.$http.post ("http://192.168.0.120:5000/user/login", this.user)
                .then(res => {
                console.log(res.body);
                if(res.body.estado=="True"){
                    this.$session.start()
                    this.$session.set('user_id', res.body.user_id)
                    this.$session.set('username', this.user['user_name'])
                    this.$router.push('/')
                }
            });
        }

    }
}
</script>

<template>
<div class='login'>

    <b-card
        title="Login"
        img-src="https://cdn.discordapp.com/attachments/823595523097100348/854796291003383808/loguito_horizontal.png"
        img-alt="Image"
        img-top
        tag="article"
        style="max-width: 20rem; position: absolute;
        margin-top: 30px;
        margin-left: auto;
        margin-right: auto;
        left: 0;
        right: 0;"
        class="mb-2"
        align="center"
    >
        <b-form @submit='login'>
            <b-form-input
                type='text'
                v-model='user.user_name'
                placeholder='Nombre de usuario'
                required
            ></b-form-input><br>

            <b-form-input
            type='password'
            v-model='user.password' 
            placeholder='Contraseña'
            required
            ></b-form-input><br>

        <b-button type="submit" variant="primary"> Ingresar </b-button>
        </b-form>
    </b-card>
  </div>
</template>
