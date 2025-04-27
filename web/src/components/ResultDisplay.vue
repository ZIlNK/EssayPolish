<template>
  <div v-if="isNewShow && (isAppraise || isRewrite)" class="appraise-container">
    <div v-if="isAppraise" class="received-data-display">
      <h3>评价内容</h3>
      <pre>{{ appraiseData }}</pre>
    </div>
    <div v-if="isRewrite" class="received-data-display">
      <h3>润色内容</h3>
      <pre>{{ rewriteData }}</pre>
    </div>
  </div>
</template>

<script setup>
defineProps({
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
  },
  appraiseData: {
    type: String,
    default: ''
  },
  rewriteData: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.appraise-container {
  margin-top: 30px;
}

.received-data-display {
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
}
</style> 