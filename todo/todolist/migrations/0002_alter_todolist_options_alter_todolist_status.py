# Generated by Django 4.2.1 on 2023-11-26 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-created_at', '-id']},
        ),
        migrations.AlterField(
            model_name='todolist',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
