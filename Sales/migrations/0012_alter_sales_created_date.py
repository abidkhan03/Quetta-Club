# Generated by Django 4.0.3 on 2022-09-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0011_alter_sales_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='created_date',
            field=models.DateTimeField(),
        ),
    ]