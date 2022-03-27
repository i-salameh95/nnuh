# Generated by Django 2.1.10 on 2022-03-23 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nnuh_doctors', '0006_auto_20220310_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsplugin',
            name='style',
            field=models.CharField(choices=[('standard', 'Standard'), ('feature', 'Feature'), ('carousel', 'Carousel')], default='standard', max_length=50, verbose_name='Style'),
        ),
    ]
