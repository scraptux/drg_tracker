import { createApp } from 'vue'
import App from './App.vue'

import router from './router.js'
import './index.css'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/*import 'bootstrap/dist/css/bootstrap.css'*/
import 'nouislider/dist/nouislider.min.css'

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)
app.config.globalProperties.$baseURL = window.location.protocol+'//'+window.location.hostname+':'+8000

app.use(router)
app.mount('#app')
