# Generated by Django 2.1.15 on 2020-05-19 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=255, unique=True)),
                ('alter_ego', models.CharField(max_length=255, unique=True)),
                ('universe', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='superheroes',
            field=models.ManyToManyField(to='core.Hero'),
        ),
    ]
