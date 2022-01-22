import cv2
import pytesseract
import re
from document_straighter import straight


def detect_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = image.copy()

    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        cropped = im2[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
        text = re.findall("[+-]?\d+[.,:]?\d*(?:[eE][+-]?\d+)?", text)
        if len(text) < 1:
            continue

        with open("recognized.txt", "a") as f:
            for t in text:
                f.write(t)
                f.write("\n")


if __name__ == '__main__':
    img = cv2.imread("data/sample_5.jpg")
    cv2.imshow("Imported img", img)
    cv2.waitKey(0)
    img = straight(img)
    detect_text(img)
