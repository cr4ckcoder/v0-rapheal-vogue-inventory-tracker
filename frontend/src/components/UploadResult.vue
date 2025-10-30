<template>
  <div :class="['result-container', result.status]">
    <div class="result-header">
      <h3>Upload Summary</h3>
      <p :class="['status-badge', result.status]">
        {{ result.status === 'success' ? '✓ Success' : '⚠ Partial' }}
      </p>
    </div>
    
    <div class="result-stats">
      <div class="stat">
        <span class="label">Successful</span>
        <span class="value success">{{ result.success_count }}</span>
      </div>
      <div class="stat">
        <span class="label">Errors</span>
        <span class="value error">{{ result.error_count }}</span>
      </div>
    </div>
    
    <div v-if="result.errors.length > 0" class="errors-section">
      <h4>Errors</h4>
      <div class="errors-list">
        <div v-for="(err, idx) in result.errors.slice(0, 10)" :key="idx" class="error-item">
          <span v-if="err.row" class="row-num">Row {{ err.row }}:</span>
          <span class="error-text">{{ err.error }}</span>
        </div>
        <div v-if="result.errors.length > 10" class="more-errors">
          ... and {{ result.errors.length - 10 }} more errors
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.result-container {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.result-container.success {
  background: #d5f4e6;
  border-color: #27ae60;
}

.result-container.partial {
  background: #fff3cd;
  border-color: #f39c12;
}

.result-container.error {
  background: #ffe6e6;
  border-color: #e74c3c;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-header h3 {
  margin: 0;
  color: #2c3e50;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.success {
  background: #27ae60;
  color: white;
}

.status-badge.partial {
  background: #f39c12;
  color: white;
}

.status-badge.error {
  background: #e74c3c;
  color: white;
}

.result-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat .label {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.stat .value {
  font-size: 1.5rem;
  font-weight: 700;
}

.value.success {
  color: #27ae60;
}

.value.error {
  color: #e74c3c;
}

.errors-section {
  margin-top: 1rem;
}

.errors-section h4 {
  margin: 0 0 0.75rem 0;
  color: #2c3e50;
  font-size: 0.95rem;
}

.errors-list {
  background: rgba(0,0,0,0.05);
  padding: 1rem;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.error-item {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.error-item:last-child {
  margin-bottom: 0;
}

.row-num {
  font-weight: 600;
  color: #e74c3c;
}

.error-text {
  margin-left: 0.5rem;
}

.more-errors {
  font-size: 0.85rem;
  color: #7f8c8d;
  font-style: italic;
  margin-top: 0.5rem;
}
</style>
