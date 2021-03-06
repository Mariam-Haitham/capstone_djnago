# Generated by Django 2.2.6 on 2019-10-31 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('care_book_api', '0007_auto_20191030_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergy',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='care_book_api.Home'),
        ),
    ]
