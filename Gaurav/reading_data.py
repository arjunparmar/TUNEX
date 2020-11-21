import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def dict_walk(base_dir):
    datas = []
    for i, j, k in os.walk(base_dir):
        
        for img in k:
            name = img.split('.')[0]
            Number = name[:4]
            expression = name[4:6]
            angle = name[6:]
            #print(Number, expression, angle)
            switch_expression = {
                "AF": 0,
                "AN": 1,
                "DI": 2,
                "HA": 3,
                "NE": 4,
                "SA": 5,
                "SU": 6
            }
            switch_angle = {
                "FL": 0,
                "FR": 1,
                "HL": 2,
                "HR": 3,
                "S" : 4
            }
            data =  Number + '/' + img + ',' + \
                    str(switch_expression[expression]) + ',' + \
                    str(switch_angle[angle])
            datas.append(data)
            #print(data)
    return datas

def save_file(file_name, rows):
    file = open(file_name, 'w', encoding='utf-8')
    
    for row in rows:
        file.write(row+"\n")
    file.close()

if __name__ == '__main__':

    base_dir = '../dataset/KDEF_and_AKDEF/KDEF/'
    datas = dict_walk(base_dir)
    print(len(datas))
    save_file('allDatas.txt', datas)
    np.random.shuffle(datas)
    num_test_samples = 500
    num_validation_samples = 500
    validation_data = datas[:num_validation_samples]
    test_data = datas[num_validation_samples:num_validation_samples+num_test_samples]
    train_data = datas[num_validation_samples+num_test_samples:]
    save_file('validation.txt', validation_data)
    save_file('test.txt', test_data)
    save_file('train.txt', train_data)
