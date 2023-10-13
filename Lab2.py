import cv2
import numpy as np

# 1 - Видео в формате hsv
def hsv_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv_video', hsv_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

#hsv_video()

# 2 - Видео с фильтром красного цвета
def red_filter():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        _, result_frame = cv2.threshold(red_mask, 10, 255, cv2.THRESH_BINARY)
        cv2.imshow('RedFilter', result_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# 3 - Морфологические преобразования (открытие, закрытие)
def morph_change():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        _, result_frame = cv2.threshold(red_mask, 10, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)

        #erosion = cv2.erode(result_frame, kernel, iterations=1)
        #dilation = cv2.dilate(result_frame, kernel, iterations=1)
        opening = cv2.morphologyEx(result_frame, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(result_frame, cv2.MORPH_CLOSE, kernel)

        cv2.imshow('Original', result_frame)
        #cv2.imshow('Erosion', erosion)
        #cv2.imshow('Dilation', dilation)
        cv2.imshow('Opening', opening)
        cv2.imshow('Closing', closing)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
# 4, 5 - Нахождение моментов 1 порядка
def find_moments():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

        _, thresh = cv2.threshold(red_mask, 10, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        moments = cv2.moments(thresh, 1)
        dArea = moments['m00']
        if dArea > 10000:
            # print(dArea)
            max_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.drawContours(frame, contours, -1, (0, 0, 0), 2, cv2.LINE_AA, hierarchy, 1)

        cv2.imshow('Moments', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
find_moments()
