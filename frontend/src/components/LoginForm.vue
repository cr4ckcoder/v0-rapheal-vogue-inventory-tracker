<template>
  <div class="login-form">
    <div class="form-card">
      <h2>Rapheal Vogue</h2>
      <p class="subtitle">Event Inventory Tracker</p>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            id="username"
            v-model="username" 
            type="text" 
            placeholder="Enter username"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Enter password"
            required
          />
        </div>
        
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authAPI } from '../api.js'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const emit = defineEmits(['login'])

const handleSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const response = await authAPI.login(username.value, password.value)
    emit('login', response.data.access_token)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-form {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
}

.form-card h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #2980b9;
}

.submit-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #ffe6e6;
  color: #c0392b;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
}
</style>
