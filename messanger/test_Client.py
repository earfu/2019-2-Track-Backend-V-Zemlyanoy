from django.test import Client
from users.models import User

def test_messaging(chat_id, message_text):
    # for this, kwargs is to be a tuple of filenames
    client = Client()
    body = {'content': message_text,}
    response = client.post('/chats/' + str(chat_id) + '/send_message/',
        body,
    )
    return response

def test_chat_create(chat_name):
    client = Client()
    response = client.post('/chats/create_chat/', {'name': chat_name})
    return response
