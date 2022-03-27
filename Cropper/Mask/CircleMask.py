import numpy as np
import cv2 as cv

from Mask.Mask import Mask
from Image import Image

class CircleMask(Mask):
    """This class is a type of mask that the cropper can use."""

    def __init__(self, image: Image) -> None:
        """Constructor of the CircleMask class."""

        super().__init__(image)

        self.x = None
        self.y = None
        self.radius = None
        
        self.set_center = cv.EVENT_LBUTTONDOWN
        self.set_radius = cv.EVENT_LBUTTONUP
        self.update = False

    def get_bounding_rect(self) -> tuple[tuple[int, int], 
            tuple[int, int]]:
        """
        This method returns the top left and bottom right coordinates 
        for the rectangle which bounds the unmasked region.
        """

        return ((self.x - self.radius, self.y - self.radius) 
            , (self.x + self.radius, self.y + self.radius))

    def make_mask(self, event, x: int, y: int) -> None:
        """
        This method is the callback function used to create a 
        circular mask. 
        """

        # define reactions to different events
        if event == self.set_center:
            self.x = x
            self.y = y
            self.update = True
        elif event == self.set_radius:
            self.radius = self.get_radius(x, y)
            self.update = True

        # generate the mask
        if (self.update and self.x != None 
            and self.y != None and self.radius != None):
            super().make_mask(event, x, y)
            self.update = False
            self.mask = np.ones((self.height, self.width, 3)) * 255
            self.mask = cv.circle(self.mask, (self.x, self.y), 
                                  self.radius, 0, -1)
            self.mask = self.mask.astype(np.bool_)

    def get_radius(self, x: int, y: int) -> int:
        """
        This method calculates the euclidean distance between the
        inputted (x, y) coordinates and the center of the circle.
        It then rounds the distance to the nearest integer.
        """

        delta_x = self.x - x
        delta_y = self.y - y
        distance = round((delta_x**2 + delta_y**2)**0.5)
        return distance