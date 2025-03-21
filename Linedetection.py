from picamera2 import Picamera2
import cv2
import numpy as np

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (900, 1080)})  
picam2.configure(camera_config)
picam2.start()  

while True:
    frame = picam2.capture_array()

    if frame.shape[2] == 4:  
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    low_b = np.array([0, 0, 0], dtype=np.uint8)  
    high_b = np.array([70, 70, 70], dtype=np.uint8)  
    mask = cv2.inRange(frame, low_b, high_b)  

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  
            cy = int(M['m01'] / M['m00'])  

            print(f"CX: {cx}, CY: {cy}")

            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

        cv2.drawContours(frame, c, -1, (0, 255, 0), 1)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
