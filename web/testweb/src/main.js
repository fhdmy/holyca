import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.productionTip = false

axios.defaults.baseURL="http://127.0.0.1:8000"
Vue.prototype.$http = axios

Vue.prototype.Base64 = require('js-base64').Base64;

new Vue({
  render: h => h(App)
}).$mount('#app')

