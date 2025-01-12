

# import os
# import cv2
# import numpy as np
# from joblib import load
# import requests
# import io
# from threading import Thread

# class ModelPredictor:
#     def __init__(self, model_paths, cache_dir="cached_models"):
#         self.model_paths = model_paths
#         self.cache_dir = cache_dir
#         self.models = {}  # Dictionary để lưu các mô hình đã tải
#         os.makedirs(self.cache_dir, exist_ok=True)

#     def _load_model(self, label):
#         """ Tải hoặc đọc mô hình từ bộ nhớ cache. """
#         if label in self.models:
#             return self.models[label]

#         model_file_path = os.path.join(self.cache_dir, f"{label}.pkl")

#         # Tải xuống nếu chưa có trong bộ nhớ cache
#         if not os.path.exists(model_file_path):
#             model_data = self.download_model(self.model_paths[label])
#             if model_data:
#                 with open(model_file_path, "wb") as f:
#                     f.write(model_data)
#             else:
#                 raise Exception(f"Không thể tải mô hình {label} từ URL.")

#         # Đọc mô hình từ bộ nhớ cache
#         with open(model_file_path, "rb") as f:
#             model = load(f)
#             self.models[label] = model
#         return model

#     def download_model(self, url, retries=3, delay=5):
#         """ Tải mô hình với khả năng thử lại khi gặp lỗi. """
#         for attempt in range(retries):
#             try:
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status()
#                 return response.content
#             except requests.exceptions.RequestException as e:
#                 print(f"Thử lại {attempt + 1}/{retries}: {e}")
#                 time.sleep(delay)
#         return None

#     def predict_info(self, extracted_info):
#         """ Dự đoán thông tin từ ảnh đã tách. """
#         predictions = {}
#         threads = []

#         for label, cropped_image in extracted_info.items():
#             thread = Thread(target=self._predict_label, args=(label, cropped_image, predictions))
#             threads.append(thread)
#             thread.start()

#         for thread in threads:
#             thread.join()

#         return predictions

#     def _predict_label(self, label, cropped_image, predictions):
#         """ Dự đoán cho từng nhãn riêng lẻ. """
#         if cropped_image is None or cropped_image.size == 0:
#             predictions[label] = "Ảnh không hợp lệ"
#             return

#         try:
#             # Tải hoặc lấy mô hình đã lưu
#             model = self._load_model(label)
#         except Exception as e:
#             predictions[label] = str(e)
#             return

#         # Tiền xử lý ảnh
#         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#         resized = cv2.resize(gray, (128, 128))
#         img = resized / 255.0
#         flattened = img.flatten().reshape(1, -1)

#         # Dự đoán
#         predicted_class = model.predict(flattened)[0]
#         predictions[label] = predicted_class

import os
import cv2
import numpy as np
from joblib import load
import requests
from threading import Thread
import time  # Thêm để sử dụng trong delay

class ModelPredictor:
    def __init__(self, model_paths, cache_dir="cached_models"):
        self.model_paths = model_paths
        self.cache_dir = cache_dir
        self.models = {}  # Dictionary để lưu các mô hình đã tải
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_model(self, label):
        """ Tải hoặc đọc mô hình từ bộ nhớ cache. """
        if label in self.models:
            print(f"Mô hình cho nhãn '{label}' đã được tải sẵn.")
            return self.models[label]

        model_file_path = os.path.join(self.cache_dir, f"{label}.pkl")

        # Tải xuống nếu chưa có trong bộ nhớ cache
        if not os.path.exists(model_file_path):
            print(f"Đang tải mô hình cho nhãn '{label}' từ URL...")
            model_data = self.download_model(self.model_paths.get(label))
            if model_data:
                with open(model_file_path, "wb") as f:
                    f.write(model_data)
            else:
                raise Exception(f"Không thể tải mô hình '{label}' từ URL.")

        # Đọc mô hình từ bộ nhớ cache
        print(f"Đang đọc mô hình '{label}' từ bộ nhớ cache.")
        with open(model_file_path, "rb") as f:
            model = load(f)
            self.models[label] = model
        return model

    def download_model(self, url, retries=3, delay=5):
        """ Tải mô hình với khả năng thử lại khi gặp lỗi. """
        if not url:
            raise ValueError("URL mô hình không hợp lệ.")
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                print(f"Thử lại {attempt + 1}/{retries}: {e}")
                time.sleep(delay)
        return None

    def predict_info(self, extracted_info):
        """ Dự đoán thông tin từ ảnh đã tách. """
        predictions = {}
        threads = []

        for label, cropped_image in extracted_info.items():
            thread = Thread(target=self._predict_label, args=(label, cropped_image, predictions))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return predictions

    def _predict_label(self, label, cropped_image, predictions):
        """ Dự đoán cho từng nhãn riêng lẻ. """
        if cropped_image is None or cropped_image.size == 0:
            predictions[label] = "Ảnh không hợp lệ"
            print(f"Lỗi: Ảnh cho nhãn '{label}' không hợp lệ.")
            return

        try:
            # Tải hoặc lấy mô hình đã lưu
            model = self._load_model(label)
        except Exception as e:
            predictions[label] = f"Lỗi mô hình: {e}"
            print(f"Lỗi mô hình cho nhãn '{label}': {e}")
            return

        # Tiền xử lý ảnh
        try:
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (128, 128))
            img = resized / 255.0
            flattened = img.flatten().reshape(1, -1)

            # Dự đoán
            predicted_class = model.predict(flattened)[0]
            predictions[label] = predicted_class
            print(f"Dự đoán cho nhãn '{label}': {predicted_class}")
        except Exception as e:
            predictions[label] = f"Lỗi xử lý ảnh hoặc dự đoán: {e}"
            print(f"Lỗi khi dự đoán cho nhãn '{label}': {e}")

