import os, sys
import time
import numpy as np
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import urllib
import caffe
import exifutil
import glob
import cv2

base_path = '/media/karthik/0ed39684-ffb3-432a-bd76-d1e04ccd8716/administrator/models/clothing/'
model_def_file=base_path+'deploy.prototxt'
pretrained_model_file=base_path+'snapshot.caffemodel'
mean_file=base_path+'mean.npy'
class_labels_file=base_path+'labels.txt'
bet_file=base_path+'betfile.empty'
image_dim=256
raw_scale=255
batch_size=256
labels = []

def loadclf():
    with open(class_labels_file) as f:
        labels_df = pd.DataFrame( [
            {
                'synset_id': j,#int(l.strip().split(' ')[0]),                                                                                                                                  
                'name': l.strip()
            }
            for j,l in enumerate(f.readlines())
        ] )
        labels = labels_df.sort('synset_id')['name'].values
        print labels

    caffe.set_mode_cpu()
    net = caffe.Classifier( model_def_file, pretrained_model_file,\
                            image_dims=(image_dim, image_dim), raw_scale=raw_scale,\
                            mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0))
    net.forward()
    return net, labels

def classify(net,labels,imagesFname):
    images = []
    for i in range(len(imagesFname)):
        images.append(exifutil.open_oriented_im(str(i)+'.jpg'))
    scores = net.predict(images, oversample=False)
    scoresLabels = [ labels[(-x).argsort()[:1][0] ] for x in scores ]
    output = zip( imagesFname, scoresLabels )
    return output

def readimage(url):
    req = urllib.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1)
    return img

