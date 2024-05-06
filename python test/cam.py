import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

# read images
capture = cv2.VideoCapture(1)
capture.set(3, 1280)
capture.set(4, 480)
s = time.time()
while True:
    ret, frame = capture.read()
    imgL = cv2.cvtColor(frame[:, :640], cv2.COLOR_BGR2GRAY)
    cv2.imshow("L",imgL)

    # # 오른쪽 이미지qqq
    imgR = cv2.cvtColor(frame[:, 640:], cv2.COLOR_BGR2GRAY)
    cv2.imshow("R",imgR)
    # estimate depth
    # stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    # disparity = stereo.compute(imgL, imgR)

    stereo = cv2.StereoSGBM.create(numDisparities=96, blockSize=1)
    disparity = stereo.compute(frame[:,:640], frame[:,640:])
    cv2.imshow("R",frame[:,:640])

    if time.time() - s > 0.5 :
        s = time.time()
        print(np.average(disparity[:,:]), end='   /    ')
        print(np.average(disparity[200:280,280:360]))
    Min, Max = np.min(disparity), np.max(disparity)
    disparity = disparity + Min
    disparity = disparity / ((Min + Max)/255)
    print(disparity)
    cv2.imshow("a", disparity)
    cv2.waitKey(20)


    # stereo = cv2.StereoBM_create(numDisparities=96, blockSize=9)
    # disparity = stereo.compute(imgL, imgR)
    # plt.figure(figsize=(7,7))
    # plt.imshow(disparity)
    # plt.colorbar()
    # plt.show()