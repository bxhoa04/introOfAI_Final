import os
from PIL import Image

# Đường dẫn tới thư mục chứa ảnh và nhãn
images_path = "D:\\Introduction for AI\\AIFinal\\data\\Lung_CT_Scan\\valid\\images"
labels_path = "D:\\Introduction for AI\\AIFinal\\data\\Lung_CT_Scan\\valid\\labels"
output_path = "D:\\Introduction for AI\\AIFinal\\data\\validCNN_LungCT_crop"

os.makedirs(output_path, exist_ok=True)

for label_file in os.listdir(labels_path):
    if label_file.endswith(".txt"):
        label_path = os.path.join(labels_path, label_file)
        image_file = label_file.replace(".txt", ".jpg")
        image_path = os.path.join(images_path, image_file)
        with Image.open(image_path) as img:
            img_width, img_height = img.size

            with open(label_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    class_name = parts[0]

                    x_center = float(parts[1]) * img_width
                    y_center = float(parts[2]) * img_height
                    box_width = float(parts[3]) * img_width
                    box_height = float(parts[4]) * img_height

                    x_min = int(x_center - box_width / 2)
                    y_min = int(y_center - box_height / 2)
                    x_max = int(x_center + box_width / 2)
                    y_max = int(y_center + box_height / 2)

                    if x_max > x_min and y_max > y_min:
                        cropped_img = img.crop((x_min, y_min, x_max, y_max))
                        class_folder = os.path.join(output_path, class_name)
                        os.makedirs(class_folder, exist_ok=True)

                        cropped_img.save(os.path.join(class_folder, f"{label_file}_{x_min}_{y_min}.jpg"))
                    else:
                        print(f"Bounding box không hợp lệ trong file {label_file}: x_max <= x_min hoặc y_max <= y_min")