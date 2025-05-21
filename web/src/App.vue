<template>
  <div class="app-container">
    <div class="content-wrapper">
      <ModeSwitch
        :is-image-mode="isImageMode"
        @switch="switchMode"
      />
      
      <ImageInput
        v-if="isImageMode"
        :is-new-show="currentModeState.newShow"
        @update:response-text="handleResponseText"
        ref="imageInputRef"
      />
      
      <TextInput
        v-else
        :is-new-show="currentModeState.newShow"
        @update:response-text="handleResponseText"
        ref="textInputRef"
      />

      <ActionButtons
        :is-form-valid="isFormValid"
        :is-appraise="currentModeState.isAppraise"
        :is-rewrite="currentModeState.isRewrite"
        @submit="handleSubmit"
        @reset="handleReset"
        @switch="underSwitchMode"
      />

      <ResultDisplay
        :is-new-show="currentModeState.newShow"
        :is-appraise="currentModeState.isAppraise"
        :is-rewrite="currentModeState.isRewrite"
        :appraise-data="appraiseData"
        :rewrite-data="rewriteData"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ModeSwitch from './components/ModeSwitch.vue'
import ImageInput from './components/ImageInput.vue'
import TextInput from './components/TextInput.vue'
import ActionButtons from './components/ActionButtons.vue'
import ResultDisplay from './components/ResultDisplay.vue'

// 状态管理
const isImageMode = ref(false)
const currentModeState = ref({
  newShow: false,
  isAppraise: false,
  isRewrite: false
})

// 组件引用
const imageInputRef = ref(null)
const textInputRef = ref(null)

// 数据
const responseText = ref('')
const appraiseData = ref('')
const rewriteData = ref('')

// 表单验证
const isFormValid = computed(() => {
  if (isImageMode.value) {
    return imageInputRef.value?.imageUrls?.length > 0
  } else {
    return textInputRef.value?.inputText?.length > 0
  }
})

// 模式切换
const switchMode = (mode) => {
  isImageMode.value = mode
  handleReset()
}

// 评价/润色模式切换
const underSwitchMode = async (mode) => {
  if (!currentModeState.value.newShow) {
    return
  }
  
  currentModeState.value.isAppraise = mode === 'appraise'
  currentModeState.value.isRewrite = mode === 'rewrite'
  
  try {
    if (currentModeState.value.isAppraise) {
      const response = await fetch('http://localhost:5000/api/assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: responseText.value,
          method: 0
        })
      })
      const data = await response.json()
      appraiseData.value = {
        total_score: data.total_score,
        breakdown: data.breakdown
      }
    } else if (currentModeState.value.isRewrite) {
      const response = await fetch('http://localhost:5000/api/polish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: responseText.value,
          instruction: '使语言更正式',
          method: 0
        })
      })
      const data = await response.json()
      rewriteData.value = {
        polished_content: data.polished_content,
        changes_made: data.changes_made
      }
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

// 处理响应文本
const handleResponseText = (text) => {
  responseText.value = text
  currentModeState.value.newShow = true
}

// 提交处理
const handleSubmit = async () => {
  if (!isFormValid.value) return

  try {
    if (isImageMode.value) {
      await imageInputRef.value?.handleImageUpload()
    } else {
      await textInputRef.value?.processText()
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

// 重置处理
const handleReset = () => {
  if (isImageMode.value) {
    imageInputRef.value?.clearPreview()
  } else {
    textInputRef.value?.clearInput()
  }
  currentModeState.value = {
    newShow: false,
    isAppraise: false,
    isRewrite: false
  }
  responseText.value = ''
  appraiseData.value = ''
  rewriteData.value = ''
}
</script>

<style>
:root {
  /* 主题色 */
  --color-primary: #1a1a1a;
  --color-primary-light: #2a2a2a;
  --color-secondary: #ffffff;
  --color-accent: #4a4a4a;
  
  /* 文字颜色 */
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #4a4a4a;
  --color-text-light: #ffffff;
  
  /* 背景色 */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f5f5;
  
  /* 边框颜色 */
  --color-border: #e0e0e0;
  
  /* 状态颜色 */
  --color-success: #2ecc71;
  --color-error: #e74c3c;
  --color-warning: #f1c40f;
  
  /* 间距 */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* 圆角 */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;
  
  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: var(--spacing-xl);
  background-color: var(--color-bg-secondary);
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

@media (max-width: 768px) {
  .app-container {
    padding: var(--spacing-md);
}

  .content-wrapper {
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
  }
}
</style>