import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import cv2
import time
import math
import numpy as np
import pickle


def main():
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

    # Capture 50 images and depth, then stop
    i = 0
    num_images=1
    image = core.PyMat()
    depth_for_display = core.PyMat()

    while i < num_images:
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            # Retrieve left depth
            zed.retrieve_image(depth_for_display,sl.PyVIEW.PyVIEW_DEPTH)
            
            # Show image dimensions
            print('depth width {}, depth height {}'.format(image.get_width(),image.get_height()))
            print('image width {}, image height {}'.format(image.get_width(),image.get_height()))

            #convert to arrays
            data=image.get_data()
            depth_data=depth_for_display.get_data()

            # Convert images to smaller square images
            square_image_size=500
            data=cv2.resize(data,(square_image_size,square_image_size))
            depth_data=cv2.resize(depth_data,(square_image_size,square_image_size))

            # Display the images on screen
            # cv2.imshow("ZED", data)
            # cv2.waitKey(0)
            # cv2.imshow("ZED", depth_data)
            # cv2.waitKey(0)

            start_time=time.time()
            pickle.dump(data,open( 'image_rgb{}.pickle'.format(i), 'wb' ))
            pickle.dump(depth_data,open( 'image_depth{}.pickle'.format(i), 'wb' ))
            elapsed_time=time.time()-start_time
            print('pickle time taken = {}'.format(elapsed_time))

            start_time=time.time()
            merge_images(data,depth_data)
            elapsed_time=time.time()-start_time
            print('merge time taken = {}'.format(elapsed_time))
        else:
            print('image collection failed')
        # Increment the loop
        i = i + 1

    # Close the camera
    zed.close()

def merge_images(data,depth):
    # Store the image dimensions
    data_shape=data.shape
    depth_shape=depth.shape

    print('image: {}'.format(data_shape))
    # print(data)
    print('depth: {}'.format(depth_shape))
    # print(depth)

    # Merge the depth and rgb image into one.
    if data_shape == depth_shape:
        output_data=[]
        for row in range(depth_shape[0]):
            output_data.append([])
            for col in range(depth_shape[1]):
                # join the rgb data with the depth data
                
                # Show pixel values
                # print('r {} g {} b {}'.format(data[row][col][0],data[row][col][1],data[row][col][2]))
                # print('depth pixel {}'.format(depth[row][col][0]))

                # Create the pixel to output
                pixel=[
                    data[row][col][0],
                    data[row][col][1],
                    data[row][col][2],
                    depth[row][col][0]
                    ]
                
                # output data is: red, green, blue, depth
                output_data[row].append(pixel)

        return output_data
    else:
        #images are different sizes and could not be merged
        print('image capture settings wrong')
        return None

if __name__ == "__main__":
    main()
