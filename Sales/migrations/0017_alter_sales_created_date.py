# Generated by Django 4.1 on 2022-10-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0016_rename_name_dummytable_cname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sales", name="created_date", field=models.DateField(),
        ),
    ]