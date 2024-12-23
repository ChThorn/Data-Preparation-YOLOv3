import os

def fix_annotations(labels_dir):
    """Fix annotation files by changing class 15 to class 0"""
    # Go through all txt files in the directory
    for filename in os.listdir(labels_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(labels_dir, filename)
            
            # Read the file
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Fix the lines
            fixed_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:  # Make sure line has all parts
                    parts[0] = '0'  # Change class id from 15 to 0
                    fixed_lines.append(' '.join(parts) + '\n')
            
            # Write back to file
            with open(filepath, 'w') as f:
                f.writelines(fixed_lines)

if __name__ == "__main__":
    # Fix training set annotations
    train_labels = "/home/thornch/Documents/Cpp/Image_after_organ/labels/train"
    val_labels = "/home/thornch/Documents/Cpp/Image_after_organ/labels/val"
    
    print("Fixing training annotations...")
    fix_annotations(train_labels)
    print("Fixing validation annotations...")
    fix_annotations(val_labels)
    print("Done!")