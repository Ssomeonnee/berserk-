# Generated by Django 5.1 on 2024-10-16 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0011_alter_album_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='berserkcreature',
            name='album',
        ),
        migrations.AddField(
            model_name='album',
            name='creature',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='photo_creature', to='berserk.berserkcreature'),
        ),
        migrations.AlterField(
            model_name='album',
            name='picture',
            field=models.ImageField(default='Album/default_image.jpg', upload_to='Album', verbose_name='Изображение'),
            preserve_default=False,
        ),
    ]
