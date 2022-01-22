import numpy as np
import cv2
from collections import Counter


# https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/

def are_close(a1, a2, error):
    cases = np.unwrap([a2 - error, a1, a2 + error])
    return cases[0] <= cases[1] <= cases[2]


def straight(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    binary = cv2.Canny(blur, 50, 200)
    lines = cv2.HoughLines(binary, 1, np.pi / 180, 1000, None, 0, 0)
    if lines is None:
        lines = cv2.HoughLines(binary, 1, np.pi / 180, 150, None, 0, 0)
    # lines = cv2.HoughLines(binary, 1, np.pi / 720, 1000, None, 0, 0)

    angles = []
    for line in lines:
        rho, theta = line[0]
        if rho < 0:
            theta = -theta
        if not are_close(theta, np.pi / 2, np.deg2rad(10)):
            continue
        angles.append(theta)

    angle_count = Counter(angles)

    frequencies = angle_count.most_common(3)

    angle_frequencies_sum = sum(angle * repetition for angle, repetition in frequencies)
    repetitions = sum(repetition for angle, repetition in frequencies)
    angles = angle_frequencies_sum / repetitions

    angles = np.rad2deg(angles - np.pi / 2)

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angles, 1.0)
    output_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return output_img
