# Cropping-Tool

<strong>Requirements:</strong> 

* Python 3.9
* opencv
* numpy

<strong>USEAGE:</strong> python Cropper.py -i {input folder path} -o {output folder path} -t {type of mask to use for cropping}

-i {input folder path}: File path of the folder containing all images to be cropped.

-o {output folder path}: File path of the folder where all cropped images will be saved to.

-t {type of mask to use for cropping}: Either 0, 1, or 2.

* 0: Circle mask
* 1: Rectangle mask
* 2: Cursor drawn mask 

<strong>For circle mask:</strong>

* Left click to set center of circle.
* Release left click to set a point on the circumference of the circle.

<strong>For rectangle mask:</strong>

* First click to set top left point of cropping region.
* Second click to set bottom right point of cropping region.

<strong>For cursor drawn mask:</strong>

* Hold left click and outline the area to be cropped.
* Upon release, the outline will be completed by a line connecting the start and end point.

<strong>Notable keyboard inputs:</strong>

* Q - terminates the program immediately 
* S - Saves the current cropped region
* SPACE - Skips the current image
