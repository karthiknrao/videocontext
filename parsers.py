from bs4 import BeautifulSoup
import urllib
import sys

def fetch(url):
    return urllib.urlopen(url).read()

def extractimages(page):
    soup = BeautifulSoup(page,'lxml')
    images = soup.findAll('div','mol-img')
    return [ x.findAll('img')[0]['src'] for x in images ]

page = fetch(sys.argv[1])
images = extractimages(page)
open( 'imgurls', 'w' ).write( '\n'.join(images) )
#test_url = 'http://www.dailymail.co.uk/tvshowbiz/article-3382383/Keira-Knightley-rocks-favoured-grunge-style-tough-leather-jacket-heavy-boots-braces-against-NYC-chill-ahead-final-Th-r-se-Raquin-performance.html'
#test_url = 'http://www.dailymail.co.uk/tvshowbiz/article-3382232/Fab-phwoarty-Abi-Titmuss-proves-s-got-exhibits-famous-curves-halterneck-bikini-Malibu-one-month-turning-40.html'
#page = fetch(test_url)
#images = extractimages(page)
#print '\n'.join(images)
