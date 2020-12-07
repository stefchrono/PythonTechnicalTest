# Generated by Django 2.2.13 on 2020-12-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=50)),
                ('size', models.IntegerField()),
                ('currency', models.CharField(max_length=3)),
                ('maturity', models.DateField()),
                ('lei', models.CharField(max_length=50)),
                ('legal_name', models.CharField(blank=True, max_length=30)),
            ],
        ),
    ]
