from flask import Flask, request, jsonify
from flask_cors import CORS
from paddleocr import PaddleOCR
from pycorrector import Corrector
import os
import json
import uuid
import requests

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 初始化OCR和纠错器
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
corrector = Corrector()

class LLM:
    url = "http://127.0.0.1:8000/v1/chat/completions"  # 假设LLM服务运行在8000端口
    mode = ""
    character = ""
    temperature = 0.0
    top_p = 0.0
    max_tokens = 0
    seed = -1
    history = []

    def __init__(self, character="PolishAI", mode="chat-instruct", temperature=1, top_p=0.9, max_tokens=4096, seed=-1, load=0, modelName="defaultLLM"):
        self.mode = mode
        self.character = character
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.seed = seed
        if load == 0:
            return
        else:
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "model_name": modelName,
                "args": {
                    "n_gpu_layers": 12
                }
            }
            response = requests.post("http://127.0.0.1:8000/v1/internal/model/load", headers=headers, json=data, verify=False)

    def changechar(self, character):
        self.mode = "chat-instruct"
        self.character = character
        if character == "PolishAI":
            self.temperature = 1
            self.top_p = 0.9
        elif character == "AssessAI":
            self.temperature = 0.8
        else:
            self.temperature = 0.5

    def process(self, user_message="continue"):
        try:
            self.history.append({"role": "user", "content": user_message})

            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "mode": self.mode,
                "character": self.character,
                "messages": self.history,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "seed": self.seed
            }

            print(f"Sending request to LLM service: {self.url}")
            print(f"Request data: {data}")
            
            response = requests.post(self.url, headers=headers, json=data, verify=False)
            
            # 检查响应状态码
            if response.status_code != 200:
                print(f"Error: Server returned status code {response.status_code}")
                print(f"Response content: {response.text}")
                return "模型处理失败，请稍后重试"

            # 尝试解析JSON响应
            try:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    assistant_message = response_data['choices'][0]['message']['content']
                    self.history.append({"role": "assistant", "content": assistant_message})
                    return assistant_message
                else:
                    print("Error: Invalid response format")
                    print(f"Response data: {response_data}")
                    return "模型返回格式错误，请稍后重试"
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Response content: {response.text}")
                return "模型返回数据格式错误，请稍后重试"
        except Exception as e:
            print(f"Error in process: {str(e)}")
            return "模型处理出错，请稍后重试"

    def sethistory(self, newhistory):
        self.history = newhistory

    def clearhistory(self):
        self.history.clear()

# 初始化LLM实例
llm = LLM()
llm.__init__()

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
        
        if method != 0:
            return jsonify({"error": "invalid method."}), 400

        output = ""
        out = []
        llm.clearhistory()
        llm.changechar("CorrectionAI")
        output = llm.process(content)
        out = output.split("‖")
        
        suggestions = []
        for item in out:
            a = item.split("¦")
            if len(a) != 5:
                suggestions = [{
                    "position": [0, 0],
                    "original": "",
                    "recommended": "invalid LLM output",
                }]
                continue

            if a[2] != content[int(a[0]):int(a[1])+1]:
                suggestions = [{
                    "position": [0, 0],
                    "original": "",
                    "recommended": "invalid LLM output",
                }]
                continue
                
            suggestion = {
                "position": [int(a[0]), int(a[1])],
                "original": a[2],
                "recommended": a[3]
            }
            suggestions.append(suggestion)

        return jsonify({
            "suggestions": suggestions
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
        
        if method != 0:
            return jsonify({"error": "invalid method."}), 400

        llm.clearhistory()
        llm.changechar("AssessAI")
        output = llm.process(content)
        out = output.split("，")
        
        if len(out) != 4:
            return jsonify({"error": "invalid llm output."}), 500

        grammar = out[0].split("：")[1]
        structure = out[1].split("：")[1]
        contentScore = out[2].split("：")[1]
        totalScore = out[3].split("：")[1]
        
        breakdown = {
            "grammar": grammar,
            "structure": structure,
            "content": contentScore
        }

        return jsonify({
            "total_score": totalScore,
            "breakdown": breakdown
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
        
        if method == 0:
            output = ""
            llm.clearhistory()
            llm.changechar("PolishAI")
            output = llm.process(content + "   对以上作文进行润色，要求：" + instruction)

            if ("模型润色时出现未知错误！" in output) or ("无法做出更改。" in output):
                return jsonify({
                    "error": "模型润色时出现未知错误！"
                }), 500

            out = output.split("‖")
            if len(out) > 2:
                return jsonify({
                    "error": "模型润色时出现未知错误！"
                }), 500

            polished_content = out[0]
            changes_made = ["优化句式结构", "替换口语化表达"]

            return jsonify({
                "polished_content": polished_content,
                "changes_made": changes_made
            })
        else:
            return jsonify({
                "error": "invalid method."
            }), 400
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 