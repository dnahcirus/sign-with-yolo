import cv2
import os
from ultralytics import YOLO
import torch

# Check Apple MPS
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
print(f"Using device: {device}")

# Load model
model = YOLO('/Users/dnahcirus/Desktop/Technical Project/sign with yolo/sign_detection_project2/yolov8_sign_detection/weights/best.pt')

# Class names and colors
class_names = [
    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J'
]

colors = {
    'A': (0, 255, 0),
    'B': (255, 255, 0),
    'C': (255, 0, 255),
    'D': (0, 128, 255),
    'E': (255, 128, 0),
    'F': (128, 0, 255),
    'G': (0, 255, 255),
    'H': (0, 100, 255),
    'I': (128, 255, 0),
    'J': (0, 0, 255)
}

# Predict on a single image
def predict_image(image_path, model):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Error reading image: {image_path}")
        return

    results = model(image, conf=0.25)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        label_index = int(box.cls[0])

        category = class_names[label_index]
        label_text = f"{category} ({confidence:.2f})"
        box_color = colors.get(category, (255, 255, 255))

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)

        # Bottom-aligned label
        font_scale = 7.0
        thickness = 7
        (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        text_x = x1
        text_y = y2 + text_height + 10

        if text_y + 5 > image.shape[0]:
            text_y = y2 - 10  # Move label above if too close to bottom

        bg_start = (text_x, text_y - text_height - 10)
        bg_end = (text_x + text_width + 10, text_y)
        cv2.rectangle(image, bg_start, bg_end, (0, 0, 0), -1)
        cv2.putText(image, label_text, (text_x + 5, text_y - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

    cv2.imshow(f"Prediction - {os.path.basename(image_path)}", image)
    print(f"🔍 Showing: {os.path.basename(image_path)} - Press any key for next")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# === Predict on images in a folder ===
image_folder = "/Users/dnahcirus/Desktop/Technical Project/sign with yolo/imgPred"
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png',))][:20]

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    predict_image(image_path, model)
