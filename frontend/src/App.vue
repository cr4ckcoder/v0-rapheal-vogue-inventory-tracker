<template>
  <div class="app-container">
    <div v-if="!store.state.token" class="login-page">
      <LoginForm @login="handleLogin" />
    </div>
    <div v-else class="main-layout">
      <header class="header">
        <div class="header-content">
          <h1>Rapheal Vogue Inventory Tracker</h1>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </header>
      
      <nav class="nav">
        <button 
          v-for="page in pages" 
          :key="page.id"
          @click="store.setPage(page.id)"
          :class="['nav-btn', { active: store.state.currentPage === page.id }]"
        >
          {{ page.label }}
        </button>
      </nav>
      
      <main class="content">
        <Dashboard v-if="store.state.currentPage === 'dashboard'" />
        <ImportUpload v-else-if="store.state.currentPage === 'import'" />
        <TransferUpload v-else-if="store.state.currentPage === 'transfer'" />
        <SalesUpload v-else-if="store.state.currentPage === 'sales'" />
        <Analytics v-else-if="store.state.currentPage === 'analytics'" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'
import LoginForm from './components/LoginForm.vue'
import Dashboard from './views/Dashboard.vue'
import ImportUpload from './views/ImportUpload.vue'
import TransferUpload from './views/TransferUpload.vue'
import SalesUpload from './views/SalesUpload.vue'
import Analytics from './views/Analytics.vue'

const store = inject('store')

const pages = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'import', label: 'Import Inventory' },
  { id: 'transfer', label: 'Transfer Stock' },
  { id: 'sales', label: 'Record Sales' },
  { id: 'analytics', label: 'Analytics' }
]

const handleLogin = (token) => {
  store.setToken(token)
}

const handleLogout = () => {
  store.logout()
  store.setPage('dashboard')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background: #2c3e50;
  color: white;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 1.8rem;
  font-weight: 600;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #c0392b;
}

.nav {
  background: #34495e;
  display: flex;
  gap: 0;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-btn {
  flex: 1;
  padding: 1rem;
  background: none;
  border: none;
  color: #ecf0f1;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
}

.nav-btn:hover {
  background: rgba(255,255,255,0.1);
}

.nav-btn.active {
  background: #2c3e50;
  border-bottom-color: #3498db;
  color: #3498db;
}

.content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
}

@media (max-width: 768px) {
  .nav {
    flex-wrap: wrap;
  }
  
  .nav-btn {
    flex: 0 1 50%;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header h1 {
    font-size: 1.4rem;
  }
}
</style>
