import factory
from faker import Faker
from users.models import User
from chats.models import Chat, Member, Message

class UserFactory(factory.Factory):
    class Meta:
        model = User
    username = factory.Faker('user_name')

class ChatFactory(factory.Factory):
    class Meta:
        model = Chat
    name = factory.Faker('word')

fake = Faker()

fixed_users = []
passwds = []
fixed_chats = []

def fix_users():
    for i in range(100):
        usr = UserFactory.build()
        passwd = fake.password()
        usr.save()
        usr.set_password(passwd)
        usr.save()
        fixed_users.append(usr)
        passwds.append(passwd)

def fix_chats():
    for i in range(1, len(fixed_users)):
        obj = ChatFactory.create()
        obj.save()
        obj.members.add(fixed_users[0])
        obj.members.add(fixed_users[i])
        obj.save()
        fixed_chats.append(obj)

def fix_messages():
    for i in range(len(fixed_chats)):
        for j in range(20):
            msg = Message(user=fixed_users[(j%2 == 1) and (i+1) or 0], chat=fixed_chats[i], content=fake.sentence())
            msg.save()

def fix():
    fix_users()
    fix_chats()
    fix_messages()

if (__name__ == 'main'):
    fix()
