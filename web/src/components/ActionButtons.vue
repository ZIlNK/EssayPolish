<template>
  <div class="action-buttons">
    <button
      class="action-button submit-button"
      :disabled="!isFormValid"
      @click="$emit('submit')"
    >
      提交
    </button>
    <button
      class="action-button reset-button"
      @click="$emit('reset')"
    >
      重置
    </button>
    <div v-if="isNewShow" class="mode-buttons">
      <button
        class="action-button mode-button"
        :class="{ active: isAppraise }"
        @click="$emit('switch', 'appraise')"
      >
        评价
      </button>
      <button
        class="action-button mode-button"
        :class="{ active: isRewrite }"
        @click="$emit('switch', 'rewrite')"
      >
        润色
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isFormValid: {
    type: Boolean,
    required: true
  },
  isNewShow: {
    type: Boolean,
    default: false
  },
  isAppraise: {
    type: Boolean,
    default: false
  },
  isRewrite: {
    type: Boolean,
    default: false
  }
});

defineEmits(['submit', 'reset', 'switch']);
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
  flex-wrap: wrap;
}

.action-button {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
}

.action-button:hover:not(:disabled) {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-button {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.submit-button:hover:not(:disabled) {
  background-color: var(--color-primary-light);
}

.reset-button:hover {
  background-color: var(--color-error);
  color: var(--color-text-light);
}

.mode-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.mode-button.active {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .mode-buttons {
    width: 100%;
  }

  .mode-button {
    flex: 1;
  }
}
</style> 