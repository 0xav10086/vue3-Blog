import { createApp } from 'vue'
import './style.css' // 导入全局样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './assets/less/index.less'
import VueKinesis from "vue-kinesis";
import Particles from "particles.vue3"
import './assets/global.css';

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.use(VueKinesis)
app.use(Particles)
app.mount('#app')
