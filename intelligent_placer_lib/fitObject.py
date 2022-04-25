import numpy as np
from intelligent_placer_lib.findBorder import findBorder


class fitObj:
    @staticmethod
    def fitObjAndPolygon(falseColors, nameImg):
        polygonAreaCoord = np.argwhere(falseColors == findBorder.CONST_COLOR_POLYGON)
        polygonCropCoord = (np.min(polygonAreaCoord[:, 0]),
                            np.min(polygonAreaCoord[:, 1]),
                            np.max(polygonAreaCoord[:, 0]),
                            np.max(polygonAreaCoord[:, 1]))

        objectAreaCoord = np.argwhere(falseColors == findBorder.CONST_COLOR_OBJECT)
        objectCropCoord = (np.min(objectAreaCoord[:, 0]),
                           np.min(objectAreaCoord[:, 1]),
                           np.max(objectAreaCoord[:, 0]),
                           np.max(objectAreaCoord[:, 1]))

        polygon = falseColors[polygonCropCoord[0]:polygonCropCoord[2], polygonCropCoord[1]:polygonCropCoord[3]]
        object = falseColors[objectCropCoord[0]:objectCropCoord[2], objectCropCoord[1]:objectCropCoord[3]]

        objFitPolygon = False
        sourceArea = np.sum(polygon > findBorder.CONST_COLOR_FOND)
        if np.all(np.less(object.shape, polygon.shape)):
            for i in range(polygon.shape[0] - object.shape[0]):
                for j in range(polygon.shape[1] - object.shape[1]):
                    # Поставим левый верхний угол объекта в точку (i, j) многоугольник
                    tmp_area = polygon.copy()
                    tmp_area[i:i + object.shape[0], j:j + object.shape[1]][object > 0] = object[object > 0]
                    new_area = np.sum(tmp_area > 0)
                    if new_area <= sourceArea:
                        objFitPolygon = True
                        break
                if objFitPolygon:
                    break

        gt = False if "False" in nameImg else True
        print("Predicted value for objects fit inside area:", objFitPolygon,
              "Required value:", gt,
              "Is correct:", objFitPolygon == gt,
              "\n")
