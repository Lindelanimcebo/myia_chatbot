from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
bot = Bot(ACCESS_TOKEN)
 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    """ Recieved messages sent to the bot
    """
    if request.method == 'GET':
        """Verify token to confirm that all messages recieved are from Facebook""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was POST, then it must be a message from a user
    else:
        # get the message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                # Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']

                # Process Text message
                if (msg := message['message'].get('text')):
                    response_sent_text = get_message(msg)
                    send_message(recipient_id, response_sent_text)

                # Process non-text message
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    """verify token sent by facebook
    """
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message(msg = "attachement"):
    """ Generate response to a message
    """
    #sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    resp = f'You sent "{msg}".'
    return resp

def send_message(recipient_id, response):
    """ Use PyMessanger to send message to a user
    """
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()