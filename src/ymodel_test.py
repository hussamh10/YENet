from cv2 import imread
import cv2
import os
from ynet import get_ynet
import keras
import numpy as np

def save(data, i, path):
    data = data.astype('float32')
    cv2.imwrite(path + str(i) + ".png",data)

def getImage(i, source, main_dir, ext, size):
    name = str(i) + ext

    path = os.path.join(main_dir, source , name)
    print(path)
    img = imread(path, 0)
    img = cv2.resize(img, size)
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype('float32')
    img /= 255
    return img

def ok(start,videoType):
    i = start
    dir1 = '..\\data\\tabletennis\\frames\\' + str(videoType) + '\\'
    dir2 = '..\\data\\tabletennis\\specs\\' + str(videoType) + '\\'
    frame_ext = '.jpg'
    audio_ext = '.png'
    x1 = getImage(i        , '', dir1, frame_ext, (224, 224))
    x2 = getImage(int(i/24), '', dir2, audio_ext, (224, 224))
    x3 = getImage(i+1      , '', dir1, frame_ext, (224, 224))
    print("-------------------------------")

    x1 = x1.reshape((1, x1.shape[0], x1.shape[1], x1.shape[2]))
    x2 = x2.reshape((1, x2.shape[0], x2.shape[1], x2.shape[2]))
    x3 = x3.reshape((1, x3.shape[0], x3.shape[1], x3.shape[2]))


    return [x1, x2], x3, x1, x2

def test():
    md = get_ynet()

    md.load_weights('..\\checkpoints\\ynet1.hdf5')
    root = '..\\data\\tabletennis\\fcnet\\y\\'
    for videoType in range(1,2):
        tc = 1
        for start in range(1,4917):
            tag = root + str(videoType) + "\\tc (" + str(tc) + ")\\"
            
            
            h, hy, x1, x2 = ok(start,videoType)
            
            hp = md.predict(h)
            
            if not os.path.exists(tag):
                os.makedirs(tag)
            
            i = start
            for p, g in zip(hp, hy):
                p *= 255;
                g *= 255;
                x1 *= 255;
                x2 *= 255;
                save(p.reshape((224, 224)), i, tag+'x3') #output
                save(g.reshape((224, 224)), i, tag+'x4') #ground truth
                save(x1.reshape((224, 224)), i, tag+'x1')#input1
                save(x2.reshape((224, 224)), i, tag+'x2')#input2
                i += 1
	    	
            tc+=1
test()
