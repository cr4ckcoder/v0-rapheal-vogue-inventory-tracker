import { reactive } from "vue"

export function createStore() {
  const state = reactive({
    token: localStorage.getItem("token") || null,
    user: localStorage.getItem("user") || null,
    currentPage: "dashboard",
  })

  const setToken = (token) => {
    state.token = token
    localStorage.setItem("token", token)
  }

  const setUser = (user) => {
    state.user = user
    localStorage.setItem("user", user)
  }

  const logout = () => {
    state.token = null
    state.user = null
    localStorage.removeItem("token")
    localStorage.removeItem("user")
  }

  const setPage = (page) => {
    state.currentPage = page
  }

  return {
    state,
    setToken,
    setUser,
    logout,
    setPage,
  }
}
