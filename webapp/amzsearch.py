import requests
import random
from bs4 import BeautifulSoup

amazonsrch = 'http://www.amazon.com/s/field-keywords='

def parsefirstres(page):
    soup = BeautifulSoup(page,'lxml')
    prodid = int(random.random()*4)
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
    print url
    try:
        page = requests.get(url).text
        img, title = parsefirstres(page)
    except:
        page = requests.get(url).text
        img, title = parsefirstres(page)
    return (img,title)


def searchtag(tag):
    sstr = ' '.join(tag.split(' > ')[-2:]).replace('&','').split()
    img, title = getamazonres(sstr)
    return img, title
