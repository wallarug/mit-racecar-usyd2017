
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

# save_all_images()
# load_and_display(0)
# load_and_display(0,'rgb')
# load_and_display(0,'depth')
