import subprocess
import numpy as np
import cv2

proc_path = '../build/examples/seek_to_stdout' 
proc = subprocess.Popen(
    [proc_path,],
    stdout=subprocess.PIPE)

try:
    while 1:
        buf = proc.stdout.read(76800 * 2)
        print('buf_len:%s' % (len(buf), ))
        print(type(buf))

        image = np.fromstring(buf, np.uint16).reshape(240, 320, 1)
        cv2.imshow('im', image)
        print('show')
        k = cv2.waitKey(1)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

finally:
    proc.terminate()