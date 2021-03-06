# Generated by Django 2.1.10 on 2019-07-14 05:37

import aldryn_common.admin_fields.sortedm2m
import aldryn_translation_tools.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='phone')),
                ('mobile', models.CharField(blank=True, max_length=100, null=True, verbose_name='mobile')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='email')),
                ('website', models.URLField(blank=True, null=True, verbose_name='website')),
                ('facebook', models.URLField(blank=True, verbose_name='Facebook')),
                ('twitter', models.URLField(blank=True, verbose_name='Twitter')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DoctorsPlugin',
            fields=[
                ('style', models.CharField(choices=[('standard', 'Standard'), ('carousel', 'Carousel')], default='standard', max_length=50, verbose_name='Style')),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='nnuh_doctors_doctorsplugin', serialize=False, to='cms.CMSPlugin')),
                ('show_links', models.BooleanField(default=False, verbose_name='Show links to Detail Page')),
                ('doctors', aldryn_common.admin_fields.sortedm2m.SortedM2MModelField(blank=True, help_text='Select and arrange specific doctors, or, leave blank to select all.', to='nnuh_doctors.Doctor')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='DoctorTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(default='', help_text="Provide this person's name.", max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, default='', help_text='Leave blank to auto-generate a unique slug.', max_length=255, verbose_name='unique slug')),
                ('speciality', models.CharField(max_length=255, verbose_name='speciality')),
                ('sub_speciality', models.CharField(max_length=255, verbose_name='sub speciality')),
                ('function', models.CharField(blank=True, default='', max_length=255, verbose_name='role')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nnuh_doctors.Doctor')),
            ],
            options={
                'verbose_name': 'Doctor Translation',
                'db_table': 'nnuh_doctors_doctor_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(blank=True, help_text='If provided, overrides the external link.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Page', verbose_name='Internal link')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SectionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(help_text="Provide this section's title.", max_length=255, verbose_name='title')),
                ('slug', models.SlugField(blank=True, default='', help_text='Leave blank to auto-generate a unique slug.', max_length=255, verbose_name='slug')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nnuh_doctors.Section')),
            ],
            options={
                'verbose_name': 'Section Translation',
                'db_table': 'nnuh_doctors_section_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='doctor',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='nnuh_doctors.Section', verbose_name='Section'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='visual',
            field=filer.fields.image.FilerImageField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='sectiontranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='doctortranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
