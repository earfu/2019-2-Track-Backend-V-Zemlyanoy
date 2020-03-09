from django.test import Client, TestCase
from users.models import User
from chats.models import Chat, Message
from faker import Faker

# Create your tests here.
fake = Faker()

user_names = ['empty', fake.user_name(), fake.user_name(), fake.user_name()]
user_passwords = ['NoThingToSeeHere', fake.password(), fake.password(), fake.password()]
chat_names = ['Not_to_test_scale', fake.word(), fake.word(), fake.word()]
user_ids = [0, 1, 2, 3]
chat_ids = [0, 1, 2, 3]


class Test_Chat(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User(username=user_names[1])
        user1.save()
        user1.set_password(user_passwords[1])
        user1.save()
        user_ids[1] = user1.id
        user2 = User(username=user_names[2])
        user2.save()
        user2.set_password(user_passwords[2])
        user2.save()
        user_ids[2] = user2.id
        chat1 = Chat(name=chat_names[1])
        chat1.save()
        chat1.members.add(user1)
        chat1.members.add(user2)
        chat1.save()
        chat_ids[1] = chat1.id
        chat2 = Chat(name=chat_names[2])
        chat2.save()
        chat_ids[2] = chat2.id


    def test_user_self(self):
        url = '/users/user/'
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)
        response_login = self.client.post('/login/', {'username': user_names[1], 'password': user_passwords[1]})
        self.assertIn(response_login.status_code, [200, 302])
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.status_code, 405)
        response_3rd = self.client.get(url)
        self.assertIn(response_3rd.status_code, [200, 302])

    def test_user_by_id(self):
        url = '/users/' + str(user_ids[2]) + '/' # seek user2 instead of self
        response_1st = self.client.post(url, {})
        self.assertEqual(response_1st.status_code, 405)
        response_2nd = self.client.get(url)
        self.assertIn(response_2nd.status_code, [200, 302])
        self.assertDictEqual(response_2nd.json()['user'], {'id': user_ids[2], 'username': user_names[2]})

    def test_user_new(self):
        url = '/users/new/'
        response_1st = self.client.get(url)
        self.assertEqual(len(response_1st.templates), 10)
        self.assertEqual(response_1st.templates[0].name, 'users/new_user.html')
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.json()['User creation:'], 'invalid form data')
