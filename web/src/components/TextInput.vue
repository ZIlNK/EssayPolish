<template>
  <div class="input-section">
    <div v-if="!isNewShow">
      <textarea
        v-model="inputText"
        placeholder="请输入文字内容..."
        class="text-input"
        @input="adjustTextareaHeight"
        @keydown="handleKeyDown"
        ref="textareaRef"
      ></textarea>
      <div class="button-group">
        <button @click="handlePolish" class="action-button">润色</button>
        <button @click="handleAssessment" class="action-button">评价</button>
      </div>
      <div class="char-counter">{{ inputText.length }}</div>
    </div>
    <!-- 新的展示页面 -->
    <div v-if="isNewShow" class="new-display-container">
      <div class="original-data-display">
        <h3>原始文本</h3>
        <textarea
          v-model="inputText"
          class="new-text-input"
          readonly
        ></textarea>
      </div>
      <div class="received-data-display">
        <h3>处理结果</h3>
        <pre>{{ responseText }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  isNewShow: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:responseText'])

const inputText = ref('')
const textareaRef = ref(null)
const responseText = ref('')

const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
  }
}

const processText = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本内容')
    return
  }

  // 添加输入验证
  if (inputText.value.trim().length < 10) {
    ElMessage.warning('请输入至少10个字符的文本内容')
    return
  }

  // 检查是否只包含数字
  if (/^\d+$/.test(inputText.value.trim())) {
    ElMessage.warning('请输入有意义的文本内容，不能只包含数字')
    return
  }

  try {
    // 提交阶段 - 进行文本纠错
    const correctionResponse = await axios.post('http://localhost:5000/api/correction', {
      content: inputText.value,
      method: 0
    })
    
    if (correctionResponse.data.data) {
      // 获取纠错建议
      const suggestions = correctionResponse.data.data.suggestions
      if (suggestions.length > 0) {
        // 应用纠错建议
        let correctedText = inputText.value
        suggestions.forEach(suggestion => {
          // 检查建议是否合理
          if (suggestion.error_type === 'spelling' && 
              suggestion.original.length === 1 && 
              /^\d+$/.test(suggestion.original)) {
            // 如果是单个数字，不应用建议
            return
          }
          correctedText = correctedText.substring(0, suggestion.position[0]) + 
                         suggestion.recommended + 
                         correctedText.substring(suggestion.position[1])
        })
        inputText.value = correctedText
      }
      
      // 确认纠错
      await axios.get('http://localhost:5000/api/correctionComfirm')
      
      responseText.value = inputText.value
      emit('update:responseText', responseText.value)
      ElMessage.success('文本处理成功')
    } else {
      ElMessage.error('文本处理失败')
    }
  } catch (error) {
    console.error('Error processing text:', error)
    ElMessage.error('处理失败，请重试')
  }
}

const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    processText()
  }
}

const handlePolish = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本内容')
    return
  }

  if (inputText.value.trim().length < 10) {
    ElMessage.warning('请输入至少10个字符的文本内容')
    return
  }

  if (/^\d+$/.test(inputText.value.trim())) {
    ElMessage.warning('请输入有意义的文本内容，不能只包含数字')
    return
  }

  try {
    // TODO: 等待后端实现
    ElMessage.info('润色功能正在开发中')
  } catch (error) {
    console.error('Error in polish:', error)
    ElMessage.error('处理失败，请重试')
  }
}

const handleAssessment = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本内容')
    return
  }

  if (inputText.value.trim().length < 10) {
    ElMessage.warning('请输入至少10个字符的文本内容')
    return
  }

  if (/^\d+$/.test(inputText.value.trim())) {
    ElMessage.warning('请输入有意义的文本内容，不能只包含数字')
    return
  }

  try {
    // TODO: 等待后端实现
    ElMessage.info('评价功能正在开发中')
  } catch (error) {
    console.error('Error in assessment:', error)
    ElMessage.error('处理失败，请重试')
  }
}

const clearInput = () => {
  inputText.value = ''
  if (textareaRef.value) {
    textareaRef.value.style.height = ''
  }
  responseText.value = ''
}

defineExpose({
  clearInput,
  inputText,
  processText
})
</script>

<style scoped>
.input-section {
  margin-bottom: var(--spacing-lg);
}

.text-input,
.new-text-input {
  width: 100%;
  min-height: 100px;
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  resize: vertical;
  font-size: 1rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
  transition: border-color 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  justify-content: flex-end;
}

.action-button {
  padding: 8px 16px;
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #66b1ff;
}

.new-text-input {
  border: none;
  background-color: var(--color-bg-secondary);
}

.char-counter {
  text-align: right;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-top: var(--spacing-xs);
}

.new-display-container {
  display: flex;
  gap: var(--spacing-md);
}

.original-data-display,
.received-data-display {
  flex: 1;
  border: 1px solid var(--color-border);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
}

h3 {
  margin: 0 0 var(--spacing-sm);
  color: var(--color-text-primary);
  font-size: 1.125rem;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: var(--color-text-primary);
  font-size: 1rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .new-display-container {
    flex-direction: column;
  }
}
</style> 