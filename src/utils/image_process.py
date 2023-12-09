import numpy as np


def paste(img1, img2, offset):
    """
    Paste img2 on img1
    """
    x1, x2 = offset[0], offset[0] + img2.shape[0]
    y1, y2 = offset[1], offset[1] + img2.shape[1]

    alpha_2 = img2[:, :, 3] / 255.0
    alpha_1 = 1.0 - alpha_2

    alpha_2 = np.repeat(alpha_2[:, :, np.newaxis], 3, axis=2)
    alpha_1 = np.repeat(alpha_1[:, :, np.newaxis], 3, axis=2)

    img1[x1:x2, y1:y2, :3] = (alpha_1 * img1[x1:x2, y1:y2, :3] + alpha_2 * img2[:, :, :3]) 
    return img1
