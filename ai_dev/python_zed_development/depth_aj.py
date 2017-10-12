def main():
    import pyzed.camera as zcam
    import pyzed.defines as sl
    import pyzed.types as tp
    import pyzed.core as core
    import time
    import pickle
    import numpy as np
    import cv2
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
    num_images=5
    image = core.PyMat()
    depth_for_display = core.PyMat()

    print('Current mode: Capture 5 images as fast as possible.\nDo not merge the images.\nSave everything to pickle files.')

    while i < num_images:
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            # Retrieve left depth
            zed.retrieve_image(depth_for_display,sl.PyVIEW.PyVIEW_DEPTH)

            # Show image dimensions
            # print('depth width {}, depth height {}'.format(image.get_width(),image.get_height()))
            # print('image width {}, image height {}'.format(image.get_width(),image.get_height()))

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

            # Save Images
            # start_time=time.time()
            pickle.dump(data,open( 'image_rgb{}.pickle'.format(i), 'wb' ))
            pickle.dump(depth_data,open( 'image_depth{}.pickle'.format(i), 'wb' ))
            # elapsed_time=time.time()-start_time
            # print('pickle time taken = {}'.format(elapsed_time))

            # Merge images
            # start_time=time.time()
            # merged = merge_images(data,depth_data)
            # elapsed_time=time.time()-start_time
            # print('merge time taken = {}'.format(elapsed_time))
            # pickle.dump(merged,open( 'image_merged{}.pickle'.format(i), 'wb' ))
        else:
            print('image collection failed')
        # Increment the loop
        i = i + 1
    print('Image capture complete')
    # Close the camera
    zed.close()

def merge_images(data,depth):
    import cv2

    # Store the image dimensions
    data_shape=data.shape
    depth_shape=depth.shape

    # Merge the depth and rgb image into one.
    if data_shape == depth_shape:
        output_data=[]

        # Split the data (left image) into its r,g,b,alpha form respectively
        # Where alpha = visual transparency(0-255)
        red, green, blue, alpha = cv2.split(data)

        # Split the depth image into r,g,b,alpha form
        depth1, depth2, depth3, depth_alpha = cv2.split(depth)

        # merge the original r,g,b with any of depth (as they are all the same in greyscale)
        # visually to a human this will look like a transparent photo
        # but this is encoding depth information into the vector for the neural network
        output_data = cv2.merge((red, green, blue, depth1))

#        original form just incase
#        for row in range(depth_shape[0]):
#            for col in range(depth_shape[1]):
#               data[row][col][3]=depth[row][col][0] #keep only the first value out of 4 depth values

        return output_data
    else:
        #images are different sizes and could not be merged
        print('image capture settings wrong')
        return None

def load_and_display(filename):
    import pickle
    import numpy as np
    from matplotlib import pyplot as plt #note there is an opencv image viewing alternative called imshow and waitkey

    fig, ax = plt.subplots()
    image = pickle.load( open( filename, "rb" ) )
    ax.imshow(image)
    plt.show()

def load_and_merge(num):
    import time
    import pickle

    # constructing filename
    filename_rgb = 'image_rgb{}.pickle'.format(num)
    filename_depth = 'image_depth{}.pickle'.format(num)

    #loading from file
    image_rgb = pickle.load( open( filename_rgb, "rb" ) )
    image_depth = pickle.load( open( filename_depth, "rb" ) )

    #timing merge operation
    start_time=time.time()
    merged = merge_images(image_rgb,image_depth)
    elapsed_time=time.time()-start_time

    print('merge time taken = {}'.format(elapsed_time))

    return elapsed_time

def check_merge():
    import pickle
    #loading from file
    image_rgb = pickle.load( open( 'image_rgb0.pickle', "rb" ) )
    image_depth = pickle.load( open( 'image_depth0.pickle', "rb" ) )
    import numpy as np
    from matplotlib import pyplot as plt #note there is an opencv image viewing alternative called imshow and waitkey
    merged=merge_images(image_rgb,image_depth)

    fig, ax = plt.subplots()
    ax.imshow(merged)
    plt.show()

# main()
# load_and_display("image_depth0.pickle")
check_merge()

import statistics
times = [load_and_merge(i) for i in range(20)]
print('avg time: {0:.4f}s'.format(statistics.mean(times)))
