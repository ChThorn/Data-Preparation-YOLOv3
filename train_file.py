import torch
from ultralytics import YOLO
import yaml

def train_yolo(dataset_path):
    """
    Train YOLOv5 model on the organized dataset
    
    dataset_path: Path to the organized dataset containing data.yaml
    """
    # Initialize YOLO model
    model = YOLO('yolov5s.pt')  # Load pretrained YOLOv5s model
    
    # Training configuration
    config = {
        'epochs': 100,          # Number of training epochs
        'batch': 16,           # Batch size
        'imgsz': 640,         # Image size
        'patience': 20,       # Early stopping patience
        'save_period': 10,    # Save checkpoint every X epochs
        'cache': True,        # Cache images for faster training
        'device': 0 if torch.cuda.is_available() else 'cpu'  # Use GPU if available
    }
    
    # Start training
    try:
        results = model.train(
            data=f"{dataset_path}/data.yaml",
            epochs=config['epochs'],
            batch=config['batch'],
            imgsz=config['imgsz'],
            patience=config['patience'],
            save_period=config['save_period'],
            cache=config['cache'],
            device=config['device']
        )
        
        print("Training completed successfully!")
        print(f"Best model saved at: {results.save_dir}")
        return results
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return None

if __name__ == "__main__":
    # Path to your organized dataset
    DATASET_PATH = "/home/thornch/Documents/Cpp/Image_after_organ"  # Change this to your dataset path
    
    # Train the model
    results = train_yolo(DATASET_PATH)