# Generated by Django 4.2 on 2023-04-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayt', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]