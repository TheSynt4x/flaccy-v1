import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@mdi/font/css/materialdesignicons.css'

import { VDataTableServer } from 'vuetify/labs/VDataTable'

const vuetify = createVuetify({
  components: {
    ...components,
    VDataTableServer
  },
  directives,
})

export default vuetify;