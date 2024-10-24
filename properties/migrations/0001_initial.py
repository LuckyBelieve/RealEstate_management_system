# Generated by Django 5.1.2 on 2024-10-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property_type', models.CharField(max_length=50)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('square_feet', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='property_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]