import os.path
import numpy as np
from PIL import Image
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.callbacks import Callback
from keras.optimizers import sgd

import argparse
from utils import load_pixels, map_imagematrix_to_tuples, generate_data

IM_SIZE = 256
IM_CHANNELS = 3


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


parser = argparse.ArgumentParser()
parser.add_argument("--target_image", type=str, action="store", help="Path to the image file we'll be trying to learn", required = True)
parser.add_argument("--model_output_root", type=str, action="store", help="root of name for various save files", default = "facepaint_out_")
parser.add_argument("--pixels", type=int, action="store", default=256, help="Input image will be resampled to this size.  Easy way to control training time.")
parser.add_argument("--batch_size", type=int, action="store", default=32, help="Size of batch of samples used to update weights at each step")
parser.add_argument("--epochs", type=int, action="store", default=1000, help="Number of passes to take through the training data")
parser.add_argument("--mask", type=str, action="store", help="A greyscale image that tells us which parts of the target are more important.", required=False)
args = parser.parse_args()

image_matrix = load_pixels(args.target_image, args.pixels, args.pixels)
mask_matrix = None
if args.mask == None:
    # Give all pixels equal weight if no mask specified
    mask_matrix = np.ones(shape=image_matrix.shape)
else:
    mask_matrix = load_pixels(args.mask, args.pixels, args.pixels)

X,Y = map_imagematrix_to_tuples(image_matrix)

model = Sequential()

# Inputs: x and y => 2 dimensions
model.add(Dense(20, input_dim=2, activation="relu"))

# Adding more layers will give better results. Don't be shy - try doubling!
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

model_weights_name = args.model_output_root + '_model.h5'
if os.path.isfile(model_weights_name):
    # Loading old model, will continue training from saved point
    print ("Loading old model...")
    model.load_weights(model_weights_name)
else:
    print ("Could not find weights, starting from scratch")


model.compile(loss='mean_squared_error',
               optimizer='adam')

# Let's see the how the output changes as the model trains
class training_monitor(Callback):
    def __init__(self):
        self.epoch = 0

    def on_epoch_end(self, epoch, logs={}):
        cur_img = model.predict(X)
        save_ndarray(args.model_output_root + "_image_epoch_" + str(self.epoch) + ".jpg", cur_img, args.pixels, args.pixels)
        model.save_weights(args.model_output_root + "_facepaint_model_epoch_" + str(self.epoch) + ".h5", overwrite=True)
        self.epoch = self.epoch + 1

image_progress_monitor = training_monitor()
#model.fit(X, Y, nb_epoch = args.epochs, batch_size = args.batch_size, callbacks=[image_progress_monitor], shuffle=True)
model.fit_generator(generator=generate_data(X,Y,mask_matrix,args.batch_size,image_size=args.pixels), steps_per_epoch=1000, epochs=args.epochs, callbacks=[image_progress_monitor])
# Save final (best?) model
model.save_weights(model_weights_name)

learnt_image = model.predict(X)
save_ndarray(args.model_output_root + "_final_image.jpg", learnt_image, args.pixels, args.pixels)
