import cv2
import numpy as np
import utils

curveList = []
avgVal = 10
initialTrackBarVals = [148,268,17,458]
initialColorVals = [0, 0, 0, 179, 255, 47]
utils.initializeTrackbars(initialTrackBarVals)
utils.colorpickupTrackbars(initialColorVals)

def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utils.thresholding(img)

    #### STEP 2
    hT, wT, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThres, points, wT, hT)
    imgWarp1 = utils.warpImg(img, points, wT, hT)
    imgWarpPoints = utils.drawPoints(imgCopy, points)

    #### STEP 3
    middlePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    #### STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    #### STEP 5
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        if curve>5: direction = "-->"
        elif curve<-5: direction = "<--"
        else: direction = "^"
        cv2.putText(imgResult, str(curve)+direction, (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imgWarpPoints, imgWarp1],
                                             [imgHist, imgWarp, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve