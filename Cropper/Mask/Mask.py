from abc import ABC, abstractmethod
import numpy as np

class Mask(ABC):
    """
    This class functions as the base class for different types of 
    masks that the cropper uses.
    """
                                                       
    def __init__(self, image) -> None:
        """
        Constructor of the mask. All subclasses of this class should 
        call this constructor.
        """

        self.height, self.width = image.get_shape()
        self.mask = None
        self.has_mask = False

    @abstractmethod
    def get_bounding_rect(self) -> tuple[tuple[int, int], 
            tuple[int, int]]:
        """
        This method returns the top left and bottom right coordinates 
        for the rectangle which bounds the unmasked region.
        """

        pass

    def get_mask(self) -> np.ndarray:
        """Getter method to get the mask."""

        return self.mask

    def make_mask(self, event, x: int, y: int) -> None:
        """
        Callback method used to create the mask. All subclasses
        of this class should override this method and call it once
        a mask has been generated.
        """

        self.has_mask = True
    
    def valid(self) -> bool:
        """Checks if there is a mask."""

        return self.has_mask