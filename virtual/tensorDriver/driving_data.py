import scipy.misc
import random

xs = []
ys = []

#points to the end of the last batch
train_batch_pointer = 0
val_batch_pointer = 0

#read data.txt
with open("driving_dataset/data.txt") as f:
    for line in f:
        xs.append("driving_dataset/" + line.split()[0])
        #the paper by Nvidia uses the inverse of the turning radius,
        #but steering wheel angle is proportional to the inverse of turning radius
        #so the steering wheel angle in radians is used as the output
        #ys.append(float(line.split()[1]) * scipy.pi / 180)
        # Input wheel ranges [-1..1]
        ys.append(float(line.split()[1]))

#get number of images
num_images = len(xs)

#shuffle list of images
c = list(zip(xs, ys))
random.shuffle(c)
xs, ys = zip(*c)

# Training set 80%
train_xs = xs[:int(len(xs) * 0.8)]
train_ys = ys[:int(len(xs) * 0.8)]

# Validation set 20%
val_xs = xs[-int(len(xs) * 0.2):]
val_ys = ys[-int(len(xs) * 0.2):]

num_train_images = len(train_xs)
num_val_images = len(val_xs)

print("Number training images: %d" % num_train_images)
print("Number validation images: %d" % num_val_images)

def LoadTrainBatch(batch_size):
    global train_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        # Load image 
        #image = scipy.misc.imread(train_xs[(train_batch_pointer + i) % num_train_images])[-150:]
        image = scipy.misc.imread(train_xs[(train_batch_pointer + i) % num_train_images], mode="RGB")
        # Resize to 66x200 and divide by 255.0
        image = scipy.misc.imresize(image, [66, 200]) / 255.0
        x_out.append(image)
        y_out.append([train_ys[(train_batch_pointer + i) % num_train_images]])
    train_batch_pointer += batch_size
    return x_out, y_out

def LoadValBatch(batch_size):
    global val_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        # Load image
        image = scipy.misc.imread(val_xs[(val_batch_pointer + i) % num_val_images], mode="RGB")
        # Resize to 66x200 and divide by 255.0
        image = scipy.misc.imresize(image, [66, 200]) / 255.0
        x_out.append(image)
        y_out.append([val_ys[(val_batch_pointer + i) % num_val_images]])
    val_batch_pointer += batch_size
    return x_out, y_out
