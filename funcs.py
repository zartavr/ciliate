import cv2
import numpy as np

ITERATE_LIMIT = 100
iterate_counter  = 0
ciliate = []

def get_diff(act, buf, counter, buf_size):
    (h, w) = act.shape[0:2]
    diff = np.copy(act)
    counter = 0
    for i in range(counter, counter + buf_size):
        if (i - counter) % 10 != 0:
            continue
        pre_frame = buf[i % buf_size]
        for y in range(0, h):
            for x in range(0, w):
                if act[y, x] != pre_frame[y, x]:
                    counter = counter + 1
                if act[y, x] == 255 and pre_frame[y, x] == 255:
                    diff[y, x] = 0    

    return diff

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


def get_ciliate(frame, y, x):
    global iterate_counter
    global ciliate
    iterate_counter = 1
    ciliate = []
    get_ciliate_rec(frame, y, x)
    x1 = x
    x2 = x
    y1 = y
    y2 = y
    for pix in ciliate:
        if pix[0] <= y1:
            y1 = pix[0]
        if pix[1] <= x1:
            x1 = pix[1]
        if pix[0] >= y2:
            y2 = pix[0]
        if pix[1] >= x2:
            x2 = pix[1]
    top_left = [y1, x1]
    bottom_right = [y2, x2]
    return [top_left, bottom_right]

    

def get_ciliate_rec(frame, y, x):
    global iterate_counter
    global ciliate
    iterate_counter = iterate_counter + 1
    ciliate.append([y, x])
    if iterate_counter == ITERATE_LIMIT:
        return
    # выход за границы изображения
    for xi in range(x-1, x+2):
        for yi in range(y-1, y+2):
            if yi > 199 or xi >399 or xi < 0 or yi < 0:
                continue
            if frame[yi, xi] == 255 and not([yi, xi] in ciliate):
                get_ciliate_rec(frame, yi, xi)

    return
    
def del_rect(frame, rect):
    for y in range(rect[0][0], rect[1][0]):
        for x in range(rect[0][1], rect[1][1]):
            frame[y, x] = 0

def highligth(frame, rects):
    for rect in rects:
        for y in range(rect[0][0]-2, rect[1][0]+2):
            l = rect[0][1]- 2
            r = rect[1][1]+2
            try:
                frame[y, l] = (255, 0, 0)
                frame[y, r] = (255, 0, 0)
            except:
                continue
        for x in range(rect[0][1]-2, rect[1][1]+2):
            t = rect[0][0]-2
            b = rect[1][0]+2
            try:
                frame[t, x] = (255, 0, 0)
                frame[b, x] = (255, 0, 0)
            except:
                continue

    return frame







