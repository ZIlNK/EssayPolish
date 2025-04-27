<template>
  <div class="upload-section">
    <input
      type="file"
      accept="image/*"
      @change="handleImageUpload"
      class="file-input"
      ref="fileInput"
    >
    <!-- 图片默认展示区 -->
    <div v-if="!imageUrls.length" class="preview-container default-preview">
      <div class="image-wrapper">
        <button
          @click="handleImageButtonClick"
          class="upload-button"
        >
          上传图片
        </button>
      </div>
    </div>
    <!--图片展示区-->
    <div v-if="imageUrls.length" class="preview-container">
      <div v-if="!isNewShow" class="image-wrapper">
        <img v-for="(url, index) in imageUrls" :key="index" :src="url" alt="Preview" class="preview-image">
        <!-- 添加图片按钮，在已有图片时显示 -->
        <button
          v-if="imageUrls.length"
          @click="handleImageButtonClick"
          class="upload-button add-image-button"
        >
          添加图片
        </button>
      </div>
      <!-- 新的展示页面 -->
      <div v-if="isNewShow" class="new-display-container">
        <div class="original-data-display">
          <h3>识别的文本</h3>
          <div class="image-wrapper">
            <img v-for="(url, index) in imageUrls" :key="index" :src="url" alt="Preview" class="preview-image">
          </div>
        </div>
        <div class="received-data-display">
          <h3>处理结果</h3>
          <pre>{{ responseText }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadFile, getImageToText } from '../api'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  isNewShow: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:responseText'])

const fileInput = ref(null)
const imageUrls = ref([])
const responseText = ref('')

const handleImageButtonClick = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleImageUpload = async (event) => {
  const files = event.target.files
  if (!files.length) return

  // 创建预览URL
  imageUrls.value = Array.from(files).map(file => URL.createObjectURL(file))

  try {
    // 上传图片
    const formData = new FormData()
    formData.append('file', files[0])
    
    const uploadResponse = await axios.post('http://localhost:5000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    console.log('Upload response:', uploadResponse.data)
    
    if (uploadResponse.data && uploadResponse.data.data && uploadResponse.data.data.filepath) {
      // 获取图片中的文本
      const textResponse = await getImageToText(uploadResponse.data.data.filepath)
      
      console.log('Text response:', textResponse)
      
      // 检查响应格式
      if (textResponse && textResponse.data) {
        const textData = textResponse.data.data || textResponse.data
        if (textData && textData.text_content) {
          responseText.value = textData.text_content
          emit('update:responseText', responseText.value)
          ElMessage.success('图片处理成功')
        } else {
          console.error('No text content found in response:', textResponse)
          ElMessage.error('未检测到文本内容')
        }
      } else {
        console.error('Invalid text response format:', textResponse)
        ElMessage.error('文本识别响应格式错误')
      }
    } else {
      console.error('Invalid upload response:', uploadResponse.data)
      ElMessage.error('图片上传失败：响应格式错误')
    }
  } catch (error) {
    console.error('Error processing image:', error)
    ElMessage.error('处理失败，请重试')
  }
}

const clearPreview = () => {
  imageUrls.value.forEach(url => {
    URL.revokeObjectURL(url)
  })
  imageUrls.value = []
  if (fileInput.value) fileInput.value.value = ''
  responseText.value = ''
}

defineExpose({
  clearPreview
})
</script>

<style scoped>
.upload-section {
  margin-bottom: 2rem;
  text-align: center;
}

.file-input {
  display: none;
}

.preview-container {
  margin-top: 1rem;
  position: relative;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.image-wrapper {
  width: 100%;
  height: auto;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.default-preview {
  border: 1px dashed #ccc;
  padding: 20px;
  text-align: center;
}

.new-display-container {
  display: flex;
  gap: 1rem;
}

.original-data-display,
.received-data-display {
  flex: 1;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
}

.upload-button {
  padding: 10px 20px;
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #66b1ff;
}

.add-image-button {
  margin-top: 10px;
  align-self: flex-end;
}
</style> 