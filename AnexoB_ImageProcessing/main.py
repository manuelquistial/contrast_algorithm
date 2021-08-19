import cv2
import numpy as np
import glob

for img_aceite in glob.glob("con_aceite/*.jpg"):
    image = cv2.imread(img_aceite)
    image = image[500:800, 500:800]

    cv2.imshow("Mask Applied to Image", image)
    cv2.imwrite("con_aceite_mask/"+img_aceite.replace(".jpg","").split("/")[1] + "_masked.jpg", image)

    Y = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)[:,:,0]

    # compute min and max of Y
    min = int(np.min(Y))
    max = int(np.max(Y))

    # compute contrast
    contrast = (max-min)/(max+min)
    print(contrast)

print()

for img_sin in glob.glob("sin_aceite/*.jpg"):
    image_sin = cv2.imread(img_sin)
    image_sin = image_sin[500:800, 400:700]
    cv2.imshow("Mask Applied to Image", image_sin)
    cv2.imwrite("sin_aceite_mask/"+img_sin.replace(".jpg","").split("/")[1] + "_masked.jpg", image_sin)

    Y_sin = cv2.cvtColor(image_sin, cv2.COLOR_BGR2YUV)[:,:,0]

    # compute min and max of Y
    min_sin = int(np.min(Y_sin))
    max_sin = int(np.max(Y_sin))

    # compute contrast
    contrast_sin = (max_sin-min_sin)/(max+min_sin)
    print(contrast_sin)
