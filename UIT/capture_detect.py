import subprocess
import cv2
import numpy as np
from ultralytics import YOLO
import os
from datetime import datetime
import time

# Initialize YOLOv8 model (nano for Pi compatibility)
model = YOLO("yolov8n.pt")  # Download from Ultralytics if not already present

# Directory to save captured images and results
output_dir = "captured_images"
os.makedirs(output_dir, exist_ok=True)

def capture_image():
    """Capture an image using Canon 1300D via gphoto2 with retries."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(output_dir, f"image_{timestamp}.jpg")
    
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Capture image and save to specified path
            subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", image_path], check=True)
            print(f"Image captured: {image_path}")
            return image_path
        except subprocess.CalledProcessError as e:
            print(f"Error capturing image (attempt {attempt + 1}): {e}")
            time.sleep(2)  # Wait before retrying
    print("Failed to capture image after retries.")
    return None

def run_detection(image_path):
    """Run object detection on the captured image."""
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}. Ensure it's a valid JPEG.")
        return
    
    # Perform detection
    results = model(img)
    
    # Plot results (draw bounding boxes)
    annotated_img = results[0].plot()  # YOLOv8's built-in plotting with boxes and labels
    
    # Save the result
    result_path = image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(result_path, annotated_img)
    print(f"Detection result saved: {result_path}")

def main():
    """Main loop to capture and process images."""
    print("Press 'q' to quit or any other key to capture an image.")
    while True:
        key = input("Capture image? (q to quit): ").lower()
        if key == 'q':
            break
        
        # Capture image
        image_path = capture_image()
        if image_path:
            # Run detection
            run_detection(image_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
