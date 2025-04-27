from paddleocr import PaddleOCR, draw_ocr
import cv2
from pycorrector import Corrector

# 初始化OCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)

img_path = 'test1.jpg'
output_txt_path = 'combined_text.txt'  # 文本输出路径

# try:
#     # 执行OCR
#     result = ocr.ocr(img_path, cls=True)
#
#     if result and len(result) > 0:
#         img_result = result[0]
#
#         # 提取所有文本并合并
#         combined_text = []
#         for line in img_result:
#             text = line[1][0]  # 提取文本内容
#             combined_text.append(text)
#
#         # 使用换行符组合文本（可根据需要修改分隔符）
#         final_text = '\n'.join(combined_text)
#
#         # 打印/保存结果
#         print("所有文本组合结果：")
#         print(final_text)
#
#         # 保存到文本文件
#         with open(output_txt_path, 'w', encoding='utf-8') as f:
#             f.write(final_text)
#         print(f"文本已保存至 {output_txt_path}")
#
#         # 可选：可视化结果（保留原功能）
#         image = cv2.imread(img_path)
#         visualized_img = draw_ocr(image,
#                                   [line[0] for line in img_result],
#                                   [line[1][0] for line in img_result],
#                                   scores=[line[1][1] for line in img_result])
#         cv2.imwrite('result_visualized.jpg', visualized_img)
#
#     else:
#         print("未检测到任何文本。")
# except Exception as e:
#     print(f"发生错误: {e}")

text1 = "我心请很好"
corrector = Corrector()
print(corrector.correct_batch([text1]))