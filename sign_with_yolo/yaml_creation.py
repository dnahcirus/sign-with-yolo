import os

# Paths to your dataset directories
train_images_dir = r'/Users/dnahcirus/Desktop/sign with yolo/YOLO_dataset/train'
test_images_dir = r'/Users/dnahcirus/Desktop/sign with yolo/YOLO_dataset/test'  # updated from valid to test

# YAML file content
yaml_content = f"""
train: {train_images_dir}
val: {test_images_dir}

nc: 10

names: ['A',
   'B',
   'C',
   'D',
   'E',
   'F',
   'G',
   'H',
   'I',
   'J']
"""

# Create the dataset.yaml file
yaml_file_path = 'dataset.yaml'
with open(yaml_file_path, 'w') as f:
    f.write(yaml_content)

print(f"✅ YOLO dataset.yaml created at: {yaml_file_path}")
