import os
import matplotlib.pyplot as plt


def paint(gray, edges, imgThin, falseColors, nameImg):
    f, ax = plt.subplots(2, 2, figsize=(10, 10))
    ax[0, 0].set_title(f"Input image")
    ax[0, 1].set_title(f"Edges from Canny")
    ax[1, 0].set_title(f"Object and polygon with errors noise")
    ax[1, 1].set_title(f"Final object and polygon without errors")
    ax[0, 0].imshow(gray, cmap="gray")
    ax[0, 1].imshow(edges, cmap="gray")
    ax[1, 0].imshow(imgThin, cmap="gray")
    ax[1, 1].imshow(falseColors, cmap="gray")
    plt.savefig(f"../output/result_{os.path.basename(nameImg)}")
    plt.close()
