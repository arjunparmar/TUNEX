import keras
import os
from keras.preprocessing import image
import numpy as np
import shutil

base_dir = '../dataset/KDEF_and_AKDEF/KDEF/'

def read(filename):
    data = []
    file = open(filename, 'r')
    for line in file:
        data.append(line.replace('\n',''))
    file.close()
    return data

def seperate_description(data):
    path = [i.split(',')[0] for i in data]
    expression = [i.split(',')[1] for i in data]
    angle = [i.split(',')[2] for i in data]
    return path, expression, angle

def make_dir(dir, label_range):
    if not os.path.exists(dir):
        os.mkdir(dir)
        for i in label_range:
            i_dir = os.path.join(dir, str(i))
            if not os.path.exists(i_dir):
                os.mkdir(i_dir)

def move_images_to_dir(dir, data, label):
    for path, expression in zip(data, label):
        file = path.split('/')[1]
        src = os.path.join(base_dir,path)
        dst = os.path.join(dir, str(expression), file)
        shutil.copyfile(src, dst)

if __name__ == '__main__':
    training_data = read('train.txt')
    test_data = read('test.txt')
    val_data = read('validation.txt')
    print(len(training_data), len(test_data), len(val_data))
    train_data, train_label, train_angle = seperate_description(training_data)
    test_data, test_label, test_angle = seperate_description(test_data)
    validation_data, validation_label, validation_angle = seperate_description(val_data)

    data_dir = 'data/'

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    label_range = np.unique(train_label)

    # training data dictionary
    train_dir = os.path.join(data_dir, 'train')
    make_dir(train_dir, label_range)

    # test data dictionary
    test_dir = os.path.join(data_dir, 'test')
    make_dir(test_dir, label_range)
    
    # validation data dictionary
    validation_dir = os.path.join(data_dir, 'validation')
    make_dir(validation_dir, label_range)

    move_images_to_dir(train_dir, train_data, train_label)
    print("Copied Training Images")

    move_images_to_dir(test_dir, test_data, test_label)
    print("Copied Test Images")

    move_images_to_dir(validation_dir, validation_data, validation_label)
    print("Copied Validation Images")