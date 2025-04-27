import paddle
print(paddle.utils.run_check())  # 检查PaddlePaddle是否安装正确
from paddleocr import PaddleOCR
print("PaddleOCR导入成功")
from pycorrector import Corrector
print("pycorrector导入成功")