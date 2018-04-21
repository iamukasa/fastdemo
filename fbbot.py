#Python libraries that we need to import for our bot
import random
import messengerbot as thebot
from flask import Flask, request
from pymessenger.bot import Bot
import os 
from fbmq import Page, Attachment, Template, QuickReply 

app = Flask(__name__)
ACCESS_TOKEN = 'EAAD06iqNXNABAEEDvVhZAKuTDIksTdC8Pn98HIFIUPdN56pH7ovWt20YcdNVgn5hYLemYVF5v32wz0EQaZCrARC8NfgTMWTZCOi2BvdBy18GBWcirZCUfE4tIfWvpUp3G8MTDjvV1ELeiAfzQ9mVdvBYKatxm59isJAkgwPsyQZDZD'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = '420'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

bot = Bot (ACCESS_TOKEN)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#page=Page(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    attachment_link = message["message"]["attachments"][0]["payload"]["url"]
                    try:
                        urltosend= thebot.getimage(attachment_link        
                    except Exception:
                           shutdown_server()
                
                    send_message_photo(recipient_id,urltosend)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["hey there we can make your photos into art just send one", "send a photo see the magic", "whats up send a photo see the magic", "send a photo see magic"]
    # return selected item to the user
    return random.choice(sample_responses)


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
def send_message_photo(recipient_id,url):
    bot.send_text_message(recipient_id,"Here is your photo made into art")
    print(url)   
    bot.send_image_url(recipient_id,url)
    #page.send(recipient_id, Attachment.File(url))
    return "sucess"
 


if __name__ == "__main__":
    try: 
        app.run(port=3000)
    except Exception:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
