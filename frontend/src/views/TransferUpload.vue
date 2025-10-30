<template>
  <div class="upload-container">
    <h2>Transfer Inventory Between Stores</h2>
    <p class="description">Upload a CSV file to transfer stock between stores</p>
    
    <div class="upload-section">
      <div class="upload-box" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
        <input 
          ref="fileInput"
          type="file" 
          accept=".csv" 
          @change="handleFileSelect"
          style="display: none"
        />
        <div class="upload-content">
          <div class="upload-icon">🔄</div>
          <p>Click to upload or drag and drop</p>
          <p class="file-hint">CSV file (ean, source_store_id, destination_store_id, quantity)</p>
        </div>
      </div>
      
      <button 
        v-if="selectedFile" 
        @click="handleUpload" 
        class="upload-btn"
        :disabled="uploading"
      >
        {{ uploading ? 'Uploading...' : 'Transfer' }}
      </button>
    </div>
    
    <div v-if="selectedFile" class="file-info">
      <p><strong>Selected file:</strong> {{ selectedFile.name }}</p>
    </div>
    
    <UploadResult v-if="result" :result="result" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { inventoryAPI } from '../api.js'
import UploadResult from '../components/UploadResult.vue'

const fileInput = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const result = ref(null)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0]
  result.value = null
}

const handleDrop = (event) => {
  const files = event.dataTransfer.files
  if (files.length > 0) {
    selectedFile.value = files[0]
    result.value = null
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  try {
    const response = await inventoryAPI.transferInventory(selectedFile.value)
    result.value = response.data
  } catch (error) {
    result.value = {
      success_count: 0,
      error_count: 1,
      errors: [{ error: error.response?.data?.detail || 'Upload failed' }],
      status: 'error'
    }
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.upload-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.upload-container h2 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.description {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.upload-section {
  margin-bottom: 2rem;
}

.upload-box {
  border: 2px dashed #f39c12;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8f9fa;
}

.upload-box:hover {
  border-color: #e67e22;
  background: #ecf0f1;
}

.upload-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.upload-box p {
  margin: 0.5rem 0;
  color: #2c3e50;
}

.file-hint {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-top: 0.5rem;
}

.upload-btn {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  background: #f39c12;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.2s;
}

.upload-btn:hover:not(:disabled) {
  background: #e67e22;
}

.upload-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.file-info {
  padding: 1rem;
  background: #ecf0f1;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
</style>
