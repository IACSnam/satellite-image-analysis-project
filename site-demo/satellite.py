import image
import os
import numpy
from PIL import Image
from scipy import stats
from joblib import load
import tempfile

def comp_analysis(composition):
    counts = [0,0,0,0] #Forested, Water, Urban, Ice
    for y in range(len(composition)):
        for x in range(len(composition)):
            val = composition[y][x]
            map = {
                1 : 0,
                2 : 1,
                3 : 0,
                4 : 2,
                5 : 2,
                6 : 3
            }
            counts[map[val]] += 1
    return counts

def flatten(picture):
    flat = None
    for y in range(len(picture)):
        if y == 0:
            flat = numpy.array(picture[y])
        else:
            flat = numpy.append(flat, picture[y], axis=0)
    flat = numpy.reshape(flat, (int(flat.size//3), 3))
    return flat

def genROI(composition):
    ROI = numpy.empty((len(composition), len(composition[0]), 3))
    key = [[0, 140, 42],[0, 20, 199],[0, 209, 63],[125, 87, 17],[130, 130, 130],[255, 255, 255]]
    for y in range(len(composition)):
        for x in range(len(composition[0])):
            for c in range(3):
                roiPixel = composition[y][x]-1
                ROI[y][x][c] = key[roiPixel][c]
    return ROI

def main(fn, model_fn="RF_96", depth=1):
    model = load(f'models\\{model_fn}.joblib') #for live, change path to f'..\\models\\{model_fn}.joblib'
    picture = image.get_pixels_from_file(fn)
    len_y = len(picture)
    len_x = len(picture[0])
    flat = flatten(picture)
    composition = model.predict(flat)
    composition = numpy.reshape(composition, (len_y, len_x))
    analysis = comp_analysis(composition)
    ROI = genROI(composition)
    '''
    composition = []
    for run_y in range(0,len_y//depth):
        comp_row = []
        for run_x in range(0,len_x//depth):
            comp_row.append(comp_analysis)
        composition.append(comp_row)
        final = overlay(composition,fn,len_y,len_x,depth)
    '''
    outfile = tempfile.mktemp(".jpg",dir="out")
    img = Image.fromarray(ROI.astype(numpy.uint8))
    return img, analysis

def runTests():
    img = main("site-demo\\images\\Gainesville.jpg")
    import shutil
    if os.path.exists("out"):
        shutil.rmtree('out')
    if not os.path.exists('out'):
        os.makedirs('out')
    img.save('out\\img.jpg')
    print("done")

if __name__ == "__main__":
    runTests()