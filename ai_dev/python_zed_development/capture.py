
import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import numpy as np
import cv2
import sys
import os

print('Setting up camera.')

# Create a PyZEDCamera object
zed = zcam.PyZEDCamera()

# Create a PyInitParameters object and set configuration parameters
init_params = zcam.PyInitParameters()
init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)

# Open the camera
err = zed.open(init_params)
if err != tp.PyERROR_CODE.PySUCCESS:
    exit(1)

# Create and set PyRuntimeParameters after opening the camera
runtime_parameters = zcam.PyRuntimeParameters()
runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode

i = 0 #counter
image = core.PyMat()
depth_for_display = core.PyMat()
print('Camera setup complete.')

def capture_image(square_image_size):
    # A new image is available if grab() returns PySUCCESS
    if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
        # Retrieve left image
        zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
        # Retrieve left depth
        zed.retrieve_image(depth_for_display,sl.PyVIEW.PyVIEW_DEPTH)

        data=cv2.resize(data,(square_image_size,square_image_size))
        depth_data=cv2.resize(depth_data,(square_image_size,square_image_size))

        #convert to arrays
        data=image.get_data()
        depth_data=depth_for_display.get_data()

        return merge_images(data,depth_data)
    else:
        print('image collection failed')