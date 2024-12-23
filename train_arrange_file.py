import os
import shutil
import random
from pathlib import Path

def organize_dataset(source_path, output_path):
    """
    Organize dataset from a single folder into YOLO training structure
    
    source_path: Path to folder containing images and annotation files
    output_path: Path where organized dataset will be created
    """
    # Create required directories
    os.makedirs(f"{output_path}/images/train", exist_ok=True)
    os.makedirs(f"{output_path}/images/val", exist_ok=True)
    os.makedirs(f"{output_path}/labels/train", exist_ok=True)
    os.makedirs(f"{output_path}/labels/val", exist_ok=True)
    
    # Get all annotated images (those with corresponding .txt files)
    image_files = []
    for img_file in os.listdir(source_path):
        if img_file.endswith(('.jpg', '.jpeg', '.png')):
            txt_file = os.path.splitext(img_file)[0] + '.txt'
            if os.path.exists(os.path.join(source_path, txt_file)):
                image_files.append(img_file)
    
    # Randomly split into train/val (80/20 split)
    random.shuffle(image_files)
    split_idx = int(len(image_files) * 0.8)
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]
    
    # Copy training files
    for img_file in train_files:
        txt_file = os.path.splitext(img_file)[0] + '.txt'
        shutil.copy(
            os.path.join(source_path, img_file),
            os.path.join(output_path, 'images', 'train', img_file)
        )
        shutil.copy(
            os.path.join(source_path, txt_file),
            os.path.join(output_path, 'labels', 'train', txt_file)
        )
    
    # Copy validation files
    for img_file in val_files:
        txt_file = os.path.splitext(img_file)[0] + '.txt'
        shutil.copy(
            os.path.join(source_path, img_file),
            os.path.join(output_path, 'images', 'val', img_file)
        )
        shutil.copy(
            os.path.join(source_path, txt_file),
            os.path.join(output_path, 'labels', 'val', txt_file)
        )
    
    # Create data.yaml file
    yaml_content = f"""
train: {output_path}/images/train
val: {output_path}/images/val
nc: 1  # number of classes
names: ['sidedish']  # replace with your class name
"""
    
    with open(f"{output_path}/data.yaml", 'w') as f:
        f.write(yaml_content)
    
    print(f"Total images: {len(image_files)}")
    print(f"Training images: {len(train_files)}")
    print(f"Validation images: {len(val_files)}")

if __name__ == "__main__":
    # Change these paths to match your setup
    SOURCE_PATH = "/home/thornch/Documents/Cpp/Image_for_train/LargeData"  # Your current folder with images and txt files
    OUTPUT_PATH = "/home/thornch/Documents/Cpp/Image_after_organ/LargeData_Organ"  # Where to create the organized dataset
    
    organize_dataset(SOURCE_PATH, OUTPUT_PATH)