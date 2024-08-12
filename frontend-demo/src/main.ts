import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

const app = createApp(App)
const pinia = createPinia();
pinia.use(piniaPersist)

app.use(pinia)
app.use(router).use(Antd)

app.mount('#app')
