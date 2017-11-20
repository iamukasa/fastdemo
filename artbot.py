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


from sys import stdout
import numpy as np
ckpoints=["checkpoint/pretrained-networks/dora-marr-network",
       "checkpoint/pretrained-networks/rain-princess-network",
       "checkpoint/pretrained-networks/starry-night-network"]

def getstyled(data_in):
 
    paths_out="styled/test.jpg"
    content_image = utils.load_image(data_in)
    reshaped_content_height = (content_image.shape[0] - content_image.shape[0] % 4)
    reshaped_content_width = (content_image.shape[1] - content_image.shape[1] % 4)
    reshaped_content_image = content_image[:reshaped_content_height, :reshaped_content_width, :]
    reshaped_content_image = np.ndarray.reshape(reshaped_content_image, (1,) + reshaped_content_image.shape)


    checkpoint_dir=random.choice(ckpoints)
    prediction = ffwd(reshaped_content_image,checkpoint_dir)
    utils.save_image(prediction,paths_out)
    


    return paths_out

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



B="@shtaki_ke"

def tweet_image(url,sn,s):
    
    filename = 'output/temp.jpg'
    # send a get request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        # read data from downloaded bytes and returns a PIL.Image.Image object
        i = Image.open(BytesIO(request.content))
        # Saves the image under the given filename
        i.save(filename)
        output = getstyled(filename)
        m ="@"+sn+" Here is your photo turned art"
        s = api.update_with_media(output,m, s.id)

	


class MyStreamListener(StreamListener):
    def on_status(self, s):
        sn = s.user.screen_name
        if 'media' in s.entities:
            for image in s.entities['media']:
                x=image['media_url']
                file=tweet_image(x,sn,s)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
       	    return  true


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@shtaki_ke'])
