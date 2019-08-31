import numpy as np
from PIL import Image
from numpy.random import choice

def load_pixels(path_to_image_file, image_width, image_height):
    im = Image.open(path_to_image_file).resize((image_width, image_height), Image.BICUBIC)
    pixels = np.array(im)
    return pixels


def normalize_image(img_tensor):
    # Normalize image data! Possibly not optimal?
    img = img_tensor / 255.0
    img = img - 0.5
    return img


# Create suitable training matrix
def map_imagematrix_to_tuples(im):

    image_height = im.shape[0]
    image_width = im.shape[1]

    # One row per pixel
    X = np.zeros((image_width * image_height, 2))

    # Fill in y values
    X[:,1] = np.repeat(range(0, image_height), image_width, 0)

    # Fill in x values
    X[:,0] = np.tile(range(0, image_width), image_height)


    # Normalize X
    X = X - X.mean()
    X = X / X.var()

    # Prepare target values
    Y = np.reshape(im, (image_width * image_height, 3))

    return (X, Y)


def generate_data(X_in, Y_in, mask_image, batch_size = 32, image_size = 80):
    # Returns a tensor X of the inputs and a tensor Y of the target values
    # Uses the mask to sample more important regions with higher probability (don't use at rendering time!)
    # Image size is width AND height (square iamages), all images will be re-sample (down or up to match this)
    # We use the yield pattern so you can work with large datasets

    # Normalize mask image

    # Average all channels (greyscale)
    mask_mat = np.mean(mask_image, 2)

    # Intensify TODO Check if really a good idea!
    mask_mat = 0.01 + mask_mat #* mask_mat

    # Make sure all numbers sum to 1
    mask_mat = mask_mat / np.sum(mask_mat)

    # ...and make it 1D to suit our choice method
    mask_mat = mask_mat.flatten()

    # Loop over images, yield batches every batch_size images
    while (1):

        pixel_selection = choice(len(X_in), size=batch_size, replace=True, p=mask_mat)
        yield (X_in[pixel_selection], Y_in[pixel_selection])

    return


