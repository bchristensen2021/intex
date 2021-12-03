# Generated by Django 3.2.7 on 2021-12-03 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('credential', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'credential',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('drug_name', models.CharField(db_column='drugname', max_length=30, primary_key=True, serialize=False)),
                ('is_opioid', models.BooleanField()),
            ],
            options={
                'db_table': 'drug',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DrugPrescriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(db_column='quantity')),
            ],
            options={
                'db_table': 'drug_prescriber',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Prescriber',
            fields=[
                ('npi', models.IntegerField(db_column='npi', primary_key=True, serialize=False)),
                ('first_name', models.CharField(db_column='firstname', max_length=11)),
                ('last_name', models.CharField(db_column='lastname', max_length=11)),
                ('gender', models.CharField(db_column='gender', max_length=1)),
            ],
            options={
                'db_table': 'prescriber',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_name', models.CharField(max_length=19)),
                ('state_abbrev', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('population', models.IntegerField()),
                ('deaths', models.IntegerField()),
            ],
            options={
                'db_table': 'state',
                'managed': False,
            },
        ),
    ]