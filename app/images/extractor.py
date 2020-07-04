import cv2
import os
import sys
import numpy as np
import copy


def extract_images(videoName, interval=5):
    savePath = videoName.split('.')[0]
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    videoCapture = cv2.VideoCapture(videoName)
    fps = videoCapture.get(5)
    curFrame = 0  # current frame in the video
    frameChecked = 0  # the number of checked frames
    step = interval * fps  # jump step of checking
    change = 0  # change value between two frames
    while True:
        success, tmpFrame = videoCapture.read()
        if not success:
            print('video is all read')
            break

        if(curFrame % step == 0):
            if frameChecked == 0:  # init
                previousFrame = np.zeros(
                    (tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.uint8)
                previousFrameF = np.zeros(
                    (tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.float32)
                currentFrame = np.zeros(
                    (tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.uint8)
                currentFrameF = np.zeros(
                    (tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.float32)
                tmpFrameF = np.zeros(
                    (tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.float32)
                frameChecked += 1
            else:
                currentFrame = cv2.cvtColor(tmpFrame, cv2.COLOR_RGB2GRAY)
                tmpFrameF = copy.deepcopy(currentFrame).astype(np.float32)
                previousFrameF = copy.deepcopy(
                    previousFrame).astype(np.float32)

                currentFrameF = np.abs(tmpFrameF - previousFrameF)
                currentFrame = copy.deepcopy(currentFrameF).astype(np.uint8)
                currentFrame = cv2.threshold(
                    currentFrame, 30, 255, cv2.THRESH_BINARY)[1]
                g_nStructElementSize = 3
                element = cv2.getStructuringElement(
                    cv2.MORPH_RECT, (2 * g_nStructElementSize + 1, 2 * g_nStructElementSize + 1), (g_nStructElementSize, g_nStructElementSize))
                currentFrame = cv2.dilate(currentFrame, element)
                currentFrame = cv2.erode(currentFrame, element)
                change = np.mean(currentFrame)
            if change > 30 or frameChecked == 1:  # big change or first frame, save it
                previousFrame = cv2.cvtColor(tmpFrame, cv2.COLOR_RGB2GRAY)
                savedName = videoName.split('.')[0].split(
                    '/')[-1] + '_' + str(int(curFrame // fps))+'.jpg'
                cv2.imwrite(savePath + '/' + savedName, tmpFrame)
                print(savePath + '/' + savedName)
                frameChecked += 1
                print('image of %s is saved' % (savedName))
        curFrame += 1
    return savePath
