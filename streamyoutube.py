import cv2
import cv
from pytube import YouTube
import sys, os
import pdb
import urllib
import numpy as np
import threading
import time
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import caffe
import exifutil
import glob
from bs4 import BeautifulSoup
import requests
import random

base_path = '/media/karthik/0ed39684-ffb3-432a-bd76-d1e04ccd8716/administrator/models/electronics/'
model_def_file=base_path+'deploy.prototxt'
pretrained_model_file=base_path+'snapshot.caffemodel'
mean_file=base_path+'mean.npy'
class_labels_file=base_path+'labels.txt'
bet_file=base_path+'betfile.empty'
image_dim=256
raw_scale=255
batch_size=256
labels = []

amazonsrch = 'http://www.amazon.com/s/field-keywords='

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

def parsefirstres(page):
    soup = BeautifulSoup(page,'lxml')
    prodid = int(random.random()*2)
    firstprod = soup.findAll( 'li', { 'id' : 'result_%d' % prodid } )[0]
    img = firstprod.findAll('img')[0]['src']
    title = firstprod.findAll('h2','a-size-medium a-color-null s-inline s-access-title a-text-normal')[0].text
    title = title.encode('ascii','ignore')
    titles = title.split()
    leng = len(titles)
    title = ' '.join(titles[:leng/2]) + '\n' + ' '.join(titles[leng/2:])
    return (img,title)

def getamazonres(srchterms):
    url = amazonsrch + '+'.join(srchterms)
    #url = 'http://www.amazon.com/s/field-keywords=Touch+Screen+Tablet+Accessories+Stands'
    print url
    try:
        page = requests.get(url).text
        img, title = parsefirstres(page)
    except:
        page = requests.get(url).text
        img, title = parsefirstres(page)
    return (img,title)
"""
print getamazonres([])
sys.exit(0)
"""
class Ad():
    def __init__(self,url,title,size):
        req = urllib.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr,-1) # 'load it as it is'
        self.image = cv2.resize(img,(50,50))
        self.title = title

    def createad(self,size):
        img = np.ones((size[0]+50,size[1],3),np.uint8)
        img = img*255
        text = np.ones((50,size[1]-50,3),np.uint8)
        text = text*255
        font = cv2.FONT_HERSHEY_SIMPLEX
        titles = self.title.split('\n')
        base = 20
        for title in titles:
            cv2.putText(text,title,(30,base), font, 0.4,(0,0,0),1)
            base += 11
        img[size[0]:,:50,:] = self.image[:,:,:3]
        img[size[0]:,50:,:] = text
        
        return img
   
def createadchange(url,title,size):
    global adblock
    req = urllib.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1) # 'load it as it is'
    image = cv2.resize(img,(50,50))
    text = np.ones((50,size[1]-50,3),np.uint8)
    text = text*255
    font = cv2.FONT_HERSHEY_SIMPLEX
    titles = title.split('\n')
    base = 20
    for title in titles:
        cv2.putText(text,title,(30,base), font, 0.35,(0,0,0),1)
        base += 11
    adblock[:50,:50,:3] = image
    adblock[:50,50:,:3] = text
    return
    
def doframeclassify():
    print 'Starting ..'
    global net
    global labels
    global capframe
    global adblock
    global size
    global adchange
    while True:
        if capframe != None:
            cv2.imwrite('img' + '.jpg', capframe )
            images = [exifutil.open_oriented_im('img.jpg')]
            scores = net.predict(images, oversample=False)
            scoresLabels = [ labels[(-x).argsort()[:1][0] ] for x in scores ]  
            sstr = ' '.join(scoresLabels[0].split(' > ')[-2:]).replace('&','').split()
            img, title = getamazonres(sstr)
            print scoresLabels[0]
            createadchange(img,title,size)
            adchange = True
        capframe = None
            
vurl = sys.argv[1]

capframe = None
yt = YouTube(vurl)
videos = yt.get_videos()
prefetchurl = ''
streamurl = ''
for video in videos:
    if '240p' == video.resolution:
        streamurl = video.url
    if '144p' == video.resolution:
        prefetchurl = video.url

cap = cv2.VideoCapture(streamurl)
fps = cap.get(cv.CV_CAP_PROP_FPS)
print 'FPS ', fps
framen = 0
cv2.namedWindow('frame')
frame = cap.read()
size = frame[1].shape
cv2.resizeWindow('frame',size[1],size[0])
blockimg = Ad('http://ecx.images-amazon.com/images/I/31F80tz4ENL._AA160_.jpg',"Syma X5C Explorers 2.4G 4CH 6-Axis Gyro\nRC Quadcopter With HD Camera",size).createad(size)
fc = 0
classifythread = threading.Thread(target=doframeclassify)
classifythread.start()
adchange = False
adblock = np.zeros((50,size[1],3))
while(True):
    blockimg[:size[0],:size[1],:] = frame[1]
    if adchange:
        blockimg[size[0]:,:,:] = adblock
        adchange = False
    if fc % 1050 == 0 or fc == 50 and fc > 0:
        capframe = frame[1]
    cv2.imshow('frame',blockimg)
    frame = cap.read()
    fc += 1
    if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
