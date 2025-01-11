# import cv2
# import numpy as np
# from joblib import load
# import requests
# import io

# class ModelPredictor:
#     def __init__(self, model_paths):
#         self.models = {}
        
#         # Tải mô hình từ URL
#         for label, path in model_paths.items():
#             model_data = requests.get(path).content
#             model = load(io.BytesIO(model_data))  # Đọc mô hình từ dữ liệu tải về
#             self.models[label] = model

#     def predict_info(self, extracted_info):
#         predictions = {}
        
#         for label, cropped_image in extracted_info.items():
#             # Kiểm tra xem ảnh có hợp lệ không
#             if cropped_image is None or cropped_image.size == 0:
#                 predictions[label] = "Ảnh không hợp lệ"
#                 continue
            
#             # Kiểm tra xem mô hình có tồn tại cho nhãn này không
#             if label in self.models:
#                 # Chuyển ảnh sang màu xám
#                 gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                
#                 # Thay đổi kích thước ảnh về 128x128
#                 resized = cv2.resize(gray, (128, 128))
                
#                 # Chuẩn hóa ảnh (chia cho 255.0 để giá trị nằm trong khoảng [0, 1])
#                 img = resized / 255.0
                
#                 # Làm phẳng ảnh thành vector một chiều
#                 flattened = img.flatten().reshape(1, -1)

#                 # Lấy mô hình dự đoán
#                 model = self.models[label]
#                 predicted_class = model.predict(flattened)[0]
#                 predictions[label] = predicted_class
#             else:
#                 predictions[label] = "Mô hình không tồn tại"
                
#         return predictions
import os
import requests
from joblib import load
import io

class ModelPredictor:
    def __init__(self, model_paths):
        self.models = {}
        
        for label, path in model_paths.items():
            model_file = f"{label}_model.pkl"
            
            # Kiểm tra nếu mô hình đã được tải xuống và lưu trữ trên máy
            if not os.path.exists(model_file):
                model_data = requests.get(path).content
                with open(model_file, "wb") as f:
                    f.write(model_data)
            
            # Tải mô hình từ file cục bộ
            with open(model_file, "rb") as f:
                model = load(f)
            self.models[label] = model

    def predict_info(self, extracted_info):
        predictions = {}
        
        for label, cropped_image in extracted_info.items():
            if label in self.models:
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (128, 128))
                img = resized / 255.0
                flattened = img.flatten().reshape(1, -1)

                model = self.models[label]
                predicted_class = model.predict(flattened)[0]
                predictions[label] = predicted_class
            else:
                predictions[label] = "Mô hình không tồn tại"
                
        return predictions


# # Đoạn mã bên dưới cho việc tải ảnh và xử lý trong Streamlit vẫn giữ nguyên
