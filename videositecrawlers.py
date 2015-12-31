import urllib
from bs4 import BeautifulSoup
import re

def fetch(url):
    return urllib.urlopen(url).read()

def extractss(data):
    regex = '\"storyboard\_spec\"\:.+'
    code = re.findall(regex,data)[0].split(',')[0]
    highestres = code.split('|')[-1]
    images = int(highestres.split('#')[2]) + 1
    imagespershot = int(highestres.split('#')[3])
    size = (int(highestres.split('#')[0]),int(highestres.split('#')[1]))
    return code.split('#')[-1].replace('"',''), images, imagespershot**2, size

def createssurl(sigh,videoid,images,imagespershot):
    url = 'https://i.ytimg.com/sb/%s/storyboard3_L2/M%d.jpg?sigh=%s'
    urls = []
    for i in range(images/imagespershot + 1):
        ssurls = url % ( videoid, i, sigh )
        urls.append(ssurls)
    return urls

def processvideourl(vurl):
    videoid = vurl.split('=')[1]
    sigh, images, imagespershot, size = extractss(fetch(vurl))
    return createssurl(sigh,videoid,images,imagespershot)

vurl = 'https://www.youtube.com/watch?v=DU5mHVR6IJ4'
#print processvideourl(vurl)
