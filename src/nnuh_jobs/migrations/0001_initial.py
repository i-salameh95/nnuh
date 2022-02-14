# Generated by Django 2.1.10 on 2022-02-02 12:03

import aldryn_apphooks_config.fields
import aldryn_translation_tools.models
import app_data.fields
import cms.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import filer.fields.image
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('aldryn_people', '0018_auto_20160802_1852'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publishing_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publishing date')),
                ('is_published', models.BooleanField(db_index=True, default=False, verbose_name='is published')),
                ('deadline_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='deadline date')),
                ('is_valid', models.BooleanField(db_index=True, default=True, verbose_name='valid')),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
                'ordering': ['-publishing_date'],
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('namespace', models.CharField(default=None, max_length=100, unique=True, verbose_name='Instance namespace')),
                ('app_data', app_data.fields.AppDataField(default='{}', editable=False)),
                ('paginate_by', models.PositiveIntegerField(default=5, help_text='When paginating list views, how many articles per page?', verbose_name='Paginate size')),
                ('pagination_pages_start', models.PositiveIntegerField(default=10, help_text='When paginating list views, after how many pages should we start grouping the page numbers.', verbose_name='Pagination pages start')),
                ('pagination_pages_visible', models.PositiveIntegerField(default=4, help_text='When grouping page numbers, this determines how many pages are visible on each side of the active page.', verbose_name='Pagination pages visible')),
                ('create_authors', models.BooleanField(default=True, help_text='Automatically create authors from logged-in user?', verbose_name='Auto-create authors?')),
                ('template_prefix', models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefix for template dirs')),
            ],
            options={
                'verbose_name': 'NNUH Jobs configuration',
                'verbose_name_plural': 'NNUH Jobs configurations',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobsConfigTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('app_title', models.CharField(max_length=234, verbose_name='name')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nnuh_jobs.JobsConfig')),
            ],
            options={
                'verbose_name': 'NNUH Jobs configuration Translation',
                'db_table': 'nnuh_jobs_jobsconfig_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='JobTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(default='', help_text="Provide this job's title.", max_length=500, verbose_name='title')),
                ('slug', models.SlugField(blank=True, help_text='Used in the URL. If changed, the URL will change. Clear it to have it re-created automatically.', max_length=255, verbose_name='slug')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nnuh_jobs.Job')),
            ],
            options={
                'verbose_name': 'Job Translation',
                'db_table': 'nnuh_jobs_job_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel_no', models.CharField(max_length=20, verbose_name='Telephone No.')),
                ('mob_no', models.CharField(max_length=20, verbose_name='Mobile No.')),
                ('email1', models.EmailField(max_length=255, verbose_name='Email')),
                ('verify_email', models.EmailField(max_length=255, verbose_name='Verify Email')),
                ('card_id', models.CharField(max_length=10, verbose_name='ID Number')),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10, verbose_name='Gender')),
                ('date_of_birth', models.DateField(verbose_name='Birthday')),
                ('country_grad', models.CharField(max_length=20, verbose_name='Country Graduation')),
                ('year_grad', models.CharField(max_length=4, verbose_name='Graduation Year')),
                ('grad_avg', models.CharField(max_length=5, verbose_name='Graduation Average')),
                ('experience_years', models.CharField(choices=[('less than year', 'LESS_THAN_YEAR'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), ('more than 10 years', '10+')], max_length=20, verbose_name='Experience Years')),
                ('exp_sum', models.TextField(verbose_name='Experience Details')),
                ('tawjihi_branch', models.CharField(choices=[('Scientific', 'Scientific'), ('Literature', 'Literature'), ('Industrial', 'Industrial'), ('Commercial', 'Commercial')], max_length=20, verbose_name='Tawjihi Branch')),
                ('tawjihi_avg', models.CharField(max_length=5, verbose_name='Tawjihi Average')),
                ('tawjihi_country', models.CharField(max_length=20, verbose_name='Tawjihi Country')),
                ('cv', models.FileField(upload_to='')),
                ('tawjihi', models.FileField(upload_to='')),
                ('certificate', models.FileField(upload_to='')),
                ('master_cert', models.FileField(upload_to='')),
                ('experience', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('first_name', models.CharField(max_length=20, verbose_name='first name')),
                ('second_name', models.CharField(max_length=20, verbose_name='second name')),
                ('third_name', models.CharField(max_length=20, null=True, verbose_name='third_name')),
                ('family', models.CharField(max_length=20, verbose_name='last name')),
                ('address', models.TextField(verbose_name='address')),
                ('relations', models.BooleanField(default=False)),
                ('relative_name', models.CharField(max_length=40, null=True, verbose_name='relative name')),
                ('relation_type', models.CharField(max_length=20, null=True, verbose_name='relation type')),
                ('univ_study', models.CharField(choices=[('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Doctoral', 'Doctoral')], max_length=20, verbose_name='University Study')),
                ('univ_name', models.CharField(max_length=50, verbose_name='University Name')),
                ('specialization', models.CharField(max_length=50, verbose_name='specialization')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nnuh_jobs.User')),
            ],
            options={
                'verbose_name': 'user Translation',
                'db_table': 'nnuh_jobs_user_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='recruits', to='nnuh_jobs.User'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='jobpost',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='nnuh_jobs.Job'),
        ),
        migrations.AddField(
            model_name='job',
            name='app_config',
            field=aldryn_apphooks_config.fields.AppHookConfigField(help_text='When selecting a value, the form is reloaded to get the updated default', on_delete=django.db.models.deletion.CASCADE, to='nnuh_jobs.JobsConfig', verbose_name='NNUH Jobs Configuration'),
        ),
        migrations.AddField(
            model_name='job',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aldryn_people.Person', verbose_name='author'),
        ),
        migrations.AddField(
            model_name='job',
            name='content',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_content', slotname='Job_Description', to='cms.Placeholder'),
        ),
        migrations.AddField(
            model_name='job',
            name='featured_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL, verbose_name='featured image'),
        ),
        migrations.AddField(
            model_name='job',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterUniqueTogether(
            name='usertranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='jobtranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='jobsconfigtranslation',
            unique_together={('language_code', 'master')},
        ),
    ]