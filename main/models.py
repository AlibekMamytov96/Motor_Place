
from django.db import models
from users.models import MyUser


class Brand(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):

    CHOICES = [
        ('Sedan', 'Седан'),
        ('Coupe', 'Купэ'),
        ('Hatchback', 'Хэтчбэк'),
        ('Minivan', 'Минивэн'),
        ('SUV', 'Внедорожник'),
        ('Pickup/Truck', 'Грузовой'),
    ]
    COLOR = [
        ('white', 'белый'),
        ('black', 'черный'),
        ('blue', 'синий'),
        ('red', 'красный'),
        ('yellow', 'желтый'),
        ('gray', 'серый'),
        ('green', 'зеленый'),
        ('orange', 'оранжевый'),
    ]

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cars')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=100)
    year = models.DateField()
    price = models.PositiveIntegerField()
    category = models.CharField(choices=CHOICES, max_length=50)
    color = models.CharField(choices=COLOR, max_length=20)
    condition = models.CharField(max_length=50)
    total_trip = models.PositiveBigIntegerField()
    phone_number = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='phones')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.yeat}'

    class Meta:
        ordering = ['-created']


class CarImage(models.Model):
    image = models.ImageField(upload_to='cars', blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='comments')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created']
