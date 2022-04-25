import cv2
import numpy as np
from intelligent_placer_lib.paint import paint


class findBorder:
    CONST_COLOR_FOND = 0
    CONST_COLOR_OBJECT = 128
    CONST_COLOR_POLYGON = 255

    # Поиск границы
    @staticmethod
    def findEdge(nameImg):
        img = cv2.imread(nameImg)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = findBorder.decreaseSize(gray)
        gray = findBorder.reduceNoise(gray)

        edges = cv2.Canny(gray, 100, 200)
        imgThick = findBorder.dilateEdge(edges)
        imgPolygon = findBorder.floorFill(imgThick)
        imgObjectAndPolygon = findBorder.uniteEdgeAndContent(imgThick, imgPolygon)
        imgOut = findBorder.erodeEdge(imgObjectAndPolygon)
        falseColors = findBorder.colorPolygonAndObject(gray, imgOut)
        paint(gray, edges, imgOut, falseColors, nameImg)
        return falseColors

    # Понизить размерность изображение для ускорения
    @staticmethod
    def decreaseSize(imgGray):
        scalePercent = 20 / 100  # Сократить размер изображение в 80%
        width = int(imgGray.shape[1] * scalePercent)
        height = int(imgGray.shape[0] * scalePercent)
        dim = (width, height)
        gray = cv2.resize(imgGray, dim)
        return gray

    # Сделать шумоподавление
    @staticmethod
    def reduceNoise(imgGray):
        gray = cv2.bilateralFilter(imgGray, d=3, sigmaColor=10, sigmaSpace=10)
        return gray

    # Разширять границы, чтобы они стали толще
    @staticmethod
    def dilateEdge(imgEdge):
        kernel = np.ones((5, 5), np.uint8)
        imgThick = cv2.dilate(imgEdge, kernel, iterations=1)
        return imgThick

    # Метод наводнение
    @staticmethod
    def floorFill(imgThick):
        imgFloodFill = imgThick.copy()
        h, w = imgThick.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        startPoint = (0, 0)
        cv2.floodFill(imgFloodFill, mask, startPoint, 255)
        imgPolygon = cv2.bitwise_not(imgFloodFill)
        return imgPolygon

    # Объединить объекты, границу многоугольника с содержимым внутри границы
    @staticmethod
    def uniteEdgeAndContent(imgThick, imgPolygon):
        imgObjectAndPolygon = imgThick | imgPolygon
        return imgObjectAndPolygon

    # Разрушать границы и одновременно сделать шумоподавление
    @staticmethod
    def erodeEdge(imgObjectAndPolygon):
        kernel = np.ones((5, 5), np.uint8)
        imgThin = cv2.erode(imgObjectAndPolygon, kernel, iterations=1)
        return imgThin

    # Покрасить многоугольник и объекты разными цветами.
    # Сначала сенгментируем изображение
    # Далее раскрашиваем их более различными цветами и отбрасываем очень мелкие часть 0.4%
    # Одна тонкость: заметил, что  нарисованный многоугольник на белом фоне всегда ярче объектов.
    # Этот признак используем для выделения сегмента, соответствующего многоугольнику
    # Находим самый яркий сегмент на изображении. И это будет многоугольник
    @staticmethod
    def colorPolygonAndObject(gray, imgOut):
        n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imgOut, connectivity=4)

        # Равномерно распределяем цветы в интервале от 0 до 200
        colors = np.arange(0, 200, 200 / n_labels).astype(np.uint8)
        colors[0] = findBorder.CONST_COLOR_FOND  # Поставим фону черный цвет
        falseColors = colors[labels]
        maxBrightness = 0
        numObject = 0
        areaThrow = 0.4 / 100  # Если какой-то сегмент < 0.4% от всего изображения, мы считаем их ошибками.
        wholeArea = imgOut.shape[0] * imgOut.shape[1]
        brightestColor = 0
        for i in range(len(colors)):
            objectArea = np.sum(falseColors == colors[i])
            if objectArea < wholeArea * areaThrow:
                falseColors[falseColors == colors[i]] = findBorder.CONST_COLOR_FOND
            else:
                numObject += 1
                curBrightness = np.mean(gray[falseColors == colors[i]])
                if colors[i] != findBorder.CONST_COLOR_FOND and curBrightness > maxBrightness:
                    maxBrightness = curBrightness
                    brightestColor = colors[i]

        falseColors[falseColors == brightestColor] = findBorder.CONST_COLOR_POLYGON
        falseColors[
            np.logical_and(falseColors != findBorder.CONST_COLOR_POLYGON, falseColors > findBorder.CONST_COLOR_FOND)] = findBorder.CONST_COLOR_OBJECT
        return falseColors
