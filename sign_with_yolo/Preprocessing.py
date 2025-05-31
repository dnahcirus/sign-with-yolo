import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from tqdm import tqdm
import random

# Define categories and their class IDs
class_mapping = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9
}

# Convert bounding box to YOLO format
def convert_bbox_to_yolo_format(bbox, img_width, img_height):
    x_min, y_min, x_max, y_max = bbox
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height

# Preprocess and augment image
def preprocess_image(pil_img):
    # Resize to 256x256
    pil_img = pil_img.resize((400, 400))

    # Random horizontal flip
    #if random.random() < 0.5:
        #pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)

    # Random brightness adjustment
    if random.random() < 0.5:
        enhancer = ImageEnhance.Brightness(pil_img)
        factor = random.uniform(0.8, 1.2)
        pil_img = enhancer.enhance(factor)

    # Random rotation (±15 degrees)
    #if random.random() < 0.5:
        #angle = random.uniform(-15, 15)
        #pil_img = pil_img.rotate(angle)

    # Convert to OpenCV BGR format (PIL is RGB)
    img_array = np.array(pil_img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    return img_array

# Process dataset
def process_dataset(dataset_dir, output_dir):
    for category in tqdm(class_mapping, desc=f"📁 Processing categories in {dataset_dir}"):
        category_dir = os.path.join(dataset_dir, category)
        if not os.path.isdir(category_dir):
            print(f"[WARN] Directory not found: {category_dir}")
            continue

        images = [img for img in os.listdir(category_dir) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

        for image_name in tqdm(images, desc=f"🖼️  {category}", leave=False):
            img_path = os.path.join(category_dir, image_name)

            try:
                pil_img = Image.open(img_path).convert("RGB")
                img = preprocess_image(pil_img)
            except Exception as e:
                print(f"[ERROR] Failed to process image {img_path}: {e}")
                continue

            img_height, img_width, _ = img.shape

            # Bounding box covers entire image
            face_bbox = [0, 0, img_width, img_height]
            yolo_bbox = convert_bbox_to_yolo_format(face_bbox, img_width, img_height)

            # Write YOLO annotation
            txt_filename = os.path.splitext(image_name)[0] + '.txt'
            txt_filepath = os.path.join(output_dir, txt_filename)
            with open(txt_filepath, 'w') as f:
                f.write(f"{class_mapping[category]} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}\n")

            # Save preprocessed image
            output_img_path = os.path.join(output_dir, image_name)
            cv2.imwrite(output_img_path, img)

# === Main Setup ===
base_dir = 'Sign_Language_Split'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')

yolo_dataset_dir = 'YOLO_dataset'
train_output_dir = os.path.join(yolo_dataset_dir, 'train')
test_output_dir = os.path.join(yolo_dataset_dir, 'test')

os.makedirs(train_output_dir, exist_ok=True)
os.makedirs(test_output_dir, exist_ok=True)

# Run processing
process_dataset(train_dir, train_output_dir)
process_dataset(test_dir, test_output_dir)