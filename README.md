# EssayPolish - 智能文本处理系统

EssayPolish 是一个基于深度学习的智能文本处理系统，提供 OCR 文字识别、文本润色和评价功能。前端使用 Vue.js，后端使用 Flask 和深度学习模型。

## 功能特点

- 📷 **OCR 文字识别**：支持从图片中提取文字
- ✨ **文本润色**：智能优化文本表达（开发中）
- 📊 **文本评价**：提供文本质量评估（开发中）
- 🎯 **用户友好**：简洁直观的操作界面
- 🔄 **实时预览**：即时查看处理结果

## 环境要求

- Windows 操作系统
- CUDA 11.8
- Python 3.8
- PyTorch 2.2.2

## 安装步骤

1. **创建并激活 conda 环境**
```bash
conda create -n paddle_env python=3.8 -y
conda activate paddle_env
```

2. **安装 PaddlePaddle**
```bash
python -m pip install paddlepaddle-gpu==2.6.2 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

3. **安装 OCR 相关依赖**
```bash
pip install paddleocr pycorrector opencv-python -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

4. **安装 PyTorch**
```bash
pip3 install torch==2.2.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

5. **安装其他依赖**
```bash
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pip install pypi-kenlm -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

## 启动服务

1. **启动后端服务**
```bash
python server.py
```

2. **启动前端服务**
```bash
cd web
npm install
npm run dev
```

## 参考资料

- [PaddlePaddle 官网](https://www.paddlepaddle.org.cn/)
- [PyTorch 官网](https://pytorch.org/)
- [环境配置参考](https://blog.csdn.net/weixin_48951678/article/details/138445010)

## 注意事项

- 确保已安装 CUDA 11.8 及相应驱动
- 按照顺序执行安装步骤
- 如遇到网络问题，建议使用国内镜像源
- 运行时需要同时启动前端和后端服务

## 开发团队

- 五个杭电最强的存在，毋庸置疑。

## 许可证

MIT License
