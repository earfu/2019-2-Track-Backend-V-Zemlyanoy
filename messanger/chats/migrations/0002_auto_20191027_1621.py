# Generated by Django 2.2.5 on 2019-10-27 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chat_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='chat_id',
            new_name='chat',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='last_read_message_id',
            new_name='last_read_message',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='chat_id',
            new_name='chat',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user_id',
            new_name='user',
        ),
    ]
