import cv2
import numpy as np
import funcs_cod

cap = cv2.VideoCapture("videos/orig_10s.MOV")
cv2.namedWindow("WinOrigin", cv2.WINDOW_FREERATIO)
cv2.namedWindow("WinOriginBin", cv2.WINDOW_FREERATIO)
cv2.namedWindow("WinModified", cv2.WINDOW_FREERATIO)
cv2.namedWindow("WinDiff", cv2.WINDOW_FREERATIO)

frame_buffer = []
counter = 0
BUFFER_SIZE = 30
buffer_ready = False

scale = 0.8
i = 0

while True:
    print(i)
    ret, frame = cap.read()

    if i == 1:
        fps = cap.get(cv2.CAP_PROP_FPS)
        video_codec = cv2.VideoWriter_fourcc(*'XVID')
        video_output = cv2.VideoWriter('temporary/captured_video.mov', video_codec, fps, [gray.shape[1], gray.shape[0]])

    if not ret:
        break

    frame = frame[1800:2000, 800:1200]
    cv2.imshow("WinOrigin", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray_cropped = gray
    threshold_value, binary_image = cv2.threshold(gray_cropped, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow("WinOriginBin", binary_image)
    i += 1

    if not buffer_ready:
        frame_buffer.append(np.copy(binary_image))
        counter += 1
        if counter == BUFFER_SIZE:
            buffer_ready = True
            counter = 0
    else:
        diff_image = funcs_cod.get_diff(binary_image, frame_buffer, counter, BUFFER_SIZE)

        cv2.imshow("WinDiff", diff_image)

        ciliates = funcs_cod.recognize_ciliates(binary_image, diff_image)

        modified_frame = funcs_cod.highlight(frame, ciliates)
        cv2.imshow("WinModified", modified_frame)

        video_output.write(modified_frame)

        frame_buffer[counter] = np.copy(binary_image)
        counter += 1

        if counter == BUFFER_SIZE:
            counter = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_output.release()
cv2.destroyAllWindows()
