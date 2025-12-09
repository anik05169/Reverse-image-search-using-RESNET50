import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

class FeatureExtractor:
    def __init__(self):
        # 1. Load ResNet50 (Pre-trained)
        # We use CPU-friendly settings
        weights = models.ResNet50_Weights.DEFAULT
        self.model = models.resnet50(weights=weights)

        # 2. Slice the Model
        # Remove the last layer (Classification) to get the "Feature Vector"
        # The output will be 2048 dimensions
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        
        # 3. Evaluation Mode (No training, just inference)
        self.model.eval()

        # 4. Define Transform (Resize to 224x224, Normalize)
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract(self, img_path):
        """
        Input: Path to an image file.
        Output: List of 2048 floats.
        """
        try:
            # Convert to RGB to handle black/white images in Caltech dataset
            img = Image.open(img_path).convert('RGB')
            
            # Preprocess and create a mini-batch of size 1
            img_tensor = self.preprocess(img).unsqueeze(0)

            with torch.no_grad():
                vector = self.model(img_tensor)
            
            # Flatten to a simple list
            return vector.flatten().tolist()
        except Exception as e:
            print(f"Error reading {img_path}: {e}")
            return None