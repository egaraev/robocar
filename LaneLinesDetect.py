import cv2
import numpy as np
import warnings
from numpy import RankWarning
import math
curveList = []
wT = 0
avgVal = 10
curr_steering_angle = 0


def display_heading_line(frame, curve, line_color=(0, 0, 255), line_width=5):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    # Convert curve back to angle in radians
    steering_angle_radian = (curve + 1) * math.pi

    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 * math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image



def compute_steering_angle(frame, lane_lines):
    if len(lane_lines) == 0:
        print('No lane lines detected, do nothing')
        return 0

    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        print('Only detected one lane line, just follow it. %s' % lane_lines[0])
        x1, _, x2, _ = lane_lines[0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0]
        _, _, right_x2, _ = lane_lines[1]
        camera_mid_offset_percent = 0.02
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)
    steering_angle = angle_to_mid_deg + 90

    #print('Steering angle: %s' % steering_angle)

    # Normalize steering angle to a value between -1 and 1
    curve_value = (steering_angle - 90) / 90
    return curve_value


def make_points(image, line):
    slope, intercept = line
    y1 = int(image.shape[0])  # bottom of the image
    y2 = int(y1 * 3 / 5)  # slightly lower than the middle
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            min_slope_threshold = 0.5  # Adjust this value based on your input image
            if abs(slope) > min_slope_threshold:
                if slope < 0:  # y is reversed in image
                    left_fit.append((slope, intercept))
                else:
                    right_fit.append((slope, intercept))
        if not left_fit or not right_fit:
            return None
        # add more weight to longer lines
        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line = make_points(image, left_fit_average)
        right_line = make_points(image, right_fit_average)
        averaged_lines = [left_line, right_line]
        return averaged_lines

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    canny = cv2.Canny(blur, 50, 350)
    return canny


def display_lines (image, lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image



def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[
        (0, height), (950, height), (475, 200)
    ]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def getLineCurve(frame):
    global curr_steering_angle
    height, width, _ = frame.shape
    wT = width
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=7)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)

    if averaged_lines is not None:
        curveRaw = compute_steering_angle(frame, averaged_lines)
        curveList.append(curveRaw)
        if len(curveList) > avgVal:
            curveList.pop(0)
        normal_angle = (sum(curveList) / len(curveList))*100
    else:
        normal_angle = 0

    # Add this block of code to call the stabilize_steering_angle function
    num_of_lane_lines = len(averaged_lines) if averaged_lines is not None else 0
    stabilized_angle = stabilize_steering_angle(curr_steering_angle, normal_angle, num_of_lane_lines)
    curve = stabilized_angle
    curr_steering_angle = stabilized_angle

    imgResult = frame
    midY = 450
    if curve > 0.5: direction = "-->"
    elif curve < -0.5: direction = "<--"
    else: direction = "^"
    curve = curve/100
    normal_angle = (sum(curveList) / len(curveList)) * 100
    cv2.putText(imgResult,  str(int(curve*1000)) + direction, (wT // 2 - 80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (int(curve) * 3), midY), (255, 0, 255), 5)
    cv2.line(imgResult, ((wT // 2 + (int(curve) * 3)), midY - 25), (wT // 2 + (int(curve) * 3), midY + 25), (0, 255, 0), 5)
    for x in range(-30, 30):
        w = wT // 20
        cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                 (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
    #cv2.putText(imgResult, 'Normal Angle: ' + str(int(normal_angle)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    #cv2.putText(imgResult, 'Stabilized Angle: ' + str(int(stabilized_angle)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    combo_image = display_heading_line(combo_image, curve)
    cv2.imshow("result", combo_image)

    return curve

def stabilize_steering_angle(curr_steering_angle, new_steering_angle, num_of_lane_lines, max_angle_deviation_two_lines=4, max_angle_deviation_one_lane=0.5):
    if num_of_lane_lines == 2 :
        # if both lane lines detected, then we can deviate more
        max_angle_deviation = max_angle_deviation_two_lines
    else:
        # if only one lane detected, don't deviate too much
        max_angle_deviation = max_angle_deviation_one_lane

    angle_deviation = new_steering_angle - curr_steering_angle
    if abs(angle_deviation) > max_angle_deviation:
        stabilized_steering_angle = int(curr_steering_angle
                                        + max_angle_deviation * angle_deviation / abs(angle_deviation))
    else:
        stabilized_steering_angle = new_steering_angle
    #print('Proposed angle: %s, stabilized angle: %s' % (new_steering_angle, stabilized_steering_angle))
    return stabilized_steering_angle


def main():
    # Ignore RankWarning
    warnings.simplefilter("ignore", RankWarning)
    cap = cv2.VideoCapture(0)  # Open the default camera, set it to 1 or 2 if you have multiple cameras
    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print("Failed to capture frame. Exiting.")
            break
        getLineCurve(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):  # Press "q" to exit the loop
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()