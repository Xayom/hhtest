/* eslint-disable */
import { HTTP } from './common'

export const Message = {
  markread (message) {
    message.seen = "true"
    return HTTP.put(`/get_messages/${message.id}/`, message).then(response => {
      response.data
    })
  },
  list () {
    return HTTP.get('/get_messages/').then(response => {
      return response.data
    })
  }
}

