# import streamlit as st
# from image_processor import ImageProcessor, CoordinateLoader
# from model_predictor import ModelPredictor
# import cv2
# from docx import Document
# from docx.shared import Inches
# import os
# import io

# # Đường dẫn các mô hình
# MODEL_PATHS = {
#     'hoten': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_hoten.pkl',
#     'ngaysinh': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_ngaysinh.pkl',
#     'lop': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_lop.pkl',
#     'msv': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_masinhvien.pkl',
#     'nienkhoa':r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_nienkhoa.pkl',
#     'anhthe': r'C:\Users\Hoang\Desktop\LTND_PROJECT\models\svm_anhthe.pkl'
# }

# # Tải mô hình và tọa độ
# coordinate_loader = CoordinateLoader()
# average_coordinates, max_hoten_box = coordinate_loader.load_coordinates_from_xml(r'C:\Users\Hoang\Desktop\LTND_PROJECT\training_data_segmentation\annotations.xml')
# all_coordinates = coordinate_loader.get_all_coordinates(average_coordinates, max_hoten_box)

# predictor = ModelPredictor(MODEL_PATHS)

# # Hàm lưu thông tin sinh viên và ảnh thẻ vào file Word
# def save_student_info_to_word(all_predictions, all_extracted_info):
#     # Tạo file Word trong bộ nhớ
#     doc = Document()
#     doc.add_heading("Thông tin Sinh viên", level=1)

#     # Duyệt qua tất cả các thẻ và ghi thông tin vào file Word
#     for idx, (predictions, extracted_info) in enumerate(zip(all_predictions, all_extracted_info), start=1):
#         doc.add_heading(f"Thông tin Thẻ {idx}", level=2)

#         # Thêm thông tin chi tiết
#         doc.add_heading("Thông tin chi tiết:", level=3)
#         for label, predicted_class in predictions.items():
#             if label != "anhthe":  # Bỏ qua nhãn ảnh thẻ
#                 doc.add_paragraph(f"{label.capitalize()}: {predicted_class}")

#         # Thêm ảnh thẻ nếu có
#         if "anhthe" in extracted_info:
#             doc.add_heading("Ảnh thẻ:", level=3)
#             # Lưu ảnh thẻ tạm thời
#             temp_image_path = "temp_anhthe.jpg"
#             cv2.imwrite(temp_image_path, extracted_info["anhthe"])

#             # Chèn ảnh vào file Word
#             doc.add_picture(temp_image_path, width=Inches(2))

#             # Xóa ảnh tạm
#             os.remove(temp_image_path)

#         # Thêm một trang mới sau mỗi thẻ
#         doc.add_page_break()

#     # Lưu vào bộ nhớ (BytesIO)
#     byte_io = io.BytesIO()
#     doc.save(byte_io)
#     byte_io.seek(0)  # Đưa con trỏ về đầu file

#     return byte_io
# # Streamlit UI
# st.title("Đọc thông tin Sinh viên")

# # Tải nhiều ảnh
# uploaded_files = st.file_uploader("Tải lên ảnh", type=["jpg", "png"], accept_multiple_files=True)
# if uploaded_files:
#     all_predictions = []  # Danh sách lưu tất cả các dự đoán
#     all_extracted_info = []  # Danh sách lưu tất cả các thông tin đã tách

#     for idx, uploaded_file in enumerate(uploaded_files):
#         image_path = uploaded_file.name
#         with open(image_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.image(image_path, caption=f"Ảnh gốc - {uploaded_file.name}", use_column_width=True)

#         # Xử lý ảnh
#         processor = ImageProcessor()
#         cropped_card = processor.crop_card(image_path)

#         if cropped_card is not None:
#             extracted_info = processor.crop_info_from_coordinates(cropped_card, all_coordinates)
#             predictions = predictor.predict_info(extracted_info)

#             st.write("Dự đoán:")
#             for label, pred in predictions.items():
#                 st.write(f"**{label.capitalize()}**: {pred}")

#             # Hiển thị các ảnh đã cắt
#             st.write("Các vùng đã tách:")
#             cols = st.columns(len(extracted_info))
#             for idx, (label, img) in enumerate(extracted_info.items()):
#                 with cols[idx]:
#                     st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption=label)

#             # Lưu kết quả vào danh sách (cập nhật thông tin vào file hiện có)
#             all_predictions.append(predictions)
#             all_extracted_info.append(extracted_info)

#         # Xóa ảnh sau khi xử lý
#         os.remove(image_path)

#     if all_predictions:
#         # Lưu kết quả vào file Word sau khi xử lý tất cả ảnh
#         byte_io = save_student_info_to_word(all_predictions, all_extracted_info)

#         # Tạo nút để tải file Word
#         st.download_button(
#             label="Tải file Word",
#             data=byte_io,
#             file_name="student_info.docx",
#             mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#             key="download_button"  
#         )
import streamlit as st
from image_processor import ImageProcessor, CoordinateLoader
from model_predictor import ModelPredictor
import cv2
from docx import Document
from docx.shared import Inches
import requests
import io
import zipfile
import os

