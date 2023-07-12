from django.db import models

# Create your models here.
class User(models.Model):
    CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact = models.PositiveIntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=5, choices=CHOICES)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Location(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    pin = models.PositiveIntegerField()
    landmarks = models.CharField(max_length=50)

    def __str__(self):
        return self.name