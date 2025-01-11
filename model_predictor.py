import cv2
import numpy as np
import pickle

class ModelPredictor:
    def __init__(self, model_paths):
        self.models = {label: self.load_model(path) for label, path in model_paths.items()}

    def load_model(self, path):
        with open(path, 'rb') as file:
            model = pickle.load(file)
        return model

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
