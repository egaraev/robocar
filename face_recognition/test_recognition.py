from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

currentname = "unknown"
encodingsP = "encodings.pickle"
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
vs = VideoStream(usePiCamera=False).start()
time.sleep(2.0)
fps = FPS().start()

# Add a counter and set the skip value
counter = 0
skip_frames = 20

while True:
    frame = vs.read()

    frame = imutils.resize(frame, width=500)
    boxes = face_recognition.face_locations(frame)
    fps.update()
    #prev_names =[]
    # Only perform face recognition when the counter is equal to 0
    if counter == 0:
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                if currentname != name:
                    currentname = name
                    print(currentname)
            names.append(name)
    else:
        # If the counter is not 0, use the previous names list
        names = prev_names

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit when 'q' key is pressed
    if key == ord("q"):
        break

    # Increment the counter and store the names list
    counter += 1
    prev_names = names.copy()

    # If the counter reaches the skip frames value, reset it to 0
    if counter == skip_frames:
        counter = 0

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
