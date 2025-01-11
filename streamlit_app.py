import streamlit as st
from image_processor import ImageProcessor, CoordinateLoader
from model_predictor import ModelPredictor
import cv2
from docx import Document
from docx.shared import Inches
import os
import io

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
import gdown
import os
from io import BytesIO
from image_processor import ImageProcessor, CoordinateLoader
from model_predictor import ModelPredictor
# URL của các file mô hình trên Google Drive (ID của từng file)
MODEL_DRIVE_URLS = {
    'hoten': 'https://drive.google.com/file/d/1eF0Q6QrPkkeGGj4SExdKFwMsG-4ibUTD/view?usp=drive_link',
    'ngaysinh': 'https://drive.google.com/file/d/1yYhMuHjiGNAoQyXmJLC4Gi8mJhGY5riO/view?usp=drive_link',
    'lop': 'https://drive.google.com/file/d/1hzPf0VZl2XDanxEDdI4IrgVAPZlwBQn6/view?usp=drive_link',
    'msv': 'https://drive.google.com/file/d/1ukMYv7nh7RXL9bCFYW5NTuCh9XLFq0kD/view?usp=drive_link',
    'nienkhoa': 'https://drive.google.com/file/d/1a5gBFvHw4CINNFJy-X-ugGf_u3Bigbmp/view?usp=drive_link',
    'anhthe': 'https://drive.google.com/file/d/1Gax9ChzEy1lw983cF_wM8TfBTcADErDr/view?usp=drive_link'
}

EXTRACT_DIR = "models"  # Thư mục giải nén

# Tải mô hình từ Google Drive và giải nén
def download_and_extract_models():
    for label, url in MODEL_DRIVE_URLS.items():
        output_path = os.path.join(EXTRACT_DIR, f'svm_{label}.pkl')
        if not os.path.exists(output_path):  # Tải và giải nén mô hình nếu chưa có
            gdown.download(url, output_path, quiet=False)
            st.write(f"Đã tải mô hình {label} thành công từ Google Drive.")
        else:
            st.write(f"Mô hình {label} đã có sẵn.")

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

for model, path in MODEL_PATHS.items(): 
    if os.path.exists(path): 
        print(f"File mô hình {model} tồn tại tại đường dẫn: {path}") 
    else: 
        print(f"Không tìm thấy file mô hình {model} tại đường dẫn: {path}")

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
