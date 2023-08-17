# Generated by Django 4.2.3 on 2023-08-17 12:57

import accounts.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('type', models.CharField(choices=[('asker', 'asker'), ('helper', 'helper')], max_length=8)),
                ('birth_Year', models.CharField(max_length=4, null=True)),
                ('birth_Month', models.CharField(max_length=2, null=True)),
                ('birth_Day', models.CharField(max_length=2, null=True)),
                ('age', models.IntegerField(null=True)),
                ('age_range', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('male', '남성'), ('female', '여성')], max_length=7, null=True)),
                ('point', models.IntegerField(default=0)),
                ('score', models.FloatField(default=0)),
                ('task_count', models.IntegerField(default=0)),
                ('kind_count', models.IntegerField(default=0)),
                ('easy_count', models.IntegerField(default=0)),
                ('endure_count', models.IntegerField(default=0)),
                ('fast_count', models.IntegerField(default=0)),
                ('etc_count', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location_latitude', models.FloatField()),
                ('location_longtitude', models.FloatField()),
                ('building_name', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(choices=[('finance', '금융'), ('shopping', '쇼핑'), ('document_and_email', '문서 및 이메일 작성'), ('video_and_photo', '영상 및 사진'), ('reservation_and_booking', '예약 및 예매'), ('device_breakdown', '기기고장'), ('internet', '인터넷'), ('etc', '기타')], max_length=25)),
                ('voice_record_name', models.CharField(blank=True, max_length=50, null=True)),
                ('asker_confirm', models.BooleanField(blank=True, default=None, null=True)),
                ('helper_confirm', models.BooleanField(blank=True, default=None, null=True)),
                ('asker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caller', to=settings.AUTH_USER_MODEL)),
                ('helper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('content', models.CharField(choices=[('kind', '친절해요'), ('easy', '설명이쉬워요'), ('endure', '인내심이깊어요'), ('fast', '빨라요'), ('etc', '기타')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asker', to=settings.AUTH_USER_MODEL)),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helper', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.post')),
            ],
        ),
    ]
