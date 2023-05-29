import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@mdi/font/css/materialdesignicons.css'

import { VDataTableServer, VDataTable } from 'vuetify/labs/VDataTable'

const vuetify = createVuetify({
  components: {
    ...components,
    VDataTableServer,
    VDataTable,
  },
  directives,
})

export default vuetify;