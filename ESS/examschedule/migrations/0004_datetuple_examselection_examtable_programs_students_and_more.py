# Generated by Django 4.2 on 2023-04-06 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0003_delete_datetuple_delete_examselection_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTuple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.CharField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'DateTuple',
            },
        ),
        migrations.CreateModel(
            name='Examselection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'exam_selection',
            },
        ),
        migrations.CreateModel(
            name='Examtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=25)),
                ('module_code', models.CharField(max_length=10)),
                ('module_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'examTable',
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('program_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('program_name', models.CharField(max_length=255, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.departments')),
            ],
            options={
                'db_table': 'Programs',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.programs')),
                ('year', models.ForeignKey(blank=True, db_column='year', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.yearofstudy')),
            ],
            options={
                'db_table': 'Students',
            },
        ),
        migrations.CreateModel(
            name='RepeatEnrollments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.modules')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.programs')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.students')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.yearofstudy')),
            ],
            options={
                'db_table': 'studentrepeats',
            },
        ),
        migrations.CreateModel(
            name='NormalEnrollments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.modules')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.programs')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.semester')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examschedule.yearofstudy')),
            ],
            options={
                'db_table': 'normalenrollments',
            },
        ),
    ]
