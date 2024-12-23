import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MatrixOperator:
    def __init__(self, image_path):
        self.image_path = Path(image_path)
        self.img = self._load_image()
        self.gray_img = None
        self.rows = None
        self.cols = None
        
    def _load_image(self):
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file not found: {self.image_path}")
        img = cv2.imread(str(self.image_path))
        if img is None:
            raise ValueError(f"Failed to load image: {self.image_path}")
        return img
    
    def prepare_image(self):
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.rows, self.cols = self.gray_img.shape
        return self.gray_img

    def scaling(self, image, scale_factor=2.0):
        """Scale the image up by a factor of 2."""
        return cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    def rotating(self, image, angle=45):
        """Rotate the image by 45 degrees."""
        matrix = cv2.getRotationMatrix2D((self.cols/2, self.rows/2), angle, 1)
        return cv2.warpAffine(image, matrix, (self.cols, self.rows))

    def translating(self, image, dx=50, dy=30):
        """Translate the image."""
        matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        return cv2.warpAffine(image, matrix, (self.cols, self.rows))

    def inverse_scaling(self, image):
        """Scale the image down by a factor of 0.5 (inverse of scaling up)."""
        return cv2.resize(image, None, fx=0.5, fy=0.5)

    def apply_operations(self):
        """Apply basic matrix operations."""
        if self.gray_img is None:
            self.prepare_image()

        operations = {
            'Original': self.gray_img,
            'Scaling (2x)': self.scaling(self.gray_img),
            'Rotation (45°)': self.rotating(self.gray_img),
            'Translation': self.translating(self.gray_img),
            'Inverse Scaling (0.5x)': self.inverse_scaling(self.gray_img)
        }
        return operations

    def plot_operations(self, save_path=None):
        """Plot the matrix operations."""
        operations = self.apply_operations()
        
        # Create figure
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.ravel()
        
        # Plot each operation
        for idx, (name, img) in enumerate(operations.items()):
            if idx < len(axes):
                axes[idx].imshow(img, cmap='gray')
                axes[idx].set_title(name, fontsize=12, pad=10)
                axes[idx].axis('off')
        
        # Remove extra subplot if any
        if len(operations) < len(axes):
            for idx in range(len(operations), len(axes)):
                fig.delaxes(axes[idx])
        
        plt.suptitle('Basic Matrix Operations', fontsize=16, y=0.95)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved operations plot to {save_path}")
        else:
            plt.show()
        
        plt.close()

def main():
    try:
        operator = MatrixOperator('./tiger.jpg')
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        operator.plot_operations(output_dir / 'matrix_operations.png')
        logger.info("Matrix operations completed successfully!")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise

if __name__ == "__main__":
    main()