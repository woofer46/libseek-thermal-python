#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import subprocess
from sensor_msgs.msg import CompressedImage

proc_path = '../build/examples/seek_to_stdout' 
proc = subprocess.Popen(
    [proc_path,],
    stdout=subprocess.PIPE)

rospy.init_node('image_thermo', anonymous=True)
image_pub = rospy.Publisher("thermo/image",Image, queue_size=1)
bridge = CvBridge()

try:
    while 1:
        buf = proc.stdout.read(76800 * 2)
        print('buf_len:%s' % (len(buf), ))

        image = np.fromstring(buf, np.uint16).reshape(240, 320, 1)
        img8 = (image/256).astype('uint8')
        rgb = cv2.cvtColor(img8,cv2.COLOR_GRAY2RGB) 
        im_color = cv2.applyColorMap(rgb, cv2.COLORMAP_JET)
        msg = bridge.cv2_to_imgmsg(im_color, "bgr8")
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "thermo_cam"
        try:
            image_pub.publish(msg)
        except CvBridgeError as e:
            print(e)

        #cv2.imshow('im', image)
        #print('show')
        #k = cv2.waitKey(1)
        #if k == 27:         # wait for ESC key to exit
        #    cv2.destroyAllWindows()

finally:
    proc.terminate()