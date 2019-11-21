from django.test import Client

def test_messaging(chat_id, message_text):
    client = Client()
    response = client.post('/chats/' + str(chat_id) + '/send_message/', {'content': message_text})
    return response

def test_chat_create(chat_name):
    client = Client()
    response = client.post('/chats/create_chat/', {'name': chat_name})
    return response
