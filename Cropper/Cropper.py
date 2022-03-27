import os
import cv2 as cv
import argparse

from Image import Image
from Mask.CircleMask import CircleMask
from Mask.RectangleMask import RectangleMask
from Mask.FreeFromMask import FreeFormMask

class Cropper:
    """
    This class manages the business logic of the cropping 
    application.
    """

    def __init__(self, input: str, output: str, type: int) -> None:
        """Constructor of the Cropper class."""

        self.mask = [CircleMask, RectangleMask, FreeFormMask][type]
        self.input = input
        self.output = output
        self.image_paths = self.list_images()
        self.window_name = "Editor"
        for image_path in self.image_paths:
            self.crop(image_path)

    def list_images(self) -> list[str]:
        """
        This method gets all the paths to all images in the input 
        folder.
        """

        # initialize list to hold all file paths
        images = []

        # define the valid image types
        file_types = [".png", ".jpg"]
        
        # traverse through the tree
        for root, dirs, files in os.walk(self.input):
            # add all images in the root folder
            images.extend([os.path.join(root, file) for file in 
                files if any([file_type in file.lower() for file_type 
                in file_types])])
            
            # add all images in the sub-directories
            for dir in dirs:
                images.extend(
                    self.list_images(os.path.join(root, dir))
                    )
        
        return images

    def crop(self, image_path: str) -> None:
        """This method crops an image."""

        # create image and mask
        image = Image(image_path)
        mask = self.mask(image)
        params = {"image" : image, "mask" : mask}

        # set up the display
        cv.imshow(self.window_name, image.show_mask(mask))
        cv.setMouseCallback(self.window_name, self.call_back, params)

        # handle keyboard inputs
        while True:
            # grab keyboard input
            key = cv.waitKey(0)

            # actions for each type of input
            if key == ord('q') or key == ord('Q'):
                cv.destroyAllWindows()
                quit()
            elif key == ord('s') or key == ord('S'):
                image.save(self.output, mask)
                return
            elif key == ord(' '):
                return 
    
    def call_back(self, event, x: int, y: int, flag, 
            params: dict) -> None:
        """
        This method defines the mouse call back used on the named
        window.
        """

        # make a mask
        params["mask"].make_mask(event, x, y)

        # update the display
        cv.imshow(
            self.window_name, 
            params["image"].show_mask(params["mask"])
            )

if __name__ == "__main__":
    # Parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", 
                    help = "Path to input image folder", 
                    required = True)
    ap.add_argument("-o", "--output", 
                    help = "Path to output image folder", 
                    required = True)
    ap.add_argument("-t", '--type', 
                    help = "Type of mask to use", 
                    required = False, type = int, 
                    default = 2)
    args = vars(ap.parse_args())
    
    # print instructors for the user
    print("==== Image Cropping Script ====")
    print("INSTRUCTIONS:")
    print("[Q] - Quit \t[S] - Save \t[SPACE] - Skip")

    # start the business logic
    Cropper(args["input"], args["output"], args["type"])