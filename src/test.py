
from PIL import Image
import cv2
import numpy as np


# # Open input images, background and overlay
# image   = Image.open('assets/board/xiangqi_gmchess_wood.png')
# overlay = Image.open('assets/pieces/black_advisor.png')

# # Paste overlay onto background using overlay alpha as mask
# image.paste(overlay, mask=overlay)

# # Save
# image.save('result.png')


img1 = cv2.imread('assets/board/xiangqi_gmchess_wood.png', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('assets/pieces/black_advisor.png', cv2.IMREAD_UNCHANGED)
x_offset=y_offset=50

y1, y2 = y_offset, y_offset + img2.shape[0]
x1, x2 = x_offset, x_offset + img2.shape[1]

alpha_s = img2[:, :, 3] / 255.0
alpha_l = 1.0 - alpha_s

alpha_s = np.repeat(alpha_s[:, :, np.newaxis], 3, axis=2)
alpha_l = np.repeat(alpha_l[:, :, np.newaxis], 3, axis=2)

# for c in range(0, 3):
#     img1[y1:y2, x1:x2, c] = (alpha_s * img2[:, :, c] +
#                               alpha_l * img1[y1:y2, x1:x2, c])
    
img1[y1:y2, x1:x2, :3] = (alpha_s * img2[:, :, :3] + alpha_l * img1[y1:y2, x1:x2, :3]) 
# Save or display the result
cv2.imshow('Result', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()