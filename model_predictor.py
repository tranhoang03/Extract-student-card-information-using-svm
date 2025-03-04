

import os
import cv2
import numpy as np
from joblib import load
import requests
import io
from threading import Thread

class ModelPredictor:
    def __init__(self, model_paths, cache_dir="cached_models"):
        self.model_paths = model_paths
        self.cache_dir = cache_dir
        self.models = {}  # Dictionary để lưu các mô hình đã tải
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_model(self, label):
 
        if label in self.models:
            return self.models[label]
    
        model_file_path = os.path.join(self.cache_dir, f"{label}.pkl")
    
        # Kiểm tra xem file có sẵn không, nếu không thì tải xuống
        if not os.path.exists(model_file_path):
            model_file_path = self.download_model(self.model_paths[label])
            if model_file_path is None:
                raise Exception(f"Không thể tải mô hình {label} từ URL.")
    
        # Đọc mô hình từ file
        model = load(model_file_path)
        self.models[label] = model
        return model

    def download_model(self, url):
        try:
            output_path = os.path.join(self.cache_dir, f"{url.split('id=')[-1]}.pkl")
            
            # Kiểm tra nếu file đã tồn tại để tránh tải lại
            if os.path.exists(output_path):
                print(f"File {output_path} đã tồn tại, không cần tải lại.")
                return output_path
    
            # Tải file từ Google Drive
            gdown.download(url, output_path, quiet=False)
            return output_path
        except Exception as e:
            print(f"Lỗi khi tải mô hình từ Google Drive: {e}")
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
            return

        try:
            # Tải hoặc lấy mô hình đã lưu
            model = self._load_model(label)
        except Exception as e:
            predictions[label] = str(e)
            return

        # Tiền xử lý ảnh
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (128, 128))
        img = resized / 255.0
        flattened = img.flatten().reshape(1, -1)

        # Dự đoán
        predicted_class = model.predict(flattened)[0]
        predictions[label] = predicted_class



