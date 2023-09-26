import cv2
import numpy as np

ITERATE_LIMIT = 100

def get_diff(act, buf, counter, buf_size):
    (h, w) = act.shape[0:2]
    diff = np.copy(act)
    for i in range(counter, counter + buf_size):
        if (i - counter) % 10 != 0:
            continue
        pre_frame = buf[i % buf_size]
        for y in range(0, h):
            for x in range(0, w):
                if act[y, x] != pre_frame[y, x]:
                    counter += 1
                if act[y, x] == 255 and pre_frame[y, x] == 255:
                    diff[y, x] = 0    
    return diff

def get_ciliate(frame, y, x):
    ciliate = []
    get_ciliate_rec(frame, y, x, ciliate)
    x1, x2, y1, y2 = x, x, y, y
    for pix in ciliate:
        y1 = min(y1, pix[0])
        x1 = min(x1, pix[1])
        y2 = max(y2, pix[0])
        x2 = max(x2, pix[1])
    top_left = [y1, x1]
    bottom_right = [y2, x2]
    return [top_left, bottom_right]

def get_ciliate_rec(frame, y, x, ciliate):
    ciliate.append([y, x])
    if len(ciliate) == ITERATE_LIMIT:
        return
    for xi in range(x-1, x+2):
        for yi in range(y-1, y+2):
            if 0 <= yi < 200 and 0 <= xi < 400 and frame[yi, xi] == 255 and not ([yi, xi] in ciliate):
                get_ciliate_rec(frame, yi, xi, ciliate)

def recognize_ciliates(frame, diff_frame):
    (h, w) = frame.shape[0:2]
    rects = []
    for y in range(0, h):
        for x in range(0, w):
            if diff_frame[y, x] == 255:
                rect = get_ciliate(frame, y, x)
                del_rect(diff_frame, rect)
                rects.append(rect)
    return rects

def del_rect(frame, rect):
    for y in range(rect[0][0], rect[1][0]):
        for x in range(rect[0][1], rect[1][1]):
            frame[y, x] = 0

def highlight(frame, rects):
    for rect in rects:
        for y in range(rect[0][0]-2, rect[1][0]+2):
            for x in range(rect[0][1]-2, rect[1][1]+2):
                try:
                    frame[y, x] = (255, 0, 0)
                except:
                    continue
    return frame
