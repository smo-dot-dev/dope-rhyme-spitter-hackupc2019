import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import store from './store'
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
  debug: true,
  connection: 'https://0886a3a6.ngrok.io',
  // connection: 'http://localhost:3000',
  vuex: {
    store,
    actionPrefix: 'socket_',
    mutationPrefix: 'socket_'
  }
}))

import {
  ToggleButton
} from 'vue-js-toggle-button'

Vue.component('ToggleButton', ToggleButton)

new Vue({
  render: h => h(App),
  store
}).$mount('#app')