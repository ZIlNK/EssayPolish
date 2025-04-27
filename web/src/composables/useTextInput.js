import { ref } from 'vue'
import { postCorrection, getCorrectionConfirm, postAssessment, postPolish } from '../api'

export function useTextInput() {
  const inputText = ref('')
  const textareaRef = ref(null)
  const responseText = ref('')
  const appraiseData = ref('')
  const rewriteData = ref('')

  const adjustTextareaHeight = () => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
    }
  }

  const handleTextSubmit = async () => {
    if (!inputText.value) return

    try {
      const correctionResult = await postCorrection(inputText.value)
      await getCorrectionConfirm()
      const assessmentResult = await postAssessment(inputText.value)
      const polishResult = await postPolish(inputText.value, '使语言更正式')
      responseText.value = polishResult.polished_content
      return responseText.value
    } catch (error) {
      console.error('Error processing text:', error)
      throw error
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleTextSubmit()
    }
  }

  const clearInput = () => {
    inputText.value = ''
    if (textareaRef.value) {
      textareaRef.value.style.height = ''
    }
    responseText.value = ''
    appraiseData.value = ''
    rewriteData.value = ''
  }

  const getAppraiseData = async () => {
    try {
      const response = await postAssessment(inputText.value)
      appraiseData.value = response.data
      return appraiseData.value
    } catch (error) {
      console.error('Error fetching appraise data:', error)
      throw error
    }
  }

  const getRewriteData = async () => {
    try {
      const response = await postPolish(inputText.value, '使语言更正式')
      rewriteData.value = response.data.polished_content
      return rewriteData.value
    } catch (error) {
      console.error('Error fetching rewrite data:', error)
      throw error
    }
  }

  return {
    inputText,
    textareaRef,
    responseText,
    appraiseData,
    rewriteData,
    adjustTextareaHeight,
    handleTextSubmit,
    handleKeyDown,
    clearInput,
    getAppraiseData,
    getRewriteData
  }
} 