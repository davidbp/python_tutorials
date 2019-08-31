import os.path
import numpy as np
from PIL import Image
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.callbacks import Callback
from keras.optimizers import sgd

import argparse

IM_SIZE = 256
IM_CHANNELS = 3

def load_pixels(path_to_image_file, image_width, image_height):
    im = Image.open(path_to_image_file).resize((image_width, image_height), Image.BICUBIC)
    pixels = np.array(im)
    return pixels


def save_pixels(path_to_image_file, image_array):
    im_out = Image.fromarray(image_array, 'RGB' )
    im_out.save(path_to_image_file)


# Takes care of clipping, casting to int8, etc.
def save_ndarray(path_to_outfile, x, width = IM_SIZE, height = IM_SIZE, channels = IM_CHANNELS):

    out_arr = np.clip(x, 0, 255)
    out_arr = np.reshape(out_arr, (width, height, channels), 1)

    out_arr = np.rot90(out_arr, k=3)
    out_arr = np.fliplr(out_arr)
    save_pixels(path_to_outfile, out_arr.astype(np.int8))


# Create suitable training matrix
def gen_input_tuples(pixels_width, pixels_height, scale, translate_x, translate_y):

    image_height = pixels_height
    image_width = pixels_width

    # One row per pixel
    X = np.zeros((image_width * image_height, 2))

    # Fill in y values
    X[:,1] = np.repeat(range(0, image_height), image_width, 0)

    # Fill in x values
    X[:,0] = np.tile(range(0, image_width), image_height)

    X = X + np.asarray([0,translate_x])
    X = X + np.asarray([translate_y,0])

    # Normalize X
    X = X - X.mean()
    X = X / X.var()

    X = X * scale

    return (X)



model = Sequential()

# Inputs: x and y
model.add(Dense(20, input_dim=2, activation="relu"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))
model.add(Dense(20,  activation="relu", init="glorot_normal"))

# Outputs: r,g,b
model.add(Dense(3))

parser = argparse.ArgumentParser()

parser.add_argument("--model", type=str, action="store", help="path to model file", required=True)
parser.add_argument("--pixels", type=int, action="store", help="Number of pixels that the square output image will be wide/high")
parser.add_argument("--scale", type=float, action="store", help="Magnification factor - below 1 zooms out", default=1.0)
parser.add_argument("--tx", type=float, action="store", help="Translate image on x axis", default=0.0)
parser.add_argument("--ty", type=float, action="store", help="Translate image on y axis", default=0.0)
parser.add_argument("--image", type=str, action="store", help="Name output file", default="out.png")

args = parser.parse_args()

model.load_weights(args.model)

model.compile(loss='mean_squared_error',
               optimizer='adamax')

X = gen_input_tuples(args.pixels, args.pixels, args.scale, args.tx, args.ty)

generated_image = model.predict(X)
save_ndarray(args.image, generated_image, args.pixels, args.pixels)
