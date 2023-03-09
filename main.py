import cv2
import numpy as np
import funcs

#-----------------------
# Кювета  в кадре [100:1050, 500:1200]
# Участок соединенения двух объемов [450:650, 800:950]
#-----------------------

cap = cv2.VideoCapture("videos/original_20s.mov")
# cap = cv2.VideoCapture(0)

# ret, frame = cap.read()
# (h, w) = frame.shape[:2]
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('temporary/output.mov', fourcc, 20.0, (h, w))
cv2.namedWindow("WinOrigin", cv2.WINDOW_FREERATIO)
cv2.namedWindow("WinModified", cv2.WINDOW_FREERATIO)
cv2.namedWindow("WinDiff", cv2.WINDOW_FREERATIO)

frame_buff = []
counter = 0
BUFF_SIZE = 30
buff_ready = False

scale = 0.8
i = 0

# Для теста фильтров
# ret = False
# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         ret, frame = cap.read()
#         if not ret:
#             break  
#         frame = frame[590:700, 800:950]
        
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     if ret:
#         cv2.imshow("WinOrigin", frame)
#         cv2.imshow("WinModified", gray)   

while True:
    ret, frame = cap.read()
    if not ret:
        break   

    frame = frame[590:700, 800:950]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray_croped = gray
    T, act_mod = cv2.threshold(gray_croped, 127, 255, cv2.THRESH_BINARY) 

    if not buff_ready:
        frame_buff.append(np.copy(act_mod))
        counter = counter + 1
        if counter == BUFF_SIZE:
            buff_ready = True
            counter = 0
    else:
        img_diff = funcs.get_diff(act_mod, frame_buff, counter, BUFF_SIZE)

        cv2.imshow("WinOrigin", act_mod)
        cv2.imshow("WinDiff", img_diff)

        ciliates = funcs.recognize_ciliates(act_mod, img_diff)

        frame_mod = funcs.highligth(frame, ciliates)
        cv2.imshow("WinModified", frame_mod)

        frame_buff[counter] = np.copy(act_mod)
        counter = counter + 1

        if counter == BUFF_SIZE:
            counter = 0


    # img = cv2.resize(gray_croped, (gray_croped.shape[0]*10, gray_croped.shape[1]*10), interpolation= cv2.INTER_LINEAR)


    # cv2.imwrite("temporary/bin_frame" +str(i)+ ".jpeg", act_mod) 
    # cv2.imwrite("temporary/gray_frame" +str(i)+ ".jpeg", gray_croped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()