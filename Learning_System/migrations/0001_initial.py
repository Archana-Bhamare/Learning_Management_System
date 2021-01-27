# Generated by Django 3.1.5 on 2021-01-27 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=15)),
                ('Description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ManyToManyField(to='Learning_System.Course')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_mob_no', models.CharField(default=None, max_length=13)),
                ('rel_alt_no', models.CharField(default=None, max_length=10)),
                ('current_location', models.CharField(default=None, max_length=20)),
                ('current_address', models.CharField(default=None, max_length=25)),
                ('git_link', models.CharField(default=None, max_length=20)),
                ('year_of_exp', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default=None)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_score', models.FloatField(default=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learning_System.course')),
                ('mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Learning_System.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learning_System.student')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(default=None, max_length=50)),
                ('stream', models.CharField(default=None, max_length=50)),
                ('university', models.CharField(default=None, max_length=50)),
                ('percentage', models.FloatField(default=None)),
                ('from_date', models.DateField(default=None)),
                ('till', models.DateField(default=None)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learning_System.student')),
            ],
        ),
    ]
