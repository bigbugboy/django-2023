# Generated by Django 4.2.7 on 2023-11-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_alter_todolist_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
