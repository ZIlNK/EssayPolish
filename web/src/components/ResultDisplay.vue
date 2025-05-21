<template>
  <div v-if="isNewShow && (isAppraise || isRewrite)" class="appraise-container">
    <div v-if="isAppraise" class="received-data-display">
      <h3>评价内容</h3>
      <div class="score-display">
        <div class="total-score">
          <h4>总分</h4>
          <p>{{ appraiseData.total_score }}</p>
        </div>
        <div class="breakdown">
          <h4>详细评分</h4>
          <div class="breakdown-item">
            <span>语法：</span>
            <span>{{ appraiseData.breakdown?.grammar }}</span>
          </div>
          <div class="breakdown-item">
            <span>结构：</span>
            <span>{{ appraiseData.breakdown?.structure }}</span>
          </div>
          <div class="breakdown-item">
            <span>内容：</span>
            <span>{{ appraiseData.breakdown?.content }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isRewrite" class="received-data-display">
      <h3>润色内容</h3>
      <div class="polish-display">
        <div class="polished-content">
          <h4>润色后的内容</h4>
          <p>{{ rewriteData.polished_content }}</p>
        </div>
        <div class="changes-made">
          <h4>修改说明</h4>
          <ul>
            <li v-for="(change, index) in rewriteData.changes_made" :key="index">
              {{ change }}
            </li>
          </ul>
        </div>
      </div>
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
    type: Object,
    default: () => ({
      total_score: '',
      breakdown: {
        grammar: '',
        structure: '',
        content: ''
      }
    })
  },
  rewriteData: {
    type: Object,
    default: () => ({
      polished_content: '',
      changes_made: []
    })
  }
})
</script>

<style scoped>
.appraise-container {
  margin-top: 30px;
}

.received-data-display {
  border: 1px solid #ccc;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.score-display {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.total-score {
  text-align: center;
  padding: 1rem;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.total-score h4 {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.total-score p {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.breakdown {
  background-color: #fff;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.breakdown h4 {
  margin: 0 0 1rem 0;
  color: #666;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.breakdown-item:last-child {
  border-bottom: none;
}

.polish-display {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.polished-content {
  background-color: #fff;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.polished-content h4 {
  margin: 0 0 1rem 0;
  color: #666;
}

.polished-content p {
  margin: 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.changes-made {
  background-color: #fff;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.changes-made h4 {
  margin: 0 0 1rem 0;
  color: #666;
}

.changes-made ul {
  margin: 0;
  padding-left: 1.5rem;
}

.changes-made li {
  margin-bottom: 0.5rem;
  color: #666;
}

.changes-made li:last-child {
  margin-bottom: 0;
}
</style> 