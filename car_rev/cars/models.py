from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, related_name='manufacturers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name='cars', on_delete=models.CASCADE)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    email = models.EmailField()
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.email} - {self.car.name}"
