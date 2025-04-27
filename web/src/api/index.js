import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // 后端服务器地址
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 文件上传 API
export const uploadFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post('http://localhost:5000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error in uploadFile:', error);
    throw error;
  }
};

// OCR API
export const getImageToText = async (imgPath) => {
  try {
    const response = await api.post('/api/image-to-text', {
      img_path: imgPath,
    });
    return response.data;
  } catch (error) {
    console.error('Error in getImageToText:', error);
    throw error;
  }
};

// Correction API
export const postCorrection = async (content, method = 0) => {
  try {
    const response = await api.post('/api/correction', {
      content,
      method,
    });
    return response.data;
  } catch (error) {
    console.error('Error in postCorrection:', error);
    throw error;
  }
};

// Correction Confirmation API
export const getCorrectionConfirm = async () => {
  try {
    const response = await api.get('/api/correctionConfirm');
    return response.data;
  } catch (error) {
    console.error('Error in getCorrectionConfirm:', error);
    throw error;
  }
};

// Assessment API
export const postAssessment = async (content, method = 0) => {
  try {
    const response = await api.post('/api/assessment', {
      content,
      method,
    });
    return response.data;
  } catch (error) {
    console.error('Error in postAssessment:', error);
    throw error;
  }
};

// Polish API
export const postPolish = async (content, instruction, method = 0) => {
  try {
    const response = await api.post('/api/polish', {
      content,
      instruction,
      method,
    });
    return response.data;
  } catch (error) {
    console.error('Error in postPolish:', error);
    throw error;
  }
}; 