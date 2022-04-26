import numpy as np
import skimage.draw

height, width = 50, 50
target = np.zeros((height, width), dtype=np.uint8)
x, y = 21.5, 18.2
radius = 14.3
target[skimage.draw.disk((x,y), radius=radius)] = 1