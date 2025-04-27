from flask import Flask, request, jsonify
from flask_cors import CORS
from paddleocr import PaddleOCR
from pycorrector import Corrector
import os
import json
import uuid

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 初始化OCR和纠错器
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
corrector = Corrector()

# 创建上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "没有文件被上传"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 生成唯一文件名
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({
            "data": {
                "filepath": filepath
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/image-to-text', methods=['POST'])
def image_to_text():
    try:
        data = request.get_json()
        img_path = data.get('img_path', '')
        
        if not img_path or not os.path.exists(img_path):
            return jsonify({"error": "图片路径无效"}), 400
            
        # 执行OCR
        result = ocr.ocr(img_path, cls=True)
        
        if result and len(result) > 0:
            img_result = result[0]
            # 提取所有文本并合并
            combined_text = []
            for line in img_result:
                text = line[1][0]  # 提取文本内容
                combined_text.append(text)
            
            # 使用换行符组合文本
            final_text = '\n'.join(combined_text)
            
            # 保存到文本文件
            output_txt_path = os.path.join(UPLOAD_FOLDER, 'combined_text.txt')
            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(final_text)
            
            return jsonify({
                "data": {
                    "text_content": final_text,
                    "filepath": output_txt_path
                }
            })
        else:
            return jsonify({
                "error": "未检测到任何文本"
            }), 400
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/correction', methods=['POST'])
def correction():
    try:
        data = request.get_json()
        content = data.get('content', '')
        method = data.get('method', 0)
        
        # 执行文本纠错
        corrected_text = corrector.correct_batch([content])[0]
        
        # 生成建议列表
        suggestions = []
        for i, (wrong, right) in enumerate(zip(content, corrected_text)):
            if wrong != right:
                suggestions.append({
                    "position": [i, i + 1],
                    "original": wrong,
                    "recommended": right,
                    "error_type": "spelling"
                })
        
        return jsonify({
            "data": {
                "suggestions": suggestions
            }
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/correctionComfirm', methods=['GET'])
def correction_confirm():
    return jsonify({
        "status": "OK"
    })

@app.route('/api/assessment', methods=['POST'])
def assessment():
    try:
        data = request.get_json()
        content = data.get('content', '')
        method = data.get('method', 0)
        
        # 这里实现文本评估逻辑
        # 示例评分
        score = {
            "total_score": 85,
            "breakdown": {
                "grammar": 18,
                "structure": 22,
                "content": 45
            }
        }
        
        return jsonify({
            "data": score
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/polish', methods=['POST'])
def polish():
    try:
        data = request.get_json()
        content = data.get('content', '')
        instruction = data.get('instruction', '使语言更正式')
        method = data.get('method', 0)
        
        # 这里实现文本润色逻辑
        # 示例润色结果
        polished_content = content  # 实际应用中这里需要实现润色逻辑
        changes_made = ["优化句式结构", "替换口语化表达"]
        
        return jsonify({
            "polished_content": polished_content,
            "changes_made": changes_made
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 