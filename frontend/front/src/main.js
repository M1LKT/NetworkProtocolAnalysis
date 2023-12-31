import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueAxios from 'vue-axios'
import axios from 'axios'
import request from './utils/request';
import JsonViewer from 'vue-json-viewer'

Vue.config.productionTip = false
Vue.use(ElementUI).use(VueAxios,axios).use(JsonViewer);
Vue.prototype.$request=request

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
