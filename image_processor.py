import cv2
import xml.etree.ElementTree as ET

class ImageProcessor:
    @staticmethod
    def crop_card(image_path):
        try:
            img = cv2.imread(image_path)
            if img is None:
                print(f"Lỗi khi đọc ảnh từ {image_path}")
                return None

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                print(f"Không tìm thấy contour trong ảnh {image_path}")
                return None

            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cropped_img = img[y:y + h, x:x + w]
            cropped_img = cv2.resize(cropped_img, (1500, 1100))

            return cropped_img
        except Exception as e:
            print(f"Lỗi khi tách thẻ: {e}")
            return None

    @staticmethod
    def crop_info_from_coordinates(image, coordinates):
        try:
            extracted_info = {}
            for item in coordinates:
                label = item['label']
                top_left = tuple(map(int, item['top_left']))
                bottom_right = tuple(map(int, item['bottom_right']))
                x1, y1 = top_left
                x2, y2 = bottom_right

                if x1 < 0 or y1 < 0 or x2 > image.shape[1] or y2 > image.shape[0]:
                    print(f"Vùng cắt {label} nằm ngoài ảnh!")
                    continue

                cropped_info = image[y1:y2, x1:x2]
                if cropped_info.size == 0:
                    print(f"Vùng cắt {label} không có dữ liệu!")
                    continue

                extracted_info[label] = cropped_info
            return extracted_info
        except Exception as e:
            print(f"Lỗi khi tách thông tin: {e}")
            return None


class CoordinateLoader:
    @staticmethod
    def load_coordinates_from_xml(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        total_coordinates = {}
        total_boxes = {}
        max_hoten_box = None
        max_hoten_area = -float('inf')

        for image in root.findall('image'):
            for box in image.findall('box'):
                label = box.get('label')
                xtl = float(box.get('xtl'))
                ytl = float(box.get('ytl'))
                xbr = float(box.get('xbr'))
                ybr = float(box.get('ybr'))

                if label not in total_coordinates:
                    total_coordinates[label] = {
                        'top_left_x': 0, 'top_left_y': 0, 'top_right_x': 0, 'top_right_y': 0,
                        'bottom_left_x': 0, 'bottom_left_y': 0, 'bottom_right_x': 0, 'bottom_right_y': 0,
                    }
                    total_boxes[label] = 0

                total_coordinates[label]['top_left_x'] += xtl
                total_coordinates[label]['top_left_y'] += ytl
                total_coordinates[label]['top_right_x'] += xbr
                total_coordinates[label]['top_right_y'] += ytl
                total_coordinates[label]['bottom_left_x'] += xtl
                total_coordinates[label]['bottom_left_y'] += ybr
                total_coordinates[label]['bottom_right_x'] += xbr
                total_coordinates[label]['bottom_right_y'] += ybr
                total_boxes[label] += 1

                if label == 'hoten':
                    area = (xbr - xtl) * (ybr - ytl)
                    if area > max_hoten_area:
                        max_hoten_area = area
                        max_hoten_box = (xtl, ytl, xbr, ybr)

        average_coordinates = {}
        for label, coords in total_coordinates.items():
            avg_top_left_x = coords['top_left_x'] / total_boxes[label]
            avg_top_left_y = coords['top_left_y'] / total_boxes[label]
            avg_top_right_x = coords['top_right_x'] / total_boxes[label]
            avg_top_right_y = coords['top_right_y'] / total_boxes[label]
            avg_bottom_left_x = coords['bottom_left_x'] / total_boxes[label]
            avg_bottom_left_y = coords['bottom_left_y'] / total_boxes[label]
            avg_bottom_right_x = coords['bottom_right_x'] / total_boxes[label]
            avg_bottom_right_y = coords['bottom_right_y'] / total_boxes[label]

            average_coordinates[label] = {
                'top_left': (avg_top_left_x, avg_top_left_y),
                'top_right': (avg_top_right_x, avg_top_right_y),
                'bottom_left': (avg_bottom_left_x, avg_bottom_left_y),
                'bottom_right': (avg_bottom_right_x, avg_bottom_right_y)
            }

        return average_coordinates, max_hoten_box

    def get_all_coordinates(self, average_coordinates, max_hoten_box):
        all_coordinates = []
        for label, coords in average_coordinates.items():
            if label != 'hoten':
                all_coordinates.append({
                    'label': label,
                    'top_left': coords['top_left'],
                    'top_right': coords['top_right'],
                    'bottom_left': coords['bottom_left'],
                    'bottom_right': coords['bottom_right']
                })
        all_coordinates.append({
            'label': 'hoten',
            'top_left': (max_hoten_box[0], max_hoten_box[1]),
            'top_right': (max_hoten_box[2], max_hoten_box[1]),
            'bottom_left': (max_hoten_box[0], max_hoten_box[3]),
            'bottom_right': (max_hoten_box[2], max_hoten_box[3])
        })
        return all_coordinates
