# Generated by Django 2.1.10 on 2019-09-23 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nnuh_doctors', '0003_auto_20190727_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='nnuh_doctors.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='nnuh_doctors.Doctor', verbose_name='Doctor'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Phone/Mobile'),
        ),
    ]
