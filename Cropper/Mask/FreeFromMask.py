import numpy as np
import cv2 as cv

from Mask.Mask import Mask
from Image import Image

class FreeFormMask(Mask):
    def __init__(self, image: Image) -> None:
        """Constructor of the FreeFormMask class."""

        super().__init__(image)

        self.contours = []

        self.start = cv.EVENT_LBUTTONDOWN
        self.stop = cv.EVENT_LBUTTONUP
        self.record = False

    def get_bounding_rect(self) -> tuple[tuple[int, int], 
            tuple[int, int]]:
        """
        
        """

        contours = np.asarray(self.contours)
        x_min = contours[np.argmin(contours[:,0]),0]
        x_max = contours[np.argmax(contours[:,0]),0]
        y_min = contours[np.argmin(contours[:,1]),1]
        y_max = contours[np.argmax(contours[:,1]),1]

        return (x_min, y_min), (x_max, y_max)

    def make_mask(self, event, x: int, y: int) -> None:
        """
        
        """

        if event == self.start:
            self.contours = []
            self.record = True

        if self.record:
            self.contours.append([x, y])

        if event == self.stop:
            self.record = False
            super().make_mask(event, x, y)
            self.mask = np.ones((self.height, self.width, 3)) * 255
            self.mask = cv.drawContours(self.mask, [np.asarray(self.contours)], -1, 0, -1)
            self.mask = self.mask.astype(np.bool_)