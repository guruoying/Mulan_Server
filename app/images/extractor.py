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
    if not videoCapture.isOpened:
        print('Error: video is not opened')
        eixt()
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    curFrame = 0  # current frame num in the video
    frameChecked = 0  # the number of extracted key frames
    step = int(interval * fps)  # jump step of checking
    change = 0  # change value between two frames
    while True:
        success, tmpFrame = videoCapture.read() 
        if not success:
            print('video is all read')
            break

        if (curFrame % step == 0):
            if frameChecked == 0:  # init
                previousFrameF = np.zeros((tmpFrame.shape[0], tmpFrame.shape[1], 1)).astype(np.float32)
                frameChecked += 1
            else:
                tmpFrameF = cv2.cvtColor(tmpFrame, cv2.COLOR_RGB2GRAY).astype(np.float32)

                diffFrame = np.abs(tmpFrameF - previousFrameF).astype(np.uint8) # difference between current frame and last key frame
                diffFrame = cv2.threshold(diffFrame, 30, 255, cv2.THRESH_BINARY)[1] # activate areas where the difference is greater than the threshold
                # get kernel for cv2.dilate and cv2.erode
                g_nStructElementSize = 3
                element = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                                    (2 * g_nStructElementSize + 1, 2 * g_nStructElementSize + 1),
                                                    (g_nStructElementSize, g_nStructElementSize))
                diffFrame = cv2.dilate(diffFrame, element) # dilate
                diffFrame = cv2.erode(diffFrame, element) # erode
                change = np.mean(diffFrame) # everage change value
            if change > 10 or frameChecked == 1:  # big change or first frame, save it
                previousFrameF = copy.deepcopy(cv2.cvtColor(tmpFrame, cv2.COLOR_RGB2GRAY).astype(np.float32)) # update previousFrameF as current frame
                savedName = videoName.split('.')[0].split('/')[-1] + '_' + str(int(curFrame // fps))+'.jpg'
                cv2.imwrite(savePath + '/' + savedName, tmpFrame)
                frameChecked += 1
                print('image of %s is saved' % (savePath + '/' + savedName))
        curFrame += 1
    return savePath
