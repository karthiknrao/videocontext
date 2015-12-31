import cv2
from skimage import io
from videositecrawlers import *

def processssimages(urls,size):
    for i, url in enumerate(urls):
        img = io.imread(url)
        print img.shape,size
        for j in range(img.shape[0]/size[1]):
            for k in range(img.shape[1]/size[0]):
                part = img[j*size[1]:(j+1)*size[1],k*size[0]:(k+1)*size[0],:]
                outname = str(i) + '_' + str(j) + '_' + str(k) + '_.jpg'
                io.imsave( outname, part )
    return

#vurl = 'https://www.youtube.com/watch?v=DU5mHVR6IJ4'
#vurl = 'https://www.youtube.com/watch?v=G3vr26wkrKc'
#vurl = 'https://www.youtube.com/watch?v=XdlmoLAbbiQ'
vurl = 'https://www.youtube.com/watch?v=B7DhVfN8i4s'
videoid = vurl.split('=')[-1]
sigh,images,imagespersshot,size = extractss(fetch(vurl))
urls = createssurl(sigh,videoid,images,imagespersshot)
processssimages(urls,size)
