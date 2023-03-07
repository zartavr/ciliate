import cv2

import numpy as np

cap = cv2.VideoCapture("videos/original_20s.mov")
# ret, frame = cap.read()
# (h, w) = frame.shape[:2]
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('temporary/output.mov', fourcc, 20.0, (h, w))
cv2.namedWindow("modified", cv2.WINDOW_FREERATIO)
cv2.namedWindow("origin", cv2.WINDOW_FREERATIO)

scale = 0.8
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # out.write(frame)

    gray_croped = gray[450:650, 800:950]

    cv2.imshow('origin', frame)
    cv2.imshow('modified', gray_croped)   

    img = cv2.resize(gray_croped, (gray_croped.shape[0]*10, gray_croped.shape[1]*10), interpolation= cv2.INTER_LINEAR)
    cv2.imwrite("temporary/gray_frame.jpeg", img) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()