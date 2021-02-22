import numpy as np
from PIL import Image
import cv2
from math import ceil

COLORS = [
    (123, 140, 191),
    (0, 0, 0),
    (244, 205, 83),
    (0, 0, 255),
    (128, 169, 128),
    (170, 175, 140),
    (205, 181, 169),
    (120, 110, 125),
    (41, 43, 81),
    (183, 172, 140),
]


def draw_bbox(img, csv):
    with Image.open(img) as image:
        # create rectangle image
        im_arr = np.asarray(image)
        # convert rgb array to opencv's bgr format
        im_arr_bgr = cv2.cvtColor(im_arr, cv2.COLOR_RGB2BGR)
        width = im_arr_bgr.shape[1]
        for index, row in csv.iterrows():
            # Draw bounding box
            cv2.rectangle(
                img=im_arr_bgr,
                pt1=(row.x, row.y + row.Height),
                pt2=(row.x + row.Width, row.y),
                color=COLORS[index],
                thickness=ceil(width / 250),
            )
            # Put text on bottom left of the bounding box
            cv2.putText(
                img=im_arr_bgr,
                text=f"{row.Label}: {row.Score}",
                org=(row.x, row.y + row.Height),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=width / 1000,
                color=COLORS[index],
                thickness=ceil(width / 500),
            )
        im_arr = cv2.cvtColor(im_arr_bgr, cv2.COLOR_BGR2RGB)
        # convert back to Image object
        bbox_image = Image.fromarray(im_arr)
        return image, bbox_image
