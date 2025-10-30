<template>
  <div class="analytics">
    <h2>Sales Analytics</h2>
    
    <div class="filters">
      <div class="filter-group">
        <label>Store</label>
        <select v-model="selectedStore">
          <option value="">All Stores</option>
          <option v-for="store in stores" :key="store" :value="store">
            Store {{ store }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Start Date</label>
        <input v-model="startDate" type="date" />
      </div>
      
      <div class="filter-group">
        <label>End Date</label>
        <input v-model="endDate" type="date" />
      </div>
      
      <button @click="loadAnalytics" class="filter-btn">Apply Filters</button>
    </div>
    
    <div v-if="loading" class="loading">Loading analytics...</div>
    
    <div v-else class="analytics-grid">
      <div class="analytics-section">
        <h3>Most Moving Items</h3>
        <div v-if="analytics.most_moving.length === 0" class="empty">
          No data available
        </div>
        <div v-else class="items-list">
          <div v-for="(item, idx) in analytics.most_moving" :key="idx" class="item">
            <div class="item-header">
              <span class="rank">{{ idx + 1 }}</span>
              <div class="item-info">
                <p class="ean">{{ item.ean }}</p>
                <p class="name">{{ item.style_name }} - {{ item.brand }}</p>
              </div>
            </div>
            <p class="movement">{{ item.movement }} units</p>
          </div>
        </div>
      </div>
      
      <div class="analytics-section">
        <h3>Least Moving Items</h3>
        <div v-if="analytics.least_moving.length === 0" class="empty">
          No data available
        </div>
        <div v-else class="items-list">
          <div v-for="(item, idx) in analytics.least_moving" :key="idx" class="item">
            <div class="item-header">
              <span class="rank">{{ idx + 1 }}</span>
              <div class="item-info">
                <p class="ean">{{ item.ean }}</p>
                <p class="name">{{ item.style_name }} - {{ item.brand }}</p>
              </div>
            </div>
            <p class="movement">{{ item.movement }} units</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { inventoryAPI } from '../api.js'

const analytics = ref({ most_moving: [], least_moving: [] })
const stores = ref([1, 2, 3, 4])
const selectedStore = ref('')
const startDate = ref('')
const endDate = ref('')
const loading = ref(false)

const loadAnalytics = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedStore.value) params.store_id = selectedStore.value
    if (startDate.value) params.start_date = startDate.value
    if (endDate.value) params.end_date = endDate.value
    
    const response = await inventoryAPI.getAnalytics(params)
    analytics.value = response.data
  } catch (error) {
    console.error('Failed to load analytics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAnalytics()
})
</script>

<style scoped>
.analytics {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.analytics h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
}

.filter-group select,
.filter-group input {
  padding: 0.5rem;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 0.9rem;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.filter-btn:hover {
  background: #2980b9;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.analytics-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.1rem;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
  background: #f8f9fa;
  border-radius: 4px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #3498db;
}

.item-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: #3498db;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
}

.ean {
  font-family: monospace;
  font-size: 0.85rem;
  color: #7f8c8d;
  margin: 0;
}

.name {
  margin: 0.25rem 0 0 0;
  color: #2c3e50;
  font-weight: 500;
}

.movement {
  margin: 0;
  color: #27ae60;
  font-weight: 600;
}

@media (max-width: 768px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-group {
    width: 100%;
  }
}
</style>
