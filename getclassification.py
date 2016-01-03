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
#caffe.set_device(int(sys.argv[1]))
net = caffe.Classifier( model_def_file, pretrained_model_file,\
                        image_dims=(image_dim, image_dim), raw_scale=raw_scale,\
                        mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0))
net.forward()

images=[]
imageFname = []
files = [ x.strip() for x in open( sys.argv[1] ).readlines() ]
#outpath = sys.argv[2] + '_' + 'output_shoess.tsv'                                                                                                                                                       
for img in files:
    try:
        images.append(exifutil.open_oriented_im(img))
        imageFname.append(img)
    except:
        print img
        continue
    if len(images) == 1 and len(imageFname) == 1:
        starttime = time.time()
        scores = net.predict(images, oversample=False)
        endtime = time.time()
        """
        x = net.blobs['fc7'].data
        filname = os.path.basename(imageFname[0]).split('.')[0]
        destname = '/home/indix/gps/cnnencodings/' + filname
        print filname
        np.save(destname,x)
        """
        scoresLabels = [ labels[(-x).argsort()[:1][0] ] for x in scores ]                                                                                                                                       
        output = zip( imageFname, scoresLabels )
        print output
        """
        with open( outpath, 'a' ) as outfile:                                                                                                                                                                   
            outfile.write( '\n'.join([ '\t'.join(x) for x in output ]) + '\n' )                                                                                                                                 
        print str(len(images)), ' images took ' , '%.3f' % (endtime - starttime) , ' Secs'                                                                                                                      
        """
        images=[]
        imageFname = []
