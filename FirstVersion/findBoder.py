import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Понизить размерность изображение для ускорения
def decreaseSize(imgGray):
    scalePercent = 20
    width = int(imgGray.shape[1] * scalePercent / 100)
    height = int(imgGray.shape[0] * scalePercent / 100)
    dim = (width, height)
    gray = cv2.resize(imgGray, dim)
    return gray


# Сделать шумоподавление
def reduceNoise(imgGray):
    gray = cv2.bilateralFilter(imgGray, 3, 10, 10)
    return gray


# Разширять границы, чтобы они стали толще
def dilateEdge(imgEdge):
    kernel = np.ones((5, 5), np.uint8)
    imgThick = cv2.dilate(imgEdge, kernel, iterations=1)
    return imgThick


# Метод наводнение
def floorFill(imgThick):
    imgFloodFill = imgThick.copy()
    h, w = imgThick.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    startPoint = (0, 0)
    cv2.floodFill(imgFloodFill, mask, startPoint, 255)
    imgContentInsideBorder = cv2.bitwise_not(imgFloodFill)
    return imgContentInsideBorder


# Объединить границу с содержимым внутри границы
def uniteEdgeAndContent(imgThick, imgContentInsideBorder):
    imgContentAndEdge = imgThick | imgContentInsideBorder
    return imgContentAndEdge


# Разрушать границы. Граница и содержимое уже должны выглядеть одним целым.
def erodeEdge(imgContentAndEdge):
    kernel = np.ones((5, 5), np.uint8)
    imgThin = cv2.erode(imgContentAndEdge, kernel, iterations=1)
    return imgThin


# Поиск границы
def findBorder(nameImg):
    img = cv2.imread(nameImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = decreaseSize(gray)
    gray = reduceNoise(gray)
    
    edges = cv2.Canny(gray, 100, 200)
    imgThick = dilateEdge(edges)
    imgContentInsideEdge = floorFill(imgThick)
    imgContentAndEdge = uniteEdgeAndContent(imgThick, imgContentInsideEdge)
    imgThin = erodeEdge(imgContentAndEdge)
    f, ax = plt.subplots(2, 3, figsize=(10, 5))

    ax[0, 0].set_title("Lena")
    ax[0, 1].set_title("Edges")
    ax[0, 2].set_title("Thick")
    ax[1, 0].set_title("Content")
    ax[1, 1].set_title("ContentAndEdge")
    ax[1, 2].set_title("Thin")
    ax[0, 0].imshow(gray)
    ax[0, 1].imshow(edges, cmap="gray")
    ax[0, 2].imshow(imgThick, cmap="gray")
    ax[1, 0].imshow(imgContentInsideEdge, cmap="gray")
    ax[1, 1].imshow(imgContentAndEdge, cmap="gray")
    ax[1, 2].imshow(imgThin, cmap="gray")
    plt.savefig(f"result_{os.path.basename(nameImg)}")
