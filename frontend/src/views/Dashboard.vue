<template>
  <div class="dashboard">
    <h2>Stock Status</h2>
    
    <div v-if="loading" class="loading">Loading inventory...</div>
    
    <div v-else-if="stocks.length === 0" class="empty-state">
      <p>No inventory data available. Start by importing initial inventory.</p>
    </div>
    
    <div v-else class="table-container">
      <table class="stock-table">
        <thead>
          <tr>
            <th>EAN</th>
            <th>Style Name</th>
            <th>Brand</th>
            <th v-for="store in stores" :key="store">Store {{ store }}</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in stocks" :key="stock.ean">
            <td class="ean">{{ stock.ean }}</td>
            <td>{{ stock.style_name }}</td>
            <td>{{ stock.brand }}</td>
            <td v-for="store in stores" :key="store" class="qty">
              {{ stock.stores[store] || 0 }}
            </td>
            <td class="total">{{ stock.total_quantity }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { inventoryAPI } from '../api.js'

const stocks = ref([])
const stores = ref([1, 2, 3, 4])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await inventoryAPI.getStockStatus()
    stocks.value = response.data
  } catch (error) {
    console.error('Failed to load stock status:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.dashboard h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.table-container {
  overflow-x: auto;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.stock-table thead {
  background: #34495e;
  color: white;
}

.stock-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
}

.stock-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.stock-table tbody tr:hover {
  background: #f8f9fa;
}

.ean {
  font-family: monospace;
  font-size: 0.85rem;
  color: #7f8c8d;
}

.qty {
  text-align: center;
  font-weight: 500;
}

.total {
  font-weight: 600;
  background: #ecf0f1;
  text-align: center;
}
</style>
