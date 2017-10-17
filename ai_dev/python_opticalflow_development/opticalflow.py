#import cv2
#import numpy as np
#cap = cv2.VideoCapture(0) #in our model this will be different
#ret, frame1 = cap.read()
#pvrs = cv2.cvtColor


### taken from information available open source from
### http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
### http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
### https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1

### this needs optimisation & testing on the CNN.

import numpy as np
import cv2

## takes in video input from current laptop camera (livefeed)
cap = cv2.VideoCapture(0)

## detection of corners
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 150, # Display #num of frames (Dot Points)
                      qualityLevel = 0.3,
                      minDistance = 5,
                      blockSize = 50 ) # Small window is more sensitive to noise and may miss larger motions

## using lk of
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),  #15 x 15 set pixel dimensions
                 maxLevel = 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

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
        img = cv2.add(frame, 0) ## adds the dot and line together into an image

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


#these just show the different images that get saved.
#    from matplotlib import pyplot as plt
#    fig, ax = plt.subplots()
#    ax.imshow(img)
#    plt.savefig('test.png', bbox_inches='tight')
#    plt.close()
#
#    fig, ax = plt.subplots()
#    ax.imshow(frame)
#    plt.savefig('test2.png', bbox_inches='tight')
#    plt.close()

#    fig, ax = plt.subplots()
#    ax.imshow(old_gray)
#    plt.savefig('test.png', bbox_inches='tight')
#    plt.close()


##  OG update the previous frame and previous points
    old_gray = frame_gray.copy()

##  NEW refresh each frame
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    #issue when all points leave the frame, program crashes.
    #thus there always needs to be a frame on the screen.




cv2.destroyAllWindows()
cap.release()
