# Generated by Django 3.1 on 2022-02-16 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('year', models.DateField()),
                ('price', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[('Sedan', 'Седан'), ('Coupe', 'Купэ'), ('Hatchback', 'Хэтчбэк'), ('Minivan', 'Минивэн'), ('SUV', 'Внедорожник'), ('Pickup/Truck', 'Грузовой')], max_length=50)),
                ('color', models.CharField(choices=[('white', 'белый'), ('black', 'черный'), ('blue', 'синий'), ('red', 'красный'), ('yellow', 'желтый'), ('gray', 'серый'), ('green', 'зеленый'), ('orange', 'оранжевый')], max_length=20)),
                ('condition', models.CharField(max_length=50)),
                ('total_trip', models.PositiveBigIntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.car')),
            ],
        ),
    ]
