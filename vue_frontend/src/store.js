import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        rhymes: []
    },
    mutations: {
        "socket_update"(state,data) {
            state.rhymes = data
        }
    },
    actions: {
        "socket_update"() {
            // do something
        }
    }
})