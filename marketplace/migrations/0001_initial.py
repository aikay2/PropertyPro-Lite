# Generated by Django 5.1.1 on 2024-09-23 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('sold', 'Sold'), ('available', 'Available')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.TextField(max_length=75)),
                ('type', models.CharField(help_text='e.g 2 bedroom, 3 bedroom, etc.', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('reason', models.CharField(help_text='e.g pricing, weird demands, etc.', max_length=15)),
                ('description', models.TextField(max_length=40)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='properties/')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='marketplace.property')),
            ],
        ),
    ]
