# Generated by Django 3.2.7 on 2021-09-10 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumable', '0003_salec_consumable_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salec',
            name='consumable_type',
            field=models.CharField(editable=False, max_length=5),
        ),
    ]
