# Generated by Django 2.2.6 on 2019-11-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_book_api', '0008_auto_20191031_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
