from flask import Flask, send_from_directory, request
from flask import render_template as render
import satellite
import shutil
import os
import tempfile

app = Flask(__name__)

# send some text or whatever
@app.route("/hi")
def hi():
    return("hi")

@app.route('/')
def getInput ():
    return send_from_directory('.','form.html')

@app.route('/image', methods = ['POST'])
def getRequest ():
    print("%s"%request)
    print (request.files)
    fn = tempfile.mktemp(".jpg",dir="site-demo\\out")
    print(fn)
    picture = request.files.get('picture') #Gets picture
    picturefn = tempfile.mktemp(".jpg",dir="site-demo\\inputs")
    picture.save(picturefn)
    out_image, analysis = satellite.main(picture) #Runs program on picture
    totals = sum(analysis)
    print(out_image)
    if not os.path.exists('out'):
        os.makedirs('out')
    out_image.save(fn)
    #return send_from_directory('out',os.path.split(fn)[1])
    return render('analysis.html', forested=(analysis[0]/totals)*100, water=(analysis[1]/totals)*100, barren=(analysis[2]/totals)*100, ice=(analysis[3]/totals)*100,
        fn='out/'+os.path.split(fn)[1], ogfn='inputs/'+os.path.split(picturefn)[1])

@app.route("/out/<fn>")
def sstatic(fn):
    return send_from_directory("out",fn)

# send a file
@app.route('/mirror') 
def introspection ():
    return send_from_directory('.','web_ui.py')

if __name__ == "__main__":
    app.run(debug=True)
