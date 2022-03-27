import cv2 as cv
import os
import numpy as np

from Mask.Mask import Mask

class Image:
    """This class models an image."""
    
    def __init__(self, path: str) -> None:
        """Constructor of the Image class."""

        self.raw_image = cv.imread(path)
        self.name = path.split(os.path.sep)[-1].split(".")[0]

    def get_shape(self) -> tuple[int, int]:
        """Returns the height and width of the image."""

        return self.raw_image.shape[:2]

    def apply_mask(self, mask: Mask) -> np.ndarray:
        """
        This method applies the inputted mask to the image and 
        converts it to a BGRA image with all masked regions set to
        transparent and crops it to the smallest region such that all
        unmasked regions are visible.
        """

        image = self.raw_image.copy()

        # add the alpha layer to the image
        image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

        # check if the mask is valid
        if not mask.valid():
            return image
        
        # get the details of the mask
        (min_x, min_y), (max_x, max_y) = mask.get_bounding_rect()
        mask = mask.get_mask()

        # apply the mask
        image[:,:,3][mask[:, :, 0]] = 0
        image = image[min_y:max_y, min_x:max_x]

        return image
        
    def show_mask(self, mask: Mask) -> np.ndarray:
        """
        This method applies the mask to the image by darkening the
        unmasked regions by 50%.
        """

        image = self.raw_image.copy()

        # check if the mask is valid
        if not mask.valid():
            return image
        
        # get the details of the mask
        mask = mask.get_mask()

        # apply the mask
        image[mask] = (image[mask] * 0.5).astype(np.uint8)
        return image

    def save(self, output: str, mask: Mask) -> None:
        """
        This method is used to save a image with a certain mask to
        the output folder.
        """

        cv.imwrite(os.path.join(output, self.name + ".png"), 
                   self.apply_mask(mask))
    