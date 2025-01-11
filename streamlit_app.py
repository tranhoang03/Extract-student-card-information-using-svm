import streamlit as st
from image_processor import ImageProcessor, CoordinateLoader
from model_predictor import ModelPredictor
import cv2
from docx import Document
from docx.shared import Inches
import os
import io

# Đường dẫn các mô hình
MODEL_PATHS = {
    'hoten': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_hoten.pkl',
    'ngaysinh': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_ngaysinh.pkl',
    'lop': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_lop.pkl',
    'msv': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_masinhvien.pkl',
    'nienkhoa':r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_nienkhoa.pkl',
    'anhthe': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_anhthe.pkl'
}

# Tải mô hình và tọa độ
coordinate_loader = CoordinateLoader()
average_coordinates, max_hoten_box = coordinate_loader.load_coordinates_from_xml(r'C:\Users\Hoang\Desktop\LTND_PROJECT\training_data_segmentation\annotations.xml')
all_coordinates = coordinate_loader.get_all_coordinates(average_coordinates, max_hoten_box)

predictor = ModelPredictor(MODEL_PATHS)

# Hàm lưu thông tin sinh viên và ảnh thẻ vào file Word
def save_student_info_to_word(all_predictions, all_extracted_info):
    # Tạo file Word trong bộ nhớ
    doc = Document()
    doc.add_heading("Thông tin Sinh viên", level=1)

    # Duyệt qua tất cả các thẻ và ghi thông tin vào file Word
    for idx, (predictions, extracted_info) in enumerate(zip(all_predictions, all_extracted_info), start=1):
        doc.add_heading(f"Thông tin Thẻ {idx}", level=2)

        # Thêm thông tin chi tiết
        doc.add_heading("Thông tin chi tiết:", level=3)
        for label, predicted_class in predictions.items():
            if label != "anhthe":  # Bỏ qua nhãn ảnh thẻ
                doc.add_paragraph(f"{label.capitalize()}: {predicted_class}")

        # Thêm ảnh thẻ nếu có
        if "anhthe" in extracted_info:
            doc.add_heading("Ảnh thẻ:", level=3)
            # Lưu ảnh thẻ tạm thời
            temp_image_path = "temp_anhthe.jpg"
            cv2.imwrite(temp_image_path, extracted_info["anhthe"])

            # Chèn ảnh vào file Word
            doc.add_picture(temp_image_path, width=Inches(2))

            # Xóa ảnh tạm
            os.remove(temp_image_path)

        # Thêm một trang mới sau mỗi thẻ
        doc.add_page_break()

    # Lưu vào bộ nhớ (BytesIO)
    byte_io = io.BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)  # Đưa con trỏ về đầu file

    return byte_io
# Streamlit UI
st.title("Đọc thông tin Sinh viên")

# Tải nhiều ảnh
uploaded_files = st.file_uploader("Tải lên ảnh", type=["jpg", "png"], accept_multiple_files=True)
if uploaded_files:
    all_predictions = []  # Danh sách lưu tất cả các dự đoán
    all_extracted_info = []  # Danh sách lưu tất cả các thông tin đã tách

    for idx, uploaded_file in enumerate(uploaded_files):
        image_path = uploaded_file.name
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption=f"Ảnh gốc - {uploaded_file.name}", use_column_width=True)

        # Xử lý ảnh
        processor = ImageProcessor()
        cropped_card = processor.crop_card(image_path)

        if cropped_card is not None:
            extracted_info = processor.crop_info_from_coordinates(cropped_card, all_coordinates)
            predictions = predictor.predict_info(extracted_info)

            st.write("Dự đoán:")
            for label, pred in predictions.items():
                st.write(f"**{label.capitalize()}**: {pred}")

            # Hiển thị các ảnh đã cắt
            st.write("Các vùng đã tách:")
            cols = st.columns(len(extracted_info))
            for idx, (label, img) in enumerate(extracted_info.items()):
                with cols[idx]:
                    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption=label)

            # Lưu kết quả vào danh sách (cập nhật thông tin vào file hiện có)
            all_predictions.append(predictions)
            all_extracted_info.append(extracted_info)

        # Xóa ảnh sau khi xử lý
        os.remove(image_path)

    if all_predictions:
        # Lưu kết quả vào file Word sau khi xử lý tất cả ảnh
        byte_io = save_student_info_to_word(all_predictions, all_extracted_info)

        # Tạo nút để tải file Word
        st.download_button(
            label="Tải file Word",
            data=byte_io,
            file_name="student_info.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="download_button"  
        )
