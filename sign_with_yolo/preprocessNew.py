import os
import shutil
import random
from tqdm import tqdm

# Parameters
source_dir = '/Users/dnahcirus/Desktop/sign with yolo/ASL_Dataset/Train'  # original dataset folder
output_dir = 'Sign_Language_Split'  # destination split folder
train_ratio = 0.8  # 80% train, 20% test

# Create output train/test folders
for split in ['train', 'test']:
    split_dir = os.path.join(output_dir, split)
    os.makedirs(split_dir, exist_ok=True)

# Process each class/category
for category in tqdm(os.listdir(source_dir), desc="Splitting data by category"):
    category_path = os.path.join(source_dir, category)
    if not os.path.isdir(category_path):
        continue

    images = os.listdir(category_path)
    random.shuffle(images)

    split_idx = int(len(images) * train_ratio)
    train_imgs = images[:split_idx]
    test_imgs = images[split_idx:]

    # Create category subfolders in train and test
    for split, split_imgs in [('train', train_imgs), ('test', test_imgs)]:
        split_category_path = os.path.join(output_dir, split, category)
        os.makedirs(split_category_path, exist_ok=True)
        
        for img_name in split_imgs:
            src_path = os.path.join(category_path, img_name)
            dst_path = os.path.join(split_category_path, img_name)
            shutil.copy2(src_path, dst_path)
