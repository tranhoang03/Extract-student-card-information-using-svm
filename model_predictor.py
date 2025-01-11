import cv2
import numpy as np
from joblib import load
import os
import streamlit as st

class ModelPredictor:
    def __init__(self, model_paths):
        self.models = {label: self.load_model(path) for label, path in model_paths.items()}
        st.write(f"Đã tải các mô hình: {self.models}")
        print(self.models)

    def load_model(self, path):
        if not os.path.exists(path):
            print(f"Không tìm thấy file mô hình tại đường dẫn: {path}")
            return None
        try:
            model = load(path)
            print(f"Đã tải mô hình từ: {path}")
        except KeyError as e:
            print(f"Lỗi khi tải mô hình từ {path}: {e}")
            model = None
        except Exception as e:
            print(f"Lỗi không xác định khi tải mô hình từ {path}: {e}")
            model = None
        return model

    def predict_info(self, extracted_info):
        predictions = {}
        for label, cropped_image in extracted_info.items():
            if label in self.models and self.models[label]:
                try:
                    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                    resized = cv2.resize(gray, (128, 128))
                    img = resized / 255.0
                    flattened = img.flatten().reshape(1, -1)

                    model = self.models[label]
                    predicted_class = model.predict(flattened)[0]
                    predictions[label] = predicted_class
                except Exception as e:
                    print(f"Lỗi trong quá trình dự đoán {label}: {e}")
                    predictions[label] = "Lỗi khi dự đoán"
            else:
                predictions[label] = "Mô hình không tồn tại hoặc không thể tải"
        return predictions
