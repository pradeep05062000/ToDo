# Generated by Django 3.0.7 on 2020-06-28 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grpid', models.CharField(max_length=60)),
                ('group', models.CharField(max_length=60)),
                ('created_by', models.CharField(max_length=60)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=60)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(default='todo', max_length=60)),
                ('description', models.TextField(default=None)),
                ('flagTask', models.CharField(default='no', max_length=60)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAssignModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_to_name', models.CharField(max_length=60)),
                ('task', models.CharField(max_length=60)),
                ('status', models.CharField(default='todo', max_length=60)),
                ('comment', models.TextField(default=None)),
                ('assigned_by', models.CharField(max_length=60)),
                ('assigned_to_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todoapp.GroupModel')),
            ],
        ),
        migrations.CreateModel(
            name='SummaryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=None)),
                ('description_summary', models.TextField(default='None')),
                ('modefied_detail', models.CharField(default=None, max_length=60, null=True)),
                ('created_update', models.CharField(default=None, max_length=60, null=True)),
                ('taskId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to='todoapp.ToDoModel')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTaskWebLinkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('linkTask_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todoapp.TaskAssignModel')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTaskAttachmentsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=60)),
                ('document', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('fileTask_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todoapp.TaskAssignModel')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTaskActivityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(default='None')),
                ('history', models.TextField(default='None')),
                ('dateTime', models.DateTimeField(blank=True, default=None)),
                ('updated_by', models.CharField(max_length=60)),
                ('grpTaskActivity_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todoapp.TaskAssignModel')),
            ],
        ),
        migrations.CreateModel(
            name='GroupAdminsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminUser', models.CharField(max_length=60)),
                ('adminUser_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
