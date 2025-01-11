# class ModelPredictor:
#     def __init__(self, model_paths):
#         self.models = {}
        
#         # Tải mô hình từ URL và kiểm tra thành công
#         for label, path in model_paths.items():
#             try:
#                 model_data = requests.get(path)
#                 if model_data.status_code == 200:
#                     model = load(io.BytesIO(model_data.content))  # Đọc mô hình từ dữ liệu tải về
#                     # Kiểm tra mô hình
#                     sample_data = np.zeros((1, 128*128))  # Giả sử kích thước ảnh là 128x128
#                     model.predict(sample_data)
#                     self.models[label] = model
#                 else:
#                     raise Exception(f"Không thể tải mô hình từ {path}, mã lỗi: {model_data.status_code}")
#             except Exception as e:
#                 print(f"Lỗi khi tải mô hình {label} từ {path}: {str(e)}")

#     def predict_info(self, extracted_info):
#         predictions = {}
        
#         for label, cropped_image in extracted_info.items():
#             if cropped_image is None or cropped_image.size == 0:
#                 predictions[label] = "Ảnh không hợp lệ"
#                 continue
            
#             if label in self.models:
#                 gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#                 resized = cv2.resize(gray, (128, 128))
#                 img = resized / 255.0
#                 flattened = img.flatten().reshape(1, -1)
                
#                 model = self.models[label]
#                 predicted_class = model.predict(flattened)[0]
#                 predictions[label] = predicted_class
#             else:
#                 predictions[label] = f"Mô hình cho nhãn {label} không tồn tại"
                
#         return predictions
import os
import cv2
import numpy as np
from joblib import load
import requests
import io
from threading import Thread

class ModelPredictor:
    def __init__(self, model_paths, cache_dir="cached_models"):
        self.models = {}
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self._load_models(model_paths)
        
    def _load_models(self, model_paths):
        """ Tải mô hình từ URL và lưu vào bộ nhớ đệm (nếu chưa tải). """
        for label, path in model_paths.items():
            model_file_path = os.path.join(self.cache_dir, f"{label}.pkl")
            if not os.path.exists(model_file_path):
                model_data = self.download_model(path)
                if model_data:
                    with open(model_file_path, "wb") as f:
                        f.write(model_data)
            else:
                print(f"Mô hình {label} đã tồn tại trong bộ nhớ đệm.")
            
            # Đọc mô hình từ bộ nhớ đệm
            with open(model_file_path, "rb") as f:
                model = load(f)
                self.models[label] = model

    def download_model(self, url, retries=3, delay=5):
        """ Tải mô hình với khả năng thử lại khi gặp lỗi. """
        for attempt in range(retries):
            try:
                model_data = requests.get(url).content
                return model_data
            except requests.exceptions.RequestException as e:
                print(f"Thử lại {attempt + 1}/{retries}: {e}")
                time.sleep(delay)
        return None

    def predict_info(self, extracted_info):
        """ Dự đoán thông tin từ ảnh đã tách. """
        predictions = {}
        threads = []

        # Dự đoán đồng thời
        for label, cropped_image in extracted_info.items():
            thread = Thread(target=self._predict_label, args=(label, cropped_image, predictions))
            threads.append(thread)
            thread.start()

        # Đợi tất cả các thread hoàn thành
        for thread in threads:
            thread.join()
        
        return predictions

    def _predict_label(self, label, cropped_image, predictions):
        """ Dự đoán cho từng nhãn riêng lẻ. """
        if cropped_image is None or cropped_image.size == 0:
            predictions[label] = "Ảnh không hợp lệ"
            return

        # Kiểm tra xem mô hình có tồn tại không
        if label not in self.models:
            predictions[label] = "Mô hình không tồn tại"
            return

        # Tiền xử lý ảnh
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (128, 128))
        img = resized / 255.0
        flattened = img.flatten().reshape(1, -1)

        # Dự đoán
        model = self.models[label]
        predicted_class = model.predict(flattened)[0]
        predictions[label] = predicted_class
