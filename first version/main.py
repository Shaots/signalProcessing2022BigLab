from findBorder import findBorder
import glob
import os


if __name__ == '__main__':
    imageList = sorted(glob.glob("./input/*.png"))
    os.mkdir("output")
    for oneImage in imageList:
        findBorder(oneImage)
