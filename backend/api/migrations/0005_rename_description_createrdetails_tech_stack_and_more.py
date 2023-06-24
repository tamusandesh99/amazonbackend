# Generated by Django 4.2.2 on 2023-06-23 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_createrdetails_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='createrdetails',
            old_name='description',
            new_name='tech_stack',
        ),
        migrations.AddField(
            model_name='createrdetails',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]