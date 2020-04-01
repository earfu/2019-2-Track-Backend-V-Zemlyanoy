from django.test import Client, TestCase
from django.urls import reverse as url_reverse
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


    def test_user_self_unlogged(self):
        url = url_reverse('user_self')
        response_1st = self.client.get(url)
        self.assertIn(response_1st.status_code, [302])
        self.assertEqual(response_1st['Location'], '/login/?next=' + url)

    def test_user_self_post(self):
        url = url_reverse('user_self')
        self.client.login(username=user_names[1],password=user_passwords[1])
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.status_code, 405)

    def test_user_self_get(self):
        url = url_reverse('user_self')
        self.client.login(username=user_names[1],password=user_passwords[1])
        response_3rd = self.client.get(url)
        self.assertIn(response_3rd.status_code, [200, 302])

    def test_user_by_id_post(self):
        url = url_reverse('user_by_id', kwargs={'user_id': user_ids[2]})
        response_1st = self.client.post(url, {})
        self.assertEqual(response_1st.status_code, 405)

    def test_user_by_id_get(self):
        url = url_reverse('user_by_id', kwargs={'user_id': user_ids[2]})
        response_2nd = self.client.get(url)
        self.assertIn(response_2nd.status_code, [200, 302])
        self.assertDictEqual(response_2nd.json()['user'], {'id': user_ids[2], 'username': user_names[2]})

    def test_user_new_get(self):
        url = url_reverse('user_new')
        response_1st = self.client.get(url)
        self.assertEqual(len(response_1st.templates), 10)
        self.assertEqual(response_1st.templates[0].name, 'users/new_user.html')

    def test_user_new_post(self):
        url = url_reverse('user_new')
        response_2nd = self.client.post(url, {})
        self.assertEqual(response_2nd.json()['User creation:'], 'invalid form data')
