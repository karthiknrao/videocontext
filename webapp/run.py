from flask import Flask, render_template, request
from parsers import *
from loadclf import *
from amzsearch import *
import cv2

app = Flask(__name__)

imageclf, labels = loadclf()

adtemplate = '<tr><h2>%s</h2><img src="%s" style="width:100px;height:100px;">'

@app.route("/")
def template_test():
    url = request.args['url']
    page = fetch(url)
    imagesfname = extractimages(page)
    print imagesfname
    images = []
    for i,x in enumerate(imagesfname):
        print x
        cv2.imwrite(str(i)+'.jpg',readimage(x))
        #images.append(readimage(x))
    #images = [ readimage(x) for x in imagesfname ]
    output = classify(imageclf,labels,imagesfname)
    ads = []
    for out in output:
        if 'lingerie' in out[1].lower() or\
           'bikini' in out[1].lower():
            tag = out[1]
            img,title = searchtag(tag)
            print img, title
            ads.append((title,img))
    return render_template('template.html', external_url=url,items=ads)

if __name__ == '__main__':
    app.run(debug=True)
