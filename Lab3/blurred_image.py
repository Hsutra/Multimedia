import cv2
import numpy as np

def gauss_func(x, y, a, b, sigma):
    return (1 / (2 * np.pi * sigma ** 2)) * (np.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sigma ** 2)))

def build_ker(size, sigma):
    a, b = (size - 1) // 2, (size - 1) // 2
    ker = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            ker[i, j] = gauss_func(i, j, a, b, sigma)
    ker /= ker.sum()
    return ker

def apply_gaussian_blur(image_path, kernel_size, sigma):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height = int(image.shape[0] * 0.5)
    width = int(image.shape[1] * 0.5)
    image = cv2.resize(image, (width, height))
    image_copy = image.copy()
    ker = build_ker(kernel_size, sigma)
    center = kernel_size // 2
    for i in range(center, height - center):
        print(i)
        for j in range(center, width - center):
            val = np.sum(image[i - center: i + center + 1, j - center: j + center + 1] * ker)
            image_copy[i, j] = val
    # оригинал
    cv2.imshow('Original Image', image)
    # без cv2
    cv2.imshow('Blurred Image', image_copy)
    # c помощью cv2
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    cv2.imshow('Blurred Image with cv2', blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = 'pictures/mount-pic.jpg'
kernel_size = 3
sigma = 2
apply_gaussian_blur(image_path, kernel_size, sigma)
