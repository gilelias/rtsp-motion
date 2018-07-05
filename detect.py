#!/usr/bin/python
import cv2
import numpy as np
from datetime import datetime
from time import gmtime, strftime, time
from config import url, username, password, channel, threshold

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def handleChange(frame):
    output_path = "images/img_%s.jpg" % str(datetime.now())
    cv2.imwrite(output_path, frame)


if __name__ == '__main__':
    rtsp_url = "rtsp://%s/user=%s&password=%s&channel=%s&stream=0.sdp?real_stream--rtp-caching=100" % (url, username, password, channel)

    print ("motion detector in: %s" % rtsp_url)
    cap=cv2.VideoCapture(rtsp_url)

    # Read three images first:
    img_minus = cap.read()[1]
    img = cap.read()[1]
    img_plus = cap.read()[1]

    t_minus = cv2.cvtColor(img_minus, cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(img_plus, cv2.COLOR_RGB2GRAY)


    while(True):
        dif = diffImg(t_minus, t, t_plus)
        difSum = dif.sum()
    
        if difSum > threshold:
            handleChange(img)
    
        # Read next image
        img = cap.read()[1]
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2GRAY)

    cap.release()
