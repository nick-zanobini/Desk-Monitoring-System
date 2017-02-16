# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import warnings
import commands
import datetime
import imutils
import time
import cv2

# filter warnings
warnings.filterwarnings("ignore")

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1280, 720))
# clear the stream in preparation for the next frame
rawCapture.truncate(0)

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(2.5)
avg = None
lastMotionTime = time.time()
count = 0
stillTime = 15
try:
    # capture frames from the camera
    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image and initialize
        # the timestamp and occupied/unoccupied text
        frame = f.array
        timestamp = datetime.datetime.now()
        text = "Unoccupied"

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average frame is None, initialize it
        if avg is None:
            print("[INFO] starting background model...")
            avg = gray.copy().astype("float")
            rawCapture.truncate(0)
            continue

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, avg, 0.2)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
            lastMotionTime = time.time()

        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Cube Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)

        # display the security feed
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            s = commands.getstatusoutput('sudo ./qlight -g off')
            s = commands.getstatusoutput('sudo ./qlight -r off')
            break

        count += 1
        now = time.time()
        if count >= 100:
            count = 0
            seconds = now - lastMotionTime
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("[Info] Cube Status: {} for {:02d}:{:02d}:{:02d}".format(text, int(h), int(m), int(s)))
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

        if lastMotionTime is not None and (now - lastMotionTime) < (stillTime) and text == "Occupied":
            s = commands.getstatusoutput('sudo ./qlight -r off')
            s = commands.getstatusoutput('sudo ./qlight -g on')
        elif lastMotionTime is not None and (now - lastMotionTime) > (stillTime) and text == "Unoccupied":
            s = commands.getstatusoutput('sudo ./qlight -g off')
            s = commands.getstatusoutput('sudo ./qlight -r on')

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

except(KeyboardInterrupt, SystemExit):
    s = commands.getstatusoutput('sudo ./qlight -g off')
    s = commands.getstatusoutput('sudo ./qlight -r off')
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
