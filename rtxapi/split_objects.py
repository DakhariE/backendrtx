import torch
from torchvision import models, transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
from PIL import Image
import os
import time
# Load a pre-trained Faster R-CNN model using the updated method
model = fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
model.eval()  # Set the model to evaluation mode

# Define the transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Mapping of COCO class IDs to human-readable names
coco_classes = {
    3: 'car',  
}

def load_and_preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image)
    return image, image_tensor

def detect_and_crop_specific_objects(image_path, threshold=0.8, margin=10, min_width=180, min_height=180):
    image, image_tensor = load_and_preprocess_image(image_path)
    predictions = model([image_tensor])[0]

    object_images = []
    for box, label, score in zip(predictions['boxes'], predictions['labels'], predictions['scores']):
        if score >= threshold and label.item() in coco_classes.keys():  # Check for keys in the coco_classes
            x1, y1, x2, y2 = box.tolist()
            x1, y1, x2, y2 = max(0, x1 - margin), max(0, y1 - margin), min(image.width, x2 + margin), min(image.height, y2 + margin)
            
            # Ensure the cropped image meets the minimum resolution requirement
            if (x2 - x1) >= min_width and (y2 - y1) >= min_height:
                cropped_image = image.crop((int(x1), int(y1), int(x2), int(y2)))
                object_images.append((cropped_image, label.item()))

    return object_images
#===============================End of the code========================================