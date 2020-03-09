from django.test import Client, TestCase
from users.models import User
from chats.models import Chat, Message
from faker import Faker

# Create your tests here.

fake = Faker()

user_names = ['empty', fake.user_name(), fake.user_name(), fake.user_name()]
user_passwords = ['NoThingToSeeHere', fake.password(), fake.password(), fake.password()]
chat_names = ['Not_to_test_scale', fake.word(), fake.word(), fake.word()]
chat_ids = [0, 1, 2, 3]
msg_texts = ['Empty', fake.sentence()]

class Test_Chat(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User(username=user_names[1])
        user1.save()
        user1.set_password(user_passwords[1])
        user1.save()
        user2 = User(username=user_names[2])
        user2.save()
        user2.set_password(user_passwords[2])
        user2.save()
        chat1 = Chat(name=chat_names[1])
        chat1.save()
        chat1.members.add(user1)
        chat1.members.add(user2)
        chat1.save()
        chat_ids[1] = chat1.id
        chat2 = Chat(name=chat_names[2])
        chat2.save()
        chat_ids[2] = chat2.id


    def test_index(self):
        url = '/chats/index/'
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)
        response_login = self.client.post('/login/', {'username': user_names[1], 'password': user_passwords[1]})
        self.assertIn(response_login.status_code, [200, 302])
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.status_code, 405)
        response_3rd = self.client.get(url)
        self.assertIn(response_3rd.status_code, [200, 304])
        self.assertEqual(response_3rd.json()['user_self'], user_names[1])
        self.assertEqual(len(response_3rd.json()['chats']), 1)

    def test_chat_messages(self):
        url = '/chats/' + str(chat_ids[1]) + '/'
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)
        response_login = self.client.post('/login/', {'username': user_names[1], 'password': user_passwords[1]})
        self.assertIn(response_login.status_code, [200, 302])
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.status_code, 405)
        response_3rd = self.client.get(url)
        self.assertIn(response_3rd.status_code, [200, 304])
        self.assertListEqual(response_3rd.json()['messages'], [])
        url2 = '/chats/' + str(chat_ids[2]) + '/' # this chat has no members, and so must be inaccessible
        response_4th = self.client.get(url2)
        self.assertRaises(KeyError, lambda: response_4th.json()['messages'])

    def test_chat_detail(self):
        url = '/chats/' + str(chat_ids[1]) + '/detail/'
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)
        response_login = self.client.post('/login/', {'username': user_names[1], 'password': user_passwords[1]})
        self.assertIn(response_login.status_code, [200, 302])
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.status_code, 405)
        response_3rd = self.client.get(url)
        self.assertIn(response_3rd.status_code, [200, 304])
        self.assertEqual(len(response_3rd.json()['members']), 2)

    def test_chat_send_message(self):
        url = '/chats/' + str(chat_ids[1]) + '/send_message/'
        self.client.login(username=user_names[1], password=user_passwords[1])
        response_1st = self.client.post(url, {'content': msg_texts[1]})
        self.assertEqual(response_1st.status_code, 200)
        url2 = '/chats/' + str(chat_ids[1]) + '/'
        response_2nd = self.client.get(url2)
        self.assertEqual(len(response_2nd.json()['messages']), 1)

    def test_create_chat(self):
        url = '/chats/create_chat/'
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)
        response_login = self.client.post('/login/', {'username': user_names[1], 'password': user_passwords[1]})
        self.assertIn(response_login.status_code, [200, 302])
        response_2nd = self.client.post(url, {'name': chat_names[3]})
        self.assertIn(response_2nd.status_code, [200])
        self.assertIsNot(response_2nd.json()['chat id'], None)
        url2 = '/chats/' + str(response_2nd.json()['chat id']) + '/detail/'
        response_3rd = self.client.get(url2)
        self.assertEqual(len(response_3rd.json()['members']), 1)

    def test_default_index(self):
        response = self.client.get('/index/')
        self.assertEqual(len(response.templates), 1)
        self.assertEqual(response.templates[0].name, 'index.html')
