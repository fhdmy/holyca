import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueRouter from 'vue-router'
import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.darkmoon.css';

//https://github.com/dankogai/js-base64
//npm install --save js-base64

Vue.config.productionTip = false

// axios.defaults.baseURL="http://101.133.226.16:8000"
axios.defaults.baseURL="http://127.0.0.1:8000"
Vue.prototype.$http = axios

Vue.prototype.Base64 = require('js-base64').Base64;

Vue.use(VueRouter)

import Home from  "./components/Home/Home.vue"
import OwnPage from  "./components/OwnPage/OwnPage.vue"
import ActivityPage from  "./components/ActivityPage/ActivityPage.vue"

const router = new VueRouter({
  routes: [
    { path: '/',
      component: Home,
      name:"homepage",
      meta:{title:'HolyCA 首页'},
    },
    { path: '/ownpage',
      component: OwnPage,
      name:"ownpage",
      meta:{title:'HolyCA 个人中心'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
        // { path: '', component: UserHome },
      ]
    },
    { path: '/activitypage',
      component: ActivityPage,
      name:"activitypage",
      meta:{title:'HolyCA 活动中心'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
        // { path: '', component: UserHome },
      ]
    }
  ]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
