import os
import shutil
from pathlib import Path

def merge_dataset_folders(first_folder, second_folder, output_folder):
    """
    Merge two dataset folders by renaming files from the second folder to continue
    from the highest number in the first folder.
    """
    # Create output directory structure if it doesn't exist
    os.makedirs(output_folder + "/images/train", exist_ok=True)
    os.makedirs(output_folder + "/images/valid", exist_ok=True)
    os.makedirs(output_folder + "/labels/train", exist_ok=True)
    os.makedirs(output_folder + "/labels/valid", exist_ok=True)
    
    # Find highest number in first folder
    highest_num = -1
    for subset in ['train', 'valid']:
        image_path = Path(first_folder) / 'images' / subset
        if image_path.exists():
            for file in image_path.glob('*.jpg'):
                try:
                    num = int(file.stem)
                    highest_num = max(highest_num, num)
                except ValueError:
                    continue
    
    print(f"Highest number in first folder: {highest_num}")
    next_num = highest_num + 1
    
    # Copy files from first folder to output
    for subset in ['train', 'valid']:
        # Copy images
        src_img_path = Path(first_folder) / 'images' / subset
        dst_img_path = Path(output_folder) / 'images' / subset
        if src_img_path.exists():
            for file in src_img_path.glob('*.jpg'):
                shutil.copy2(file, dst_img_path)
        
        # Copy labels
        src_label_path = Path(first_folder) / 'labels' / subset
        dst_label_path = Path(output_folder) / 'labels' / subset
        if src_label_path.exists():
            for file in src_label_path.glob('*.txt'):
                shutil.copy2(file, dst_label_path)
    
    # Process second folder
    for subset in ['train', 'valid']:
        # Process images
        src_img_path = Path(second_folder) / 'images' / subset
        dst_img_path = Path(output_folder) / 'images' / subset
        if src_img_path.exists():
            for file in sorted(src_img_path.glob('*.jpg')):
                new_name = f"{next_num}.jpg"
                shutil.copy2(file, dst_img_path / new_name)
                
                # Copy corresponding label if it exists
                label_file = Path(second_folder) / 'labels' / subset / f"{file.stem}.txt"
                if label_file.exists():
                    new_label_name = f"{next_num}.txt"
                    shutil.copy2(label_file, Path(output_folder) / 'labels' / subset / new_label_name)
                
                next_num += 1
                print(f"Renamed {file.name} to {new_name}")

    print(f"\nMerge complete! Files from second folder start from number {highest_num + 1}")
    print(f"Total files after merge: {next_num - 1}")

if __name__ == "__main__":
    # Get folder paths from user
    # first_folder = input("Enter path to first dataset folder: ")
    first_folder = "/home/thornch/Documents/Cpp/Kimbab_dataset/darknet_dataset_capture"
    # second_folder = input("Enter path to second dataset folder: ")
    second_folder = "/home/thornch/Documents/Cpp/Kimbab_dataset/darknet_dataset_capture_first"
    # output_folder = input("Enter path for merged dataset: ")
    output_folder = "/home/thornch/Documents/Cpp/Kimbab_dataset/darknet_dataset_total"
    
    merge_dataset_folders(first_folder, second_folder, output_folder)