import cv2
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
while True:
    success, img = cap.read()

    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    img = cv2.imread("Resources/lena.png")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break