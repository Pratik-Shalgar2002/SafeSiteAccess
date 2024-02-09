from ultralytics import YOLO
import cv2
import cvzone
import math
import sys
import time
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = YOLO("../Yolo-weights/best.pt")
classNames = ['Gloves', 'Helmet', 'Non-Helmet', 'Person', 'Shoes', 'Vest', 'bare-arms']
myColor = (0, 0, 255)

# Boolean variable for PPE detection
ppe_detection = False

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # BoundingBox
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.5:
                if currentClass == 'bare-arms' or currentClass == 'Non-Helmet':
                    myColor = (0, 0, 255)
                elif currentClass == 'Gloves' or currentClass == 'Helmet' or currentClass == "Vest":
                    myColor = (0, 255, 0)

                    # Check for Helmet and Vest detection
                    if currentClass == 'Helmet':
                        helmet_detected = True
                    elif currentClass == 'Vest':
                        vest_detected = True

                    # Check if both Helmet and Vest are detected
                    if 'helmet_detected' in locals() and 'vest_detected' in locals():
                        ppe_detection = True
                        # Close the program
                        time.sleep(3)
                        sys.exit()

                else:
                    myColor = (255, 0, 0)

                cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                                   (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor, colorT=(255, 255, 255),
                                   colorR=myColor, offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
