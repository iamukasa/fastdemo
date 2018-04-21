from io import BytesIO
from PIL import Image
from PIL import ImageFile

from stylize_image import ffwd
import tweepy
import wget
import requests
import tweepy
from tweepy.streaming import StreamListener
from credentials import *
import random
import utils
import transform
import tensorflow as tf

from sys import stdout
import numpy as np
import pyrebase
import random


config = {
  "apiKey":"AIzaSyDQ52QqpRAHRJK5MiwrzPAybnp_J9Ehjpo",
  "authDomain": "artgallery-e8143.firebaseapp.com",
  "databaseURL": "https://artgallery-e8143.firebaseio.com",
  "storageBucket": "artgallery-e8143.appspot.com"
}

firebase = pyrebase.initialize_app(config)
cin=0;
ckpoints=["checkpoint/pretrained-networks/dora-marr-network",
       "checkpoint/pretrained-networks/rain-princess-network",
"checkpoint/pretrained-networks/starry-night-network"]
def getstyled(data_in):

    paths_out="styled/fb.jpg"
    content_image = utils.load_image(data_in)
    reshaped_content_height = (content_image.shape[0] - content_image.shape[0] % 4)
    reshaped_content_width = (content_image.shape[1] - content_image.shape[1] % 4)
    reshaped_content_image = content_image[:reshaped_content_height, :reshaped_content_width, :]
    reshaped_content_image = np.ndarray.reshape(reshaped_content_image, (1,) + reshaped_content_image.shape)

    prediction = ffwd(reshaped_content_image,random.choice(ckpoints))
    utils.save_image(prediction,paths_out)

    return paths_out
def getimage(url):

    filename = 'output/fb.jpg'
    # send a get request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        # read data from downloaded bytes and returns a PIL.Image.Image object
        i = Image.open(BytesIO(request.content))
        # Saves the image under the given filename
        i.save(filename)
        output = getstyled(filename)
        storage = firebase.storage()
        db = firebase.database()
        xgon=str(db.generate_key())+".jpeg"
        storage.child("messengerbot/"+xgon).put(output)
        url=storage.child("messengerbot/"+xgon).get_url(1)
    return  url

def getimagelocal(url):

    filename = 'output/fb.jpg'
    output = getstyled(url)
    return  output
