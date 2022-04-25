from intelligent_placer_lib.findBorder import findBorder
from intelligent_placer_lib.fitObject import fitObj


def checkImage(strPathToImg):
    falseColor = findBorder.findEdge(strPathToImg)
    fitObj.fitObjAndPolygon(falseColor, strPathToImg)
