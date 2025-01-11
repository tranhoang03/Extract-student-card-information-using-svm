class ModelPredictor:
    def __init__(self, model_paths):
        self.models = {}
        
        # Tải mô hình từ URL và kiểm tra thành công
        for label, path in model_paths.items():
            try:
                model_data = requests.get(path)
                if model_data.status_code == 200:
                    model = load(io.BytesIO(model_data.content))  # Đọc mô hình từ dữ liệu tải về
                    # Kiểm tra mô hình
                    sample_data = np.zeros((1, 128*128))  # Giả sử kích thước ảnh là 128x128
                    model.predict(sample_data)
                    self.models[label] = model
                else:
                    raise Exception(f"Không thể tải mô hình từ {path}, mã lỗi: {model_data.status_code}")
            except Exception as e:
                print(f"Lỗi khi tải mô hình {label} từ {path}: {str(e)}")

    def predict_info(self, extracted_info):
        predictions = {}
        
        for label, cropped_image in extracted_info.items():
            if cropped_image is None or cropped_image.size == 0:
                predictions[label] = "Ảnh không hợp lệ"
                continue
            
            if label in self.models:
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (128, 128))
                img = resized / 255.0
                flattened = img.flatten().reshape(1, -1)
                
                model = self.models[label]
                predicted_class = model.predict(flattened)[0]
                predictions[label] = predicted_class
            else:
                predictions[label] = f"Mô hình cho nhãn {label} không tồn tại"
                
        return predictions
