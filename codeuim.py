import numpy as np

# create 2D array of random numbers from 0 to 255 of given size
def create_array(size):
    arr = []
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            arr.append(np.random.randint(0, 255))
    return arr





# create png grayscale image from array
def create_png(arr):
    img = Image.fromarray(arr, 'L')
    img.save('test.png')

create_array()
