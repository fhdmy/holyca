import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueRouter from 'vue-router'
import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.darkmoon.css';

import zhMessages from "devextreme/localization/messages/zh.json";
import { locale, loadMessages } from "devextreme/localization";

loadMessages(zhMessages);
locale(navigator.language);

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
import Replay from "./components/Home/Replay.vue"
import ForumPage from "./components/ActivityPage/ForumPage.vue"
import BetPage from "./components/ActivityPage/BetPage.vue"

const router = new VueRouter({
  routes: [
    { path: '/',
      component: Home,
      name:"homepage",
      meta:{title:'HolyCA 首页'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
      ]
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
    },
    { path: '/replay', 
      component: Replay,
      name:"replay", 
      meta:{title:'HolyCA 录像'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
        // { path: '', component: UserHome },
      ]
    },
    { path: '/forum_page', 
      component: ForumPage,
      name:"forum_page", 
      meta:{title:'HolyCA 论坛'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
        // { path: '', component: UserHome },
      ]
    },
    { path: '/bet_page', 
      component: BetPage,
      name:"bet_page", 
      meta:{title:'HolyCA 积分专区'},
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /user/:id is matched
        // { path: '', component: UserHome },
      ]
    },
  ]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
