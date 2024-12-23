from ultralytics import YOLO
import os
import glob

def auto_annotate(model_path, images_path, output_path):
    """
    Auto-annotate images using trained YOLO model
    
    model_path: Path to your trained model (best.pt)
    images_path: Path to folder containing images to annotate
    output_path: Where to save the annotation files
    """
    # Load your trained model
    model = YOLO(model_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Get all images
    image_files = glob.glob(os.path.join(images_path, '*.jpg'))  # Add other formats if needed
    
    # Process each image
    for img_path in image_files:
        # Get image filename without extension
        filename = os.path.basename(img_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Predict
        results = model(img_path)
        
        # Get the first result (since we only predict on one image)
        result = results[0]
        
        # Create YOLO format annotation file
        txt_path = os.path.join(output_path, f"{name_without_ext}.txt")
        
        with open(txt_path, 'w') as f:
            for box in result.boxes:
                # Get box coordinates in YOLO format
                x, y, w, h = box.xywhn[0].tolist()  # normalized coordinates
                # Class 0 since we have only one class
                f.write(f"0 {x} {y} {w} {h}\n")
        
        print(f"Processed {filename}")

if __name__ == "__main__":
    # Update these paths
    MODEL_PATH = "runs/detect/train/weights/best.pt"  # Path to your trained model
    IMAGES_PATH = "/home/thornch/Documents/Cpp/Kimbab_dataset/darknet_dataset_total_detected/images/train"  # Path to your remaining images
    OUTPUT_PATH = "/home/thornch/Documents/Cpp/Kimbab_dataset/darknet_dataset_total_detected/images/train"   # Where to save the annotation files
    
    auto_annotate(MODEL_PATH, IMAGES_PATH, OUTPUT_PATH)