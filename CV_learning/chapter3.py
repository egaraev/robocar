import cv2

img = cv2.imread("Resources/lambo.jpg")
print(img.shape)

imgResize = cv2.resize(img,(200,100))

imgCropped = img[0:150, 150:300]



cv2.imshow("Image", img)
#cv2.imshow("Image resized", imgResize)
cv2.imshow("Image cropped", imgCropped)

cv2.waitKey(0)