# URL của file models.zip trên GitHub
MODEL_ZIP_URL = "https://github.com/tranhoang05/LTND/raw/master/models.zip"
EXTRACT_DIR = "models"  # Thư mục giải nén

# Tải và giải nén file ZIP chứa mô hình trực tiếp từ bộ nhớ tạm
def download_and_extract_models():
    # Tải file từ GitHub
    response = requests.get(MODEL_ZIP_URL)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        
        # In ra thông tin để kiểm tra
        extracted_files = os.listdir(EXTRACT_DIR)
        st.write(f"File đã được giải nén: {extracted_files}")
    else:
        st.error("Không thể tải file models.zip từ GitHub. Vui lòng kiểm tra URL.")

# Gọi hàm tải và giải nén mô hình
download_and_extract_models()

# Kiểm tra xem các mô hình đã có trong thư mục chưa
MODEL_PATHS = {
    'hoten': os.path.join(EXTRACT_DIR, 'svm_hoten.pkl'),
    'ngaysinh': os.path.join(EXTRACT_DIR, 'svm_ngaysinh.pkl'),
    'lop': os.path.join(EXTRACT_DIR, 'svm_lop.pkl'),
    'msv': os.path.join(EXTRACT_DIR, 'svm_masinhvien.pkl'),
    'nienkhoa': os.path.join(EXTRACT_DIR, 'svm_nienkhoa.pkl'),
    'anhthe': os.path.join(EXTRACT_DIR, 'svm_anhthe.pkl')
}

# Kiểm tra sự tồn tại của các mô hình
for model, path in MODEL_PATHS.items():
    if not os.path.exists(path):
        st.error(f"Không tìm thấy mô hình: {model} tại đường dẫn: {path}")
    else:
        st.write(f"Đã tải mô hình: {model} từ đường dẫn: {path}")

# Khởi tạo các đối tượng cần thiết
coordinate_loader = CoordinateLoader()
average_coordinates, max_hoten_box = coordinate_loader.load_coordinates_from_xml(
    r'training_data_segmentation/annotations.xml'
)
all_coordinates = coordinate_loader.get_all_coordinates(average_coordinates, max_hoten_box)

predictor = ModelPredictor(MODEL_PATHS)

# Hàm lưu thông tin sinh viên và ảnh thẻ vào file Word
def save_student_info_to_word(all_predictions, all_extracted_info):
    doc = Document()
    doc.add_heading("Thông tin Sinh viên", level=1)

    for idx, (predictions, extracted_info) in enumerate(zip(all_predictions, all_extracted_info), start=1):
        doc.add_heading(f"Thông tin Thẻ {idx}", level=2)

        doc.add_heading("Thông tin chi tiết:", level=3)
        for label, predicted_class in predictions.items():
            if label != "anhthe":
                doc.add_paragraph(f"{label.capitalize()}: {predicted_class}")

        if "anhthe" in extracted_info:
            doc.add_heading("Ảnh thẻ:", level=3)
            temp_buffer = io.BytesIO()
            success, encoded_image = cv2.imencode('.jpg', extracted_info["anhthe"])
            if success:
                temp_buffer.write(encoded_image)
                temp_buffer.seek(0)
                doc.add_picture(temp_buffer, width=Inches(2))

        doc.add_page_break()

    byte_io = io.BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io

# Streamlit UI
st.title("Đọc thông tin Sinh viên")

uploaded_files = st.file_uploader("Tải lên ảnh", type=["jpg", "png"], accept_multiple_files=True)
if uploaded_files:
    all_predictions = []
    all_extracted_info = []

    for uploaded_file in uploaded_files:
        image = uploaded_file.read()
        image_path = io.BytesIO(image)

        st.image(image_path, caption=f"Ảnh gốc - {uploaded_file.name}", use_column_width=True)

        processor = ImageProcessor()
        cropped_card = processor.crop_card(image_path)

        if cropped_card is not None:
            st.write("Đã cắt thẻ thành công.")
            extracted_info = processor.crop_info_from_coordinates(cropped_card, all_coordinates)
            if extracted_info:
                st.write("Đã tách thông tin thành công.")
                predictions = predictor.predict_info(extracted_info)
                if predictions:
                    st.write("Dự đoán thành công.")
                    for label, pred in predictions.items():
                        st.write(f"**{label.capitalize()}**: {pred}")

                    st.write("Các vùng đã tách:")
                    cols = st.columns(len(extracted_info))
                    for idx, (label, img) in enumerate(extracted_info.items()):
                        with cols[idx]:
                            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption=label)

                    all_predictions.append(predictions)
                    all_extracted_info.append(extracted_info)
                else:
                    st.error("Lỗi khi dự đoán thông tin.")
            else:
                st.error("Lỗi khi tách thông tin từ thẻ.")
        else:
            st.error("Lỗi khi cắt thẻ.")

    if all_predictions:
        byte_io = save_student_info_to_word(all_predictions, all_extracted_info)
        st.download_button(
            label="Tải file Word",
            data=byte_io,
            file_name="student_info.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
