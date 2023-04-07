import cv2
import os
import datetime

class VideoCapture:
    def __init__(self, device=0, size=[640, 480]):
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def get_frame(self, display=False):
        _, img = self.cap.read()
        if display:
            cv2.imshow('IMG', img)
        return img

def save_image_with_timestamp(img, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, img)
    print(f"Image saved as {filepath}")

if __name__ == '__main__':
    vc = VideoCapture()
    img = vc.get_frame()
    save_image_with_timestamp(img, "captured_images")
