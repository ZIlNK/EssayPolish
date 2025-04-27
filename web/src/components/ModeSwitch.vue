<template>
  <div class="mode-switch">
    <button
      class="switch-button"
      :class="{ active: !isImageMode }"
      @click="$emit('switch', false)"
    >
      <i class="fas fa-font"></i>
      <span>文本模式</span>
    </button>
    <button
      class="switch-button"
      :class="{ active: isImageMode }"
      @click="$emit('switch', true)"
    >
      <i class="fas fa-image"></i>
      <span>图片模式</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  isImageMode: {
    type: Boolean,
    required: true
  }
});

defineEmits(['switch']);
</script>

<style scoped>
.mode-switch {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
  background-color: var(--color-bg-secondary);
  padding: var(--spacing-xs);
  border-radius: var(--radius-full);
}

.switch-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: var(--radius-full);
}

.switch-button:hover {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.switch-button.active {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.switch-button i {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .mode-switch {
    margin-bottom: var(--spacing-lg);
  }
  
  .switch-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 0.875rem;
  }
}
</style> 