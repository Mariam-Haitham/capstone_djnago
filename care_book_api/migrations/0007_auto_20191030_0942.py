# Generated by Django 2.2.6 on 2019-10-30 06:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('care_book_api', '0006_auto_20191030_0842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allergy',
            options={'verbose_name_plural': 'allergies'},
        ),
        migrations.AlterModelOptions(
            name='child',
            options={'verbose_name_plural': 'children'},
        ),
        migrations.RenameField(
            model_name='allergy',
            old_name='allergy_type',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='home',
            name='care_taker',
        ),
        migrations.RemoveField(
            model_name='home',
            name='feed',
        ),
        migrations.RemoveField(
            model_name='home',
            name='parent',
        ),
        migrations.AddField(
            model_name='home',
            name='caretakers',
            field=models.ManyToManyField(related_name='caretaker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='home',
            name='parents',
            field=models.ManyToManyField(related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='child',
            name='allergies',
            field=models.ManyToManyField(related_name='children', to='care_book_api.Allergy'),
        ),
    ]