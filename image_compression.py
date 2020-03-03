import io
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
import urllib2
import scipy.misc

def get_image(image_url='http://www.montefiore.ulg.ac.be/~asutera/ict_projects/image.png', size=(128, 128)):
    file_descriptor = urllib2.urlopen(image_url)
    image_file = io.BytesIO(file_descriptor.read())
    image = Image.open(image_file)
    img_color = image.resize(size, 1)
    img_grey = img_color.convert('L')
    img = np.array(img_grey, dtype=np.float)
    return img
 
def get_2D_dct(img):
    """ Get 2D Cosine Transform of Image
    """
    return fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')

def get_2d_idct(coefficients):
    """ Get 2D Inverse Cosine Transform of Image
    """
    return fftpack.idct(fftpack.idct(coefficients.T, norm='ortho').T, norm='ortho')

def get_reconstructed_image(raw):
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img

if __name__ == "__main__":
	pixels = get_image(size=(256, 256))
	dct_size = pixels.shape[0]
	dct = get_2D_dct(pixels)
	reconstructed_images = []

	for ii in range(dct_size):
	    dct_copy = dct.copy()
	    dct_copy[ii:,:] = 0
	    dct_copy[:,ii:] = 0
	    
	    # Reconstructed image
	    r_img = get_2d_idct(dct_copy)
	    reconstructed_image = get_reconstructed_image(r_img)

	    # Create a list of images
	    reconstructed_images.append(reconstructed_image)

	save_path = 'reconstructed_images/'
	if not os.path.exists(save_path):
		os.mkdir(save_path)
	for i,ii in enumerate(reconstructed_images):
		scipy.misc.imsave(save_path+'image_{}.jpg'.format(i), ii)

