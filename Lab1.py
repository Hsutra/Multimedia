import cv2
import numpy as np

# № 2, 5 - Чтение изображения

def show_image(window, color):
    image = cv2.imread('C:/Users/artus/PycharmProjects/MultiMedia/pictures/mount-pic.jpg', color)
    hsvimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.namedWindow('image', window)
    cv2.namedWindow('image2', window)
    cv2.imshow('image', image)
    cv2.imshow('image2', hsvimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#show_image(cv2.WINDOW_NORMAL, 1)
#show_image(cv2.WINDOW_AUTOSIZE, 0)
#show_image(cv2.WINDOW_FREERATIO, 4)


# №3, 9 - Видео c камеры

def show_camera(color):
    url = 'http://192.168.43.28:8080/video'
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        colored = cv2.cvtColor(frame, color)
        cv2.imshow('camera', colored)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
show_camera(cv2.COLOR_BGR2GRAY)

# №4 - Запись видео в файл
def ReadVidToFile():
    video = cv2.VideoCapture(0)
    ok, image = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter('output3.mov', fourcc, 25, (w, h))
    while True:
        ok, img = video.read()
        cv2.imshow('img', img)
        video_writer.write(img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()

#ReadVidToFile()

#6 - Крест с размытием

def draw_cross():
    image = cv2.imread('C:/Users/artus/PycharmProjects/MultiMedia/pictures/mount-pic.jpg')
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    height, width, _ = image.shape

    center_x = width // 2
    center_y = height // 2

    cross_size = 200
    cross_thickness = 60
    red_color = (0, 0, 255)

    # горизонтальный прямоугольник
    cv2.rectangle(image, (center_x - cross_size, center_y - cross_thickness // 2),
                  (center_x + cross_size, center_y + cross_thickness // 2), red_color, 3)

    # вертикальный верхний
    cv2.rectangle(image, (center_x - cross_thickness // 2, center_y - cross_size),
                  (center_x + cross_thickness // 2, center_y - cross_thickness // 2), red_color, 3)

    # вертикальный нижний
    cv2.rectangle(image, (center_x - cross_thickness // 2, center_y + cross_thickness // 2),
                  (center_x + cross_thickness // 2, center_y + cross_size), red_color, 3)

    horizontal_rect = image[center_y - cross_thickness // 2: center_y + cross_thickness // 2, center_x - cross_size: center_x + cross_size]
    blurred_horizontal_rect = cv2.GaussianBlur(horizontal_rect, (15, 15), 0)

    image[center_y - cross_thickness // 2: center_y + cross_thickness // 2,
    center_x - cross_size: center_x + cross_size] = blurred_horizontal_rect

    cv2.imshow('image', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 8 - Заполнение ближайшим к центральному пикселю цветом
def find_closest_color(pixel):
    max_index = np.argmax(pixel)
    colors = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255)}
    closest_color = colors.get(max_index)
    return closest_color

def draw_colored_cross():
    image = cv2.imread('C:/Users/artus/PycharmProjects/MultiMedia/pictures/pig.png')
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    height, width, _ = image.shape

    center_x = width // 2
    center_y = height // 2

    cross_size = 200
    cross_thickness = 60

    central_pixel_color = image[center_y, center_x]
    closest_color = find_closest_color(central_pixel_color)

    cv2.rectangle(image, (center_x - cross_thickness // 2, center_y - cross_size),
                  (center_x + cross_thickness // 2, center_y + cross_size), closest_color, thickness=cv2.FILLED)
    cv2.rectangle(image, (center_x - cross_size, center_y - cross_thickness // 2),
                  (center_x + cross_size, center_y + cross_thickness // 2), closest_color, thickness=cv2.FILLED)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cross_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        ret, frame = cap.read()

        height, width, _ = frame.shape

        center_x = width // 2
        center_y = height // 2

        cross_size = 150
        cross_thickness = 45

        central_pixel_color = frame[center_y, center_x]
        closest_color = find_closest_color(central_pixel_color)

        cv2.rectangle(frame, (center_x - cross_thickness // 2, center_y - cross_size),
                      (center_x + cross_thickness // 2, center_y + cross_size), closest_color, thickness=cv2.FILLED)
        cv2.rectangle(frame, (center_x - cross_size, center_y - cross_thickness // 2),
                      (center_x + cross_size, center_y + cross_thickness // 2), closest_color, thickness=cv2.FILLED)

        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

cross_camera()
