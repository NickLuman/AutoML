import 'bootstrap/dist/css/bootstrap.css'
import axios from 'axios'
import Vue from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'
axios.defaults.headers = { 'Access-Control-Allow-Origin': 'http://localhost:8000/', 'Content-Type': 'application/json' }

Vue.config.productionTip = false
Vue.prototype.$log = console.log


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
