import cv2

class VideoCapture:
    def __init__(self, device=0, size=[640,480]):
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def get_frame(self, display=False):
        _, img = self.cap.read()
        if display:
            cv2.imshow('IMG', img)
        return img

if __name__ == '__main__':
    vc = VideoCapture()
    while True:
        img = vc.get_frame(True)
