import cv2
import numpy as np

def extract_imgs(img):
    img = ~img # Invert the bits of image 255 -> 0
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) # Set bits > 127 to 1 and <= 127 to 0
    thresh = thresh.astype(np.uint8)
    ctrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0]) # Sort by x

    img_data = []
    rects = []
    for c in ctrs :
        x, y, w, h = cv2.boundingRect(c)
        rect = [x, y, w, h]
        rects.append(rect)

    bool_rect = []
    # Check when two rectangles collide
    for r in rects:
        l = []
        for rec in rects:
            flag = 0
            if rec != r:
                if r[0] < (rec[0] + rec[2] + 10) and rec[0] < (r[0] + r[2] + 10) and r[1] < (rec[1] + rec[3] + 10) and rec[1] < (r[1] + r[3] + 10):
                    flag = 1
                l.append(flag)
            else:
                l.append(0)
        bool_rect.append(l)

    dump_rect = []
    # Discard the small collide rectangle
    for i in range(0, len(ctrs)):
        for j in range(0, len(ctrs)):
            if bool_rect[i][j] == 1:
                area1 = rects[i][2] * rects[i][3]
                area2 = rects[j][2] * rects[j][3]
                if(area1 == min(area1,area2)):
                    dump_rect.append(rects[i])

    # Get the final rectangles
    final_rect = [i for i in rects if i not in dump_rect]
    for r in final_rect:
        x = r[0]
        y = r[1]
        w = r[2]
        h = r[3]

        im_crop = thresh[y:y+h+10, x:x+w+10] # Crop the image as most as possible
        im_resize = cv2.resize(im_crop, (28, 28)) # Resize to (28, 28)
        im_resize = np.reshape(im_resize, (1, 28, 28)) # Flat the matrix
        img_data.append(im_resize)

    return img_data

img = cv2.imread('2.jpg')
img =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_data = extract_imgs(img)
print(len(img_data))
cv2.imshow('name',img)
cv2.waitKey(0)
cv2.destroyAllWindows()