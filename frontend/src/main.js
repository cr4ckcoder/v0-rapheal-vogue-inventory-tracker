import { createApp } from "vue"
import App from "./App.vue"
import { createStore } from "./store.js"

const app = createApp(App)
const store = createStore()

app.provide('store', store)
app.mount("#app")
