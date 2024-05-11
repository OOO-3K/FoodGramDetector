import numpy as np
import cv2
from ultralytics import YOLO
from .apps import DetectorConfig

def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances.keys():
            instances[cls] = cls(*args, **kwargs)   
        return instances[cls]
    
    return get_instance

@singleton
class FoodDetector:
    def __init__(self):
        self.model = YOLO(f'{DetectorConfig.name}/models/yolov8m.pt')
        self.names = self.model.names
    
    def __call__(self, img):
        if type(img) is str:
            img = cv2.imread(img)
        results = self.model(
            img,
            imgsz=(640, 640),
            save=False,
        )
        classes = results[0].boxes.cls.cpu().numpy()
        classes = list(set(map(int, classes)))
        return [self.names[cls] for cls in classes]
            