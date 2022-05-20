from PIL import Image

im = Image.open('data/light/clearance.png')
pix = im.load()
w, hhhhh = im.size

for i in range(w):
    for j in range(hhhhh):
        r, g, b, h = pix[i, j]
        pix[i, j] = 255 - r, 255 - g, 255 - b, 255 - h
im.save('data/light/clearance.png')
