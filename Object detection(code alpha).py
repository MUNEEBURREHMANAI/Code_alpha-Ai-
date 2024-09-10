import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

# Load YOLO model and COCO labels
def load_yolo():
    net = cv2.dnn.readNet(r"c:\Users\munee\Downloads\weight config .zip", r"C:\Users\munee\Downloads\yolov config.zip")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    with open(r"C:\Users\munee\Downloads\coco names.zip", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes, output_layers

# Perform object detection
def detect_objects(img, net, output_layers):
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Perform Non-Maximum Suppression to remove duplicate bounding boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    return boxes, confidences, class_ids, indexes

# Draw bounding boxes and labels on detected objects
def draw_labels(img, boxes, confidences, class_ids, indexes, classes):
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, f"{label} {confidence}", (x, y - 5), font, 1, color, 2)

class VideoStreamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.net, self.classes, self.output_layers = load_yolo()

    def initUI(self):
        # Set up the layout and widgets
        self.setWindowTitle('Real-time Object Detection')
        self.setGeometry(100, 100, 800, 600)

        # Create label to display the video
        self.label = QLabel(self)
        self.label.setFixedSize(800, 600)
        self.label.setAlignment(Qt.AlignCenter)

        # Create buttons for start and stop
        self.startButton = QPushButton('Start Video', self)
        self.startButton.clicked.connect(self.start_video)

        self.stopButton = QPushButton('Stop Video', self)
        self.stopButton.clicked.connect(self.stop_video)

        # Layout arrangement
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)

        self.setLayout(layout)

    def start_video(self):
        # Start capturing video
        self.capture = cv2.VideoCapture(0)
        self.timer.start(20)  # Update every 20 ms

    def stop_video(self):
        # Stop the video stream
        self.timer.stop()
        if self.capture is not None:
            self.capture.release()

    def update_frame(self):
        # Read the frame from the video stream
        ret, frame = self.capture.read()
        if ret:
            # Perform object detection
            boxes, confidences, class_ids, indexes = detect_objects(frame, self.net, self.output_layers)
            draw_labels(frame, boxes, confidences, class_ids, indexes, self.classes)

            # Convert the frame to QImage for display in the PyQt5 label
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # Release video capture when the window is closed
        self.stop_video()
        event.accept()

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = VideoStreamApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
