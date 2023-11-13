import cv2
import numpy as np


def video():
    # cap = cv2.VideoCapture('videos/movie.mov')
    global old_frame
    cap = cv2.VideoCapture(0)
    first_frame = True

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("movements.mov", fourcc, 25, (w, h))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 1)
        if first_frame:
            first_frame = False
            old_frame = blurred_frame
        else:
            new_frame = cv2.absdiff(old_frame, blurred_frame)
            _, threshold = cv2.threshold(new_frame, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 100
            for contour in contours:
                if cv2.contourArea(contour) > min_contour_area:
                    video_writer.write(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

video()
