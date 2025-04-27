import { ref } from 'vue'
import { getImageToText } from '../api'
import axios from 'axios'

export function useImageInput() {
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

    // 上传图片到后端
    const formData = new FormData()
    Array.from(files).forEach(file => {
      formData.append('images', file)
    })

    try {
      const uploadResponse = await axios.post('http://localhost:5000/api/upload', formData)
      const imagePath = uploadResponse.data.path
      const response = await getImageToText(imagePath)
      responseText.value = response.data.text_content
      return responseText.value
    } catch (error) {
      console.error('Error processing image:', error)
      throw error
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

  return {
    fileInput,
    imageUrls,
    responseText,
    handleImageButtonClick,
    handleImageUpload,
    clearPreview
  }
} 