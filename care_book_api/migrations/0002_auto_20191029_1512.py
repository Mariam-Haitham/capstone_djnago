# Generated by Django 2.2.6 on 2019-10-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_book_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='allergies',
            field=models.ManyToManyField(related_name='allergies', to='care_book_api.Allergy'),
        ),
    ]
