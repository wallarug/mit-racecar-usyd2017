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
            print('depth width {}, depth height {}'.format(image.get_width(),image.get_height()))
            print('image width {}, image height {}'.format(image.get_width(),image.get_height()))

            #convert to arrays
            data=image.get_data()
            depth_data=depth_for_display.get_data()

            print('image:')
            data_shape=data.shape
            print(data_shape)
            # print(data)

            print('depth:')
            depth_shape=depth_data.shape
            print(depth_shape)
            # print(depth_data)

            # Display the images on screen
            # cv2.imshow("ZED", data)
            # cv2.waitKey(0)
            # cv2.imshow("ZED", depth_data)
            # cv2.waitKey(0)

            if data_shape == depth_shape:
                start_time=time.process_time()
                for row in range(depth_shape[0]):
                    for col in range(depth_shape[1]):
                        # join the rgb data with the depth data
                        
                        # Show pixel values
                        # print('r {} g {} b {}'.format(data[row][col][0],data[row][col][1],data[row][col][2]))
                        # print('depth pixel {}'.format(depth_data[row][col][0]))

                        # output data is: red, green, blue, depth
                        depth_data[row][col]=[
                            data[row][col][0],
                            data[row][col][1],
                            data[row][col][2],
                            depth_data[row][col][0]
                            ]
                elapsed_time=time.process_time()-start_time

                print('new data for neural network')
                print(depth_data.shape)
                print('time taken = {}'.format(elapsed_time))
                
                # save the pickle
                pickle.dump(depth_data,open( 'depth.pickle', 'wb' ))
            else:
                print('image capture settings wrong')
        else:
            print('image collection failed')
        # Increment the loop
        i = i + 1

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
