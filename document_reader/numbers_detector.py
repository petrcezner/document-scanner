import datetime
from pathlib import Path

import cv2
import pytesseract
import re
from image_straighter import straight


def detect_text(image, file_name: Path = Path('data/converted.txt'), language='eng'):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = image.copy()
    file_name.parent.mkdir(parents=True, exist_ok=True)
    file = open(file_name, "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        cropped = im2[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped, lang=language)
        text = re.findall("[+-]?\d+[.,:]?\d*(?:[eE][+-]?\d+)?", text)
        if len(text) < 1:
            continue

        with open(file_name, "a") as f:
            for t in text:
                f.write(t)
                f.write("\n")
    return file_name


def convert_image(image, language='eng'):
    image = straight(image)
    result_path = detect_text(image, language=language)
    return result_path


if __name__ == '__main__':
    img = cv2.imread("data/sample_5.jpg")
    cv2.imshow("Imported img", img)
    cv2.waitKey(0)
    img = straight(img)
    detect_text(img, Path('data'))
