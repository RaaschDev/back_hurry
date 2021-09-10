# Generated by Django 3.2.7 on 2021-09-10 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=155)),
                ('consumable_type', models.CharField(choices=[('drink', 'DRINK'), ('food', 'FOOD')], max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('img', models.URLField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumables', to='events.eventmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]