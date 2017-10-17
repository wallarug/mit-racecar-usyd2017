#import cv2
#import numpy as np
#cap = cv2.VideoCapture(0) #in our model this will be different
#ret, frame1 = cap.read()
#pvrs = cv2.cvtColor


### taken from information available open source from
### http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
### http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
### https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1

### this needs optimisation. And to have the optimisation tested.

import numpy as np
import cv2

## takes in video input from current laptop camera (livefeed)
cap = cv2.VideoCapture(0)

## detection of corners
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 5, #100
                      qualityLevel = 0.01, #0.9
                      minDistance = 7, #7
                      blockSize = 7 ) #7

##
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                 maxLevel = 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
#mask = np.zeros_like(0)


## we may want to compare each old frame to the previous
while(1):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    
    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), (103, 209, 51), 6) ## visual line which is connected to the dot point
        frame = cv2.circle(frame,(a,b),5, (255, 255, 255),2) ## visual circle dot point
    img = cv2.add(frame,mask) ## adds the dot and line together into an image

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#these just show the different images that get saved.

#    from matplotlib import pyplot as plt
#   fig, ax = plt.subplots()
#    ax.imshow(mask)
#    plt.savefig('test.png', bbox_inches='tight')
#    plt.close()
#
#   fig, ax = plt.subplots()
#   ax.imshow(frame)
#   plt.savefig('test2.png', bbox_inches='tight')
#   plt.close()

    # Now update the previous frame and previous points
    #old_gray = frame_gray.copy()
    old_gray = frame_gray.copy() - cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    #p0 = good_new.reshape(-1,1,2)

    #still not working, however below gives an iterative attempt every frame to re-calculate new points to detect.
    #issue when all points leave the frame, program crashed. thus there always needs to be a frame on the screen.
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)



cv2.destroyAllWindows()
cap.release()
