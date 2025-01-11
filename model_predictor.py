import cv2
import numpy as np
from joblib import load
import io

class ModelPredictor:
    def __init__(self, model_files):
        self.models = {label: self.load_model(file_content) for label, file_content in model_files.items()}

    def load_model(self, file_content):
        try:
            model = load(io.BytesIO(file_content))
            print(f"Đã tải mô hình từ bộ nhớ tạm")
        except KeyError as e:
            print(f"Lỗi khi tải mô hình: {e}")
            model = None
        except Exception as e:
            print(f"Lỗi không xác định khi tải mô hình: {e}")
            model = None
        return model

    def predict_info(self, extracted_info):
        predictions = {}
        for label, cropped_image in extracted_info.items():
            if label in self.models and self.models[label]:
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (128, 128))
                img = resized / 255.0
                flattened = img.flatten().reshape(1, -1)

                model = self.models[label]
                predicted_class = model.predict(flattened)[0]
                predictions[label] = predicted_class
            else:
                predictions[label] = "Mô hình không tồn tại hoặc không thể tải"
        return predictions
