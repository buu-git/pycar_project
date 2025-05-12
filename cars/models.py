from django.db import models
from datetime import timedelta

# Create your models here.
# dodac pola description, color, size, typ do tabeli Cars

class Car(models.Model):

    TYPE_CHOICES = [
        ("S", "SUV"),
        ("SP", "SPORT"),
        ("H", "HATCHBACK"),
    ]

    image = models.ImageField(upload_to='cars_images/', null=True, blank=True)
    name = models.CharField(max_length=32)
    specification = models.TextField()
    car_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "cars"

    def __str__(self):
        return self.name

    def if_reserved(self, new_start_date, new_end_date):
        reservations = self.rezerwacje.all()
        return reservations.filter(date_start__lt=new_end_date, date_end__gt=new_start_date).exists()

from django.contrib.auth import get_user_model


class Rezerwacja(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="rezerwacje")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="rezerwacje")
    date_start = models.DateField()
    date_end = models.DateField()

    def price(self):
        return self.car.price

    class Meta:
        verbose_name_plural = "rezerwacje"

    def __str__(self):
        return f"Rezerwacja id: {self.id} na samochod {self.car.name}"

    def save(self, *args, **kwargs):
        if self.date_end < self.date_start:
            self.date_start, self.date_end = self.date_end, self.date_start

        super(Rezerwacja, self).save(*args, **kwargs)


    def total_days(self):
        return (self.date_end - self.date_start).days + 1  # +1, by doliczyć ostatni dzień

    def total_price(self):
        return self.total_days() * self.car.price




# python manage.py makemigrations
# python manage.py migrate