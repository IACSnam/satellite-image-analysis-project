from PIL import Image
import os
import numpy
import shutil


def get_pixels_from_file (filename):
  '''Return an array of pixels representing grey
  values of pixels in file filename'''
  img = Image.open(filename)
  #img = img.convert("P",palette=Image.ADAPTIVE,colors=16)
  img = img.convert("RGB")
  #img.save(os.path.join("convert",filename))
  return numpy.array(img)

def write_file_from_pixels (pixels, filename):
  '''Create a file filename containing a greyscale image
  based on grey values in array greypixels.

  Image will be placed in directory 'out'
  '''
  if not os.path.exists('out'):
    os.makedirs('out')
  if not hasattr(pixels,'__array_interface__'):
    pixels = numpy.array(pixels,dtype=numpy.uint8)
  outImage = Image.fromarray(pixels)
  outImage.save(os.path.join('out',filename))

  #Credit to the man, the myth, the legend: MR. HINKLE
