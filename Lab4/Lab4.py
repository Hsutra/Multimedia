import cv2
import numpy as np

def gradient(image, kernel_size, sigma):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    g_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    g_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(g_x, g_y)
    angle = np.arctan2(g_y, g_x)
    return magnitude, angle

def non_max_suppression(image, kernel_size, sigma):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    g_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    g_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(g_x, g_y)
    angle = np.arctan2(g_y, g_x)
    height, width = magnitude.shape
    suppressed_image = np.zeros_like(magnitude)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            current_angle = angle[i, j]
            if (0 <= current_angle < 22.5) or (157.5 <= current_angle <= 180):
                neighbors = [magnitude[i, j - 1], magnitude[i, j + 1]]
            elif (22.5 <= current_angle < 67.5):
                neighbors = [magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]]
            elif (67.5 <= current_angle < 112.5):
                neighbors = [magnitude[i - 1, j], magnitude[i + 1, j]]
            else:
                neighbors = [magnitude[i - 1, j + 1], magnitude[i + 1, j - 1]]
            if magnitude[i, j] >= max(neighbors):
                suppressed_image[i, j] = magnitude[i, j]

    return suppressed_image

def double_thresholding(image, low_threshold, high_threshold):
    height, width = image.shape
    result_image = np.zeros_like(image)

    strong_edge_value = 255
    weak_edge_value = 50

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if image[i, j] >= high_threshold:
                result_image[i, j] = strong_edge_value
            elif image[i, j] >= low_threshold:
                result_image[i, j] = weak_edge_value
            else:
                result_image[i, j] = 0
    return result_image


image_path = 'pictures/mount-pic.jpg'
kernel_size = 3
sigma = 0.25

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (int(image.shape[1] // 3), int(image.shape[0] // 3)))
blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

suppressed_image = non_max_suppression(image, kernel_size, sigma)

low_threshold = 30
high_threshold = 80

canny_image = double_thresholding(suppressed_image, low_threshold, high_threshold)

cv2.imshow('Original Image', image)
cv2.imshow('Suppressed Image', suppressed_image)
cv2.imshow('Canny Edge Detection', canny_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
