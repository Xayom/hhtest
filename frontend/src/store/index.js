import Vue from 'vue'
import Vuex from 'vuex'
import { Message } from '../api/messages'
import {
  SET_MESSAGES,
  MARK_READ
} from './mutation-types.js'

Vue.use(Vuex)

const state = {
  messages: []
}

const getters = {
  messages: state => state.messages
}

const mutations = {
  [MARK_READ] (state, message) {
    state.messages = [message, ...state.messages]
  },
  [SET_MESSAGES] (state, { messages }) {
    state.messages = messages
  }
}

const actions = {
  markRead ({ commit }, messageData) {
    Message.markread(messageData).then(message => {
      commit(MARK_READ, message)
    })
  },
  getMessages ({ commit }) {
    Message.list().then(messages => {
      commit(SET_MESSAGES, { messages })
    })
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations})
