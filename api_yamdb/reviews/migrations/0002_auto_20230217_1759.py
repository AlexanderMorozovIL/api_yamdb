# Generated by Django 3.2 on 2023-02-17 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('-pub_date',), 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='created',
            new_name='pub_date',
        ),
    ]