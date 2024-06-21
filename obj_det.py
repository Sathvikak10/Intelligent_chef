import cv2
import imutils
import torch
import numpy as np
import sys
sys.path.insert(0, r'C:\Users\ADMIN\OneDrive\Projects\2024\Projects\Pix2Code\yolov7')

from hubconf import custom

class ObjectDetector:
    def __init__(self):
        print('Loading YOLOv7 weights')
        self.model = custom(path_or_model='best.pt')
        self.model.eval()
        self.class_names = ['Apple', 'Banana', 'Bottle gourd', 'Brinjal', 'Cabbage', 'Carrot', 'Cauliflower', 'Kiwi', 'Strawberry', 'Mango', 'Spinach', 'Tomato', 'Onion', 'Ladyfinger', 'Potato']

    def obj_detection(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        results = self.model([frame])
        frame = np.squeeze(results.render())
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame, results

    def crop_objects_by_name(self, results, frame, target_labels='', confidence_threshold=0.00):
        detections = results.xyxy[0].tolist()
        sorted_detections = sorted(detections, key=lambda x: x[0])
        filtered_detections = [d for d in sorted_detections if d[4] >= confidence_threshold]

        labels_summary = ""
        
        for detection in filtered_detections:
            x1, y1, x2, y2, conf, class_id = detection
            class_name = self.class_names[int(class_id)]
            #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            #cv2.putText(frame, class_name, (int(x1), int(y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            labels_summary += f'{class_name}, '

        cv2.imshow('Detected Objects', imutils.resize(frame,width=500))
        cv2.waitKey(1000)
        
        
        return labels_summary.strip(', ')

if __name__ == "__main__":
    detector = ObjectDetector()
    frame = cv2.imread('8.jpg')
    if frame is None:
        print("Failed to load image")
        sys.exit(1)

    frame, results = detector.obj_detection(frame)
    labels_summary = detector.crop_objects_by_name(results, frame)
    print("Detected Labels: ", labels_summary)
    cv2.destroyAllWindows()
