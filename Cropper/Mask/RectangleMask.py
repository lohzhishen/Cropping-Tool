import cv2 as cv
import numpy as np

from Mask.Mask import Mask
from Image import Image

class RectangleMask(Mask):
    """This class is a type of mask that the cropper can use."""

    def __init__(self, image: Image) -> None:
        """Constructor of the RectangleMask class."""

        super().__init__(image)

        self.tl_x = None
        self.tl_y = None
        self.br_x = None
        self.br_y = None

        self.set_point = cv.EVENT_LBUTTONDOWN
        self.stage = 0

    def get_bounding_rect(self) -> tuple[tuple[int, int], 
            tuple[int, int]]:
        """
        This method returns the top left and bottom right coordinates
        for the rectangle which bounds the unmasked region.
        """

        return ((self.tl_x, self.tl_y), (self.br_x, self.br_y))

    def make_mask(self, event, x: int, y: int) -> None:
        """
        This method is the callback function used to create a
        rectangular mask.
        """
        
        if event == self.set_point and self.stage == 0:
            self.tl_x = x
            self.tl_y = y
            self.stage = 1
        elif event == self.set_point and self.stage == 1:
            self.br_x = x
            self.br_y = y
            self.stage = 2
        elif self.stage == 2:
            self.stage = 0
            super().make_mask(event, x, y)
            self.mask = np.ones((self.height, self.width, 3)) * 255
            self.mask = cv.rectangle(
                self.mask, (self.tl_x, self.tl_y), 
                (self.br_x, self.br_y), 0, - 1
                )
            self.mask = self.mask.astype(np.bool_)