def main(num_images):
    import pyzed.camera as zcam
    import pyzed.defines as sl
    import pyzed.types as tp
    import pyzed.core as core
    import time
    import pickle
    import numpy as np
    import cv2
    import pygame
    from time import sleep
    import sys

    # CONTROLLER SETUP
    joystick_events_filename="joystick_events.txt"
    joystick_events_file= open(joystick_events_filename, "w")
    # start pygame
    pygame.init()

    # count how many joysticks there are...
    joycount = pygame.joystick.get_count() 

    # check that a joystick is actually connected.
    if joycount < 1:
        print("No Joystick detected!")
        sys.exit(0)

    # there is atleast one joystick, let's get it.
    j = pygame.joystick.Joystick(0)
    j.init()

    # joystick static storage setup
    axes = [0] * j.get_numaxes()
    buts = [0] * j.get_numbuttons()

    # display which joystick is being used
    print("You are using the {0} controller.".format(j.get_name))
    # CONTROLLER SETUP COMPLETE

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

    print('Current mode: Capture {} images as fast as possible.\nMerge the images.\nSave to pickle files.'.format(num_images))
    start_time=time.time()
    while i < num_images:
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            # Retrieve left depth
            zed.retrieve_image(depth_for_display,sl.PyVIEW.PyVIEW_DEPTH)

            # JOYSTICK
            pygame.event.pump() # keep everything current
            throttle = (j.get_axis(0)+1)/2 # left stick
            steering = (j.get_axis(4)+1)/2 # right stick steering
            exit_button = j.get_button(9) # Options button exits

            # For saving timestamped messages
            button_message={
                0 : "driving started",	# A button
                1 : "driving finished",		# B button
                2 : "bad driving",	# X button
                3 : "good driving",	# Y button
                9 : "exiting"		# Options button
            }

            for button_number, message in button_message.items():
                if j.get_button(button_number):
                    saved_string='image_{}_event_{}_time_{}\n'.format(i,message,time.strftime('%X %x %Z'))
                    print(saved_string)
                    joystick_events_file.write()

            if exit_button:
                print('Exit button (options) pressed. Stopping data collection')
                break

            #convert to arrays
            data=image.get_data()
            depth_data=depth_for_display.get_data()

            # Convert images to smaller square images
            # square_image_size=500
            # data=cv2.resize(data,(square_image_size,square_image_size))
            # depth_data=cv2.resize(depth_data,(square_image_size,square_image_size))

            merged = merge_images(data,depth_data)
            print('writing dataset/image_{0}_{1:.4f}_{2:.4f}.pickle'.format(i,throttle,steering))
            pickle.dump(merged,open( 'dataset/image_{0}_{1:.4f}_{2:.4f}.pickle'.format(i,throttle,steering), 'wb' ))
        else:
            print('image collection failed')
        # Increment the loop
        i = i + 1

    j.quit()
    print('Image capture complete')
    print('Total time taken = {}'.format(time.time()-start_time))
    joystick_events_file.close()
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

        return output_data
    else:
        #images are different sizes and could not be merged
        print('image capture settings wrong')
        return None

def load_and_display(file_index,mode='both'):
    filename = get_image_filename(file_index)
    import pickle
    import numpy as np

    image = pickle.load( open( filename, "rb" ) )
    if mode == 'both':
        display_image(image)
    else:
        # Reconstruct the original rgb and depth images from the merged values
        import cv2
        red, green, blue, depth = cv2.split(image)
        if mode == 'rgb':
            rgb_image = cv2.merge((red,green,blue))
            display_image(rgb_image)
        elif mode == 'depth':
            depth_image = cv2.merge((depth,depth,depth))
            display_image(depth_image)
        else:
            print('Invalid image display mode. Please select from both, rgb or depth.')

def display_image(image):
    from matplotlib import pyplot as plt #note there is an opencv image viewing alternative called imshow and waitkey
    fig, ax = plt.subplots()
    ax.imshow(image)
    plt.show()

def get_image_filename(index):
    import os
    prefix='image_{}_'.format(index)
    prefixed = [filename for filename in os.listdir('dataset') if filename.startswith(prefix)]
    if len(prefixed)>0:
        return 'dataset/'+prefixed[0]
    else:
        raise FileNotFoundError("No filename found with index of {}".format(index))
        return ''

def save_all_images():
    import cv2
    import pickle
    import os

    # saves all the files in the dataset folder as image files in a different folder
    image_folder= 'images/'

    # all files
    prefix='image_'
    prefixed = [filename for filename in os.listdir('dataset') if filename.startswith(prefix)]

    for image_pickle_file in prefixed:
        image = pickle.load( open( 'dataset/'+image_pickle_file, "rb" ) )

        red, green, blue, depth = cv2.split(image)
        rgb_image = cv2.merge((red,green,blue))
        depth_image = cv2.merge((depth,depth,depth))

        image_name = image_pickle_file.replace('.pickle','')

        print('saving image {}'.format(image_name))

        save_image(image_folder+'rgb/'+image_name , rgb_image)
        save_image(image_folder+'depth/'+image_name , depth_image)

def save_image(filename,image):
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.imshow(image)
    plt.savefig(filename+'.png', bbox_inches='tight')
    plt.close()

main(10000) #capture 60 images
# save_all_images()
# load_and_display(0)
# load_and_display(0,'rgb')
# load_and_display(0,'depth')
