# Generated by Django 3.1.6 on 2021-02-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_management', '0002_auto_20210202_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='git_link',
            field=models.CharField(default=None, max_length=60, null=True),
        ),
    ]
