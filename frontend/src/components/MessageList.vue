<template lang="pug">
  #app
    .card(v-for="message in messages")
      .card-header
        button.btn.float-right(@click="markRead (message)") Прочитано
      .card-body {{ message.text }}
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'message-list',
  computed: mapGetters(['messages']),
  methods: {
    markRead (message) {
      // Вызываем действие `markRead` из нашего хранилища
      this.$store.dispatch('markRead', message)
    },
    updateStuff: function () {
      this.$store.dispatch('getMessages')
      setTimeout(this.updateStuff, 3000)
    }
  },
  beforeMount () {
    // Перед тем как загрузить страницу, нам нужно получить список всех
    // имеющихся сообщений. Для этого мы вызываем действие `getMessages` из
    // нашего хранилища
    this.updateStuff()// каждые 3 секунды возвращается текущий список непрочитанных сообщений
    this.$store.dispatch('getMessages')
  }
}
</script>

<style>
  header {
    margin-top: 50px;
  }
</style>
