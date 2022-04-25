from intelligent_placer_lib import intelligent_placer
import glob
import os

if __name__ == '__main__':
    imageList = sorted(glob.glob("../input/*.png"))
    if not os.path.exists("../output"):
        os.mkdir("../output")
    for oneImage in imageList:
        intelligent_placer.checkImage(oneImage)