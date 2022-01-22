import cv2
import pytesseract
from document_straighter import straight


def detect_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = image.copy()

    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
        with open("recognized.txt", "a") as f:
            f.write(text)
            f.write("\n")

        print(text)


if __name__ == '__main__':
    img = cv2.imread("data/sample_6.png")
    cv2.imshow("Imported img", img)
    cv2.waitKey(0)
    img = straight(img)
    detect_text(img)
