
from mask_rcnn import Mask
from io import BytesIO
from PIL import Image
import requests
import skimage
import numpy as np
from io import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

model = Mask()

def predict(url, verbose=1):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    input_array = np.array(img) 
    #input_array = np.expand_dims(input_array,axis=0)
    print(input_array.shape)
    fig = model.mask_detection(input_array, verbose=verbose)
    canvas=FigureCanvas(fig)
    return canvas


# https://www.parisinfo.com/var/otcp/sites/images/node_43/node_51/node_77884/node_77889/avenue-des-champs-%C3%A9lys%C3%A9es-no%C3%ABl-%7C-630x405-%7C-%C2%A9-studio-ttg/20001523-2-fre-FR/Avenue-des-Champs-%C3%89lys%C3%A9es-No%C3%ABl-%7C-630x405-%7C-%C2%A9-Studio-TTG.jpg