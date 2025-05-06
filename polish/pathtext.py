import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
from fastapi.middleware.cors import CORSMiddleware  # 引入 CORS 中间件
'''run:D:\anaconda3\python.exe D:\Desktop\chess\polish\pathtext.py'''
# 加载模型和分词器（只加载一次）
model_path = r"E:\下载\Qwen-7B-Chat-Int4"

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="cuda:0",  # 使用 GPU
    trust_remote_code=True
).eval()

app = FastAPI()

# =================== ⚠️ 添加 CORS 支持 ===================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以指定前端地址，例如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（包括 POST 和 OPTIONS）
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/polish")
async def polish_text(request: Request, text_request: TextRequest):
    start_time = time.time()
    input_text = text_request.text
    print(f"Received text to polish: {input_text}")

    prompt = f"请将以下文本进行润色，使其更加流畅和专业：\n{input_text}"
    response = model.chat(
        tokenizer,
        prompt,
        history=None,
        temperature=0.2,
        top_p=0.9,
        max_new_tokens=500
    )[0]

    elapsed_time = time.time() - start_time
    print(f"Polished result: {response}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    return {"polished_text": response}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)