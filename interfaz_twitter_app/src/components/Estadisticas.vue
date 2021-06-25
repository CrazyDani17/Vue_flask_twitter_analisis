<script>
import { Plotly } from 'vue-plotly'
import SideBar from './SideBar'
export default{   
    components: {
      SideBar,
      Plotly
    },
    data(){
        return {
            show_loading: false,
            selected: null,
            options: [],
            data:[{
              y: [],
              type:"box",
              name: "Negativo",
              jitter: 0.3,
              pointpos: -1.8,
              boxpoints: 'all'
            },
            {
              y: [],
              type:"box",
              name: "Neutro",
              jitter: 0.3,
              pointpos: -1.8,
              boxpoints: 'all'
            },
            {
              y: [],
              type:"box",
              name: "Positivo",
              jitter: 0.3,
              pointpos: -1.8,
              boxpoints: 'all'
            }
            ],
            layout:{
              margin: {
                  l: 40,
                  r: 30,
                  b: 80,
                  t: 100
              },
              showlegend: false,
              title: "Vista General"
            }
        }
    },
    methods: {
        filtrar(e) {
          e.preventDefault();
            this.$http.get ("http://192.168.0.120:5000/estadisticas/tema/" + this.selected)
                .then(res => { 
            this.data[0]["y"] = res.body["negativos"]
            this.data[1]["y"] = res.body["neutros"]
            this.data[2]["y"] = res.body["positivos"]
          }
        );
        }
    },
    created(){ // call when component is created
      this.$http.get ('http://192.168.0.120:5000/estadisticas/temas')
        .then(res => this.options = res.body);
      this.$http.get ('http://192.168.0.120:5000/estadisticas')
        .then(res => { 
            this.data[0]["y"] = res.body["negativos"]
            this.data[1]["y"] = res.body["neutros"]
            this.data[2]["y"] = res.body["positivos"]
          }
        );
    }
}
</script>

<template>
  <div class='estadisticas'>
    <div align="justify">
      <SideBar/>
    </div>
    <b-overlay :show="show_loading" rounded="sm" style="max-width: 320px; position: absolute;left:38%">
        <b-card 
        header="Selecciona los filtros" :aria-hidden="show_loading ? 'true' : null" 
        border-variant="dark" 
        header-bg-variant="dark"
        header-border-variant="dark"
        header-text-variant="white"
        align="center"
        class="text-center">
        <b-form @submit='filtrar'>
          <b-form-select v-model="selected" :options="options" size="sm" class="mt-3"></b-form-select>
          <b-button type="submit" variant="primary"> Filtrar </b-button>
        </b-form>
    </b-card>
  </b-overlay>
  <Plotly :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
  </div>
</template>